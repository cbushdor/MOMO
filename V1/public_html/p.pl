#!/usr/bin/perl

use LWP::Simple;
use JSON;
use Data::Dumper;

print "Content-Type: text/html\n\n";
print &getTZN(48.8592,2.3417,"");

chomp(my $tz = qx/date +%Z/);print "</br>$tz --". localtime. "</br>";

use POSIX qw(tzset);

my $was = localtime;
print "It was      $was\n</br>";

$ENV{TZ} = 'America/Los_Angeles';

$was = localtime;
print "It is still $was\n</br>";

tzset;

my $now = localtime;
print "It is now   $now\n</br>";


sub getTZN{ # Begin Get time Zone Name
	my ($lon,$lat,$id)=@_;
	#my $url = "https://maps.googleapis.com/maps/api/timezone/json?location=$lon,$lat 39.6034810,-119.6822510&timestamp=1331161200&key=$id";
	my $url = "https://maps.googleapis.com/maps/api/timezone/json?location=$lon,$lat&timestamp=1331161200&key=$id";
	my $json=get("$url");
	my $json_obj = new JSON;
	my $perl = $json_obj->decode($json);
	return $perl->{timeZoneId};
} # End Get Time Zone Name
