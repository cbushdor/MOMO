#!/usr/bin/perl

print "Content-Type: text/html\n\n";

my $res=system('/usr/bin/curl --url "smtps://smtp.gmail.com:465" --ssl-reqd  --mail-from "sebastiendorey75@gmail.com" --mail-rcpt "dorey_s@laposte.net"  --upload-file ./file.txt --user "sebastiendorey75@gmail.com:kaxYOs3p" --insecure');
print "--->$res</br>";
