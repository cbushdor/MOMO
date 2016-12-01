package packages::Time;

# +-------------------------------+
# | Dorey Sebastien               |
# | Time.pm                       |
# | Written on August 8 th 2005   |
# | Last update on Sept 15th 2005 |
# +-------------------------------+
  
require Exporter;

$VERSION    = '1.0';
$VERSION    = eval $VERSION;
@ISA    = qw( Exporter );
@EXPORT = qw( dates_substracted  are_dates_greater  are_dates_smaller are_dates_equal 
	      print_res test_for_smaller test_for_greater test_for_equal);
@EXPORT_OK = qw( timegm_nocheck timelocal_nocheck );

# Sat Sep 10 16:12:01 UTC 2005

@nday = ("Sun","Mon","Tues","Wed","Thu","Fri","Sat");
@nmonth = ("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec");

use Time::Local;

# my $a = localtime(timelocal(01,42,15,10,8,2005));
# my $b = localtime(timelocal(42,10,16,10,6,2004));

# Substract 2 dates at the format above and returns the result in the format 2 hours 3 min for instance
sub dates_substracted {
    return  &translate(&substract_date($_[0],$_[1])) . "\n";
}

# Prints dates result
sub print_res {
    my ($d1,$d2,$res) = @_;

    return ($res == 0) ? "ok\n":"nok\n";
}

# Looks if date 1 is greater than date 2
sub are_dates_greater {
    my ($d1,$d2) = @_;

    if (&get_year_from_string($d1) > &get_year_from_string($d2)) {
	return 0;
    } elsif (&get_year_from_string($d1) == &get_year_from_string($d2)) {
	if (&get_month_number_from_string($d1) > &get_month_number_from_string($d2)) {
	    return 0;
	} elsif (&get_month_number_from_string($d1) == &get_month_number_from_string($d2)) {
	    if (&get_day_number_from_string($d1) > &get_day_number_from_string($d2)) {
		return 0;
	    } elsif (&get_day_number_from_string($d1) == &get_day_number_from_string($d2)) { 
		if (&get_hour_from_string($d1) > &get_hour_from_string($d2)) {
		    return 0;
		} elsif (&get_hour_from_string($d1) == &get_hour_from_string($d2)) {
		    if (&get_minutes_from_string($d1) > &get_minutes_from_string($d2)) { 
			return 0;
		    }  elsif (&get_minutes_from_string($d1) == &get_minutes_from_string($d2)) {
			if (&get_seconds_from_string($d1) > &get_seconds_from_string($d2)) {
			    return 0;
			}
			return -1;
		    } else {
			return -1;
		    }
		} else {
		    return -1;
		}
	    } else {
		return -1;
	    }
	} else {
	    return -1;
	}
    } else {
	return -1;
    }
}

# Looks if date 1 is smaller than date 2
sub are_dates_smaller {
    my ($d1,$d2) = @_;

    if (&get_year_from_string($d1) > &get_year_from_string($d2)) {
	return -1;
    } elsif (&get_year_from_string($d1) == &get_year_from_string($d2)) {
	if (&get_month_number_from_string($d1) > &get_month_number_from_string($d2)) {
	    return -1;
	} elsif (&get_month_number_from_string($d1) == &get_month_number_from_string($d2)) {
	    if (&get_day_number_from_string($d1) > &get_day_number_from_string($d2)) {
		return -1;
	    } elsif (&get_day_number_from_string($d1) == &get_day_number_from_string($d2)) { 
		if (&get_hour_from_string($d1) > &get_hour_from_string($d2)) {
		    return -1;
		} elsif (&get_hour_from_string($d1) == &get_hour_from_string($d2)) {
		    if (&get_minutes_from_string($d1) > &get_minutes_from_string($d2)) { 
			return -1;
		    }  elsif (&get_minutes_from_string($d1) == &get_minutes_from_string($d2)) {
			if (&get_seconds_from_string($d1) < &get_seconds_from_string($d2)) {
			    return 0;
			}
			return -1;
		    } else {
			return 0;
		    }
		} else {
		    return 0;
		}
	    } else {
		return 0;
	    }
	} else {
	    return 0;
	}
    } else {
	return 0;
    }
}

