#!/usr/bin/perl -wT

# +-------------------------------+
# | Dorey Sebastien               |
# | index.cgi                     |
# | Written on August 29th 2005   |
# | Last update on Sept 21st 2005 |
# +-------------------------------+

BEGIN {
    @INC = (@INC,"/usr/local/home/users/dorey_s/www/cgi-bin");
    @INC = (@INC,"/usr/local/home/users/dorey_s/www/");
}

use Time::Local;
use Fcntl qw(:DEFAULT :flock);
use packages::Common;
use packages::Time;
use CGI;

my $cgi = new CGI();
my $sid = create_short_id;
my $log_file = "loguser";
my $dir      = "../logbook";
my $log_index= "$dir/index_log.txt";
my $log_f    = "$dir/one_log.$sid.txt";
my $id_session= $cgi->param("id_session");
my $id_index = create_short_id;
my $next_page= $cgi->param("next_page");

chomp($id_index);

print "Content-type: text/html\n\n";
print "($next_page;$id_session)";
if (!defined($child_pid = fork())) {
    die "Cannot fork $!";
}elsif ($child_pid) {
    if ( !&is_current_website_not_permitted ) {
	if (! -f "done") {	
	    & grant_access_info_websites;
	}
	insert_info_logfile("That's the first page","$log_file","$id_index");
	print_file("$next_page",$id_session);
    } else {
	print "not permitted<br><br>";
	print "<center><img src=\"image/farside.gif\"></center>\n";
    }
} else  {
    my $laps = ();
    my $my_date_stamp = `date`;
    my $line = ();

    if (!-d "$dir") {
	mkdir("$dir");
    }

    if (-f "$log_index") {
	sysopen(APPEND_WRITE_INDEX,"$log_index",O_WRONLY|O_APPEND) or die("Cannot open RW $log_index");
	flock(APPEND_WRITE_INDEX,LOCK_EX);
	print APPEND_WRITE_INDEX "$id_index" . "=$log_f\n";
	close(APPEND_WRITE_INDEX);
    } else {
	sysopen(WRITE_INDEX,"$log_index",O_WRONLY|O_CREAT) or die("Cannot open RW $log_index");
	flock(WRITE_INDEX,LOCK_EX);
	print WRITE_INDEX "$id_index" . "=$log_f\n";
	close(WRITE_INDEX);	
    }
    chomp($my_date_stamp);
    sysopen(CREATE_WRITE_FILE,"$log_f",O_WRONLY|O_CREAT) or die("Cannot open RW $log_index");
    flock(WRITE_INDEX,LOCK_EX);
    print CREATE_WRITE_FILE "$my_date_stamp\n";
    close(CREATE_WRITE_FILE);
    $line = `date`;
    chomp($line);
    $laps = dates_substracted($line,$my_date_stamp);
    chomp($laps);

    while (1) {
	my ($val,$loc_time) = split(/\ \ /,$laps);

#	print "($val,$loc_time) $laps\n";
	if ( -f "$log_f" ) {
	    if ($val < 59 ) {
		open(R,"$log_f");
		$file_fork = <R>;
		close(R);
		$line = (split(/\n/,$file_fork))[0];
		chomp($line);
		open(W,">$log_f");
		print W "$line\n";
		$my_date_stamp = `date`;
		chomp($my_date_stamp);
		$laps = dates_substracted($my_date_stamp,$line);
		chomp($laps);
		print W "$my_date_stamp laps:$laps\n";
		close(W);
		sleep(1);
	    } else {
		close(W);
		print "end 1\n";
		exit(-1);
	    }
	} else {
	    close(W);
	    print "end 3\n";
	    exit(-1);
	}
    }
    close(W);
    send_mail;
}

# Check the black list
sub is_current_website_not_permitted {
    my $current_web_site = &return_website_address_format_according_to_permission;
    
    open(READ_FILE_LOG,"$log_file") or die("$log_file not found\n");
    foreach my $i (<READ_FILE_LOG>) {
	chomp($i);
	if ($i =~ m/$current_web_site/) {
	    my ($other,$grant) = split(/\ WEB_ACCESS_GRANT/,$i);
	    if ($grant eq "nok") {
		close(READ_FILE_LOG);
		return (1); # ok not permitted 
	    } elsif ($grant eq "nallok") {
		close(READ_FILE_LOG);
		return (1); # ok not permitted 
	    }
	}
    }
    close(READ_FILE_LOG);
    # ok can log on website
    return (0);
}

# Return the format of current url to check
sub return_website_address_format_according_to_permission {
    my $current_web_site = $ENV{REMOTE_HOST} || $ENV{REMOTE_ADDR};
    
    open(READ_FILE_LOG,"$log_file") or die("$log_file not found\n");
    foreach my $i (<READ_FILE_LOG>) {
	chomp($i);
	if ($i =~ m/$current_web_site/) {
	    my ($other,$grant) = split(/\ WEB_ACCESS_GRANT/,$i);

	    if ($grant eq "nallok") {
		close(READ_FILE_LOG);
		my @new_url = split(/\./,$current_web_site);
		return ("$new_url[0].$new_url[1].$new_url[2]"); # ok not permitted 
	    }
	}
    }
    close(READ_FILE_LOG);
    # ok can log on website
    return ($current_web_site);
}

# We check if a user or ip address ios already in DB and we count it
# now we insert info for the DB s.a IP address, time, and counter (see above)
sub grant_access_info_websites {
    sysopen(READ_FILE_LOG,"$log_file",O_RDONLY) or die("$log_file not found\n");;
    flock(READ_FILE_LOG,LOCK_EX);
    sysopen(WRITE_FILE_LOG_TMP,"$log_file.tmp",O_WRONLY) or die("File $log_file.tmp problem");
    flock(WRITE_FILE_LOG_TMP,LOCK_EX);
    foreach my $i (<READ_FILE_LOG>) {
	chomp($i);
	if ($i =~ m/WEB_ACCESS_GRANT/m) {
	    print WRITE_FILE_LOG_TMP "${i}\n";
	} else {
	    print WRITE_FILE_LOG_TMP "${i} WEB_ACCESS_GRANTok\n";
	}
    } 
    close(READ_FILE_LOG);
    close(WRITE_FILE_LOG_TMP);
    copy_file("$log_file.tmp","$log_file");
# unlink loguser.tmp;
}

