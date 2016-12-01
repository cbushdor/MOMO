#!/usr/bin/perl -wT

# +-------------------------------+
# | Dorey Sebastien               |
# | open_log.cgi                  |
# | Written on Sept 16th 2005     |
# | Last update on Sept 26th 2005 |
# +-------------------------------+

BEGIN {
    @INC = (@INC,"/usr/local/home/users/dorey_s/www/cgi-bin");
}

use CGI;
use packages::Common;
use Time::Local;
use Fcntl qw(:DEFAULT :flock);

# Get values from url
my $cgi             = new CGI;
my $passwd          = $cgi->param("password");
my $one_address     = $cgi->param("address");
my $process         = $cgi->param("process");
my $one_id          = $cgi->param("id");

# Base
my $dir_logbook     = "../logbook";
my $open_log_cgi    = "open_log.cgi";
my $index_logbook   = "../logbook/index_log.txt";
my $loguser_file    = "loguser";
my $prev_session_id = ();
my $loc_time        = ();
my $ref             = ();

$ref             = "${dir_logbook}/one_log." . &get_line_from_logbook($one_id) . ".txt";
$loc_time        = scalar localtime;
$prev_session_id = get_id;
print "Content-type: text/html\n\n";
print "<html>\n";
chomp($one_id);
if (!-f "$index_logbook") { # Begin if (!-f "$index_logbook") 
    print "No file found\n";
}  # End if (!-f "$index_logbook") 
else {  # Begin if (-t "$index_logbook") 
    $momo = "___: ($prev_session_id eq $passwd) :___" . (($prev_session_id eq $passwd) ? "ok" : "ko") . "--";
    &write_process($prev_session_id,$new_id,$loc_time,$momo);
    if ($prev_session_id eq $passwd) { # Begin if ($prev_session_id == $passwd)
	&write_process($prev_session_id,$new_id,$loc_time,"5");
	print "    <head>\n";
	my_head_definition(250000,$one_id,"1");
	print "    </head>\n";
	print "    <body text=yellow bgcolor=#000030 link=#green vlink=red onload='display_time_in_status_line();'>\n";
	&running_menu($ref,$one_id);
	print "        <a href='javascript:window.close()'>Close</a>\n";
	print "    </body>\n";
	print "</html>\n";
    }  # End if ($prev_session_id == $passwd)
    elsif (!($passwd eq get_password("configuration_file/password"))) { # Begin elsif (!($passwd eq get_password("configuration_file/password")))
	$id = &get_line_from_logbook;
#	my $new_id = &create_id;

#	&write_process($prev_session_id,$new_id,$loc_time,"login screen");
	print "   <body text=yellow bgcolor=\#000030 link=\#green vlink=red>\n";
	print "     <center>\n";
	print "         <table border=0 width=50%>\n";
	print "            <tr>\n";
	print "                <td bgcolor='#001F2D'>\n";
	print "                       <br>\n";
	print "                       <center><h1>CASHIER ROOM#3</h1> $id</center>\n";
	print "                       <br>\n";
	print "            </tr>\n";
	print "        </table>\n";
	print "     </center>\n";
	print "     <br>\n";
	print "     <br>\n";
	print "     <br>\n";
	auth($one_address,"$open_log_cgi","id=$one_id");
	print "  </body>\n";
	print "</html>\n";
    } # End elsif (!($passwd eq get_password("configuration_file/password")))
    else { # Begin else
	print "    <head>\n";
	my_head_definition(250000,$one_id,"(($passwd eq get_password(\"configuration_file/password\")))");
	print "    </head>\n";
	print "    <body text=yellow bgcolor=#000030 link=#green vlink=red onload='display_time_in_status_line();'>\n";
	&write_process($prev_session_id,$new_id,$loc_time,"4");
	&running_menu($ref,$one_id);
	print "    <a href='javascript:window.close()'>Close</a>\n";
	print "    </body>\n";
	print "</html>\n";
    } # End else
}  # End if (-t "$index_logbook") 

