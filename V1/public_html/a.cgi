#!/usr/bin/perl
# Available under BSD License.
# See url http://www.cyberciti.biz/faq/how-can-i-find-out-perl-version/
$command=`perl -v`;
$title = "Perl Version";
 
print "Content-type: text/html\n\n";
print "<html><head><title>$title</title></head><body>";
 
print "<h1>$title</h1>\n";
 
print '&lt;pre>';
print $command;
print '&lt;/pre>';
 
print "</body></html>";