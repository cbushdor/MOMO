#!/usr/bin/perl -T

use strict;
use warnings;
use Cwd;

use constant CURRENT_DIRECTORY  => "./";
my $some_dir=" ";# directory where to start search
my @recdir=();
my @dirs=();# all directories from $some_dir
my $prevdir=();
my @resu=();
my @res=();

&req(
		{
			-req=>'toto',# query
			-path=>'/Users/sdo/Sites/cgi-bin' # Where the search must start
			#-nli=>'ok',# put a num of line that match in the file 
			##-hli=>'wod' # hightlight
		}
	);

print "Content-Type: text/html\n\n";
foreach(@res){
	print "$_\n";
}
foreach(@resu){
	print "$_\n";
}

# Gets the tree
sub recTree{
	my $cpt=0;
	opendir(DH,CURRENT_DIRECTORY) || die("Error $!") ;
	my @l=readdir(DH);
	closedir(DH) || die("$!");
	foreach my $i (@l) {
		delete $l[$cpt++];
		if($i!~m!^\.{1,2}$!){
			if(-d "$i"){
				my $loc=getcwd;
				if(scalar grep(/$loc/,@dirs) == 0){ push(@dirs,$loc);}
				push(@recdir,\@l);
				if ($i =~ /^(.*)$/) { $i=$1; }# otherwise there is an error with taint
				chdir("./$i") ;
				&recTree;

				# --------------------------------------------------------
				# Begin position to previous configuration
				chdir("..") ;
				$prevdir=pop(@recdir);
				@l=@$prevdir;
				# End position to previous configuration
				# --------------------------------------------------------
			}
		}
	}
	return;
}

# example: perl -e 'my $count=0;my @l=();my @a=('aaa','eee','tttt'); grep{$count++;if($_=~m/^a*e$/){@l=(@l,$count);}} @a;print "@l\n";'
sub req{
	my ($o) = @_;
	my $cpt = 0;
	my $cptf = 0;

	$some_dir = (defined($o->{-path})) ? $o->{-path} : "./"; # Where the search must star default currentt
	my $req = (defined($o->{-req})) ? $o->{-req} : " ";# query
	my $nli = (defined($o->{-nli})) ? $o->{-nli} : " ";# number of lines
	chdir($some_dir);
	&recTree;# Records the directory structure in @dirs
	foreach my $v (@dirs){#All directories
		delete $dirs[$cpt++];
		if($v =~ /^(.*)$/) { $v = $1; }# otherwise there is an error with taint
		chdir($v);#We go in the directory
		opendir(DH,$v) || die("Error $!") ;#we open the directory
		my @l = readdir(DH);#we store all the file names in the memory
		closedir(DH) || die("$!");#we close the currect directory
		foreach my $i (@l) {#All files in current directory
			delete $l[$cptf++];
			if(!-d "$i"){# only if it is not a directory
				@res=grep(/$req/,$i);
				my $count=0;
				open(R,"$i")||die("error $!");
				my @co=<R>;
				close(R)||die("error $!");
				grep {
					$count++;
					#print "$count ". (($_=~m/$req/) ? "ok $_":"ok") . "\n";
					if($_=~m/$req/){
						my $pos="$-[0] $+[0]";
						@resu=(@resu,"<p><b>".getcwd."/$i:</b>$count $-[0], $+[0]</p>");
					}
				} @co;

			}
		}
		$cptf=0;
	}
}
