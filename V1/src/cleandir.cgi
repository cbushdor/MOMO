#!/usr/bin/perl -w

use strict;
use warnings;
use CGI;

$|=1;

print "Content-Type: text/html\n\n";

my $doc=new CGI;
my $mpid=$doc->param("pid");chomp($mpid);# ensure that it is the father
my $opid=$doc->param("opid");chomp($opid);# ensure that one tar operation ok

if(length($mpid)==length($opid)&&length($opid)==0){ # begin if(length($mpid)==length($opid)&&length($opid)==0)
	print "error XXXXXX";
	exit(-1);
} # end if(length($mpid)==length($opid)&&length($opid)==0)

open(R,"mfpid.txt") or die("problem with open $!");;
my $smfpid=<R>; # get saved mfpid (from process that had launched the backup process)
close R or die "problem with close $!";
chomp($smfpid);

open(R,"mpid.txt") or die("problem with open $!");;
my $smpid=<R>; # get saved mpid (from process that had tar file)
close R or die "problem with close $!";
chomp($smpid);

if($smfpid=~m/^$mpid$/){ # begin if($smfpid=~m/^$mpid$/)
	#print "$opid=~m/^$smpid$/)\n<br>";
	# we check that tar file was launched by the backup.cgi file
	if($opid=~m/^$smpid$/){ # begin if($opid=~m/^$smpid$/)
		&clean(".","backups_album.tgz");# clean backup file
		&clean(".","mfpid.txt");# clean extra files
		&clean(".","mpid.txt");# clean extra files
		chdir("cgi-bin");
		&clean(".","wfc_data.*.xml");# clean extra files
		chdir("..");
		exit(0);
	} # end if($opid=~m/^$smpid$/)
	else{ # begin else
		print "error K1";
		exit(-1);
	} # end else
} # end if($smfpid=~m/^$mpid$/)
else{ # begin else
	print "error K2";
	exit(-1);
} # end else

# cleaning operation: need $directory where cleaning will occur and the file to be cleaned
sub clean{ # begin sub clean
	my ($dir,$fil)=@_;
	my $file= ();

	#chdir("$dir");
	opendir (DIR,".") or die "Couldn't open directory, $!";
	while ($file = readdir DIR) { # begin while ($file = readdir DIR)
		if($file=~m/$fil/){ # begin if($file=~m/$fil/)
			print "---->$file\n";
			unlink("$file");
		} # end if($file=~m/$fil/)
	} # end while ($file = readdir DIR)
	closedir DIR;
	#chdir("..");
} # end sub clean