# Looks if date 1 is equal to date 2
sub are_dates_equal {
    my ($d1,$d2) = @_;

    if (&get_year_from_string($d1) > &get_year_from_string($d2)) {
	return -1;
    } elsif (&get_year_from_string($d1) == &get_year_from_string($d2)) {
	if (&get_month_number_from_string($d1) > &get_month_number_from_string($d2)) {
	    return -1;
	} elsif (&get_month_number_from_string($d1) == &get_month_number_from_string($d2)) {
	    if (&get_day_number_from_string($d1) > &get_day_number_from_string($d2)) {
		return -1;
	    } elsif (&get_day_number_from_string($d1) == &get_day_number_from_string($d2)) { 
		if (&get_hour_from_string($d1) > &get_hour_from_string($d2)) {
		    return -1;
		} elsif (&get_hour_from_string($d1) == &get_hour_from_string($d2)) {
		    if (&get_minutes_from_string($d1) > &get_minutes_from_string($d2)) { 
			return -1;
		    }  elsif (&get_minutes_from_string($d1) == &get_minutes_from_string($d2)) {
			if (&get_seconds_from_string($d1) == &get_seconds_from_string($d2)) {
			    return 0;
			}
			return -1;
		    } else {
			return -1;
		    }
		} else {
		    return -1;
		}
	    } else {
		return -1;
	    }
	} else {
	    return -1;
	}
    } else {
	return -1;
    }
}

# Returns as year days month year min sec format according to epoc
sub translate {
    my ($epoc) = @_;
    my ($sec,$min) = &div_time($epoc,60); # left minute(s)
    my ($min_r,$hour) = &div_time($min,60); # left hour(s)
    my ($hour_r,$day) = &div_time($hour,24); # left day(s)
    my ($day_r,$year) = &div_time($day,365); # left year(s)

    return
	&print_peace_of_date($year," year(s) ") .
	&print_peace_of_date($day_r," day(s) ") . 
	&print_peace_of_date($hour_r," hour(s) ") .
	&print_peace_of_date($min_r," min(s) ") .
	&print_peace_of_date($sec," sec(s)");
}

# Returns if value non 0 the string 
sub print_peace_of_date {
    my ($value,$string) = @_;

    $value =~ s/\ *//g;
    return ($value != 0) ? "$value $string" : "";
}

# Division for time. Returns reminder and time left after operation
sub div_time {
    my ($epoc,$max_time) = @_;
    my $first_div = ($epoc % $max_time);

    return ($first_div,(($epoc - $first_div) / $max_time));
}


# Substracts two dates and return as epoc format
sub substract_date {
    my ($my_date_left,$my_date_right) = (&clean_dates($_[0]),&clean_dates($_[1]));
    my $reminder = 0;


    chomp($my_date_left);
    chomp($my_date_right);

    $my_date_left =~ s/\ UTC//g;
    $my_date_right =~ s/\ UTC//g;

    my ($date_left_nday,$date_left_month,$date_left_mday,$date_left_hour,$date_left_min,$date_left_sec,$date_left_year) = split(/\ /,$my_date_left);
    my ($date_right_nday,$date_right_month,$date_right_mday,$date_right_hour,$date_right_min,$date_right_sec,$date_right_year) = split(/\ /,$my_date_right);

    return timelocal($date_left_sec,$date_left_min,$date_left_hour,$date_left_mday,&get_num_month($date_left_month),$date_left_year) 
	- timelocal( $date_right_sec,$date_right_min,$date_right_hour,$date_right_mday,&get_num_month($date_right_month),$date_right_year);
}

# We clean format of 2 dates received
sub clean_dates{
    my ($my_date_left) = @_;

    $my_date_left =~ s/\:/\ /g;
    $my_date_left =~ s/^\ *//g;

    return ($my_date_left);
}

# from a given month return its rank in year
sub get_num_month {
    my ($month) = @_;
    my $n = 0;

    while ($nmonth[$n] ne $month) {
	$n++;
    }
    return ($n);
}

