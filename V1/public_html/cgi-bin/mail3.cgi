#!/usr/bin/perl

use strict;
use warnings;
use MIME::Lite;

my $subject   = "Welcome to Booking Request";
my $sender    = 'dorey_s@laposte.net';
my $recipient = 'sebastien.dorey@laposte.net';

print "Content-Type: text/html\n\n";
print "Sending mail";
my $data = qq{
    <h1>Hello</h1>
};

my $mime = MIME::Lite->new(
    'From'    => $sender,
    'To'      => $recipient,
    'Subject' => $subject,
    'Type'    => 'text/html',
    'Data'    => $data,
);

$mime->send() or die "Failed to send mail\n";

open(MAIL, "|/usr/sbin/sendmail -t");

# Email Header
print MAIL $mime;
# Email Body
close(MAIL);
