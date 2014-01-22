#!/usr/bin/perl -w

use strict;
use warnings;
use CGI;

$|=1;

my $doc=new CGI;
my $mpid=$doc->param("mpid");# ensure that it is the father
my $opid=$doc->param("opid");# ensure that one tar operation ok

open(R,"mfpid.txt") or die("problem with open $!");;
my $smfpid=<R>; # get saved mfpid (from process that had launched the backup process)
close R or die "problem with close $!";
chomp($smfpid);

open(R,"mpid.txt") or die("problem with open $!");;
my $smpid=<R>; # get saved mpid (from process that had tar file)
close R or die "problem with close $!";
chomp($smpid);

if($smfpid=~m/^$mpid$/){
	# we check that tar file was launched by the backup.cgi file
	if($mpid=~m/^$smpid$/){ # begin if($mpid=~m/^$smpid$/)
		&clean(".","backups_album.tgz");# clean backup file
		&clean("cgi-bin/.","wfc_data.*.xml");# clean extra files
		#&clean(".","mfpid");# clean extra files
		#&clean(".","mpid");# clean extra files
	} # end if($mpid=~m/^$smpid$/)
}

# cleaning operation: need $directory where cleaning will occur and the file to be cleaned
sub clean{ # begin sub clean
	my ($dir,$fil)=@_;
	my $file= ();

	chdir("$dir");
	opendir (DIR,".") or die "Couldn't open directory, $!";
	while ($file = readdir DIR) { # begin while ($file = readdir DIR)
		if($file=~m/$fil/){ # begin if($file=~m/$fil/)
			print "---->$file\n";
			unlink("$file");
		} # end if($file=~m/$fil/)
	} # end while ($file = readdir DIR)
	closedir DIR;
} # end sub clean
