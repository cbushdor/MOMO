package io::MyTime;
use CGI::Carp qw(fatalsToBrowser); 


# ------------------------------------------------------
q##//q#
* Created By : sdo
* File Name : MyTime.pm
* Creation Date : Thu Oct 13 12:18:08 2005
* Last Modified : Fri Oct 26 21:59:11 2018
* Email Address : sdo@macbook-pro-de-sdo.home
* Version : 0.0.0.0
* License:
*       Permission is granted to copy, distribute, and/or modify this document under the terms of the Creative Commons Attribution-NonCommercial 3.0
*       Unported License, which is available at http: //creativecommons.org/licenses/by- nc/3.0/.
* Purpose :
#;
# ------------------------------------------------------


# +-------------------------------+
# | MyTime.pm                     |
# | Last update on Oct 13rd 2005  |
# | Written     on Aug 8 th 2005  |
# +-------------------------------+

require Exporter;
#use strict;

my $VERSION    = '1.0.3.0';
$VERSION    = eval $VERSION;
my @ISA    = qw( Exporter );
my @EXPORT = qw(
	     dates_substracted            are_dates_greater  are_dates_smaller        are_dates_equal
	     print_res                    test_for_smaller   test_for_greater         test_for_equal
	     gets_formated_date            is_timer_ok        gets_digital_date_format  add_days
	     format_number_on_two_digits
	     );
my @EXPORT_OK = qw( timegm_nocheck timelocal_nocheck );

# Sat Sep 10 16:12:01 UTC 2005

my @nday = ("Sun","Mon","Tues","Wed","Thu","Fri","Sat");
my @nmonth = ("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec");


my %rankmonth = (Jan => 1,
		 Feb => 2,
		 Mar => 3,
		 Apr => 4,
		 May => 5,
		 Jun => 6,
		 Jul => 7,
		 Aug => 8,
		 Sep => 9,
		 Oct => 10,
		 Nov => 11,
		 Dec => 12);

my %month_rank = (1 => Jan,
		  2 => Feb,
		  3 => Mar,
		  4 => Apr,
		  5 => May,
		  6 => Jun,
		  7 => Jul,
		  8 => Aug,
		  9 => Sep,
		  10 => Oct,
		  11 => Nov,
		  12 => Dec);


my %month_rank_day = (1 => 31,
		      2 => 29,
		      3 => 31,
		      4 => 30,
		      5 => 31,
		      6 => 30,
		      7 => 31,
		      8 => 31,
		      9 => 30,
		      10 => 31,
		      11 => 30,
		      12 => 31);

use Fcntl qw(:DEFAULT :flock);
use Time::Local;

=head1 NAME

io::MyTime.pm

$VERSION='1.0.3.0'

=head1 ABSTRACT

This package helps to manipulate dates.

JFYI function time() returns epoc format s.a Mon Jul 31 02:29:29 UTC 2006.

=head2 LIST OF FUNCTIONS

=over 4

add_days
are_dates_equal
are_dates_greater
are_dates_smaller
clean_dates
dates_substracted
div_time
format_number_on_two_digits
gets_day_name
gets_day_number_from_string
gets_day_num_in_year
gets_digital_date_format
gets_formated_date
gets_hour
gets_hour_from_string
gets_min
gets_minutes_from_string
gets_month
gets_month_from_string
gets_month_name
gets_month_number_from_string
gets_name_of_the_day_from_string
gets_num_day
gets_num_month
gets_sec
gets_seconds_from_string
gets_time_epoc
gets_utc_from_string
gets_year
gets_year_from_string
is_timer_ok
print_peace_of_date
print_res
remove_carriage_return
split_info_for_timer
substract
substracts_date
test_for_equal
test_for_greater
test_for_smaller
translate
substract
substracts_date

=back

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF MODIFICATIONS

=over 4

- I<Last modification:> May 26th 2009

- I<Last modification:> Oct 13rd 2005

- I<Created on:> Aug 8th 2005

=back

=cut

=head1 sub is_timer_ok(...)

This function checks if current time is elapsed or not. Then it returns a result.

=head2 PARAMETER(S)

=over 4

$time: A given time (see exemple below).

$laps: a given time not to over due.

=back

=head2 RETURNED VALUE

=over 4

is laps within one time session passed (1 min(s) 2sec(s),1 min(s) 1 sec(s)) is     ok returns  0
                                       (1 min(s) 2sec(s),1 min(s) 2 sec(s)) is not ok returns -1
                                       (1 min(s) 2sec(s),1 min(s) 3 sec(s)) is not ok returns -1

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 EXEMPLE

=over 4

is_timer_ok("3 min(s) 42 sec(s)",$laps) == 0 means it is ok if so.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 EXEMPLES

=over 4

my $a = localtime(timelocal(time()));

my $b = localtime(timelocal(time()));

is laps within one time session passed (1 min(s) 2sec(s),1 min(s) 1 sec(s)) is     ok returns  0
                                       (1 min(s) 2sec(s),1 min(s) 2 sec(s)) is not ok returns -1
                                       (1 min(s) 2sec(s),1 min(s) 3 sec(s)) is not ok returns -1

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Oct 13rd 2005

- I<Created on:> Aug 8th 2005

=back

=cut

