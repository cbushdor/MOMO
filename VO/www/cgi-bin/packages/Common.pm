package packages::Common;
require Exporter;

# +-------------------------------+
# | Dorey Sebastien               |
# | Common.pm                     |
# | Written on Sept 13rd 2005     |
# | Last update on Nov 3rd 2005   |
# +-------------------------------+

# The aim of this package is to gather all functions that are basic

$VERSION    = '1.0';
$VERSION    = eval $VERSION;
@ISA        = qw( Exporter );
@EXPORT     = qw(
		 get_script_file_name
		 print_file       copy_file  insert_info_logfile get_file_content                         send_mail
		 get_current_date auth       create_id get_id    get_password                             create_short_id 
		 send_mail        head       get_line_logbook    insert_info_when_index_already_created   my_head_definition
		 );
# @EXPORT_OK  = qw( $file_log );

use Fcntl qw(:DEFAULT :flock);
use Time::Local;
use packages::MyTime;
use packages::MyCrypto;

# Returns current script name
sub get_script_file_name {
    my ($f_name)    = @_;
    my $f_name_size = split(/\//,$f_name);

    return (split(/\//,$f_name))[$f_name_size-1];
}

# Inserts info in a secure way with sysopen and flock in log_file
sub insert_info_logfile {
    my ($menu_info,$log_file,$id_index) = @_;
    my $rem_host = $ENV{REMOTE_HOST} || $ENV{REMOTE_ADDR};
    my $ip_counter = 0;
    my $max_line = 1;
#    my $id = &create_short_id;

    chomp($rem_host);
    sysopen(READ_LOG_USER_FILE,"$log_file",O_RDONLY) or die("Pb with $log_file: $!");
#    flock(READ_LOG_USER_FILE,LOCK_EX);
    foreach (<READ_LOG_USER_FILE>) { 
	$max_line++;
	chomp($_);
	if ($_ =~ m/$rem_host/) {
	    $ip_counter++;
	}
    }
    close(READ_LOG_USER_FILE);
    sysopen(APPEND_LOG_USER_FILE,"$log_file",O_WRONLY|O_APPEND) or die("Pb with $log_file: $!");
    flock(APPEND_LOG_USER_FILE,LOCK_EX);
    $mydate = &get_current_date;
    @keys = create_keys;
    my $enc_line = jarriquez_givenKey_encrypt("$id_index*$rem_host*$menu_info*$ip_counter*ok*$max_line",@keys);
    $enc_line =~ s/[\'\"]//g;
    my $trunc_enc_line = substr($enc_line,0,length($enc_line)/2);
    print APPEND_LOG_USER_FILE "$id_index*$rem_host*$menu_info*$ip_counter*ok*$trunc_enc_line\n";
    close(APPEND_LOG_USER_FILE);
}

# Inserts info in a file according to $id_session
sub insert_info_when_index_already_created {
    my ($id_session,$menu_name) = @_;
    my $my_date_stamp = ();

    chomp($id_session); # can be removed to check
    sysopen(APPEND_WRITE_FILE,"$id_session",O_WRONLY|O_APPEND) or die("Cannot open $id_session $!");
    flock(APPEND_WRITE_FILE,LOCK_EX);
    $my_date_stamp = get_formated_date;
#    chomp($my_date_stamp);
    print APPEND_WRITE_FILE "\n$my_date_stamp*$menu_name\n";
    close(APPEND_WRITE_FILE);
}


# We get current date
sub get_current_date {
    return get_formated_date ;
}

# Print a file
sub print_file {
    my ($file_name,$id) = @_;

    open(READ_INDEX,"$file_name") or die("file $file_name does not exist $!\n");
    foreach my $o (<READ_INDEX>) {
	$o =~ s/\_\_id\_session\_\_/$id/g;
	print "$o";
    }
    close(READ_INDEX);
    return 0;
}

# Do a basic copy from one file(src) to another (dst)
sub copy_file {
    my ($src,$dst) = @_;
    
    sysopen(READ_SRC,"$src",O_RDONLY) or die("Cant read file $src: $!\n");
    flock(READ_SRC,LOCK_EX);
    sysopen(WRITE_DST,"$src",O_WRONLY) or die("Cant read file $src: $!\n");
    flock(WRITE_DST,LOCK_EX);
    foreach my $line (<READ_SRC>) {
	chomp($line);
	print WRITE_DST "$line\n";
    }
    close(WRITE_DST);
    close(READ_SRC);
    return 0;
}

# Authentication
sub auth {
    my ($one_address,$name_script,@other) = @_;
    my $process = ();
    my $margin = "     ";

    $process = &create_id;
    print  $margin . "<table width=100\% border=0>\n";
    print  $margin . "    <tr>\n";
    print  $margin . "        <td valign=op align=right bgcolor=\#002E40>\n";
    print  $margin . "            <form action=\"$name_script\" method=post>\n";
    print  $margin . "                 <font color=yellow>Can you give me your ticket please</font>\n";
    print  $margin . "                 <input type=password name=password>\n";
    print  $margin . "                 <input type=hidden name=address value=$one_address>\n";
    if (&my_length_array(@other)) {
	foreach my $i (@other) {
	    my ($name,$value) = split(/\=/,$i);

	    print  $margin . "                 <input type=hidden name=$name value=$value>\n";
	}
    }
    print $margin . "                  <input type=hidden name=process value=\'$process\'>\n";
    print $margin . "         <td valign=center align=center>\n";
    print $margin . "                  <input type=submit value=Submit>\n";
    print $margin . "             </form>\n";
    print $margin . "             <form action=\"JavaScript:window.close();\" method=post>\n";
    print $margin . "                  <input type=submit value=\"Close\">\n";
    print $margin . "             </form>\n";
    print $margin . "     </tr>\n";
    print $margin . "</table>\n";    
}

# That's bs but return size of array
sub my_length_array {
    my $c = 0;

    foreach (@_) {
	$c++;
    }
    return $c;
}

# Create id for the session
sub create_id {
    my $date                = &get_current_date;
    my @keys                = create_keys;
    my $sentence_to_encrypt = ();
    my $encrypted_sentence  = ();
    my $counter             = 0;

    chomp($date);    
    $sentence_to_encrypt = "$$-$date-";
#    $encrypted_sentence = jarriquez_givenKey_encrypt($sentence_to_encrypt,@keys);
    $encrypted_sentence = $sentence_to_encrypt;
#    chop($encrypted_sentence);
    sysopen(W_MY_PROCESS,"my_process",O_CREAT|O_WRONLY) or die("Cannot create my_process file $!");
    print   W_MY_PROCESS "$encrypted_sentence";
#    print   W_MY_PROCESS "$sentence_to_encrypt";
    close  (W_MY_PROCESS);
    return $encrypted_sentence;
}

# Create id for the session
sub create_short_id {
    my $sentence_to_encrypt = $$;
    my $date = &get_current_date;
    my @keys = create_keys;
    my $encrypted_sentence = ();

    $date =~ s/\ /\_/g;
    chomp($date);    
    $sentence_to_encrypt .= "-" . $date;
    $encrypted_sentence = jarriquez_givenKey_encrypt($sentence_to_encrypt,@keys);
    return $encrypted_sentence;
}

# Get id of previous session
sub get_id {
    if (-f "my_process") {
	my $old_id = ();

	open(R_MY_PROCESS,"my_process") or die("Cannot create file");
	$old_id = <R_MY_PROCESS>;
	close(R_MY_PROCESS);
	chomp($old_id);
	
	return $old_id;
    }
    return 0;
}

sub get_password {
    my $my_password = ();
    my ($conf_file) = @_;
    
    open(READ_CONF_FILE,"$conf_file") or die("$conf_file cannot be found $! !!!!");
    foreach my $i(<READ_CONF_FILE>) {
	chomp($i);
	$my_password .= $i;
    }
    close(READ_CONF_FILE);
    return $my_password;
}

# Get the file content
sub get_file_content {
    my ($conf_file) = @_;
    my @file_content = ();
    
    open(READ_CONF_FILE,"$conf_file") or die("File -- $conf_file -- cannot be found $!");
    @file_content = <READ_CONF_FILE>;
    close(READ_CONF_FILE);
    return @file_content;
}

sub send_mail {
    my ($from,$to,$subject,$message) = @_;
    open(SENDMAIL, "|/usr/sbin/sendmail -oi -t -odq") or die("Can't fork for sendmail: $!\n");
    print SENDMAIL "   From: Dorey Sebastien's web site <$from>\n";
    print SENDMAIL "     To: dorey_s <$to>\n";
    print SENDMAIL "Subject: $subject\n";
    print SENDMAIL "$message\n";
    close(SENDMAIL)     or warn "sendmail didn't close nicely";
}


# Refresh screen
sub head {
    my ($timer,$load_prog) = @_;
    my ($ref) = &get_line_logbook(@file);
    my $new_id = &create_id;

    print "<head>\n";
    print "<script>\n";
    print "function display_time_in_status_line()\n";
    print "{ \n";
    foreach my $i (split(/\,/,$ref)) {
	chomp($i);
	foreach my $j (get_file_content($i)) {
	    print "$j<br>";
	}
    }
    print "for (i = 0; i != $timer;i++) {\n 1;\n};\n";
    print "location = \"$load_prog\";\n";
    print "}\n";
    print "</script>\n";
    print "</head>\n";
}

# Returns line info according to its id 
sub get_line_logbook {
    my (@line) = @_;

    foreach my $l (@line) {
	chomp($l);
	if ($l =~ m/$one_id/) {
	    $other_ref = (split(/\=/,$l))[1];
	    return $other_ref;
	}
    }
}

# definition of header for html file
sub my_head_definition {
    my ($time,$one_id,$num) = @_;
    my $new_id = &create_id;
    my $extra_marge = "                    ";

    print $extra_marge . "    <!-- queblo $num-->\n";
    print $extra_marge . "    <script language=\"JavaScript\"> <!--\n";
    print $extra_marge . "        function display_time_in_status_line()\n";
    print $extra_marge . "        {\n";
    print $extra_marge . "            for (i = 0; i != $time;i++) {\n";
    print $extra_marge . "                1;\n";
    print $extra_marge . "            };\n";
    print $extra_marge . "            location.replace(\"open_log.cgi?id=$one_id&password=$new_id\");\n";
    print $extra_marge . "        }\n";
    print $extra_marge . "    -->\n";
    print $extra_marge . "    </script>\n";
    print $extra_marge . "\n";
}

1;
