#!/usr/bin/perl

use LWP::Simple;
use JSON;
use Data::Dumper;

print "Content-Type: text/html\n\n";
print "<pre>\n";
my $url = "http://ip-api.com/json";
#$url="http://dorey.sebastien.free.fr";
my $json=get("$url");
print "$json";
my $json_obj = new JSON;
my $perl = $json_obj->decode($json);
# Same effect as $perl = ['golden', 'fleece'];
print  "\n".Dumper($perl);
print "\n$perl->{timezone}\n";
print "</pre>\n";