sub is_timer_ok { # Begin sub is_timer_ok
	my ($time,$laps) = @_;
	my ($y_t,$d_t,$h_t,$m_t,$s_t) = &split_info_for_timer($time);
	my ($y_l,$d_l,$h_l,$m_l,$s_l) = &split_info_for_timer($laps);

	if ($y_t > $y_l) { # Begin if ($y_t > $y_l)
		return 0;
	}  # End if ($y_t > $y_l)
	elsif ($y_t == $y_l) { # Begin elsif ($y_t == $y_l)
		if ($d_t > $d_l) { # Begin if ($d_t > $d_l)
		    return 0;
		}  # End if ($d_t > $d_l)
		elsif ($d_t == $d_l) { # Begin elsif ($d_t == $d_l)
		    if ($h_t > $h_l) { # Begin if ($h_t > $h_l)
			return 0;
		    } # End if ($h_t > $h_l)
		    elsif ($h_t == $h_l) { # Begin elsif ($h_t == $h_l)
			if ($m_t > $m_l) {  # Begin if ($m_t > $m_l)
			    return 0;
			} # End if ($m_t > $m_l)
			elsif ($m_l == $m_t) { # Begin elsif ($m_l == $m_t)
			    if ($s_t > $s_l) { # Begin if ($s_t > $s_l)
				return 0;
			    } # End if ($s_t > $s_l)
			    elsif ($s_l == $s_t) { # Begin elsif ($s_l == $s_t)
				return -1;
			    }  # End elsif ($s_l == $s_t)
			    else {  # Begin else
				return -1;
			    }  # End else
			}  # End elsif ($m_l == $m_t)
			else {  # Begin else
			    return -1;
			} # End else
		    } # End elsif ($h_t == $h_l)
		    else {  # Begin else
			return -1;
		    } # End else
		} # End elsif ($d_t == $d_l)
		else {  # Begin else
		    return -1;
		} # End else
	}  # End elsif ($y_t == $y_l)
	else { # Begin else
		return -1;
	}  # End else
}  # End sub is_timer_ok


=head1 sub split_info_for_timer(...)

This function splits time something like that 1 hour(s) 2 min(s) 5sec(s) into separate fields no field for month is available only days.

=head2 PARAMETER(S)

=over 4

$schedule: that's a given scheduler: 1 hour(s) 2 min(s) 5sec(s)

=back

=head2 RETURNED VALUE

=over 4

Returns the associative array: ($year,$day,$hour,$min,$sec).

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Oct 13rd 2005

- I<Created on:> Aug 8th 2005

=back

=cut

sub split_info_for_timer { # Begin sub split_info_for_timer
	my ($schedule) = @_;
	my ($year,$day,$hour,$min,$sec,$other) = ();
	
	$schedule =~ s/\(s\)//g;
	if ($schedule =~ m/year/) {  # Begin if ($schedule =~ m/year/)
		($year,$schedule) = split(/year/,$schedule);
		$year =~ s/\ *//g;
	}   # End if ($schedule =~ m/year/)
	else { # Begin else
		$year = 0;
	}  # End else
	if ($schedule =~ m/day/) { # Begin  if ($schedule =~ m/day/)
		($day,$schedule)  = split(/day/ ,$schedule);
		$day =~ s/\ *//g;
	} # End  if ($schedule =~ m/day/)
	else { # Begin else
		$day = 0;
	}  # End else
	if ($schedule =~ m/hour/) { # Begin if ($schedule =~ m/hour/)
		($hour,$schedule) = split(/hour/,$schedule);
		$hour =~ s/\ *//g;
	}  # End if ($schedule =~ m/hour/)
	else { # Begin else
		$hour = 0;
	} # End else
	if ($schedule =~ m/min/) { # if ($schedule =~ m/min/)
		($min,$schedule)  = split(/min/ ,$schedule);
		$min =~ s/\ *//g;
	} # End if ($schedule =~ m/min/)
	else { # Begin else
		$min = 0;
	}  # End else
	if ($schedule =~ m/sec/) { # Begin if ($schedule =~ m/sec/)
		($sec,$other)  = split(/sec/ ,$schedule);
		$sec =~ s/\ *//g;
	} # End if ($schedule =~ m/sec/)
	else { # Begin else
		$sec = 0;
	}  # End else
	return ($year,$day,$hour,$min,$sec);
}  # End sub split_info_for_timer
	
	
=head1 sub dates_substracted(...)

This function substracts 2 dates with a given format (see substracts_date function parameter) and returns the result in the format 2 hours 3 min for instance. Operation is done s.a $time1 - $time2.

my $time1 = localtime(timelocal(time()));

my $time2 = localtime(timelocal(time()));

=head2 PARAMETER(S)

=over 4

$time1: given date (see format above).

$time2: given date (see format above).

=back

=head2 RETURNED VALUE

=over 4

Returns translated date. See returned format for translated function.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 EXAMPLE

=over 4

$laps = dates_substracted($current_date,$string_to_print[0]);

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Oct 13rd 2005

- I<Created on:> Aug 8th 2005

=back

=cut

sub dates_substracted { # Begin sub dates_substracted
	my ($time1,$time2) = @_;
	chomp($time1);
	chomp($time2);
	my $s = &translate(&substracts_date($time1,$time2));
	
	return $s;
} # End sub dates_substracted


=head1 sub print_res(...)

This function looks if parameter is equal to 0. If so, it returns ok string otherwise a negative answer string nok.

=head2 PARAMETER(S)

=over 4

$res: a value

=back

=head2 RETURNED VALUE

=over 4

Returns a string ok (0) or not ok (-1) that's the question ;-).

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Oct 13rd 2005

- I<Created on:> Aug 8th 2005

=back

=cut

sub print_res { # Begin sub print_res
	my ($res) = @_;
	
	return ($res == 0) ? "ok":"nok";
} # End sub print_res


=head1 sub are_dates_greater(...)

Function looks if date $d1 is greater than date $d2. The format of each dates is like this Mon Jul 31 02:29:29 UTC 2006.

my $d1 = localtime(timelocal(time()));

my $d2 = localtime(timelocal(time()));

=head2 PARAMETER(S)

=over 4

$d1: given date (see format above).

$d2: given date (see format above).

=back

=head2 RETURNED VALUE

=over 4

Returns O if ok otherwise -1.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Oct 13rd 2005

- I<Created on:> Aug 8th 2005

=back

=cut

