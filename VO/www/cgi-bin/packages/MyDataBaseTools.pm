package packages::MyDataBaseTools;

# +-------------------------------+
# | Dorey Sebastien               |
# | MyDataBaseTools.pm            |
# | Written     on Oct 3rd 2005   |
# | Last update on Oct 4th 2005   |
# +-------------------------------+
  
require Exporter;

$VERSION    = '1.0';
$VERSION    = eval $VERSION;
@ISA    = qw( Exporter );
@EXPORT = qw( 
	      get_field transform_log_book add add_new_field_id_ip
	      );
@EXPORT_OK = qw();

use packages::Common;
use packages::MyCrypto;


# This routine transforms the logfile
sub transform_log_book {
    my ($file_name) = @_;
    my @file = &open_log_book("$file_name");
    my $f = "a_$file_name.tmp";
    my $counter = 0;

    if (!&is_already_transformed($file_name)) { # Begin if (!&is_already_transformed($file_name))
	open(RE_ARRANGE,">$f") or die("Can't create $f $!");    
	foreach (@file) { # Begin foreach (@file)
	    if ($_ =~ m/[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/) { # Begin if ($_ =~ m/[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/)
		my $line_to_record = ();
		chomp ($_);
		my $ll = &rearange($_);
		my @line_array = &get_field($ll);
		my $size = @line_array;
		
		print "$size: ";
		if ($size == 3) { # Begin if ($size == 3)
		    $line_array[1] =~ s/\ $//g;
		    $line_array[1] =~ s/\ /\_/g;
		    $line_array[1] = "0-$line_array[1]";
		    if ($line_array[0] =~ m/first/) { # Begin if ($line_array[0] =~ m/first/)
			$line_to_record = "$line_array[1]*$line_array[2]*X*X";
		    }  # End if ($line_array[0] =~ m/first/)
		    else {
			$line_to_record = "$line_array[1]*$line_array[2]*X*X";
		    }
		} # End if ($size == 3)
		elsif ($size == 4) { # Begin if ($size == 4)
#		    print "case 1.0:(";
#		    foreach (@line_array) {
#			print "\"$_\" ";
#		    }
#		    print "):";
		    $line_array[2] =~ s/\ $//g;
		    $line_array[2] =~ s/\ /\_/g;
#		    $line_array[1] = "0-$line_array[1]";
		    if ($line_array[1] =~ m/\ at\ this\ address/) {
#			print "($line_array[1])\n";
			$line_array[1] =~ s/([0-9])+\ at\ this\ address/$line_array[0]\*$1/;
			$line_to_record = "0-$line_array[2]*$line_array[3]*$line_array[1]";
		    } else {
#			print "case 1.1:";
			$line_to_record = "0-$line_array[2]*$line_array[3]*$line_array[1]*X";
		    } # End if ($size == 4)
#		    else {
#			print "case 1.2:";
#			$line_array[2] =~ s/\ /\_/g;
#			$line_to_record	= "$line_array[1]*$line_array[2]*X*X*$line_array[3]\n";
#		    }
		}
		elsif ($size == 5) { # Begin if ($size == 5)
		    $line_array[2] =~ s/\ $//g;
		    $line_array[2] =~ s/\ /\_/g;
		    $line_array[2] = "0-$line_array[2]";
		    $line_array[3] =~ s/\ +//g;
		    if ($line_array[1] =~ m/\ at\ this\ address/) { # Begin if ($line_array[1] =~ m/\ at\ this\ address/)
			$line_array[1] =~ s/\ at\ this\ address//g;

			$line_to_record = "$line_array[2]*$line_array[3]*$line_array[0]*$line_array[1]" . (($line_array[4] =~ m/\@/) ? "" :  "*$line_array[4]");
		    } # End if ($line_array[1] =~ m/\ at\ this\ address/)
		    else {
			$line_to_record = "$line_array[2]*$line_array[3]*$line_array[1]*X" . (($line_array[4] =~ m/\@/) ? "" :  "*$line_array[4]");
		    }
		} # End if ($size == 5)
		elsif ($size == 6) { # Begin if ($size == 6)
		    $line_array[2] =~ s/\ $//g;
		    $line_array[2] =~ s/\ /\_/g;
		    if ($line_array[4] =~ m/\@/) { # Begin if ($line_array[4] =~ m/\@/) (case email)
			$line_to_record = "0-$line_array[2]*$line_array[3]*$line_array[1]*X*$line_array[5]";
		    } # End if ($line_array[4] =~ m/\@/) (case email)
		    else {
			$line_to_record = "$line_array[0]*$line_array[4]*$line_array[1]*$line_array[2]*$line_array[5]";
		    }
		} # End if ($size == 6)
		else {
		    print "to trash " . $ll . "\n";
		}
#		chomp($line_to_record);
#		$counter++;
		my @keys = create_keys;
		my $m = jarriquez_givenKey_encrypt("$line_to_record*$counter",@keys);
		my $n = substr($m,2,length($m)/2);
#		if ($line_to_record =~ m/0\-/) {# Begin if ($line_to_record =~ m/0\-/) 
#		    print RE_ARRANGE "$line_to_record*ok*X\n";
#		    print            "$line_to_record*ok*X\n";
#		} # End if ($line_to_record =~ m/0\-/) 
#		else { # Begin if ($line_to_record !~ m/0\-/) 
		    print RE_ARRANGE "$line_to_record*ok*$n\n";
		    print            "$line_to_record*ok*$n\n";
#		} # End if ($line_to_record !~ m/0\-/) 
	    } # End if ($_ =~ m/[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/) {
	} # End foreach
	close(W);
#	copy_file("$f","$file_name");
    } # End if (!&is_already_transformed($file_name))
    return $f;
}

# We get ip address from ID
sub get_ip_from_id  {
    my ($file,$id) = @_;
    my $f = 0;
    my @lines = ();

    sysopen(READ_FILE,"${file}",O_RDONLY) or die("Can't read file $file $!");
    @lines = <READ_FILE>;
    close(READ_FILE);
    foreach (@lines) {
	my $line = $_;
	chomp($line);
	my $one_id = (split(/\*/,$line))[5];

	if ($one_id == $id) {
	    return (split(/\*/,$line))[1];
	}
    }
}

# Add a new fields to DB s.a special id
sub add_new_field_id_ip {
    my ($file) = @_;
    my @lines = ();
    my $counter = 0;
    my $f = "a_${file}";

    sysopen(READ_FILE,"${file}",O_RDONLY) or die("Can't read file $file $!");
    @lines = <READ_FILE>;
    close(READ_FILE);
    open(WRITE_FILE,">$f") or die("Can't create file $f $!");
    foreach (@lines) {
	chomp($_);
	@keys = create_keys;
	$m = jariquez_givenKey_encrypt("$_*$counter",@keys);
	$n = substr($m,0,length($m)/2);
	$_ .= "ok*$n\n";
	print "$_";
	print WRITE_FILE $_;
	$counter++;
	sleep(3);
    }
    close(WRITE_FILE);
    return $f;
}

# This function add a new line in $file (that's usually a logfile)
sub add {
    my ($file,$date_process,$ip_address,$choice,$visit_number,$access_grant) = @_;
    my $line_to_record = "$date_process,$ip_address,$choice,$visit_number,$access_grant\n";

    sysopen(WRITE_APPEND,"$file",O_APPEND|O_WRONLY) or die("Can't azppend to file $file $!");
    print WRITE_APPEND "$line_to_record";
    close(WRITE_APPEND);
}

# Returns an array of the log file
sub get_field {
    my ($line) = @_;

    return (split(/\*/,$line));
}

# Get file
sub open_log_book {
    my ($file_name) = @_;

    sysopen(R_LOG_BOOK,"$file_name",O_RDONLY) || die("File $file_name does not exists $!");
    my @file_content = 	<R_LOG_BOOK>;
    close(R_LOG_BOOK);
    return @file_content;
}

# Rearange line
sub rearange {
    my ($line) = @_;

    $line =~ s/Logged\ on\ //g;
    $line =~ s/\ by\ user\ with\ address\ /\*/g;
    $line =~ s/Menu\ choosen\ /\*/g;
    $line =~ s/[\ ]+/\ /g;
    $line =~ s/(\ )([0-9])(\ )/${1}0$2$3/g;
    $line =~ s/\ logged\ /\*/g;
    $line =~ s/\ time\(s\)//;
    $line =~ s/at\ this\ address\ //g;
    $line =~ s/TAG.*ADDRESS/\*/g;
    $line =~ s/TAG/\*/g;
    $line =~ s/\<\/a\>//g;
    $line =~ s/\ ID/\*/g;
    $line =~ s/\ WEB_ACCESS_GRANT/\*/;
    $line =~ s/PID\ at\ this\ address//g;
    $line =~ s/\*\*/\*/g;
    return $line;
}

# This routine is local and check is lofile file already transformed
sub is_already_transformed {
    my ($file_name) = @_;
    my ($process,$rest) = ();

    open(R,"$file_name") or die("$file_name");
    my @f = <R>;
    close(R);
    foreach (@f) { # Begin foreach (@f) 
	($process,$rest) = split(/\-/,$_);

	if ($process !~ m/^[0-9]+$/) { # Begin if ($process !~ m/^[0-9]+$/)
	    return ($process =~ m/^[0-9]+$/);
	} # End if ($process !~ m/^[0-9]+$/)
    } # End foreach (@f) 
    return ($process =~ m/^[0-9]+$/);
}

1;
