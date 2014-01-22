#!/usr/bin/perl -w 

use strict;
use warnings 'all';
use Archive::Tar;
use File::Find;
use CGI;

$|=1;

print "Content-Type: text/html\n\n";

my $doc=new CGI;
my $archive=$doc->param("archive");
my $dir=$doc->param("dir");
my $mpid=$doc->param("pid");

if(length($archive)==length($doc)&&$archive=~m/^\ */){ # begin if(length($archive)==length($doc)&&$archive=~m/^\ */)
	print "<url>/tarcvf.cgi?dir=directory&archive=file.tgz<br>";
	exit -1;
} # end if(length($archive)==length($doc)&&$archive=~m/^\ */)
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