sub are_dates_greater { # Begin sub are_dates_greater
	my ($d1,$d2) = @_;
	
	if (&gets_year_from_string($d1) > &gets_year_from_string($d2)) { # Begin if (&gets_year_from_string($d1) > &gets_year_from_string($d2))
		return 0;
	} # End if (&gets_year_from_string($d1) > &gets_year_from_string($d2))
	elsif (&gets_year_from_string($d1) == &gets_year_from_string($d2)) { # Begin elsif (&gets_year_from_string($d1) == &gets_year_from_string($d2))
		if (&gets_month_number_from_string($d1) > &gets_month_number_from_string($d2)) { # Begin if (&gets_month_number_from_string($d1) > &gets_month_number_from_string($d2))
		    return 0;
		}  # End if (&gets_month_number_from_string($d1) > &gets_month_number_from_string($d2))
		elsif (&gets_month_number_from_string($d1) == &gets_month_number_from_string($d2)) { # Begin elsif (&gets_month_number_from_string($d1) == &gets_month_number_from_string($d2))
		    if (&gets_day_number_from_string($d1) > &gets_day_number_from_string($d2)) { # Begin if (&gets_day_number_from_string($d1) > &gets_day_number_from_string($d2))
			return 0;
		    }  # End if (&gets_day_number_from_string($d1) > &gets_day_number_from_string($d2))
		    elsif (&gets_day_number_from_string($d1) == &gets_day_number_from_string($d2)) { # Begin elsif (&gets_day_number_from_string($d1) == &gets_day_number_from_string($d2))
			if (&gets_hour_from_string($d1) > &gets_hour_from_string($d2)) { # Begin if (&gets_hour_from_string($d1) > &gets_hour_from_string($d2))
			    return 0;
			}  # End if (&gets_hour_from_string($d1) > &gets_hour_from_string($d2))
			elsif (&gets_hour_from_string($d1) == &gets_hour_from_string($d2)) { # Begin elsif (&gets_hour_from_string($d1) == &gets_hour_from_string($d2))
			    if (&gets_minutes_from_string($d1) > &gets_minutes_from_string($d2)) { # Begin if (&gets_minutes_from_string($d1) > &gets_minutes_from_string($d2))
				return 0;
			    } # End if (&gets_minutes_from_string($d1) > &gets_minutes_from_string($d2))
			    elsif (&gets_minutes_from_string($d1) == &gets_minutes_from_string($d2)) { # Begin  elsif (&gets_minutes_from_string($d1) == &gets_minutes_from_string($d2))
				if (&gets_seconds_from_string($d1) > &gets_seconds_from_string($d2)) { # Begin if (&gets_seconds_from_string($d1) > &gets_seconds_from_string($d2))
				    return 0;
				}  # End if (&gets_seconds_from_string($d1) > &gets_seconds_from_string($d2))
				return -1;
			    }  # End  elsif (&gets_minutes_from_string($d1) == &gets_minutes_from_string($d2))
			    else { # Begin else
			      return -1;
			    } # End else
			}  # End elsif (&gets_hour_from_string($d1) == &gets_hour_from_string($d2))
			else { # Begin else
			  return -1;
			} # End else
		    } # End elsif (&gets_day_number_from_string($d1) == &gets_day_number_from_string($d2))
		    else { # Begin else
			return -1;
		    } # End else
		}  # End elsif (&gets_month_number_from_string($d1) == &gets_month_number_from_string($d2))
		else { # Begin else
		    return -1;
		}  # End else
	} # End elsif (&gets_year_from_string($d1) == &gets_year_from_string($d2))
	else { # Begin else
		return -1;
	}  # End else
} # Begin sub are_dates_greater


=head1 sub are_dates_smaller(...)

Function looks if date $d1 is smaller than date $d2. The format of each dates is like this Mon Jul 31 02:29:29 UTC 2006.

my $d1 = localtime(timelocal(time()));

my $d2 = localtime(timelocal(time()));

=head2 PARAMETER(S)

=over 4

$d1: given date (see format above).

$d2: given date (see format above).

=back

=head2 RETURNED VALUE

=over 4

Returns O if ok otherwise -1.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Oct 13rd 2005

- I<Created on:> Aug 8th 2005

=back

=cut

sub are_dates_smaller { # Begin sub are_dates_smaller
	my ($d1,$d2) = @_;
	
	if (&gets_year_from_string($d1) > &gets_year_from_string($d2)) { # Begin if (&gets_year_from_string($d1) > &gets_year_from_string($d2))
		return -1;
	}  # End if (&gets_year_from_string($d1) > &gets_year_from_string($d2))
	elsif (&gets_year_from_string($d1) == &gets_year_from_string($d2)) { # Begin elsif (&gets_year_from_string($d1) == &gets_year_from_string($d2))
		if (&gets_month_number_from_string($d1) > &gets_month_number_from_string($d2)) {
		    return -1;
		}
	elsif (&gets_month_number_from_string($d1) == &gets_month_number_from_string($d2)) { # Begin  elsif (&gets_month_number_from_string($d1) == &gets_month_number_from_string($d2))
		    if (&gets_day_number_from_string($d1) > &gets_day_number_from_string($d2)) { # Begin if (&gets_day_number_from_string($d1) > &gets_day_number_from_string($d2))
			return -1;
		    }  # End if (&gets_day_number_from_string($d1) > &gets_day_number_from_string($d2))
		    elsif (&gets_day_number_from_string($d1) == &gets_day_number_from_string($d2)) { # Begin elsif (&gets_day_number_from_string($d1) == &gets_day_number_from_string($d2))
			if (&gets_hour_from_string($d1) > &gets_hour_from_string($d2)) { # Begin if (&gets_hour_from_string($d1) > &gets_hour_from_string($d2))
			    return -1;
			} # End if (&gets_hour_from_string($d1) > &gets_hour_from_string($d2))
			elsif (&gets_hour_from_string($d1) == &gets_hour_from_string($d2)) { # Begin elsif (&gets_hour_from_string($d1) == &gets_hour_from_string($d2))
			    if (&gets_minutes_from_string($d1) > &gets_minutes_from_string($d2)) { # Begin if (&gets_minutes_from_string($d1) > &gets_minutes_from_string($d2))
				return -1;
			    } # End if (&gets_minutes_from_string($d1) > &gets_minutes_from_string($d2))
			    elsif (&gets_minutes_from_string($d1) == &gets_minutes_from_string($d2)) { # Begin  elsif (&gets_minutes_from_string($d1) == &gets_minutes_from_string($d2))
				if (&gets_seconds_from_string($d1) < &gets_seconds_from_string($d2)) { # Begin if (&gets_seconds_from_string($d1) < &gets_seconds_from_string($d2))
				    return 0;
				}  # End if (&gets_seconds_from_string($d1) < &gets_seconds_from_string($d2))
				return -1;
			    } # End  elsif (&gets_minutes_from_string($d1) == &gets_minutes_from_string($d2))
			    else { # Begin else
			      return 0;
			    } # End else
			}  # End elsif (&gets_hour_from_string($d1) == &gets_hour_from_string($d2))
			else { # Begin else
			  return 0;
			} # End else
		    }  # End elsif (&gets_day_number_from_string($d1) == &gets_day_number_from_string($d2))
		    else { # Begin else
		      return 0;
		    } # End else
		} # Begin  elsif (&gets_month_number_from_string($d1) == &gets_month_number_from_string($d2))
		else { # Begin else
		  return 0;
		} # End else
	} # End elsif (&gets_year_from_string($d1) == &gets_year_from_string($d2))
	else { # Begin else
		return 0;
	} # End else
} # End sub are_dates_smaller



