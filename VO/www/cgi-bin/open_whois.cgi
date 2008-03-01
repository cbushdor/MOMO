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

my $open_log_cgi="open_log.cgi";
my $cgi = new CGI;
my $passwd = $cgi->param("password");
my $one_address = $cgi->param("address");
my $logbook = "loguser";

chomp($one_address);
if (!($passwd eq get_password("configuration_file/password"))) { # Begin if (!($passwd eq get_password("configuration_file/password")))
    print "Content-type: text/html\n\n";
    print "<html>\n";
    print "<body bgcolor=\#C5FFAC text=yellow>\n";
    print "   <center>\n";
    print "         <table border=0 width=50%>\n";
    print "            <tr>\n";
    print "                <td bgcolor='#001F2D'>\n";
    print "                       <br>\n";
    print "                       <center>\n";
    print "                            <h1>CASHIER ROOM#2</h1>\n";
    print "                       </center>\n";
    print "                       <br>\n";
    print "            </tr>\n";
    print "         </table>\n";
    print "   </center>\n";
    print "   <br>\n";
    print "   <br>\n";
    print "   <br>\n";
    auth($one_address,"open_whois.cgi","id=$one_id");
} # End case password not correct 
else { # Begin case we print menu    
    my @file = get_file_content("$logbook");
    my $laddress = &get_line_log_book(@file);

    print "Location: http://www.samspade.org/t/whois?a=$laddress&server=auto&_charset_=utf-8&btnGo=Whois\n\n";
}  # End case we print menu    

# Returns line info according to its id 
sub get_line_log_book {
    my (@line) = @_;

    foreach my $l (@line) {
	chomp($l); 
	@other_ref = (split(/\*/,$l));
	if ($other_ref[5] =~ m/$one_address/) {
	    print "$other_ref[5] =~ m/$one_address/ = $other_ref[1]";
	    return $other_ref[1];
	}
    }
}
