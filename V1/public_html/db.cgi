#!/usr/bin/perl
#simpledb.plx
use warnings;
use strict;
use POSIX;
use GDBM_File;      # or SDBM _ File / GDBM _ File / NDBM _ File / AnyDBM _ File...

print "Content-Type: text/html\n\n";

my %dbm;
my $db_file = "simpledb.dbm";
tie %dbm, 'GDBM_File', $db_file, O_CREAT|O_RDWR, 0644;

if (tied %dbm) {
	print "File $db_file now open.\n";
} else {
	die "Sorry - unable to open $db_file\n";
}
$_ = "";         # make sure that $_ is defined

untie %dbm;