=head1 sub are_dates_equal(...)

Function looks if date $d1 is equal to date $d2. The format of each dates is like this Mon Jul 31 02:29:29 UTC 2006.

my $d1 = localtime(timelocal(time()));

my $d2 = localtime(timelocal(time()));

=head2 PARAMETER(S)

=over 4

$d1: given date (see format above).

$d2: given date (see format above).

=back

=head2 RETURNED VALUE

=over 4

Returns O if ok otherwise -1.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Oct 13rd 2005

- I<Created on:> Aug 8th 2005

=back

=cut

sub are_dates_equal { # Begin sub are_dates_equal
	my ($d1,$d2) = @_;
	
	if (&gets_year_from_string($d1) > &gets_year_from_string($d2)) { # Begin if (&gets_year_from_string($d1) > &gets_year_from_string($d2))
		return -1;
	} # End if (&gets_year_from_string($d1) > &gets_year_from_string($d2))
	elsif (&gets_year_from_string($d1) == &gets_year_from_string($d2)) { # Begin elsif (&gets_year_from_string($d1) == &gets_year_from_string($d2))
		if (&gets_month_number_from_string($d1) > &gets_month_number_from_string($d2)) { # Begin if (&gets_month_number_from_string($d1) > &gets_month_number_from_string($d2))
		    return -1;
		} # End if (&gets_month_number_from_string($d1) > &gets_month_number_from_string($d2))
		elsif (&gets_month_number_from_string($d1) == &gets_month_number_from_string($d2)) { # Begin elsif (&gets_month_number_from_string($d1) == &gets_month_number_from_string($d2))
		    if (&gets_day_number_from_string($d1) > &gets_day_number_from_string($d2)) { # Begin if (&gets_day_number_from_string($d1) > &gets_day_number_from_string($d2))
			return -1;
		    }  # End if (&gets_day_number_from_string($d1) > &gets_day_number_from_string($d2))
		    elsif (&gets_day_number_from_string($d1) == &gets_day_number_from_string($d2)) { # Begin elsif (&gets_day_number_from_string($d1) == &gets_day_number_from_string($d2))
			if (&gets_hour_from_string($d1) > &gets_hour_from_string($d2)) { # Begin if (&gets_hour_from_string($d1) > &gets_hour_from_string($d2))
			    return -1;
			}  # End if (&gets_hour_from_string($d1) > &gets_hour_from_string($d2))
			elsif (&gets_hour_from_string($d1) == &gets_hour_from_string($d2)) { # Begin elsif (&gets_hour_from_string($d1) == &gets_hour_from_string($d2))
			    if (&gets_minutes_from_string($d1) > &gets_minutes_from_string($d2)) { # Begin if (&gets_minutes_from_string($d1) > &gets_minutes_from_string($d2))
				return -1;
			    } # End if (&gets_minutes_from_string($d1) > &gets_minutes_from_string($d2))
			    elsif (&gets_minutes_from_string($d1) == &gets_minutes_from_string($d2)) { # Begin if (&gets_minutes_from_string($d1) == &gets_minutes_from_string($d2))
				if (&gets_seconds_from_string($d1) == &gets_seconds_from_string($d2)) { # Begin if (&gets_seconds_from_string($d1) == &gets_seconds_from_string($d2))
				    return 0;
				}  # End if (&gets_seconds_from_string($d1) == &gets_seconds_from_string($d2))
				return -1;
			    }  # End elsif (&gets_minutes_from_string($d1) == &gets_minutes_from_string($d2))
			    else { # Begin else
			      return -1;
			    }  # End else
			}  # End elsif (&gets_hour_from_string($d1) == &gets_hour_from_string($d2))
			else { # Begin else
			    return -1;
			}  # End else
		    } # End elsif (&gets_day_number_from_string($d1) == &gets_day_number_from_string($d2))
		    else { # Begin else
		      return -1;
		    }  # End else
		}  # End elsif (&gets_month_number_from_string($d1) == &gets_month_number_from_string($d2))
		else { # Begin else
		  return -1;
		}  # End else
	}  # End elsif (&gets_year_from_string($d1) == &gets_year_from_string($d2))
	else { # Begin else
		return -1;
	}  # End else
}  # End sub are_dates_equal


=head1 sub translate(...)

Returns as year days month hour min sec format according to epoc.

=head2 PARAMETER(S)

=over 4

$epoc: epoc format of date (reminder it is time()).

=back

=head2 RETURNED VALUE

=over 4

$date_to_return: formated date

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Oct 13rd 2005

- I<Created on:> Aug 8th 2005

=back

=cut

