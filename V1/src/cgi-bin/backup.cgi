#!/usr/bin/perl -w

use strict;
use warnings;
use Net::Ping;

use LWP::Simple;

my $host="http://derased.heliohost.org/";
my $nob="backups_album.tgz"; # name of backup

my $url="http://derased.heliohost.org/$nob";
my $urlexec="http://derased.heliohost.org//cgi-bin/tarcvf.cgi?archive=../$nob&dir=album/hist";


my $content = get $urlexec;
`wget -c -P /Users/sdo/../Shared/BackUps/ $url`;
