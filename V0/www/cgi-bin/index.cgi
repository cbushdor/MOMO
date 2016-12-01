#!/usr/bin/perl

open(W,">toto.my.tutu") || die("open $!");
print W "tutu 42";
close(W) || die("close $!");
print "Content-type: text/html\n\n";
print "Hello world";