sub translate { # Begin sub translate
	my ($epoc) = @_;
	my ($sec,
		$min,$min_r,
		$hour,$hour_r,
		$day,$day_r,
		$year) = ();
	my $date_to_return = ();
	
	($sec,$min) = &div_time($epoc,60); # left minute(s)
	($min_r,$hour) = &div_time($min,60); # left hour(s)
	($hour_r,$day) = &div_time($hour,24); # left day(s)
	($day_r,$year) = &div_time($day,365); # left year(s)
	$date_to_return =
		&print_peace_of_date($year," year(s) ") .
		&print_peace_of_date($day_r," day(s) ") .
		&print_peace_of_date($hour_r," hour(s) ") .
		&print_peace_of_date($min_r," min(s) ") .
		&print_peace_of_date($sec," sec(s)");
	$date_to_return =~ s/\ +/\ /g;
	$date_to_return =~ s/^[\ ]+//g;
	$date_to_return =~ s/[\ ]+$//g;
	return $date_to_return;
}  # End sub translate
	
	
=head1 sub remove_carriage_return(...)

A bug showed up at 2 min with translate function: a carriage return shows up in the middle of the string formated. This function removes it.

=head2 PARAMETER(S)

=over 4

$string: that's the string to analyse. The $string format UTC string clean (see gets_formated_date for the string format).

=back

=head2 RETURNED VALUE

=over 4

Returns new formated string.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Oct 13rd 2005

- I<Created on:> Aug 8th 2005

=back

=cut

sub remove_carriage_return { # Begin sub remove_carriage_return
	my ($string) = @_;
	my $new_string = ();
	
	foreach (split(/\n/,$string)) { # Begin foreach (split(/\n/,$string))
		$new_string .= $_ . " ";
	}  # End foreach (split(/\n/,$string))
	$new_string =~ s/^\ //;
	return $new_string;
}  # End sub remove_carriage_return


=head1 sub print_peace_of_date(...)

Prints a formated date. Similar to print_res.

=head2 PARAMETER(S)

=over 4

$value: value to check

$string: that's the string to analyse. The $string format UTC string clean (see gets_formated_date for the string format).

=back

=head2 RETURNED VALUE

=over 4

Returns new formated string according to $value parameter;.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Oct 13rd 2005

- I<Created on:> Aug 8th 2005

=back

=cut

sub print_peace_of_date { # Begin sub print_peace_of_date
	my ($value,$string) = @_;
	my $result = ($value != 0) ? "$value $string" : "";

	return $result;
} # End sub print_peace_of_date


=head1 sub remove_carriage_return(...)

Division for time. Returns reminder and time left after operation. Equivalent to modulo and division as a result.

=head2 PARAMETER(S)

=over 4

$epoc: that's date format (epoc).

$max_time: that's divisor

$string: that's the string to analyse. The $string format UTC string clean (see gets_formated_date for the string format).

=back

=head2 RETURNED VALUE

=over 4

Returns reminder and time left after operation.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Oct 13rd 2005

- I<Created on:> Aug 8th 2005

=back

=cut

sub div_time { # Begin sub div_time
	my ($epoc,$max_time) = @_;
	my $first_div = ($epoc % $max_time);

	return ($first_div,(($epoc - $first_div) / $max_time));
} # End sub div_time

=head1 sub substracts_date(...)

Substracts two dates and returns as epoc format. Operation is $time1 - $time2.

my $time1 = localtime(timelocal(time()));

my $time2 = localtime(timelocal(time()));

=head2 PARAMETER(S)

=over 4

$time1: given date (see format above).

$time2: given date (see format above).

=back

=head2 RETURNED VALUE

=over 4

Returns new date as a result of substraction.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Oct 13rd 2005

- I<Created on:> Aug 8th 2005

=back

=cut

sub substracts_date { # Begin sub substracts_date
	my ($time1,$time2) = @_;
	my ($my_date_left,$my_date_right) = (&clean_dates($time1),&clean_dates($time2));
	my $result = 0;
	my ($date_left_nday ,$date_left_month ,$date_left_mday ,$date_left_hour ,$date_left_min ,$date_left_sec ,$date_left_year ) =
		split(/\ /,$my_date_left);
	my ($date_right_nday,$date_right_month,$date_right_mday,$date_right_hour,$date_right_min,$date_right_sec,$date_right_year) =
		split(/\ /,$my_date_right);
	
	my ${result_tmloc1} = timelocal(
			  &format_number_on_two_digits($date_left_sec),
			  &format_number_on_two_digits($date_left_min) ,
			  &format_number_on_two_digits($date_left_hour) ,
			  &format_number_on_two_digits($date_left_mday) ,
			  &format_number_on_two_digits(&gets_num_month($date_left_month)),
			  &format_number_on_two_digits($date_left_year));
	my ${result_tmloc2} = timelocal(
			     &format_number_on_two_digits($date_right_sec),
			     &format_number_on_two_digits($date_right_min),
			     &format_number_on_two_digits($date_right_hour),
			     &format_number_on_two_digits($date_right_mday),
			     &format_number_on_two_digits(&gets_num_month($date_right_month)),
			     &format_number_on_two_digits($date_right_year));
	return  $result_tmloc1 -  ${result_tmloc2};
} # End sub substracts_date


=head1 sub clean_dates(...)

We clean format of one date received. This date olds UTC, at least one space at the begining of the string by nothing, every single ':' character by one space, and many spaces by one (format UTC see above in function gets_formated_date). This is the date format Mon Jul 31 02:15:58 UTC 2006.

=head2 PARAMETER(S)

=over 4

$my_date: that's the string to analyse (here the date).

=back

=head2 RETURNED VALUE

=over 4

Returns new formated date.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Oct 13rd 2005

- I<Created on:> Aug 8th 2005

=back

=cut