# Substracts 2 dates. If result < 0 then error
sub substract {
    if (($_[0] - $_[1]) < 0 ) { 
	return -1;
    }
    return ($_[0] - $_[1]);
}

# Returns time in second from a given date 
sub get_time_epoc {
    return time();
}

# Prints a formated date (s.a Sat Sep 10 16:12:01 UTC 2005) according to date function
sub print_formated_date {
    return &get_day_name . " " . &get_month_name . " " . &get_num_day . " " . &get_hour . ":" . &get_min . ":" . &get_sec . " UTC " . &get_year . "\n";
}

# Returns seconds from localtime() function
sub get_sec {
    return ((localtime(time()))[0]);
}

# Returns minutes from localtime() function
sub get_min {
    return ((localtime(time()))[1]);
}

# Returns seconds from localtime() function
sub get_hour {
    return ((localtime(time()))[2]);
}

# Returns number of the day from localtime() function
sub get_num_day {
    return ((localtime(time()))[3]);
}

# Returns month from localtime() function
sub get_month {
    return ((localtime(time()))[4]);
}
 
# Returns month name from localtime() function
sub get_month_name {
    return ($nmonth[(localtime(time()))[4]]);
}

# Returns year from localtime() function
sub get_year {
    return (1900+(localtime(time()))[5]);
}

# Returns day name from localtime() function
sub get_day_name {
    return ($nday[(localtime(time()))[6]]);
}

# Returns day number from Jan 1st from current year from localtime() function
sub get_day_num_in_year {
    return ((localtime(time()))[7]);
}

# Get name of the day  from this date format Sat Sep 10 16:12:01 UTC 2005
sub get_name_of_the_day_from_string {
    my ($string) = &clean_dates($_[0]);

    return ((split(/\ /,$string))[0]);
}

# Get month from this date format Sat Sep 10 16:12:01 UTC 2005
sub get_month_from_string {
    my ($string) = &clean_dates($_[0]);

    return ((split(/\ /,$string))[1]);
}

# Get month from this date format Sat Sep 10 16:12:01 UTC 2005
sub get_month_number_from_string {
    my ($string) = &clean_dates($_[0]);
    my $counter = 0;

    foreach my $m (@nmonth) {
	if ($string =~ m/$m/i) {
	    return $counter;
	}
	$counter++;
    }
    return -1;
}

# Get day number in month from this date format Sat Sep 10 16:12:01 UTC 2005
sub get_day_number_from_string {
    my ($string) = &clean_dates($_[0]);

    return ((split(/\ /,$string))[2]);
}

# Get hour from this date format Sat Sep 10 16:12:01 UTC 2005
sub get_hour_from_string {
    my ($string) = &clean_dates($_[0]);

    return ((split(/\ /,$string))[3]);
}

# Get minutes from this date format Sat Sep 10 16:12:01 UTC 2005
sub get_minutes_from_string {
    my ($string) = &clean_dates($_[0]);

    return ((split(/\ /,$string))[4]);
}

# Get seconds from this date format Sat Sep 10 16:12:01 UTC 2005
sub get_seconds_from_string {
    my ($string) = &clean_dates($_[0]);

    return ((split(/\ /,$string))[5]);
}

# Get UTC from this date format Sat Sep 10 16:12:01 UTC 2005
sub get_utc_from_string {
    my ($string) = &clean_dates($_[0]);

    return ((split(/\ /,$string))[6]);
}

# Get year from this date format Sat Sep 10 16:12:01 UTC 2005
sub get_year_from_string {
    my ($string) = &clean_dates($_[0]);

    return ((split(/\ /,$string))[7]);
}


sub test_for_equal {
    my ($d1,$d2) = @_;

    print "equal:( $d1,$d2):" . print_res("$d1","$d2", are_dates_equal( "$d1","$d2"));
}

sub test_for_greater {
    my ($d1,$d2) = @_;

    print "greater:( $d1,$d2):" . print_res("$d1","$d2", are_dates_greater( "$d1","$d2"));
}

sub test_for_smaller {
    my ($d1,$d2) = @_;

    print "smaller:( $d1,$d2):" . print_res("$d1","$d2", are_dates_smaller( "$d1","$d2"));
}

1;
