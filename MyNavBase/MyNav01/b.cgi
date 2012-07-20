#!/usr/bin/perl

print "Content-type: text/html\n\n";

my $u= `ls -a`;
foreach(split(/\n/,$u)){
print "<description>$_</description><br>";
}
