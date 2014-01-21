#!/usr/bin/perl -w 

use strict;
use warnings 'all';
use Archive::Tar;
use File::Find;
use CGI;

#my $archive=$ARGV[0];
#my $dir=$ARGV[1];

print "Content-Type: text/html\n\n";

my $doc=new CGI;
my $archive=$doc->param("archive");
my $dir=$doc->param("dir");

if(length($archive)==length($doc)&&$archive=~m/^\ */){
	print "<url>/tarcvf.cgi?dir=directory&archive=file.tgz<br>";
	exit;
}else{
	print "Star taring<br>";
}

# Create inventory of files & directories
my @inventory = ();
find (sub { push @inventory, $File::Find::name }, $dir);

# Create a new tar object
my $tar = Archive::Tar->new();

$tar->add_files( @inventory );

# Write compressed tar file
#$tar->write( $archive, 9 );
$tar->write("$archive", COMPRESS_GZIP); # gzip compressed
print "finished<br>";
