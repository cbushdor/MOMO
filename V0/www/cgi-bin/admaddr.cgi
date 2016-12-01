#!/usr/bin/perl -wT

# +-------------------------------+
# | Dorey Sebastien               |
# | admaddr.cgi                   |
# | Written on Sept 2sd 2005      |
# | Last update on Sept 17rd 2005 |
# +-------------------------------+

BEGIN {
    @INC = (@INC,"/usr//home/users/dorey_s/www/cgi-bin");
}

use Fcntl qw(:DEFAULT :flock);
use CGI;
use packages::Common;

my $cgi = new CGI;
my $passwd = $cgi->param("password");
my $one_address = $cgi->param("address");
my $my_allow = $cgi->param("allow");
my $log_file = "loguser";
chomp($one_address);
chomp($passwd);
chomp($my_allow);

print "Content-type: text/html\n\n";
print "<html>\n";
print "  <body text=yellow bgcolor=black>\n";
#print "$one_address-----";
&analyze($passwd,$one_address);
print "  </body>\n";
print "</html>\n";

# Analyze password
sub analyze {
    my ($passwd,$my_addr) = @_;
    my $prev_session_id = get_id;
    my $border = "     ";

    chomp($my_addr);    
    if (&is_address_referenced($my_addr) == 1) { # we check if address is well formed or if does not exist in order to avoid hack
	if ($passwd =~ m/^[\w\ .!?-]$/) {
	    print $border . "      <center> <!-- choice 1 -->\n";
	    print $border . "          <table border=0 width=50%>\n";
	    print $border . "              <tr>\n";
	    print $border . "                  <td bgcolor='#001F2D'>\n";
	    print $border . "                      <br>\n";
	    print $border . "                      <center>\n";
	    print $border . "                         <h1>CASHIER ROOM#1</h1>\n";
	    print $border . "                      </center>\n";
	    print $border . "                      <br>\n";
	    print $border . "              </tr>\n";
	    print $border . "          </table>\n";
	    print $border . "      </center>\n";
	    print $border . "      <br>\n";
	    print $border . "      <br>\n";
	    print $border . "      <br>\n";
	    #	print "Error: malicious code detected<br><br><br><br>\n";
	    auth($my_addr,"admaddr.cgi");
	} elsif ($passwd eq get_password("configuration_file/password") ) {
	    if ($my_addr eq "") { # case we don't want to have an empty IP address (then we can remove or forbid all adress) that a hack a shack security hole ;-)
#		print "Error: no url defined<br><br><br><br>\n";
		print $border . "   <center> <!-- Choice 2 -->\n";
		print $border . "         <table border=0 width=50%>\n";
		print $border . "            <tr>\n";
		print $border . "                <td bgcolor='#001F2D'>\n";
		print $border . "                       <br>\n";
		print $border . "                       <center>\n";
		print $border . "                           <h1>CASHIER</h1>\n";
		print $border . "                       </center>\n";
		print $border . "                       <br>\n";
		print $border . "            </tr>\n";
		print $border . "     </table>\n";
		print $border . "   </center>\n<br>\n<br>\n<br>\n";		
		auth($my_addr,"admaddr.cgi");
	    } else {
		admin($my_addr);
	    }
	} elsif ($prev_session_id eq $passwd ) {
	    if ($my_addr eq "") { # case we don't want to have an empty IP address (then we can remove or forbid all adress) that a hack a shack security hole ;-)
		#	print "Error: no url defined<br><br><br><br><br>\n";
		print $border . "   <center> <!-- Choice 3 --> \n";
		print $border . "       <table border=0 width=50%>\n";
		print $border . "          <tr>\n";
		print $border . "              <td bgcolor='#001F2D'>\n";
		print $border . "                 <br>\n";
		print $border . "                 <center><h1>CASHIER</h1></center>\n";
		print $border . "                 <br>\n";
		print $border . "          </tr>\n";
		print $border . "       </table>\n";
		print $border . "   </center>\n";
		print $border . "   <br>\n";
		print $border . "   <br>\n";
		print $border . "   <br>\n"; 
		auth($my_addr,"admaddr.cgi");		
	    } else {
		&change_website_permissions($one_address,$my_allow);
		&admin($one_address);
	    }
	} else {
#	    print "Error: no password entered<br><br><br><br>\n";
	    print $border . "<center> <!-- Choice 4 -->\n";
	    print $border . "      <table border=0 width=50%>\n";
	    print $border . "         <tr>\n";
	    print $border . "             <td bgcolor='#001F2D'>\n";
	    print $border . "                    <br>\n";
	    print $border . "                    <center>\n";
	    print $border . "                         <h1>CASHIER</h1>\n";
	    print $border . "                    </center>\n";
	    print $border . "                    <br>\n";
	    print $border . "         </tr>\n";
	    print $border . "      </table>\n";
	    print $border . "</center>\n";
	    print $border . "<br>\n";
	    print $border . "<br>\n";
	    print $border . "<br>\n"; 
	    auth($my_addr,"admaddr.cgi");
	}
    } else {
	print "Error: IP address <i><font color=red>$my_addr</font></i> not registered<br><br><br><br><center><img src=\"image/farside.gif\"></center>\n";
    }
}