# Writes process
sub write_process {
    my ($old_process,$new_process,$time,$op) = @_;

    chomp($time);
    if ($op eq "0") {
#	if (-f "process_open_log_list") {
#	    # unlink("process_open_log_list");
#	}
	sysopen(WRA,"process_open_log_list",O_CREAT|O_WRONLY) || die("process_open_log_list error $!\n");
	print WRA "$op) prev($old_process)\n    new($new_process)\ndone on $time\n------------------------\n";
	close(WRA);
    } else {
	sysopen(WRA,"process_open_log_list",O_CREAT|O_WRONLY|O_APPEND) || die("process_open_log_list error $!\n");
	print WRA "$op) prev($old_process)\n    new($new_process)\ndone on $time\n------------------------\n";
	close(WRA);
    }
}

# Gets line of the file logbook and returns the requested line
sub get_line_from_logbook {
    my ($my_id_to_seek) = @_;

#    print "Content-type: text/html \n\n";
    open(R,"$loguser_file") || die("Cannot find $loguser_file $!\n");
    foreach (<R>) { # Begin foreach (<R>)
	if ($_ =~ m/$my_id_to_seek/) { # Begin if ($_ =~ m/$my_id_to_seek/)
#	    chomp($_);
	    my $f = (split(/\*/,$_))[0];
	    return $f;
	} # End if ($_ =~ m/$my_id_to_seek/)
    } # End foreach (<R>)
    close(R);
}

# Returns line info according to its id 
sub get_line_index_logbook {
    my (@line) = @_;
    
    foreach my $l (@line) { # Begin foreach my $l (@line)
	print "---->$l<br>";
	chomp($l);
	if ($l =~ m/$one_address/) { # Begin if ($l =~ m/$one_address/)
	    return $l;
	} # End if ($l =~ m/$one_address/)
    }  # End foreach my $l (@line)
}

# Prints menu that as to be printed  while process are running
sub running_menu {
    my ($ref,$one_id) = @_;
    my $margin = "    ";

    print $margin . "    <center>\n";
    print $margin . "        <br>\n";
    print $margin . "        <u><font color=red>$loc_time</font></u>:$ref\n";
    print $margin . "    </center>\n";
    print $margin . "    <br>\n";
    print $margin . "    <br>\n";
    print $margin . "    <br>\n";
    print $margin . "    <br>\n";
    print $margin . "    <br>\n";
    print $margin . "    <center>\n";
    print $margin . "        <table border=0 width=75\%>\n";
    print $margin . "            <tr>\n";
    print $margin . "                <td bgcolor=#000033 align=center>\n";
    print $margin . "                      <table border=0 width=100\%>\n";
    print $margin . "                          <tr>\n";
    print $margin . "                               <td align=center bgcolor=#001F2D width=42\%>Date\n";
    print $margin . "                               <td align=center width=25\% bgcolor=#001F2D>Choice\n";
    print $margin . "                               <td width=25\% align=center bgcolor=#001F2D>Laps\n";
    print $margin . "                          </tr>\n";
    foreach my $j (get_file_content("$ref")) { # Begin foreach my $j (get_file_content($ref))
	my ($local_date,$menu,$laps) = ();
	
	if ($j =~ m/\*/) { # Begin if ($j =~ m/\*/)
	    ($local_date,$menu,$laps) = split(/\*/,$j);
	} # End if ($j =~ m/\*/)
	else { # Begin if ($j !~ m/\*/)
	    $local_date = $j;
	} # End if ($j !~ m/\*/)
	print $margin . "                          <tr>\n";
	print $margin . "                               <td align=center>$local_date\n";
	print $margin . "                               <td align=center><font color=pink>" . (($menu eq "X")? "" : "$menu") . "</font>\n";
	print $margin . "                               <td align=right>" . (($local_date eq "") ? "\n" : "$laps\n");
	print $margin . "                          </tr>\n";
    } # End foreach my $j (get_file_content($ref))
    print $margin . "                      </table>\n";
    print $margin . "            </tr>\n";
    print $margin . "        </table>\n";
    print $margin . "    </center>\n";
}