sub clean_dates{ # Begin sub clean_dates
	my ($my_date) = @_;

	$my_date =~ s/UTC//ig;
	$my_date =~ s/\:/\ /g; # we remove : and replace it with a space
	$my_date =~ s/^\ *//g; # we remove spaces at the first place
	$my_date =~ s/\ +/\ /g;# we remove spaces and replace them with a single space
	return ($my_date);
}  # End sub clean_dates
	

=head1 sub gets_num_month(...)

From a given month returns its rank in a given year period.

=head2 PARAMETER(S)

=over 4

$month: that's the string that contains the $month.

=back

=head2 RETURNED VALUE

=over 4

Returns rank in a year.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Oct 13rd 2005

- I<Created on:> Aug 8th 2005

=back

=cut

sub gets_num_month { # Begin sub gets_num_month
	my ($month) = @_;
	my $n = 0;
	
	while ($n != 12) { # Begin  while ($n != 12)
		if ($nmonth[$n] =~ m/$month/i ) { # Begin if ($nmonth[$n] =~ m/$month/i )
		    return $n;
		} # End if ($nmonth[$n] =~ m/$month/i )
		$n++;
	} # End while ($n != 12)
	return (11);
}  # End sub gets_num_month


=head1 sub substract(...)

Substracts 2 dates.

=head2 PARAMETER(S)

=over 4

$_[0]: a number

$_[1]: a number

=back

=head2 RETURNED VALUE

=over 4

Returns 0 if < 0 else substraction.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Oct 13rd 2005

- I<Created on:> Aug 8th 2005

=back

=cut

sub substract { # Begin sub substract
	if (($_[0] - $_[1]) < 0 ) { # Begin if (($_[0] - $_[1]) < 0 )
		return 0;
	} # End if (($_[0] - $_[1]) < 0 )
	return ($_[0] - $_[1]);
} # End sub substract


=head1 sub gets_time_epoc(...)

Returns epoc format of date.

=head2 PARAMETER(S)

=over 4

Returns time() that's epoc format.

=back

=head2 RETURNED VALUE

=over 4

Returns new formated string.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Oct 13rd 2005

- I<Created on:> Aug 8th 2005

=back

=cut

sub gets_time_epoc { # Begin sub gets_time_epoc
	return time();
} # End sub gets_time_epoc


=head1 sub  gets_digital_date_format(...)

Returns a digital date on each field 2 digits at least.

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

Returns new formated date as the following format: MM/DD/YY HH:MM:SS.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Oct 13rd 2005

- I<Created on:> Aug 8th 2005

=back

=cut

sub gets_digital_date_format { # Begin sub gets_digital_date_format
	my @my_localtime = localtime(time());
	
	return
		&format_number_on_two_digits($my_localtime[4]+1) . "/" .
		&format_number_on_two_digits($my_localtime[3]) . "/" .
		&format_number_on_two_digits($my_localtime[5]+1900) . " " .
		&format_number_on_two_digits($my_localtime[2]) . ":" .
		&format_number_on_two_digits($my_localtime[1]) . ":" .
		&format_number_on_two_digits($my_localtime[0]);
}  # End sub gets_digital_date_format


=head1 sub  gets_formated_date(...)

Prints a formated date (s.a Sat Sep 10 16:12:01 UTC 2005) according to date function.

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

Returns new formated date as the following format: D_name M_name Num_D HH:MM:SS UTC YYYY.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Oct 13rd 2005

- I<Created on:> Aug 8th 2005

=back

=cut

sub gets_formated_date { # Begin sub gets_formated_date
	return
		&gets_day_name . " " .
		&gets_month_name . " " .
		&format_number_on_two_digits(&gets_num_day) . " " .
		&format_number_on_two_digits(&gets_hour) . ":" .
		&format_number_on_two_digits(&gets_min) . ":" .
		&format_number_on_two_digits(&gets_sec) . " UTC " .
		&gets_year;
} # End sub gets_formated_date


=head1 sub format_number_on_two_digits(...)

Reformats a number on 2 digits.

=head2 PARAMETER(S)

=over 4

$digit: that's the digit to reformat.

=back

=head2 RETURNED VALUE

=over 4

Returns new formated number on 2 digits.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Oct 13rd 2005

- I<Created on:> Aug 8th 2005

=back

=cut

sub format_number_on_two_digits { # Begin sub format_number_on_two_digits
	my ($digit) = @_;
	
	$digit = ($digit == 0 || $digit eq "") ? 0 : $digit;
	return ($digit  < 10) ? "0$digit" : "$digit";
}  # End sub format_number_on_two_digits


=head1 sub gets_sec(...)

Returns seconds from localtime() function

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

Returns second from local time.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Oct 13rd 2005

- I<Created on:> Aug 8th 2005

=back

=cut

sub gets_sec { # Begin sub gets_sec
	return ((localtime(time()))[0]);
}  # End sub gets_scec


=head1 sub gets_min(...)

Returns minutes from localtime() function.

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

Returns second from local time.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Oct 13rd 2005

- I<Created on:> Aug 8th 2005

=back

=cut

sub gets_min { # Begin sub gets_min
	return ((localtime(time()))[1]);
}  # End sub gets_min


=head1 sub gets_hours(...)

Returns hours from localtime() function.

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

Returns hours from local time.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Oct 13rd 2005

- I<Created on:> Aug 8th 2005

=back

=cut

sub gets_hour { # Begin sub gets_hour
	return ((localtime(time()))[2]);
}  # End sub gets_hour


=head1 sub gets_num_day(...)

Returns number of the day from localtime() function

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

Returns second from local time.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Oct 13rd 2005

- I<Created on:> Aug 8th 2005

=back

=cut

sub gets_num_day { # Begin sub gets_num_day
	return ((localtime(time()))[3]);
} # End sub gets_num_day


=head1 sub gets_month(...)

Returns month from localtime() function.

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

Returns second from local time.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Oct 13rd 2005

- I<Created on:> Aug 8th 2005

=back

=cut

sub gets_month {
	return ((localtime(time()))[4]);
}


=head1 sub gets_month_name(...)

Returns month name from localtime() function.

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