# Check the IP address in order to avoid hack
sub is_address_referenced {
    my ($current_web_site) = @_;
    
    if (!-f "$log_file") { # Begin if (!-f "$log_file")
	return 0; 
    }  # End if (!-f "$log_file")
    else {  # Begin case if (-f "$log_file")
	open(READ_LOG_FILE,"$log_file") or die("$log_file not found\n");
	foreach my $i (<READ_LOG_FILE>) { # Begin foreach my $i (<READ_LOG_FILE>) {
#	    print "$i<br>\n";
	    chomp($i);
	    if ($i =~ m/$current_web_site/) { # Begin if ($i =~ m/$current_web_site/) 
		return 1; # ok permitted
	    } # End if ($i =~ m/$current_web_site/) 
	} # End foreach my $i (<READ_LOG_FILE>) {
	close(READ_LOG_FILE);
	# ok cannot log on website
    } # End case if (-f "$log_file")
    return 0;
}

# Change website permissions
sub change_website_permissions {
    my ($change_web_site_permission_address,$new_permission) = @_;
    chomp($change_web_site_permission_address);

    unlink("$log_file.tmp");
#    return 0;
    sysopen(READ_LOG_FILE,"$log_file"    ,O_RDONLY         ) or die("$log_file not found\n");
    sysopen(WRITE_FILE   ,"$log_file.tmp", O_CREAT|O_WRONLY) or die("$log_file.tmp not found\n");
    foreach my $i (<READ_LOG_FILE>) {
	if ($i =~ m/$change_web_site_permission_address/) {
	    chomp($i);
	    my @my_line = split(/\*/,$i);
#	    print "-----$my_line[0]*$my_line[1]*$my_line[2]*$my_line[3]*$new_permission*$my_line[5]<br>\n";
	    print WRITE_FILE "$my_line[0]*$my_line[1]*$my_line[2]*$my_line[3]*$new_permission*$my_line[5]\n";
	} else {
	    print WRITE_FILE "$i";
	}
    }
    close(WRITE_FILE);
    close(READ_LOG_FILE_TMP);
    unlink("$log_file");
    sysopen(READ_LOG_FILE_TMP,"$log_file.tmp",O_RDONLY         ) or die("$log_file.tmp not found\n");
    sysopen(WRITE_FILE       ,"$log_file"    , O_CREAT|O_WRONLY) or die("$log_file not found\n");
    foreach my $i (<READ_LOG_FILE_TMP>) {
#	print "COPY $i<br>\n";
	print WRITE_FILE "$i";
    }
    close(WRITE_FILE);
    close(READ_LOG_FILE_TMP);
    # ok can log on website
}

