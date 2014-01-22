#!/usr/bin/perl -w

use strict;
use warnings;
use Net::Ping;

use LWP::Simple;

$|=1;

my $mpid=$$;# pid of current process
#my $host="http://derased.heliohost.org/";
my $host="http://localhost/~sdo";
my $nob="backups_album.tgz"; # name of backup
my $file="/Users/Shared/Library/biblio/My-Distant-Programs-Backups/$nob" ;

if (-e $file){# begin if (-e $file)
	unlink $file;
}# end if (-e $file)

my $url="$host/$nob";
my $urlexec="$host/tarcvf.cgi?archive=$nob&dir=.&pid=$mpid";
my $content=get $urlexec;

print "--------------------->$content\n";
`wget -c -P /Users/Shared/Library/biblio/My-Distant-Programs-Backups $url`;

$urlexec="$host/cleandir.cgi?pid=$mpid&opid=$content";# need to proof that the process to start cleaning came from the fact that it is requested by a backup
$content = get $urlexec;
