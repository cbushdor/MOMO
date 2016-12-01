#!/usr/bin/perl

use packages::Time;

@set_of_date = ("Sat Sep 10 16:12:02 UTC 2005","Sat Sep 10 16:12:01 UTC 2005","Sat Sep 10 16:08:00 UTC 2005",
		"Sat Sep 10 16:12:02 UTC 2004","Sat Sep 10 16:12:01 UTC 2004","Sat Sep 10 16:09:00 UTC 2004",
		"Sat Oct 11 16:12:02 UTC 2005","Sat Sep 16 16:12:01 UTC 2005","Sat Sep 16 16:10:00 UTC 2005",
		"Sat Sep 10 14:10:02 UTC 2005","Sat Sep 10 14:20:01 UTC 2003","Sat Jan 19 16:22:00 UTC 2005" );


print dates_substracted( "Sat Sep 10 16:12:01 UTC 2005","Sat Sep 08 16:12:01 UTC 2001");

foreach my $i (@set_of_date) {
    foreach my $j (@set_of_date) {
	chomp($i);
	chomp($j);
	test_for_equal($i,$j);
	test_for_greater($i,$j);
	test_for_smaller($i,$j);
	print "-----\n";
    }
}