Returns second from local time.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Oct 13rd 2005

- I<Created on:> Aug 8th 2005

=back

=cut

sub gets_month_name { # Begin sub gets_month_name
	return ($nmonth[(localtime(time()))[4]]);
}  # End sub gets_month_name


=head1 sub gets_year(...)

Returns year from localtime() function.

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

Returns second from local time.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Oct 13rd 2005

- I<Created on:> Aug 8th 2005

=back

=cut

sub gets_year { # Begin sub gets_year
	return (1900+(localtime(time()))[5]);
} # End sub gets_year


=head1 sub gets_day_name(...)

Returns day name from localtime() function.

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

Returns second from local time.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Oct 13rd 2005

- I<Created on:> Aug 8th 2005

=back

=cut

sub gets_day_name { # Begin sub gets_day_name
	return ($nday[(localtime(time()))[6]]);
}  # End sub gets_day_name


=head1 sub gets_day_num_in_year(...)

Returns day number from Jan 1st from current year from localtime() function.

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

Returns second from local time.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Oct 13rd 2005

- I<Created on:> Aug 8th 2005

=back

=cut

# Returns day number from Jan 1st from current year from localtime() function
sub gets_day_num_in_year { # Begin sub gets_day_num_in_year
	return ((localtime(time()))[7]);
} # End sub gets_day_num_in_year


=head1 sub gets_name_of_the_day_from_string(...)

Gets name of the day  from this date format Sat Sep 10 16:12:01 UTC 2005.

=head2 PARAMETER(S)

=over 4

$string: UTC string clean (see gets_formated_date for the string format).

=back

=head2 RETURNED VALUE

=over 4

Returns second from local time.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Oct 13rd 2005

- I<Created on:> Aug 8th 2005

=back

=cut

sub gets_name_of_the_day_from_string { # Begin sub gets_name_of_the_day_from_string
	my ($string) = &clean_dates($_[0]);
	
	return ((split(/\ /,$string))[0]);
}  # End sub gets_name_of_the_day_from_string


=head1 sub gets_month_from_string(...)

Gets month from this date format Sat Sep 10 16:12:01 UTC 2005.

=head2 PARAMETER(S)

=over 4

$string: UTC string clean (see gets_formated_date for the string format).

=back

=head2 RETURNED VALUE

=over 4

Returns second from local time.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Oct 13rd 2005

- I<Created on:> Aug 8th 2005

=back

=cut

sub gets_month_from_string { # Begin sub gets_month_from_string
	my ($string) = &clean_dates($_[0]);
	
	return ((split(/\ /,$string))[1]);
}  # End sub gets_month_from_string



=head1 sub gets_month_number_from_string(...)

Gets month from this date format Sat Sep 10 16:12:01 UTC 2005.

=head2 PARAMETER(S)

=over 4

$string: UTC string clean (see gets_formated_date for the string format).

=back

=head2 RETURNED VALUE

=over 4

Returns second from local time.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Oct 13rd 2005

- I<Created on:> Aug 8th 2005

=back

=cut

sub gets_month_number_from_string { # Begin sub gets_month_number_from_string
	my ($string) = &clean_dates($_[0]);
	my $counter = 0;
	
	foreach my $m (@nmonth) { # Begin foreach my $m (@nmonth)
		if ($string =~ m/$m/i) { # Begin if ($string =~ m/$m/i)
		    return $counter;
		}  # End if ($string =~ m/$m/i)
		$counter++;
	} # End foreach my $m (@nmonth)
	return -1;
}  # End sub gets_month_number_from_string


=head1 sub gets_day_number_from_string(...)

Gets day number in month from this date format Sat Sep 10 16:12:01 UTC 2005.

=head2 PARAMETER(S)

=over 4

$string: UTC string clean (see gets_formated_date for the string format).

=back

=head2 RETURNED VALUE

=over 4

Returns second from local time.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Oct 13rd 2005

- I<Created on:> Aug 8th 2005

=back

=cut

sub gets_day_number_from_string { # Begin sub gets_day_number_from_string
	my ($string) = &clean_dates($_[0]);
	
	return ((split(/\ /,$string))[2]);
} # End sub gets_day_number_from_string


=head1 sub gets_hour_from_string(...)

Gets hour from this date format Sat Sep 10 16:12:01 UTC 2005

=head2 PARAMETER(S)

=over 4

$string: UTC string clean (see gets_formated_date for the string format).

=back

=head2 RETURNED VALUE

=over 4

Returns second from local time.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Oct 13rd 2005

- I<Created on:> Aug 8th 2005

=back

=cut

sub gets_hour_from_string { # Begin sub gets_hour_from_string
	my ($string) = &clean_dates($_[0]);
	
	return ((split(/\ /,$string))[3]);
} # End sub gets_hour_from_string


=head1 sub gets_minutes_from_string(...)

Gets minutes from this date format Sat Sep 10 16:12:01 UTC 2005.

=head2 PARAMETER(S)

=over 4

$string: UTC string clean (see gets_formated_date for the string format).

=back

=head2 RETURNED VALUE

=over 4

Returns second from local time.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Oct 13rd 2005

- I<Created on:> Aug 8th 2005

=back

=cut
	
sub gets_minutes_from_string { # Begin sub gets_minutes_from_string
	my ($string) = &clean_dates($_[0]);
	
	return ((split(/\ /,$string))[4]);
}  # End sub gets_minutes_from_string


=head1 sub gets_seconds_from_string(...)

Gets seconds from this date format Sat Sep 10 16:12:01 UTC 2005.

=head2 PARAMETER(S)

=over 4

$string: UTC string clean (see gets_formated_date for the string format).

=back

=head2 RETURNED VALUE

=over 4

Returns second from local time.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Oct 13rd 2005

- I<Created on:> Aug 8th 2005

=back

=cut

sub gets_seconds_from_string { # Begin sub gets_seconds_from_string
	my ($string) = &clean_dates($_[0]);
	
	return ((split(/\ /,$string))[5]);
}  # End sub gets_seconds_from_string


