#!/usr/bin/perl -w

use strict;
use warnings 'all';
use Archive::Tar;
use File::Find;
use CGI;
use Cwd;

$|=1;

print "Content-Type: text/html\n\n";

my $doc=new CGI;
my $archive=$doc->param("archive");chomp($archive);
my $dir=$doc->param("dir");chomp($dir);
my $mpid=$doc->param("pid");chomp($mpid);
my $hostn=$doc->param("hostn");chomp($hostn);

if(length($hostn)==0){
	print "error length host: $hostn=".length($hostn)."\n";
	exit -1;
}
if(! -e "cgi-bin/private/info.txt"){
	print "\nuuuuuuu)(tarcvf.cgi) creation \n";
	open(W,">cgi-bin/private/info.txt") or die("problem with open $!");
	print W "$hostn";
	close W or die "problem with close $!";
}
else {
	open(R,"cgi-bin/private/info.txt") or die("problem with open $!");
	my $z=<R>;chomp($z);
	close R or die "problem with close $!";
#	print "\n(tarcvf.cgi)oooooo)tests regarding $hostn $z ";
	if($hostn!~m/^$z$/){
#		print "ko\n";
		#print "error host";
		print "error";
		exit -1;
	}
#	else{
#		print "ok\n";
#	}
}

if(length($mpid)==0){ # begin if(length($mpid)==0)
	print "error";
	exit -1;
} # end if(length($mpid)==0)
elsif(length($archive)==length($doc)&&($archive=~m/^\ *$/||length($doc)==0)){ # begin elsif(length($archive)==length($doc)&&$archive=~m/^\ */)
	print "error";
	exit -1;
} # end elsif(length($archive)==length($doc)&&$archive=~m/^\ */)
else{ # begin else
	# --------------------------------------------------------------------------------------------
	# we save pid of the father to ensure security
	open(W,">mfpid.txt") or die("problem with open $!");
	print W "$mpid";
	close W or die "problem with close $!";
	# --------------------------------------------------------------------------------------------

	# --------------------------------------------------------------------------------------------
	# we save current pid to ensure security
	open(W,">mpid.txt") or die("problem with open $!");
	print W "$$";
	close W or die "problem with close $!";
	# --------------------------------------------------------------------------------------------
	print "$$";# to ensure security problems
} # end else

# Create inventory of files & directories
my @inventory = ();
find (sub { push @inventory, $File::Find::name }, $dir);

# Create a new tar object
my $tar = Archive::Tar->new();

$tar->add_files( @inventory );

# Write compressed tar file tgz
$tar->write("$archive", COMPRESS_GZIP); # gzip compressed
exit 0;
