package packages::MyDaemon;

# +-------------------------------+
# | Dorey Sebastien               |
# | Daemon.pm                       |
# | Written on August 8 th 2005   |
# | Last update on Sept 19th 2005 |
# +-------------------------------+
  
require Exporter;

$VERSION    = '1.0';
$VERSION    = eval $VERSION;
@ISA    = qw( Exporter );
@EXPORT = qw( start_daemon );
@EXPORT_OK = qw(  );

use packages::Common;

sub start_daemon {
    my ($log_f,$log_index) = @_;
    my $laps = ();
    my $my_date_stamp = get_formated_date;
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
    my @stat_file_log_index = stat($log_index);
    
    chomp($my_date_stamp);
    sysopen(CREATE_WRITE_FILE,"$log_f",O_WRONLY|O_CREAT) or die("Cannot open RW $log_index");
    flock(WRITE_INDEX,LOCK_EX);
    print CREATE_WRITE_FILE "$my_date_stamp\n";
    close(CREATE_WRITE_FILE);
    $line = get_formated_date;
    chomp($line);
    $laps = dates_substracted($line,$my_date_stamp);
    chomp($laps);
    while (1) { # Begin while (1)
	my ($val,$loc_time) = split(/\ \ /,$laps);
	
	if ( -f "$log_f" ) {
	    if ($val < 59 ) {
		open(R,"$log_f");
		$file_fork = <R>;
		close(R);
		$line = (split(/\n/,$file_fork))[0];
		chomp($line);
		open(W,">$log_f");
		print W "$line\n";
		$my_date_stamp = get_formated_date ;
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
    } # End while (1)
    close(W);
}

1;