=head1 sub gets_utc_from_string(...)

Gets UTC from this date format Sat Sep 10 16:12:01 UTC 2005.

=head2 PARAMETER(S)

=over 4

$string: that's the date (format UTC see above in function gets_formated_date).

=back

=head2 RETURNED VALUE

=over 4

Returns UTC.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Oct 13rd 2005

- I<Created on:> Aug 8th 2005

=back

=cut

sub gets_utc_from_string { # Begin sub gets_utc_from_string
	my ($string) = &clean_dates($_[0]);
	
	return ((split(/\ /,$string))[6]);
} # End sub gets_utc_from_string


=head1 sub gets_year_from_string(...)

Gets year from this date format Sat Sep 10 16:12:01 UTC 2005.

=head2 PARAMETER(S)

=over 4

$string: that's the date (format UTC see above in function gets_formated_date).

=back

=head2 RETURNED VALUE

=over 4

Returns seconds from local time.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Oct 13rd 2005

- I<Created on:> Aug 8th 2005

=back

=cut

sub gets_year_from_string { # Begin sub gets_year_from_string
	my ($string) = &clean_dates($_[0]);

	return ((split(/\ /,$string))[7]);
}  # End sub gets_year_from_string


=head1 sub test_for_equal(...)

Tests if two dates $d1 and $d2 are equal then prints the result.

=head2 PARAMETER(S)

=over 4

$d1 = localtime(timelocal(time()));

$d2 = localtime(timelocal(time()));

=back

=head2 RETURNED VALUE

=over 4

None.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Oct 13rd 2005

- I<Created on:> Aug 8th 2005

=back

=cut

sub test_for_equal { # Begin sub test_for_equal
	my ($d1,$d2) = @_;

	print "equal:( $d1,$d2):" . print_res("$d1","$d2", are_dates_equal( "$d1","$d2"));
}  # End sub test_for_equal


=head1 sub test_for_greater(...)

Tests if two dates $d1 is greater than $d2 and prints the result.

my $d1 = localtime(timelocal(time()));

my $d2 = localtime(timelocal(time()));

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

None.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Oct 13rd 2005

- I<Created on:> Aug 8th 2005

=back

=cut

sub test_for_greater { # Begin sub test_for_greater
	my ($d1,$d2) = @_;

	print "greater:( $d1,$d2):" . print_res("$d1","$d2", are_dates_greater( "$d1","$d2"));
}  # End sub test_for_greater


=head1 sub test_for_smaller(...)

Function looks if date $d1 is smaller than date $d2 then prints the results.

my $d1 = localtime(timelocal(time()));

my $d2 = localtime(timelocal(time()));

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

Returns second from local time.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Oct 13rd 2005

- I<Created on:> Aug 8th 2005

=back

=cut

sub test_for_smaller { # Begin sub test_for_smaller
	my ($d1,$d2) = @_;

	print "smaller:( $d1,$d2):" . print_res("$d1","$d2", are_dates_smaller( "$d1","$d2"));
} # End sub test_for_smaller


=head1 FUNCTION add_days(...)

This function adds days to a given date and returns its result like this yyyy/mm/dd

=head2 PARAMETER(S)

=over 4

$year: it is the year here 2006

$month: Number of the month in the year: $month = 7

$num_day: day number (without st, sd or, th) in a month. Jul 1st 2006 will be $num_day = 1

$lag_day: that's the lag between the given day (see date above) and the new date that will be (Jul 1st 2006) + 7 days

$schedule: that's a given scheduler: 1 hour(s) 2 min(s) 5sec(s)

=back

=head2 RETURNED VALUE

=over 4

Returns a specific date as this format yyyy/mm/dd.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 EXEMPLE(S)

=over 4

&add_days("3","Feb","2006",4); is the 3rd of Feb 2006 and will return after a lag of 4 days new day s.a 2006/02/7.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Jul 29th 2006

- I<Created on:> Jul 29th 2006

=back

=cut

sub add_days { # Begin sub add_days
	my ($year,$month,$num_day,$lag_day) = @_;
	my $my_lag = 0;
	my $prev_num_day_date = $num_day;
	my $local_rank_month = $month;
	my $num_day_month = $month_rank_day{$month};

	while ($my_lag < $lag_day) { # Begin while ($my_lag < $lag_day)
		#    print "$num_day/$num_day_month $rank_month $year    $lag_day  $my_lag\n";
		$num_day %= $num_day_month;
		$num_day++;
		if ($prev_num_day_date > $num_day) { # Begin if ($prev_num_day_date > $num_day)
			$num_day = 1;
			$local_rank_month++;
			if ($local_rank_month > 12) { # Begin if ($local_rank_month > 12)
				$local_rank_month = 1;
				$num_day = 1;
				$year++;
			}  # End if ($local_rank_month > 12)
		} # End if ($prev_num_day_date > $num_day)
		if ($local_rank_month == 2) { # Begin if ($local_rank_month == 2)
			if ((($year % 100) == 0) && ($year % 400) == 0) { # Begin if ((($year % 100) == 0) && ($year % 400) == 0)
				$num_day_month = 30;
			} # End if ((($year % 100) == 0) && ($year % 400) == 0)
			elsif (($year % 4) == 0) { # Begin elsif (($year % 4) == 0)
				$num_day_month = 30;
			} # End elsif (($year % 4) == 0)
		} # End if ($local_rank_month == 2)
		else { # Begin else
			$num_day_month = $month_rank_day{$local_rank_month};
		}  # End else
		$prev_num_day_date = $num_day;
		$my_lag++;
	}  # End while ($my_lag < $lag_day)
	return "DAY_NAME $month_rank{$local_rank_month} ${num_day}  $year";
}  # End sub add_days

1;

=head1 SEE ALSO

Look packages Fcntl, Time::Local,

=cut

=head1 AUTHOR

Current maintainer: M. Flotilla Reindeer, <flotilla.reindeer@laposte.net>

=cut
