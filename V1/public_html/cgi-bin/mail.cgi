#!/usr/bin/perl

use warnings;
use strict;
use CGI;

my $doc=new CGI;
my $message=$doc->param("message");

print "Content-type: text/html\n\n";
my $to = 'dorey_s@laposte.net';
my $from = 'shark.b@laposte.net';
my $subject = 'Test Email';
my $message = '<b>This is test email sent by Perl Script</b>';

open(MAIL, "|/usr/sbin/sendmail -t");

# Email Header
print MAIL "To: $to\n";
print MAIL "From: $from\n";
print MAIL "Subject: $subject\n\n";
print MAIL "Content-type: text/html\n";
# Email Body
print MAIL $message;

close(MAIL);