# Menu admin for a specific address
sub admin {
    my ($my_addr) = @_;
    my $line = &return_line($my_addr);
    my @line_granted = split(/\*/,$line);
    my $new_process_id = &create_id($$);
    $my_addr = (split(/\*/,$line))[1];
    my @this_address = split(/\./,$my_addr);
    my $sub_net_addr = "$this_address[0].$this_address[1].$this_address[2].*";
    my $border       = "     ";

    print $border . "<center>\n";
    print $border . "    <h1>ADMINISTRATION OF URL</h1>\n";
    print $border . "    <br>\n";
    print $border . "    <br>\n";
    print $border . "    <br>\n";
    print $border . "    <br>\n";
    print $border . "    <table border=2>\n";
    print $border . "        <tr>\n";
    print $border . "             <td align=center bgcolor=red>$my_addr\n";
    print $border . "        </tr>\n";
    print $border . "        <tr>\n";
    print $border . "             <td align=right bgcolor=grey><br>\n";
    print $border . "                 <form action=\"admaddr.cgi\" method=get>\n";
    print $border . "                     <table border=0>\n";

    if ($line_granted[4] eq "ok") {
	my $prev = $cgi->param("prev");	
	chomp($prev);
	if ($prev eq "nallok") {
	    &grant_access_info_websites_update($sub_net_addr,"ok");
	}
	print $border . "                         <tr>\n";    
	print $border . "                             <td align=right>Grant this address\n";
	print $border . "                             <td><input type=radio name=allow value=ok checked>\n";
	print $border . "                         </tr>\n";
	print $border . "                         <tr>\n";
	print $border . "                             <td align=right>Do not grant this address\n";
	print $border . "                             <td><input type=radio name=allow value=nok>$my_addr\n";
	print $border . "                         </tr>\n";
	print $border . "                         <tr>\n";
	print $border . "                             <td>\n";
	print $border . "                             <td><input type=radio name=allow value=nallok>$sub_net_addr\n";
	print $border . "                         </tr>\n";
    } elsif ($line_granted[4] eq "nallok") {
	&grant_access_info_websites_update($sub_net_addr,"nallok");
	print $border . "                         <input type=hidden name=prev value=nallok>\n";
	print $border . "                         <tr>\n";
	print $border . "                             <td align=right>Grant this address\n";
	print $border . "                             <td><input type=radio name=allow value=ok>\n";
	print $border . "                         </tr>\n";
	print $border . "                         <tr>\n";
	print $border . "                             <td align=right>Do not grant this address\n";
	print $border . "                             <td><input type=radio name=allow value=nok>$my_addr\n";
	print $border . "                         </tr>\n";
	print $border . "                         <tr>\n";
	print $border . "                             <td>\n";
	print $border . "                             <td><input type=radio name=allow value=nallok checked>$sub_net_addr\n";
	print $border . "                         </tr>\n";
    } else {
	print $border . "                         <tr>\n";
	print $border . "                             <td align=right>Grant this address\n";
	print $border . "                             <td><input type=radio name=allow value=ok>\n";
	print $border . "                         </tr>\n";
	print $border . "                         <tr>\n";
	print $border . "                             <td align=right>Do not grant this address\n";
	print $border . "                             <td><input type=radio name=allow value=nok checked>$my_addr\n";
	print $border . "                         </tr>\n";
	print $border . "                         <tr>\n";
	print $border . "                             <td>\n";
	print $border . "                             <td><input type=radio name=allow value=nallok>$sub_net_addr\n";
	print $border . "                         </tr>\n";
    }
    print $border . "                         <input type=hidden name=password value=\"$new_process_id\">\n";
    print $border . "                         <input type=hidden name=address value=\"$my_addr\">\n";
    print $border . "                         <input type=hidden name=prev value=$line_granted[4]>\n";
    print $border . "                    </table>\n";
    print $border . "                    <center>\n";
    print $border . "                        <table border=0>\n";
    print $border . "                            <tr>\n";
    print $border . "                                <td valign=center align=center><input type=submit>\n";
    print $border . "                 </form>\n";
    print $border . "                 <form action=\"JavaScript:window.close();\" method=post>\n";
    print $border . "                                <td valign=center align=center><input type=submit value='Exit'>\n";
    print $border . "                        </table>\n";
    print $border . "                    </center>\n";
    print $border . "                 </form>\n";
    print $border . "           </table>\n";
    print $border . "           </tr>\n";
    print $border . "      </table>\n";
    print $border . "    </center>\n";
#    print $border . "</body>\n";
#    print $border . "</html>\n";
}

# returns the requested line according to the given IP address
sub return_line {
    my ($addr) = @_;
    my $line = ();
    
    open(R,"loguser") or die("Can't find loguser");
    foreach my $u (<R>) {
	chomp($u);
	if ($u =~ m/$addr/) {
	    close(R);
	    return $u;
	}
    }
    close(R);
    return 0;
}

# We update all info related to subnetwork permission
# now we insert info for the DB s.a IP address, time, and counter (see above)
sub grant_access_info_websites_update {
    my ($sub_net,$grant_permission) = @_;
    
    sysopen(READ_LOG_FILE ,"$log_file"  ,O_RDONLY        ) or die("$log_file not found\n");;
    sysopen(WRITE_LOG_FILE,"loguser.tmp",O_CREAT|O_WRONLY) or die("File loguser.tmp problem");
    foreach my $i (<READ_LOG_FILE>) {
	chomp($i);
	if ($i =~ m/$sub_net/m) {
	    @local_line = split(/\*/,$i);
	    print WRITE_LOG_FILE "$local_line[0]*$local_line[1]*$local_line[2]*$local_line[3]*$grant_permission*$local_line[5]\n";
	} else {
	    print WRITE_LOG_FILE "${i}\n";
	}
    }
    close(READ_LOG_FILE);
    close(WRITE_LOG_FILE);
    sysopen(READ_LOG_FILE_TMP2,"$log_file.tmp",O_RDONLY        ) or die("$log_file.tmp not found\n");
    sysopen(WRITE_FILE        ,"$log_file"    ,O_CREAT|O_WRONLY) or die("$log_file not found\n");
    foreach my $i (<READ_LOG_FILE_TMP2>) {
#	chomp($i);
	print WRITE_FILE "$i";
    }
    close(WRITE_FILE);
    close(READ_LOG_FILE_TMP2);
    
    # `rm loguser.tmp`;
}
