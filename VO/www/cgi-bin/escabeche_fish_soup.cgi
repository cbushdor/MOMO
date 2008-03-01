#!/usr/bin/perl -wT

# +-------------------------------+
# | Dorey Sebastien               |
# | escabeche_fish_soup.cgi       |
# | Written on Jan 4th 2005       |
# | Last update on Sept 26th 2005 |
# +-------------------------------+

BEGIN {
    @INC = (@INC,
	    "/usr//home/users/dorey_s/www/cgi-bin"
	    );
}

use packages::MyTime;
use packages::Common;

my $file_name   = get_script_file_name("$ENV{SCRIPT_NAME}");
my $file_log    = "loguser";
my @res         = &who_is($file_log);

print "Content-type: text/html\n\n";
print @res;
print "</html>\n";

# Who is function print a dash bord with different connexions info
sub who_is {
    my $log_f = $_[0];
    my @result_with_link = ();
    my $counter = 0;
    my @dressing = ("Rust","Croutons","Cheese","Everything","Extra fish","Extra cheese");
    my $n_dressing = @dressing;

    open(R,"$log_f");
    @result_with_link = <R>;
    close(R);
    @result_with_link = reverse(@result_with_link);
    foreach my $line ( @result_with_link ) { # Begin foreach my $line ( @result_with_link )
	chomp($line);
	$counter++;
	my @l = split(/\*/,$line);
	my ($process,$date) = split(/\-/,$l[0]);
	$date =~ s/\_/\ /g;
	chomp($line);
	my $extra_marge = "                    ";
	$line = 
	    $extra_marge . "<tr>\n".
	    $extra_marge . "    <td align=center><img src='../image/fish_icon_2.gif' width=50%>\n" .
	    $extra_marge . "    <td align=left valign=center>$date\n" . 
	    $extra_marge . "    <td valign=center align=center>\n".
	    $extra_marge . "        <table border=0 width=100\%>\n" .
	    $extra_marge . "              <tr>\n".
	    $extra_marge . "                  <td valign=center align=right>\n".
	    $extra_marge . "                      <form action=\"JavaScript:window.open('admaddr.cgi?address=$l[5]');location.replace(\'$file_name\');\" method=post>\n".
	    $extra_marge . "                          <input type=submit              value=\"What's on fire\">\n".
#	    $extra_marge . "                          <input type=hidden name=address value=$l[5]>\n".
	    $extra_marge . "                      </form>\n".
	    $extra_marge . "                  <td valign=center align=left>\n".
	    $extra_marge . "                      <form action=\"JavaScript:window.open('open_whois.cgi?address=$l[5]');location.replace(\'$file_name\');\" method=post>\n".
	    $extra_marge . "                          <input type=submit                value=\"What's on grill\">\n".
#	    $extra_marge . "                          <input type=hidden name=address value=$l[5]>\n".
	    $extra_marge . "                      </form>\n".
	    $extra_marge . "              </tr>\n".
	    $extra_marge . "        </table>\n".
	    $extra_marge . "    <td bgcolor=\#002A3E align=center valign=center>\n" .
	    (($l[0] !~ m/^0/) ? (
				 $extra_marge . "          <form action=\"JavaScript:window.open('open_log.cgi?id=$l[5]');location.replace(\'$file_name\');\" method=post>\n".
				 $extra_marge . "                <input type=submit length=10 value=\"" . $dressing[(($l[3] ne "X")  ? ($counter*$l[3]) : $counter) % $n_dressing] . "\">\n".
				 $extra_marge . "          </form>\n"
				 )
	     :
	     "...."	 ) .
	     $extra_marge . (($l[3] ne "X")  ? "    <td valign=center align=center>$l[3]\n" : "    <td>\n") .
	    $extra_marge . "</tr>\n";
	$counter++;
    };  # End foreach my $line ( @result_with_link )
    return (
	    "<html>\n",
	    "<!-- \n",
	    "  Code written by Sebastien DOREY and genrated with PERL on ". get_formated_date . "\n",
	    "  Perl script that generates this code was written by Sebastien Dorey\n",
	    "  email address: dorey_s\@laposte.net\n",
	    " -->\n",
	    "   <title>\n",
	    "      Eat at jaws\n",
	    "   </title>\n",
	    "   <head>\n",
	    "   <style type=\"text/css\">\n",
	    "      OLD_ADAGE {\n",
	    "           font-family : URW Chancery L;\n",
	    "           font-style : italic;\n",
	    "           font-size : small;\n",
	    "           color : pink;\n",
	    "         }\n" ,
	    "   </style>\n",
	    "   </head>\n",
	    "   <body text=yellow bgcolor=#000030 link=#green vlink=red onload='display_time_in_status_line();'>\n",
	    "      <center>\n",
	    "         <table border=0 width=42\%>\n",
	    "            <tr>\n",
	    "                <td>\n",
	    "                    <table border=1 width=100\%>\n",
	    "                       <tr>\n",
	    "                           <td bgcolor='\#001F2D'>\n",
	    "                               <center><h1>EAT<br>AT JAWS<br><blink>TONIGHT</blink></h1></center>\n",
	    "                       </tr>\n",
	    "                    </table>\n",
	    "            </tr>\n",
	    "            <tr>\n",
	    "                <td align=center>\n",
	    "                    |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|\n",
	    "            </tr>\n",
	    "            <tr>\n",
	    "                <td align=center>\n",
	    "                    <table border=1 width=70\%>\n",
	    "                        <tr>\n",
	    "                            <td valign=center align=center bgcolor='\#001F2D'>\n",
	    "                                <OLD_ADAGE>Have a chew. Who knows who is going to eat you tomorow.</OLD_ADAGE>\n",
	    "                        </tr>\n",
	    "                    </table>\n",
	    "            </tr>\n",
	    "         </table>\n",
	    "      </center>\n",
	    "      <br>\n",
	    "      <br>\n",
	    "      <br>\n",
	    "      <br>\n",
	    "      <br>\n",
	    "      <table border=0 width=100\%>\n",
	    "          <tr>\n",
	    "             <td bgcolor='\#002A3E'>\n",
	    "                <table border=0 width=100\%>\n",
	    "                    <tr>\n",
	    "                         <td bgcolor=\#001F2D>\n".
	    "                         <td align=center  bgcolor=\#001F2D><font color=green>RESERVED ON</font>\n",
	    "                         <td align=center  bgcolor=\#001F2D><font color=green>MENU (<i>only with reservation</i>)</font>\n",
	    "                         <td align=center  bgcolor=\#001F2D><font color=green>DRESSING ADVICED</font>\n",
	    "                         <td align=center  bgcolor=\#001F2D><font color=green>CAME BACK</font>\n",
	    "                    </tr>\n",
	    @result_with_link,
	    "                </table>\n",
	    "          </tr>\n",
	    "      </table>\n",
	    "      <u><b>Author:</b></u><a href='mailto:dorey_s\@free.fr'>Dorey Sebastien</a>\n",
	    "   </body>\n",
	    "</html>\n"
	    );
}

