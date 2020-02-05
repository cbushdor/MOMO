#!/usr/bin/perl-5.30.0
# ------------------------------------------------------
q##//q#
* Created By : sdo
* File Name : login.cgi
* Creation Date : Mon Feb 3 22:51:08 2003
* @modify date 2020-02-05 01:19:38
* Email Address : sdo@macbook-pro-de-sdo.home
* License:
*       Permission is granted to copy, distribute, and/or modify this document under the terms of the Creative Commons Attribution-NonCommercial 3.0
*       Unported License, which is available at http: //creativecommons.org/licenses/by- nc/3.0/.
* Version : 1.5.5.1036
* Purpose :
#;
# ------------------------------------------------------

BEGIN {
	use CGI;
	push @INC,"/Users/sdo/Sites/cgi-bin/"; # We add a new path to @INC
	# A bug was solved and that's it was "...but still, the newly generated form has al the values from the previous form...".
	$doc=$CGI::Q ||= new CGI; # It is using the special internal $CGI::Q object, rather than your 'my $doc' object that's why we do this.
	$rtrip="blue"; # We don't record trip
}
END {
	$doc->delete_all(); # We clean all variables and parameters when the script is over
}

my $VERSION="1.5.5.1036";

use io::MyUtilities;
use io::MyTime;

use constant PACKAGE_DIRECTORY            => "io/";
use constant GUEST_BOOK_DIRECTORY_DEPOSIT => "Guest_Book_Deposit/";
use constant IMAGE_DIRECTORY_DEPOSIT      => &io::MyUtilities::finds_directory_where_are_stored_images();
use constant TEMPORARY_FILE               => "removeTmp.";
use constant DEFAULT_NAME_FOR_GUEST_BOOK  => "body.my";
use constant DEFAULT_URL                  => "http://storm.prohosting.com/dorey/";
#use constant DEFAULT_URL                  => "http://comanche.com/~prohosting/";
use constant MY_URL_WITH_CGI_FILE         => DEFAULT_URL . "cgi-bin/login.cgi?guest_book_name=";

my $id=io::MyUtilities::loadFile("private/pswGuBo.txt");	
my $doc = new CGI();

=head1 NAME

login.cgi

$VERSION="1.5.5.0"

=head1 ABSTRACT

This file creates a guest book but at the end many guest book will be created according to tutorials given or, evening shows.
here is an exemple of url : http://localhost/~prohosting/cgi-bin/login.cgi?guest_book_name=body.my

=head2 LIST OF FUNCTIONS

=over 4

TABLE_BEGIN
TD
TD_E
TR
TR_E
admin
adminLog
checks_if_album_exists
cleanMyVariable
cleanMyVariableExtra
count_messages
create_help_file
create_new_guest_book_name
create_translate_time_to_trigger
creates_Guest_Book_directory
eraseAdmin
foot
form_to_fill_guestbook
gets_line_URL_back
gets_line_colors_stored
gets_line_num
gets_private_message
gets_separator_bar
gets_string_css_private_message
giveDate
giveLogDate
head
insertMessageGuestBook
is_file_date_not_over
loginAndPassword
number_of_private_messages
numeric
pageGranted
pageNotGranted
parse_form
print_List_GB 
print_Remove_GB
print_Save_settings
print_Show_messages
print_create_gb
print_title
prints_authenticate
prints_help_for_main_menu
prints_help_message_if_signing_up_guest_book
prints_messages_on_admin_screen
removeGuestBook
removes_old_guest_book_name
saveConf
selects_color
selects_option_color
show_guest_book
show_guest_book_help
show_list_of_guest_books

=back

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF MODIFICATIONS

=over 4

- I<Last modification: v1.5.5.0> Aug 14 2011: getDocVers changed to getsDocVers

- I<Last modification: v1.5.4.0> Jul 16 2011: see service of numMes

- I<Last modification: v1.5.3.10> Jul 15 2011: see admin

- I<Last modification: v1.5.3.1> Feb 17 2011: see io::MyUtilies::setUrlFile

- I<Last modification:1.5.3.0> Oct 5th 2010: modification on this file.
Modification see packages::MyUtilities.pm. 
$function eq "verDoc" added.

- I<Last modification:1.5.1.0> Oct 3rd 2010: modification/tests
Modification see packages::MyUtilities.pm. 
$function eq "versioning" added

- I<Last modification:1.4.0.9> Aug 4th 2006: creation/tests

- I<Last modification:0.5.19.0> Jun 6th 2003: creation/tests

- I<Starting date Nov:0.0.1.ˆ> Feb 2003: creation

=back

=cut

&creates_Guest_Book_directory;
#print '<?php include("../Project/php/base.php"); ?>';
#print '<script language="javascript" src="../Project/js/menu.js"></script>';

# Information related to admin
my $remhost = $ENV{REMOTE_HOST} || $ENV{REMOTE_ADDR};
my ($my_login,$my_password ) = split(/\n/,$id);

# Information related parameters set within URL
my $home_name     =             $doc->param('home_name'); #  home name
$home_name     =~            s/^\ //g;
my $home_url      =             $doc->param('home_url'); # url that leads to home page
$home_url      =~            s/^\ //g;
my $author        =             $doc->param('author'); # author of the message
my $function      =             $doc->param('function'); # Function that is used to redirect to services
my $loc           =             $doc->param('loc'); # That's location where the person comes from
my $mess          =             $doc->param('mess'); # That's the message
my $email         =             $doc->param('email'); # That the email of the person that enter message
my $login         =             $doc->param('login'); # That's the login of admin
my $torem         =             $doc->param('torem'); # That's the message to remove
my $password      =             $doc->param('password'); # That's the password
my $urlBack       =             $doc->param('urlBack'); # That's the url to go back
my $page          =             $doc->param('page'); # That's the page number where to go in guest book
my $max_mess_page =             $doc->param('max_mess_page'); # That's the max of message per page
my $colorText     =             $doc->param('colorText'); # That's the text color
chomp($colorText);
my $separator_bar =             $doc->param('separator_bar'); # That's the separator bar (image)
my $saveConf      =             $doc->param('saveConf'); # That's the conf to save
my $privateMess   =             $doc->param('privateMess'); # Private message that old mess
my $guest_book_name =           $doc->param('guest_book_name'); # Returns guest book name
chomp($guest_book_name);
my $old_guest_book_name =       $doc->param('old_guest_book_name'); # Returns old guest book name in order to go back to it when admin is over
chomp($old_guest_book_name);
my $function_admin_extra   =    $doc->param('function_admin_extra'); # That is used for extra administration task
chomp($function_admin_extra);
my $new_Guest_book_name =       $doc->param('new_Guest_book_name'); # That's in extra admin task new guest book name to create
chomp($new_Guest_book_name);
my $old_Guest_book_name =       $doc->param('old_Guest_book_name'); # That is used to old guest book (used to go back from admin menu to user menu: page that user can watch).
chomp($old_Guest_book_name);
my $timer =                     $doc->param('timer'); # That's used for timer not in used yet
chomp($timer);
my $period =                     $doc->param('period'); # That's when the user has created guest book
chomp($period);
my $login_private_message =      $doc->param("login_private_message"); # Use to authenticate with login but to watch  private messages
chomp($login_private_message);
my $password_private_message =   $doc->param("password_private_message");  # Use to authenticate with password but to watch  private messages
chomp($password_private_message);
my $private_message = $doc->param("message"); # That's the private message
my $id_private_mess = $doc->param(""); # ID to authenticate message

#packages::MyUtilities::getsDocVers("login.cgi","$VERSION");
print "Content-type: text/html\n\n";

if($function eq "verDoc"){ # Only version is asked
	#print "Content-Type: text/html\n\n";
	print "<font color=orange>";
	print io::MyUtilities::getsDocVers("login.cgi","$VERSION");
	print "</font>";
	exit(0); # Exit that's it
}
elsif($function eq "versioning"){ # Only version is asked
	#print "Content-Type: text/html\n\n";
	print "<font color=orange>";
	print "(V$VERSION)";
	print "</font>";
	exit(0);# Exit that's it
}
elsif($function eq "numMes"){ # Only number of messages per guestbook
	#print "Content-Type: text/html\n\n";
	my $counter = &count_messages(DEFAULT_NAME_FOR_GUEST_BOOK);
	print "$counter";
	exit(0);# Exit that's it
}

print <<HTML;
	<html>
		<head>

		<meta name="keywords" content="HTML, CSS, XML, XHTML, JavaScript, PHP">

		<script>
		var mcwd="../Project/";
		</script>
		<script language="javascript" src="../Project/js/menu.js"></script>
		<script>
			my_menu(mcwd,new Array(
				"Admin", 				"Administration / <font color='orange'>Administration</font>", 
				"Calculus/default.htm", 	"Calcul / <font color='orange'>Calculus</font>", 
				"Methodology", 			"Méthodologie / <font color='orange'>Methodology</font>", 
				"NFS", 				"Simultion de NFS / <font color='orange'>Simulation of NFS</font>", 
				"Perl", 			"Perl / <font color='orange'>Perl</font>", 
				"teamProject", 			"Equipe / <font color='orange'>Team</font>"),
				"LDO / <font color='orange'>GuBo</font>"); 
		</script>
		<style>
		pre {
 white-space: pre-wrap;       /* css-3 */
 white-space: -moz-pre-wrap;  /* Mozilla, since 1999 */
 white-space: -pre-wrap;      /* Opera 4-6 */
 white-space: -o-pre-wrap;    /* Opera 7 */
 word-wrap: break-word;       /* Internet Explorer 5.5+ */
}
		</style>
		</head>
	<body>
	<div id='admin_project_menu'>
HTML

# Information related to set about guest book
my $num_of_private_messages = &number_of_private_messages($guest_book_name); # That's number that idetify private message
my $max_message          = &gets_line_num; # That's maximum of message(s) that can be printed on the screen.
my $separator_bar_stored = &gets_separator_bar; # That's the séparator bar image
my $url_stored           = &gets_line_URL_back; # That's url stored
my $color_text_stored    = &gets_line_colors_stored; # That's the text color

if ( "$guest_book_name" eq "") { # Begin if ( "$guest_book_name" eq "")
	#print "Content-type: text/html\n\n";
	print "<br><br>Le livre d'or n'existe pas.<br><font color=orange>Guest book does not exist.</font><br><br><br>\n";
	#print "<br><br>".
	#	io::MyUtilities::footer(
	#				$doc, 
	#				IMAGE_DIRECTORY_DEPOSIT . "powered.gif",
	#IMAGE_DIRECTORY_DEPOSIT . "hangada.gif",
	#				"http://www.perl.org", 
	#				$VERSION,
	#"Mozilla 1.7.12");
	exit;
}  # End if ( "$guest_book_name" eq "")

my %tab = ();


if ( "$guest_book_name" =~ m/^body.my$/i) { # Begin elsif ( "$guest_book_name" =~ m/^body.my$/i)
	$guest_book_name =  DEFAULT_NAME_FOR_GUEST_BOOK;
} # End elsif ( "$guest_book_name" =~ m/^body.my$/i)

&create_translate_time_to_trigger;


if (&checks_if_album_exists($guest_book_name) != 0 ) { # Begin if (&checks_if_album_exists($guest_book_name) != 0 )
	#print "Content-type: text/html\n\n";
	print <<HTML;
	<br><br>Le livre d'or [$guest_book_name] n'a pas été trouvé !!!<br> <font color=orange> Guest book  [$guest_book_name] was not found !!!</font><br><br><br>
	</div>
		<script>
			if (is_not_nav_tests(new Array( "Microsoft", "Konqueror"))) {
				document.write("<br>");
				document.write("<br>");
			}
footer("http://dorey.sebastien.free.fr","javascript:history.back()");
		</script>
	</body>
	</html>
HTML

	#print io::MyUtilities::footer($doc, IMAGE_DIRECTORY_DEPOSIT . "powered.gif","0.2","Mozilla 1.7.12");
	#print POSIT . "powered.gif","0.2","Mozilla 1.7.12");
	exit;
} # End if (&checks_if_album_exists($guest_book_name) != 0 )

if ("$page" eq "") { # Begin if ($page eq "")
	$page = 1;
} # End if ($page eq "")

# &eraseAdmin;
if ($function eq "fill") { # Begin if ($function eq "fill")
	&head;
	&form_to_fill_guestbook;
}  # End if ($function eq "fill")
elsif ($function eq "admin") { #   Begin elsif ($function eq "admin")
	#                              That's the case where a user wants to authenticate
	#                              An authentication menu shows up

	if (($my_login ne $login || $my_password ne $password) && ($login ne "" || $password ne "")) { #   Begin if (($my_login ne $login || $my_password ne $password) && ($login ne "" || $password ne ""))
		#                                                                                              Case where login does not match and or password are correct.
		&head;
		print "<html>\n";
		print <<HEADER;
<style type="text/css">
     a, a:link, a:visited {
	 color: orange;
	 text-decoration: none;
     }

     table.footer {
		       font-size: 12px;
		       text-align: right;
		       color: yellow;
		       background-color: #353135;
		       opacity: .50;
		  }
</style>
HEADER
		print "Login and password are not good.<br>\n";
		&show_guest_book;
	} # End if (($my_login ne $login || $my_password ne $password) && ($login ne "" || $password ne ""))
	elsif ($my_login eq $login && $my_password eq $password) { # Begin elsif ($my_login eq $login && $my_password eq $password)
		#                                                          Case where user login and password are correct.
		$function = "";
		if ( $function_admin_extra eq "creates_guest_book" ) { # Begin if ( $function_admin_extra eq "creates_guest_book" )
			if ( &create_new_guest_book_name == 0) { # Begin if ( &create_new_guest_book_name == 0)
				#	print "Content-type: text/html\n\n";
				print "Congratulation: le livre d'or [$new_Guest_book_name] créé <br> <font color=orange>Congratulation: guest book [$new_Guest_book_name] created</font><br>";
			}  # End if ( &create_new_guest_book_name == 0)
			else { # Begin else
				#print "Content-type: text/html\n\n";
				print "<html>\n";
				print <<HEADER;
     a, a:link, a:visited {
	 color: orange;
	 text-decoration: none;
     }


    table.footer {
		 font-size: 12px;
		 text-align: right;
		 color: black;
		 background-color: #D2D2FF;
		 opaque: .80;
	      }

</style>
HEADER
				print "<body>";
				print "Erreur: le livre d'or $new_Guest_book_name ne peux pas etre crée <br><font color=orange>Error: guest book $new_Guest_book_name cannot be created</font><br>";
				#print &footer($doc, IMAGE_DIRECTORY_DEPOSIT . "powered.gif","0.2","Mozilla 1.7.12");
				print <<HTML;
				<script>
footer("http://dorey.sebastien.free.fr","javascript:history.back()");
				</script>
HTML
			}  # End else
		} # End if ( $function_admin_extra eq "creates_guest_book" )
		elsif ( $function_admin_extra eq "removes_guest_book" ) { # Begin if ( $function_admin_extra eq "removes_guest_book" )
			if ( &removes_old_guest_book_name == 0) { # Begin if ( &removes_old_guest_book_name == 0)
				#print "Content-type: text/html\n\n";
				print "<html>\n";
				print <<HEADER;
<style type="text/css">
     a, a:link, a:visited {
	 color: orange;
	 text-decoration: none;
     }

     table.footer {
		       font-size: 12px;
		       text-align: right;
		       color: yellow;
		       link: yellow;
		       vlink: orange;
		       background-color: #353135;
		       opacity: .50;
		  }
</style>
HEADER
				print "Congratulation: livre d'or $old_Guest_book_name a été supprimé <br> <font color=orange>Congratulation: guest book $old_Guest_book_name was removed</font><br>";
			}  # End if ( &removes_old_guest_book_name == 0)
			else { # Begin else
				#print "Content-type: text/html\n\n";
				print "<html>\n";
				print <<HEADER;
<style type="text/css">
     a, a:link, a:visited {
	 color: orange;
	 text-decoration: none;
     }

     table.footer {
		       font-size: 12px;
		       text-align: right;
		       color: yellow;
		       background-color: #353135;
		       opacity: .50;
		  }

</style>
HEADER
				print "Erreur: le livre d'or $old_Guest_book_name  ne peux pas être supprimé <br><font color=orange>Error: guest book $old_Guest_book_name cannot be removed</font><br>";
			}  # End else
		} # End if ( $function_admin_extra eq "removes_guest_book" )
		&admin;
	} # End elsif ($my_login eq $login && $my_password eq $password)
	else { # Begin else
		#      Prints login and passwords
		#print "Content-type: text/html\n\n";
		&loginAndPassword ;
	}  # End else
} # End elsif ($function eq "admin")
elsif ($function eq "post") { # Begin elsif ($function eq "post")
	#  print "Content-type: text/html\n\n";
	#  print "toto<br>";
	&insertMessageGuestBook;
	&head;
	&show_guest_book;
	#  &foot;
} # End elsif ($function eq "post")
else { # Begin else
	#  print "Content-type: text/html\n\n";
	&head;
	&show_guest_book;
	#  &foot;
} # End else

print <<HTML;
</div>
				<script>
footer("http://dorey.sebastien.free.fr","javascript:history.back()");
				</script>
HTML

=head1 FUNCTION  saveConf

This function saves information related to the look and feel of the guest book (user part).
The user (or the administrator) filled a form protected by a password. The administrator is the moderator.

=head2 PARAMETER(S)

=over 4

None but information are taken from parameters from url.

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

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:>  Aug 1st 2006

- I<Last modification:>  Jun 6th 2003

- I<Created on:> Feb 2003

=back

=cut

sub saveConf { # Begin sub saveConf
	if ($saveConf ne "") { # Begin if ($saveConf ne "")
		open(SAVE,">". GUEST_BOOK_DIRECTORY_DEPOSIT ."conf.my");

		print SAVE "numLine=" . $max_mess_page . "\n";

		if ($urlBack ne "") { # Begin if ($urlBack ne "")
			print SAVE "backGround=" . $urlBack . "\n";
		}  # End if ($urlBack ne "")
		else { # Begin else
			print SAVE "backGround=" . $url_stored . "\n";
		} # End else

		if ($separator_bar ne "") { # Begin if ($separator_bar ne "")
			print SAVE "separator_bar=" . $separator_bar . "\n";
		}  # End if ($separator_bar ne "")
		else { # Begin else
			print SAVE "separator_bar=" . $separator_bar_stored . "\n";
		} # End else
		if ($colorText ne "") { # Begin if ($colorText ne "")
			print SAVE "colorText=" . $colorText . "\n";
		} # End if ($colorText ne "")
		else { # Begin else
			print SAVE "colorText=" . $color_text_stored . "\n";
		} # End else
		close(SAVE) ||  die("Cannot close file ". GUEST_BOOK_DIRECTORY_DEPOSIT ." $!");
	}  # End if ($saveConf ne "")
} # End sub saveConf


=head1 FUNCTION show_list_of_guest_books

This function creates a sliding menu where shows up the given name of the guest book, date and time of creation and timer.

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

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:>  Jul 23rd 2006

- I<Created on:> Jul 9th 2006

=back

=cut

sub show_list_of_guest_books { # Begin sub show_list_of_guest_books
	print "<dd id=\"manage_guest_book6\">\n";
	print  "<div id='create_gbook'>\n";
	my $counter = 0;
	print "<form action=\"login.cgi\" method=\"post\">\n";
	print "<input type=hidden name=\"old_guest_book_name\" value=\"$old_guest_book_name\">\n";
	# -------------------------------------------------------
	print  "<input type=hidden name=\"login\" value=\"$login\">\n";		
	print  "<input type=hidden name=\"password\" value=\"$password\">\n";		
	print  "<input type=hidden name=\"function\" value=\"admin\">\n";
	# -------------------------------------------------------
	print "<select name='guest_book_name'>\n";
	my $opt_gb = ("${line_gb_tmp}" eq "$guest_book_name") ? " selected " : "";
	$counter = &count_messages(DEFAULT_NAME_FOR_GUEST_BOOK);
	print "<option value='default' $opt_gb >Default [$counter message(s)]</option>\n";
	if (-f  GUEST_BOOK_DIRECTORY_DEPOSIT ."guest_book_list.my") { # Begin if (-f  GUEST_BOOK_DIRECTORY_DEPOSIT ."guest_book_list.my")
		open(R_GB, GUEST_BOOK_DIRECTORY_DEPOSIT ."guest_book_list.my") || die( GUEST_BOOK_DIRECTORY_DEPOSIT . "guest_book_list.my cannot be found $!");
		my @lines_from_gb = <R_GB>;
		close(R_GB) ||  die("Cannot close file $!");
		if (scalar(@lines_from_gb) != 0) { # Begin if (scalar(@lines_from_gb) != 0)
			foreach my $line_gb_tmp (@lines_from_gb) { # Begin foreach my $line_gb_tmp (@lines_from_gb)
				chomp($line_gb_tmp);
				$counter = &count_messages($line_gb_tmp . ".guest_book.my");
				my ($f,$t) = split(/\_/,$line_gb_tmp);
				#      print "('$line_gb_tmp' eq '$guest_book_name')<br>\n";
				$opt_gb = ("${line_gb_tmp}" eq "$guest_book_name") ? " selected " : "";
				$f =~ s/MY-UNDERSCORE-TAG/\_/g;
				$t =~ s/[\;\-]/\ /;
				$f =~ s/\-\-\-\-/\ /g;
				print "<option value='${line_gb_tmp}' $opt_gb >$f <$t> [$counter message(s)] </option>\n";
			}  # End foreach my $line_gb_tmp (@lines_from_gb)
		}  # End if (scalar(@lines_from_gb) != 0)
	}  # End if (-f  GUEST_BOOK_DIRECTORY_DEPOSIT ."guest_book_list.my")
	print "</select>\n";
	print "<input type=submit value=\"Charger le livre d'or\nLoad guest book\">\n";
	print "</form>\n";
	print "</dd>\n";
}  # End sub show_list_of_guest_books


=head1 FUNCTION  count_messages

This function counts messages within each guest books. This is only for admin menu.

=head2 PARAMETER(S)

=over 4

File name of a guest book.

=back

=head2 RETURNED VALUE

=over 4

Number of messages according to one line: date that was posted the message ie (Posted on Sat Jun 2004 12sd 19:57:25pm).

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jun 9th 2006

- I<Created on:> Jun 9th 2006

=back

=cut

sub count_messages { # Begin sub count_messages
	my $counter = 0;
	my ($line_gb_tmp) = @_;

	if (-f GUEST_BOOK_DIRECTORY_DEPOSIT . "$line_gb_tmp") { # Begin if (-f "$line_gb_tmp")
		if ( -f GUEST_BOOK_DIRECTORY_DEPOSIT . "$line_gb_tmp") { # Begin  if ( -f GUEST_BOOK_DIRECTORY_DEPOSIT . "$line_gb_tmp")
			open(R, GUEST_BOOK_DIRECTORY_DEPOSIT . "$line_gb_tmp") || die( GUEST_BOOK_DIRECTORY_DEPOSIT . "$line_gb_tmp cannot be opened $!");
			my @file = <R>;
			close(R) ||  die("Cannot close file $!");
			if (scalar(@file) != 0) { # Begin if (scalar(@file) != 0)
				foreach my $lines (@file) { # Begin foreach my $lines (@file)
					chomp($lines);
					if ($lines =~ m/^Posted on/) { # Begin if ($lines =~ m/^Posted on.+m$/)
						++$counter;
					}  # End if ($lines =~ m/^Posted on.+m$/)
				}  # End foreach my $lines (@file)
			}  # End if (scalar(@file) != 0)
		} # End  if ( -f GUEST_BOOK_DIRECTORY_DEPOSIT . "$line_gb_tmp")
	} # End if (-f "$line_gb_tmp")
	return $counter;
} # End sub count_messages

=head1 FUNCTION  admin

This function creates a menu for the administrator and saved it in a file that will be printed later on.
This technique was used for a security reason.

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

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jul 27th 2006

- I<Last modification:> Jun 6th 2003

- I<Created on:> Feb 2003

=back

=cut

sub admin { # Begin sub admin
	&saveConf;
	#print "Content-type: text/html\n\n";
	print  "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\">\n";
	print  "<!--\nCode written by shark bait\n-->\n";
	print  "<html>\n";
	print <<END_JAVASCRIPT;
    <head>
      <style type="text/css">
     a, a:link, a:visited {
	 color: orange;
	 text-decoration: none;
     }

	 table.footer {
		       font-size: 12px;
		       text-align: right;
		       color: yellow;
		       link: yellow;
		       vlink: orange;
		       background-color: #353135;
		       opacity: .50;
		     }
END_JAVASCRIPT
	for (my $tag = 0; $tag <= 5; $tag++ ) { # Begin for (my $tag = 1; $tag <= 5; $tag++ )
		print "                 #manage_guest_book$tag {\n";
		print <<END_JAVASCRIPT;
		       position: relative;
		       margin-left: 1px;
		  }
END_JAVASCRIPT
	} # End for (my $tag = 1; $tag <= 5; $tag++ )
	print <<END_JAVASCRIPT;
		  dl {
		       display: inline;
		       width: 100%;
		  }
		  dd {
		       display: none;
		  }
		  ul, li, a {
		     display: inline;
		  }
		  a:link { text-decoration: none; }
		  a:hover { background-color: blue; color: white;}
		  #gb_menu_help {
			-moz-border-radius:10px;
			-webkit-border-radius: 10px;
			border-radius: 10px;

			position: relative;
END_JAVASCRIPT
	print <<END_JAVASCRIPT;
		  }
      </style>
      <script type="text/javascript">
	  <!--
	     function show(id) {
		var d = document.getElementById(id);
END_JAVASCRIPT
	print "                for (var i = 0; i <= " . ((($num_of_private_messages + $max_mess_page) != 0) ? ( $num_of_private_messages + $max_mess_page + 8) : 15 )." ; i++) {\n";
	print <<END_JAVASCRIPT;
			if (document.getElementById('manage_guest_book'+i)) {document.getElementById('manage_guest_book'+i).style.display='none';}
		}
		if (d) {d.style.display='block';}
	     }
	   -->
	</script>
    </head>
END_JAVASCRIPT
	my $tmp = $guest_book_name;
	my $tmp_gb = ();

	if ("$guest_book_name" eq "") { # Begin if ("$tmp" eq "")
		$tmp_gb = "Default";
	}  # End if ("$tmp" eq "")
	else { # Begin else
		$tmp_gb = $guest_book_name;
		$tmp_gb =~ s/MY-UNDERSCORE-TAG/\_/g;
		$tmp_gb =~ s/\-\-\-\-/\ /g;
	} # End else

	print "<body bgcolor='black' text=\"green\" link=yellow vlink=\"red\" onload=\"JavaScript:show()\" >\n";
	print "\n<table width=100% border=0>\n";
	print "<tr>\n<td width=95%  align=center><h1>ADMINISTRATOR MENU</h1>\n";
	if (&checks_if_album_exists($guest_book_name) == 0 ) { # Begin if (&checks_if_album_exists($guest_book_name) == 0 )
		print "[<b>$tmp_gb</b>]\n";
	}  # End if (&checks_if_album_exists($guest_book_name) == 0 )
	else { # Begin else
		print "{Un message de l'administrateur: aller dans un autre livre d'or de ce menu [<b>aller autre livre d'or</b>]}\n<br>{<font color=orange>A message from admin: go to another guest book from current menu [<b>Go to guest book</b>]</font>}\n";
	} # End else
	print "</center>\n</tr>\n";
	print "</table>\n";
	print "<br><br><br>";
	print "<dl>\n<ul id=\"choices\">\n<li>\n";
	if (&checks_if_album_exists($old_guest_book_name) == 0 ) { # Begin if (&checks_if_album_exists($old_guest_book_name) == 0 )
		print "<a href='login.cgi?guest_book_name=$old_guest_book_name'>Leave this menu</font></a></li>\n";
	} # End if (&checks_if_album_exists($old_guest_book_name) == 0 )
	print "<li><dt onclick='javascript:show();javascript:show(\"manage_guest_book6\")'>Changement de livre d'or <font color=orange>Switch Guest Book</font>\n";
	&show_list_of_guest_books;
	print "</li>\n<li>\n<dt onclick='javascript:show();javascript:show(\"manage_guest_book5\")'>Aller à un livre d'or <font color=orange>Go to guest book</font></dt>\n";
	&print_List_GB($tmp_gb) ;
	print "\n</li>\n";
	print "<li>\n<dt onclick='javascript:show();javascript:show(\"manage_guest_book1\")'>Creer un nouveau livre d'or <font color=orange>Create new guest book</font></dt>\n";
	&print_create_gb;
	print "\n</li>\n";
	print "<li>\n<dt onclick='javascript:show();javascript:show(\"manage_guest_book2\")'>Supprimer un livre d'or <font color=orange>Delete guest book</font></dt>\n";
	&print_Remove_GB;
	print "</li>\n";
	print "<li>\n<dt onclick='javascript:show();javascript:show(\"manage_guest_book3\")'>Sauvegarder configuration <font color=orange>Save settings</font></dt>\n";
	&print_Save_settings;
	print "\n</li>\n";
	print "<li>\n\n<dt onclick='javascript:show();javascript:show(\"manage_guest_book4\")'>Lire les messages <font color=orange>Read messages</font></dt>\n";
	&print_Show_messages;
	print "\n</li>\n</ul>\n</dl>\n";
}  # End sub admin

sub print_Show_messages { # Begin sub print_Show_messages
	print "<dd id=\"manage_guest_book4\">\n";
	print  "<div id='set_gbook_messages'>\n";
	&prints_messages_on_admin_screen;
	print "</div>\n</dd>\n";
} # End sub print_Show_messages


=head1 FUNCTION print_Save_settings

This function saves setting for guest book s.a text color, separator bar, background, number of messages per page(s)...

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

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jul 27th 2006

- I<Created on:> Jul 27th 2006

=back

=cut

sub print_Save_settings { # Begin sub print_Save_settings
	print "<dd id=\"manage_guest_book3\">\n";
	print  "<div id='set_gbook'>\n";
	print  "<table>\n";
	print  "<form action=\"login.cgi\" method=\"post\">\n";
	print  "<input type=hidden name=\"function\" value=\"admin\">\n";
	print  "<input type=hidden name=\"password\" value=\"$password\">\n";
	print  "<input type=hidden name=\"login\" value=\"$login\">\n";
	print  "<input type=hidden name=\"page\" value=\"1\">\n";
	#    print  "<input type=hidden name=\"granted\" value=\"ok\">\n";
	print  "<tr><td>\n";
	print "<input type=hidden name=\"old_guest_book_name\" value=\"$old_guest_book_name\">\n";
	print "<input type=hidden name=\"guest_book_name\" value=\"$guest_book_name\">\n";
	print  "<input type=submit name=\"saveConf\" value=\"Sauvegarde\nSave settings\"></tr>\n";
	$separator_bar_stored = &gets_separator_bar;
	print  "<tr><td><td align=right width=45%>Barre de separation <br><font color=orange>Separator bar</font>\n";
	chomp( $separator_bar_stored);
	if ( $separator_bar_stored eq  IMAGE_DIRECTORY_DEPOSIT . "bow.gif" ) { # Begin if ( $separator_bar_stored eq  IMAGE_DIRECTORY_DEPOSIT . "bow.gif" )
		print  "<td>Bow <input type=radio name=\"separator_bar\" value=\"". IMAGE_DIRECTORY_DEPOSIT ."bow.gif\" checked >\n";
	}  # End if ( $separator_bar_stored eq  IMAGE_DIRECTORY_DEPOSIT . "bow.gif" )
	else { # Begin else
		print  "<td>Bow <input type=radio name=\"separator_bar\" value=\"". IMAGE_DIRECTORY_DEPOSIT ."bow.gif\">\n";
	} # End else
	if (  $separator_bar_stored eq  IMAGE_DIRECTORY_DEPOSIT . "hruler13.gif" ) { # Begin if ( $separator_bar_stored eq  IMAGE_DIRECTORY_DEPOSIT . "hruler13.gif" )
		print  "Leaf <input type=radio name=\"separator_bar\" value=\"". IMAGE_DIRECTORY_DEPOSIT ."hruler13.gif\" checked >\n";
	}  # End if ( $separator_bar_stored eq  IMAGE_DIRECTORY_DEPOSIT . "hruler13.gif" )
	else { # Begin else
		print  "Leaf <input type=radio name=\"separator_bar\" value=\"". IMAGE_DIRECTORY_DEPOSIT ."hruler13.gif\">\n";
	}  # End else
	if (  $separator_bar_stored eq  IMAGE_DIRECTORY_DEPOSIT . "wavy.gif" ) { # Begin if (  $separator_bar_stored eq  IMAGE_DIRECTORY_DEPOSIT . "wavy.gif" )
		print  "Wavy <input type=radio name=\"separator_bar\" value=\"". IMAGE_DIRECTORY_DEPOSIT ."wavy.gif\" checked>\n";
	}  # End if (  $separator_bar_stored eq ". IMAGE_DIRECTORY_DEPOSIT ."wavy.gif" )
	else { # Begin else
		print  "Wavy <input type=radio name=\"separator_bar\" value=\"". IMAGE_DIRECTORY_DEPOSIT ."wavy.gif\">\n";
	} # End else
	if (  $separator_bar_stored =~ m/<hr[^\>]*\>$/i ) { # Begin  if (  $separator_bar_stored =~ m/<hr[^\>]*\>$/i )
		print  "Standard <input type=radio name=\"separator_bar\" value=\"<hrSPACEwidthEQUAL42\%>\" checked></tr>\n";
	}  # End if (  $separator_bar_stored =~ m/<hr[^\>]*\>$/i )
	else { # Begin else
		print  "Standard <input type=radio name=\"separator_bar\" value=\"<hrSPACEwidthEQUAL42\%>\"></tr>\n";
	} # End else
	print  "<tr><td><td align=right>Changer le nombre de messages par pages<br><font color=orange>Change number of messages per pages</font>";
	print  "<td><input type=int name=\"max_mess_page\" value=\"" . &gets_line_num ."\"></tr>\n";
	print  "<tr><td><td align=right>Image de font <br> <font color=orange>Background image</font>";
	print  "<td><input type=text name=\"urlBack\" value=\"" . &gets_line_URL_back ."\"></tr>\n";
	print  "<tr><td><td align=right>Selectionner la couleur de texte <br> <font color=orange>Select text color</font><td><select name=\"colorText\">\n";
	print  &selects_color("Black","Yellow","Red","BeOs","Green","CDE","plum","tomato","turquoise","dodgerblue","forestgreen","darkorange","orange","darkred","darkmagenta","darkseagreen","aquamarine","blanchedalmon","chocolate") . "\n";
	print  "</select></tr>\n";
	#    print  "</form></table><tr><td><td><hr width=42></tr>\n";
	print "</form>\n</table>\n</div>\n</dd>\n";
}  # End sub print_Save_settings


=head1 FUNCTION sub print_Remove_GB

This function removes a message from guest book.

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

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Aug 5th 2006

- I<Created on:> Jul 27th 2006

=back

=cut


sub print_Remove_GB { # Begin sub print_Remove_GB
	print "<dd id=\"manage_guest_book2\">\n";
	print  "<div id='remove_gbook'>\n";
	print  "<form action=\"login.cgi\" method=\"post\">\n";

	# -----------------------------

	print  "<input type=hidden name=\"new_guest_book_name\" value=\"$messageId\">\n";		
	print  "<input type=hidden name=\"login\" value=\"$login\">\n";		
	print  "<input type=hidden name=\"password\" value=\"$password\">\n";		
	print  "<input type=hidden name=\"function\" value=\"admin\">\n";
	print  "<input type=hidden name=\"function_admin_extra\" value=\"removes_guest_book\">\n";

	# -----------------

	print "<table>\n<tr><td>";
	print "<input type=hidden name=\"old_guest_book_name\" value=\"$old_guest_book_name\">\n";
	print "<input type=hidden name=\"guest_book_name\" value=\"$guest_book_name\">\n";
	print "<input type=submit name=\"removeGuestBook\" value=\"Supprimer un nouveau livre d'or\nDelete a new guest book\">\n";
	print "<tr>\n<td><td align=right>Supprimer le livre d'or<br>\n<font color=orange>Delete guest book</font>\n<td>\n<select name=\"old_Guest_book_name\">\n";
	if ( -f GUEST_BOOK_DIRECTORY_DEPOSIT . "guest_book_list.my") { # Begin if ( -f "guest_book_list.my")
		open(READ_GUEST_BOOK, GUEST_BOOK_DIRECTORY_DEPOSIT . "guest_book_list.my") || die(" Cannot open ". GUEST_BOOK_DIRECTORY_DEPOSIT ."guest_book_list.my $!");
		foreach my $file (<READ_GUEST_BOOK>) { # Begin foreach my $file (<READ_GUEST_BOOK>)
			chomp($file);
			my $file_tmp = $file;
			$file_tmp =~ s/MY-UNDERSCORE-TAG/\_/g;
			print "<option value='$file'>$file_tmp</option>\n";
		} # End foreach my $file (<READ_GUEST_BOOK>)
		close(READ_GUEST_BOOK) || die("Can't close ". GUEST_BOOK_DIRECTORY_DEPOSIT . "guest_book_list.my $!");
	} # End if ( -f "guest_book_list.my")
	print "</select></tr>\n";
	print "</form>\n";
	print "</table>\n";
	print "</div>\n</dd>\n";
} # End sub print_Remove_GB


=head1 FUNCTION sub print_create_gb

This function prints a given guest book.

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

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Jul 27th 2006

- I<Created on:> Jul 27th 2006

=back

=cut

sub print_create_gb { # Begin sub print_create_gb
	print "<dd id=\"manage_guest_book1\">\n";
	print  "<div id='create_gbook'>\n";
	print  "<table>\n";
	print  "<form action=\"login.cgi\" method=\"post\">\n";
	print  "<tr><td>";
	print "<input type=hidden name=\"old_guest_book_name\" value=\"$old_guest_book_name\">\n";
	print "<input type=hidden name=\"guest_book_name\" value=\"$guest_book_name\">\n";
	print  "<input type=submit name=\"createGuestBook\" value=\"Creer un nouveau livre d'or\nCreate a new guest book\">\n</tr>";
	print  "<tr>\n<td>\n<td align=right>Nom du nouveau livre d'or<br><font color=orange>Name of new guest book </font>\n<td><input type=text name=\"new_Guest_book_name\" maxlength=30></tr>\n";
	print  "<tr>\n<td>\n<td align=right>Durée de disponibilité pour saisir un message dans le livre d'or<br><font color=orange>Timer lag of availability of new guest book to fill messages</font>\n<td><select name='timer'>\n";
	for (my $i = 1; $i <= 31; $i++) { # Begin for (my $i = 1; $i <= 31; $i++)
		print "<option value=$i>$i jour(s)/day(s)</option>\n";
	} # End for (my $i = 1; $i <= 31; $i++)
	print "</option>\n</select>\n";
	print "<td>Option de timing<br><font color=orange>Timing options</font>\n";
	print "<td><select name='period'>\n<option value=n selected>Aucune / None</option>\n<option value=d>Jour(s) / Day(s)</option>\n\n<option value=t>Amorcer / Trigger</option>\n</select>\n</tr>\n</table>\n";

	# --------------------------------------------------------

	print  "<input type=hidden name=\"new_guest_book_name\" value=\"$messageId\">\n";		
	print  "<input type=hidden name=\"login\" value=\"$login\">\n";		
	print  "<input type=hidden name=\"password\" value=\"$password\">\n";		
	print  "<input type=hidden name=\"function\" value=\"admin\">\n";
	print  "<input type=hidden name=\"function_admin_extra\" value=\"creates_guest_book\">\n";

	# --------------------------------------------------------

	print  "</form>\n";
	print  "</div>\n";
	print "</dd>\n";
}  # End sub print_create_gb


=head1 FUNCTION sub print_List_GB

This function prints all guest books as links.

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

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Aug 3rd 2006

- I<Created on:> Jul 27th 2006

=back

=cut

sub print_List_GB  { # Begin sub print_List_GB
	my $status = "Fermé <br><font color=orange>Closed</font>";

	print "<dd id=\"manage_guest_book5\">\n";
	print  "<div id='create_gbook'>\n";
	if (-f  GUEST_BOOK_DIRECTORY_DEPOSIT . "guest_book_list.my") { # Begin  if (-f  GUEST_BOOK_DIRECTORY_DEPOSIT . "guest_book_list.my")
		open(R_GB, GUEST_BOOK_DIRECTORY_DEPOSIT . "guest_book_list.my") || die( GUEST_BOOK_DIRECTORY_DEPOSIT . "guest_book_list.my cannot be found $!");
		print "<table border=1 width=100\%>\n";
		foreach my $line_gb (<R_GB>) { # Begin foreach my $line_gb (<R_GB>)
			chomp($line_gb);
			# We look if line from file (that contains all referenced guest book) contains TRIGERED to get current date if so.
			if ($line_gb =~ m/TRIGGERED/) { # Begin if ($line_gb =~ m/TRIGGERED/)
				($o,$line_gb) = split(/TRIGGERED/,$line_gb);
			}  # End if ($line_gb =~ m/TRIGGERED/)
			# That look if the file is not triggered yet to a date. (File anyway exists).
			if ($line_gb =~ m/[0-9]+t/) { # Begin if ($line_gb =~ m/[0-9]+t/)
				$status = "En attente d'ouverture<br><font color=orange>Stand by for the opening</font>";
			} # End if ($line_gb =~ m/[0-9]+t/)
			# File are trigered and started an existance (file taken from triggered if just below)
			if (&is_file_date_not_over($line_gb) == 0) { # Begin if (&is_file_date_not_over($guest_book_name) == 0)
				# Checks if date is limited
				if ($line_gb =~ m/([0-9]+)d$/) { # Begin if ($guest_book_name =~ m/([0-9]+)d$/)
					my ($file_name,$schedule) = split(/\_/,$line_gb);
					my ($date,$time) = split(/\-/,$schedule);
					$date =~ s/\:/\//g;
					$line_gb =~ m/([0-9]+)d$/;
					$status = "Ouvert pour $1 jour(s) à partir du $date<br><font color=orange>Open during $1 day(s) from $date</font>\n";
				}  # End if ($guest_book_name =~ m/([0-9]+)d$/)
				# Check if no limited date
				elsif ($line_gb =~ m/[0-9]+n$/) { # Begin elsif ($guest_book_name =~ m/[0-9]+n$/)
					$status = "Ouvert<br><font color=orange>Open</font>\n";
				} # End elsif ($guest_book_name =~ m/[0-9]+n$/)
			} # End if (&is_file_date_not_over($guest_book_name) == 0)
			else { # Begin else
				$status = "Fermé <br><font color=orange>Closed</font>";
			} # End else
			my ($f,$t) = split(/\_/,$line_gb);
			$f =~ s/\-\-\-\-/\ /g;
			print "<form action=\"login.cgi\" method=\"post\">\n";
			$f =~ s/MY-UNDERSCORE-TAG/\_/g;
			print "<input type=hidden name=\"guest_book_name\" value=\"$line_gb\">\n";
			print "<tr><th colspan=3 rowspan=2><input type=submit value='$f'></th>\n";
			print "</form>\n";
			print "<td align=left valign=top>$status\n</tr>";
			print "<tr><td>".MY_URL_WITH_CGI_FILE."$line_gb\n";
			print "</tr>\n";
		}  # End foreach my $line_gb (<R_GB>)
		close(R_GB) ||  die("Cannot close file $!");
	}  # End if (-f  GUEST_BOOK_DIRECTORY_DEPOSIT . "guest_book_list.my")
	print "</table>\n";
	print "</div>\n</dd>\n";
} # End sub print_List_GB


=head1 FUNCTION adminLog

This file cleans information in log.html file.

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

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:>  Jun 6th 2003

- I<Created on:> Feb 2003

=back

=cut

sub adminLog { # Begin sub adminLog
	open(DATE,"log.html");
	@lineDate = <DATE>;
	close(DATE) ||  die("Cannot close file $!");
	foreach $l (@lineDate) { # Begin foreach $l (@lineDate)
		$l =~ s!(ok) log!!g;
		$l =~ s!<br>!!g;
	}  # End foreach $l (@lineDate)
}  # End sub adminLog


=head1 FUNCTION eraseAdmin

Prints error messages in the admin.html file.

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

=head2 STATUS

=over 4

Deprecated.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jun 6th 2003

- I<Created on:> Feb 2003

=back

=cut

sub eraseAdmin { # Begin eraseAdmin
	open(ADM,">../admin.html"); 
	print ADM "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\">\n";
	print ADM "<--Code written by shark bait june 6th 2003 \n<br>email:shark.bait\@laposte.net-->\n";
	print ADM "<html><body>file error</body></html>";
	close(ADM) ||  die("Cannot close file $!");
} # End eraseAdmin


=head1 FUNCTION cleanMyVariable

Cleans variables.

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

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:>  Jun 6th 2003

- I<Created on:> Feb 2003

=back

=cut

sub cleanMyVariable { # Begin sub cleanMyVariable
	print "<form action=\"login.cgi\" method=\"post\">\n";
	print "<input type=hidden name=\"privateMess\" value=\"\">\n";
	print "<input type=\"submit\" value=\"Revenir\nGo back\">\n";
	print "<input type=hidden name=\"function\" value=\"\">\n";
	print "<input type=hidden name=\"password\" value=\"\">\n";
	print "<input type=hidden name=\"login\" value=\"\">\n";
	print "<input type=hidden name=\"page\" value=\"1\">\n";
	print "</form>\n";
}  # End sub cleanMyVariable


=head1 FUNCTION cleanMyVariableExtra

Cleans extra variables.

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

=head2 STATUS

=over 4

Deprecated.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Jun 6th 2003

- I<Created on:> Feb 2003

=back

=cut

sub cleanMyVariableExtra { # Begin sub cleanMyVariableExtra
	open(ADMIN,">>../admin.html");
	print ADMIN "<form action=\"cgi-bin/login.cgi\" method=\"post\">\n";
	print ADMIN "<input type=\"submit\" value=\"Go back\">\n";
	print ADMIN "<input type=hidden name=\"function\" value=\"\">\n";
	print ADMIN "<input type=hidden name=\"password\" value=\"\">\n";
	print ADMIN "<input type=hidden name=\"login\" value=\"\">\n";
	print ADMIN "<input type=hidden name=\"page\" value=\"1\">\n";
	print ADMIN "<input type=hidden name=\"saveConf\" value=\"\">\n";
	print ADMIN "</form>\n";
} # End sub cleanMyVariableExtra


=head1 FUNCTION loginAndPassword

Creates the login page. For security reasons a file contains all the code and then is printed on the screen. This function only creates the file.

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

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:>  Jun 28th 2006

- I<Last modification:>  Jun  6th 2003

- I<Created on:> Feb 2003

=back

=cut

sub loginAndPassword { # Begin sub loginAndPassword
	$my_date_log = &giveDate;
	$my_date_log =~ s/When\:/Log\ at/g;
	print  "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\">\n";
	print "<html>\n";
	print  "<!--\nCode written by shark bait june 6th 2003 \nemail:try.to.find@skark.bait.com\n-->\n";
	print <<HEADER;
    <head>
      <style type="text/css">
     body {
	color: yellow;
     }
     a, a:link, a:visited {
	 color: orange;
	 text-decoration: none;
     }
     #my_footer {
	 width: 100%;
	 position: relative;
	 bottom: -250px
     }
     table.footer {
		       font-size: 12px;
		       text-align: right;
		       color: yellow;
		       background-color: #353135;
		       opacity: .50;
		  }
</style>
<script>
// document.write("beg:"+ screen.width + "-" + screen.height +" end");
</script>
</head>
HEADER
	print '<body bgcolor="black" OnLoad="namosw_init_animation();">';
	print "<br><center><h1>$my_date_log<h1></center>";
	print <<ACCESS;
 <p><br>
 </p>
<center>
<table border=0>
	<form action="login.cgi" method="post">
ACCESS
	print "<input type=hidden name=\"guest_book_name\" value=\"$guest_book_name\">\n";
	print "<input type=hidden name=\"old_guest_book_name\" value=\"$guest_book_name\">\n";
	print <<ACCESS;
		<tr>
			<td>Login<td><input type="text" name="login" maxlength="20" size="10">
		</tr>
		<tr>
			<td>Password<td><input type="password" name="password" maxlength="20" size="10">
		</tr>
		<tr>
			<td>
			<td align=center valign=center> <input type="submit" value="Submit" maxlength="20" size="10" >
							<input type="hidden" name="function" value="admin" maxlength="20" size="10" >
	</form>
			    <td align=center valign=center>
	<form action="login.cgi" method="post">
ACCESS
	print "                          <input type=hidden name=\"guest_book_name\" value=\"$guest_book_name\">\n";
	print <<ACCESS;
			     <input type="submit" value="Go back" maxlength="20" size="10" >
			     <input type="hidden" name="function" value="" maxlength="20" size="10" >
		</tr>
	 </form>
</table>
</center>
ACCESS
}  # End sub loginAndPassword


=head1 FUNCTION pageNotGranted

Returns code to print on the screen for a not granted access.

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

String to print not granted access page.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 STATUS

=over 4

Deprecated.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jun 6th 2003

- I<Created on:> Feb 2003

=back

=cut

sub pageNotGranted { # Begin sub pageNotGranted
	open(MY_DYN,"../pageNotGranted.html");
	$my_bkg = $url_stored;
	$my_bkg =~ s/\.\.\///g;
	@lin = <MY_DYN>;
	close(MY_DYN) ||  die("Cannot close file $!");
	$my_date_log = &giveDate;
	$my_date_log =~ s/When\:/Log\ at/g;
	foreach $l     (@lin)  { # Begin foreach $l     (@lin) 
		$l =~ s/\_\&backurl\&\_/$my_bkg/g;
		$l =~ s/\_\&time\&\_/\<center\>\<h1\>$my_date_log\<h1\>\<\/center\>/g;
	}  # End foreach $l     (@lin) 
	return "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\">\n" .
	"<!--\nCode written by shark bait june 6th 2003 \nemail:shark.bait\@laposte.net\n-->\n" .
	"@lin";
}  # End sub pageNotGranted


=head1 FUNCTION  pageGranted

Returns code to print on the screen for the granted access page.

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

String to print granted access page.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 STATUS

=over 4

Deprecated.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jun 6th 2003

- I<Created on:> Feb 2003

=back

=cut

sub pageGranted { # Begin sub pageGranted
	open(MY_DYN,"../pageGranted.html");
	$my_bkg = $url_stored;
	$my_bkg =~ s/\.\.\///g;
	@lin = <MY_DYN>;
	close(MY_DYN) ||  die("Cannot close file $!");
	$my_date_log = &giveDate;
	$my_date_log =~ s/When\:/Log\ at/g;
	foreach $l     (@lin)  { # Begin foreach $l     (@lin)
		$l =~ s/\_\&backurl\&\_/$my_bkg/g;
		$l =~ s/\_\&time\&\_/\<center\>\<h1\>$my_date_log\<h1\>\<\/center\>/g;
	}  # End foreach $l     (@lin)
	return "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\">\n" .
	"<!--\nCode written by shark bait june 6th 2003 \nemail:shark.bait\@laposte.net\n-->\n" .
	"@lin";
}  # End sub pageGranted


=head1 FUNCTION insertMessageGuestBook

This function inserts or stores message in the guest book.

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

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Sep 4th 2006

- I<Last modification:> Jul 12sd 2006

- I<Last modification:> Jun 6th 2003

- I<Created on:> Feb 2003

=back

=cut

sub insertMessageGuestBook { # Begin sub insertMessageGuestBook
	$compDate = &giveDate;
	$noSpace = $compDate;
	$compDate =~ s/When\:/Posted on/g;
	$noSpace =~ s/\ //g;
	$author =~ s/^\ //g;
	chomp($noSpace);
	$tmp_mess = $mess;
	$tmp_mess =~ s/\ //g;
	chomp($tmp_mess);

	my $gb_name = ( "$guest_book_name" =~ m/^body.my$/ ) ?  DEFAULT_NAME_FOR_GUEST_BOOK : "${guest_book_name}.guest_book.my";

	if (!-f GUEST_BOOK_DIRECTORY_DEPOSIT . "$gb_name") {
		open(GUESTBOOK,">". GUEST_BOOK_DIRECTORY_DEPOSIT ."$gb_name") || die("Can't create ". GUEST_BOOK_DIRECTORY_DEPOSIT ."$gb_name $!");;
		flock GUESTBOOK, LOCK_EX;
		print GUESTBOOK "\<!--${noSpace}--\>\n";
		if ($privateMess =~ /Submit as private message/) { # Begin if ($privateMess =~ /Submit as private message/)
			print GUESTBOOK "\<!--privateMessage--\>\n<i><b>This is a private message</b><br></i>\n";
		}  # End if ($privateMess =~ /Submit as private message/)
		if ($email eq "") { # Begin if ($email eq "")
			if ($author eq "") { # Begin if ($author eq "")
			}  # End if ($author eq "")
			else { # Begin else
				if ($home_url eq "") { # Begin if ($home_url eq "")
				}  # End if ($home_url eq "")
				else { # Begin else
					print GUESTBOOK "Auteur/Author: $author ($remhost)<br>\n";
				} # End else
			}  # End else
		}  # En if ($email eq "")
		else { # Begin else
			if ($author eq "") { # Begin if ($author eq "")
				print GUESTBOOK "Auteur/Author: <a href=\"mailto:$email\">-</a><br>\n";
			}  # End if ($author eq "")
			else { # Begin else
				print GUESTBOOK "Auteur/Author: <a href=\"mailto:$email\">$author</a><br>\n";
			}  # End else
		}  # End else
		if ($loc ne "") { # Begin if ($loc ne "")
			print GUESTBOOK "Lieu/Location\: $loc<br>\n";
		} # End if ($loc ne "")
		if ($home_url =~ /http\:\/\/$/) { # Begin if ($home_url =~ /http\:\/\/$/)
		}  # End if ($home_url =~ /http\:\/\/$/)
		else { # Begin else
			print GUESTBOOK "Votre site/Your home page: <a href=\"JavaScript:window.open(\'$home_url\') onclick=\"login?guest_book_name=$guest_book_name&page=$page\"\">$home_name</a><br>\n";
		}  # End else
		print GUESTBOOK "$compDate<br>\n";
		$nbwordOffSet = 120;
		$wordLength = 0;
		$max = length("$mess") ;
		print GUESTBOOK "<pre>\n";
		# Messages are stored here in a file
		while ($wordLength < $max) { # Begin while ($wordLength < $max)
			$str = substr($mess,$wordLength,$nbwordOffSet);
			print GUESTBOOK  $str  . "\n<br>\n" ;
			$wordLength += ($nbwordOffSet);
		}  # End while ($wordLength < $max)
		print GUESTBOOK "</pre>\n<br>\n";
		if ($privateMess =~ /Submit as private message/) { # Begin if ($privateMess =~ /Submit as private message/)
			print GUESTBOOK "\<!--privateMessageEnd--\>\n";
		} # End if ($privateMess =~ /Submit as private message/)
		print GUESTBOOK "\n<center>\n<img width=\"90\%\" src=\"_\&separator_bar_stored\&_\">\n</center>\n<br>\n";
		print GUESTBOOK "\<!--${noSpace}End--\>\n";
		close(GUESTBOOK) ||  die("Cannot close file $!");
	}
	elsif ($tmp_mess ne "") { # Begin if ($tmp_mess ne "")
		while (open(GUESTBOOK, GUEST_BOOK_DIRECTORY_DEPOSIT . "$gb_name") < 0 ) { # Begin while (open(GUESTBOOK, GUEST_BOOK_DIRECTORY_DEPOSIT . "$gb_name") < 0 )
			sleep(1000);
		} # End while (open(GUESTBOOK, GUEST_BOOK_DIRECTORY_DEPOSIT . "$gb_name") < 0 )
		# || die ("File ". GUEST_BOOK_DIRECTORY_DEPOSIT ."$gb_name is not found [sub insertMessageGuestBook] $!");
		flock GUESTBOOK, LOCK_EX;

		open(GUESTBOOK_OLD_TMP,">". GUEST_BOOK_DIRECTORY_DEPOSIT ."bidon.my") || die ("File ". GUEST_BOOK_DIRECTORY_DEPOSIT."bidon.my cannot be created [sub insertMessageGuestBook] $!");
		flock GUESTBOOK_OLD_TMP, LOCK_EX;
		@oldGuestBook = <GUESTBOOK>;
		print GUESTBOOK_OLD_TMP "@oldGuestBook";
		close(GUESTBOOK) ||  die("Cannot close file $!");
		close(GUESTBOOK_OLD_TMP) ||  die("Cannot close file $!");
		while (open(GUESTBOOK,">". GUEST_BOOK_DIRECTORY_DEPOSIT ."$gb_name") < 0) { # Begin while (open(GUESTBOOK,">". GUEST_BOOK_DIRECTORY_DEPOSIT ."$gb_name") < 0)
			sleep(1000);
		} # End while (open(GUESTBOOK,">". GUEST_BOOK_DIRECTORY_DEPOSIT ."$gb_name") < 0)
		#|| die("Can't create ". GUEST_BOOK_DIRECTORY_DEPOSIT ."$gb_name $!");;
		flock GUESTBOOK, LOCK_EX;
		print GUESTBOOK "\<!--${noSpace}--\>\n";
		if ($privateMess =~ /Submit as private message/) { # Begin if ($privateMess =~ /Submit as private message/)
			print GUESTBOOK "\<!--privateMessage--\>\n<i><b>This is a private message</b><br></i>\n";
		}  # End if ($privateMess =~ /Submit as private message/)
		if ($email eq "") { # Begin if ($email eq "")
			if ($author eq "") { # Begin if ($author eq "")
			}  # End if ($author eq "")
			else { # Begin else
				if ($home_url eq "") { # Begin if ($home_url eq "")
				}  # End if ($home_url eq "")
				else { # Begin else
					print GUESTBOOK "Auteur/Author: $author ($remhost)<br>\n";
				} # End else
			}  # End else
		}  # En if ($email eq "")
		else { # Begin else
			if ($author eq "") { # Begin if ($author eq "")
				print GUESTBOOK "Auteur/Author: <a href=\"mailto:$email\">-</a><br>\n";
			}  # End if ($author eq "")
			else { # Begin else
				print GUESTBOOK "Auteur/Author: <a href=\"mailto:$email\">$author</a><br>\n";
			}  # End else
		}  # End else
		if ($loc ne "") { # Begin if ($loc ne "")
			print GUESTBOOK "Lieu/Location\: $loc<br>\n";
		} # End if ($loc ne "")
		if ($home_url =~ /http\:\/\/$/) { # Begin if ($home_url =~ /http\:\/\/$/)
		}  # End if ($home_url =~ /http\:\/\/$/)
		else { # Begin else
			print GUESTBOOK "Votre site/Your home page: <a href=\"JavaScript:window.open(\'$home_url\') onclick=\"login?guest_book_name=$guest_book_name&page=$page\"\">$home_name</a><br>\n";
		}  # End else
		print GUESTBOOK "$compDate<br>\n";
		$nbwordOffSet = 120;
		$wordLength = 0;
		$max = length("$mess") ;
		print GUESTBOOK "<pre>\n";
		# Messages are stored here in a file
		while ($wordLength < $max) { # Begin while ($wordLength < $max)
			$str = substr($mess,$wordLength,$nbwordOffSet);
			print GUESTBOOK  $str  . "\n<br>\n" ;
			$wordLength += ($nbwordOffSet);
		}  # End while ($wordLength < $max)
		print GUESTBOOK "</pre>\n<br>\n";
		if ($privateMess =~ /Submit as private message/) { # Begin if ($privateMess =~ /Submit as private message/)
			print GUESTBOOK "\<!--privateMessageEnd--\>\n";
		} # End if ($privateMess =~ /Submit as private message/)
		print GUESTBOOK "\n<center>\n<img width=\"90\%\" src=\"_\&separator_bar_stored\&_\">\n</center>\n<br>\n";
		print GUESTBOOK "\<!--${noSpace}End--\>\n";
		close(GUESTBOOK) ||  die("Cannot close file $!");
		while (open(GUESTBOOK,">>". GUEST_BOOK_DIRECTORY_DEPOSIT ."$gb_name") < 0) { # Begin while (open(GUESTBOOK,">>". GUEST_BOOK_DIRECTORY_DEPOSIT ."$gb_name") < 0)
			# || die("Can't open and add and end of ". GUEST_BOOK_DIRECTORY_DEPOSIT ."$gb_name $!");;
			sleep(1000);
		} # End while (open(GUESTBOOK,">>". GUEST_BOOK_DIRECTORY_DEPOSIT ."$gb_name") < 0)
		flock GUESTBOOK, LOCK_EX;
		open(GUESTBOOK_OLD_TMP,  GUEST_BOOK_DIRECTORY_DEPOSIT . "bidon.my") || die("Can't open ". GUEST_BOOK_DIRECTORY_DEPOSIT ."bidon.my $!");;
		flock GUESTBOOK_OLD_TMP, LOCK_EX;
		while (<GUESTBOOK_OLD_TMP>) { # Begin while (<GUESTBOOK_OLD_TMP>)
			chomp($_);
			$_ =~ s/^\ //g;
			print GUESTBOOK "$_\n";
		}  # End while (<GUESTBOOK_OLD_TMP>)
		close(GUESTBOOK) ||  die("Cannot close file $!");
		close(GUESTBOOK_OLD_TMP) ||  die("Cannot close file $!");
		unlink  GUEST_BOOK_DIRECTORY_DEPOSIT . "bidon.my" || die("Cannot remove ". GUEST_BOOK_DIRECTORY_DEPOSIT ."bidon.my");
	}  # End if ($tmp_mess ne "")
	$page = 1;
} # End sub insertMessageGuestBook


=head1 FUNCTION prints_messages_on_admin_screen

This function removes a selected message from a given guest book name. That's at the moderator side. In this case the moderator is the administrator.

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

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:>  Aug 5th 2006

- I<Last modification:>  Jun 6th 2003

- I<Created on:> Feb 2003

=back

=cut

sub prints_messages_on_admin_screen { # Begin sub prints_messages_on_admin_screen
	chomp($torem);
	&removeGuestBook($torem);
	$torem = "";
	if ( $guest_book_name !~ m/TimerDelay/i) { # Begin if ( $guest_book_name !~ m/TimerDelay/i)
		open(GUESTBOOK, GUEST_BOOK_DIRECTORY_DEPOSIT . "body.my") || die("Can't open ".  GUEST_BOOK_DIRECTORY_DEPOSIT."body.my $!");
	}  # End if ( $guest_book_name !~ m/TimerDelay/i)
	else { # Begin else
		open(GUESTBOOK, GUEST_BOOK_DIRECTORY_DEPOSIT . "${guest_book_name}.guest_book.my") || die("Can't find ". GUEST_BOOK_DIRECTORY_DEPOSIT ."${guest_book_name}.guest_book.my $!");
	}  # End else
	$localized = "";
	$lineStored = "";
	$toSave = "-->";
	$next = "";
	print  "<table border=1 width=60\%><tr><td width=50\%>Messages</tr>\n";
	while (<GUESTBOOK>) { # Begin while (<GUESTBOOK>)
		$_ =~ s/\<\!\-\-privateMessage\-\-\>//g;
		$_ =~ s/\<\!\-\-privateMessageEnd\-\-\>//g;
		if (/\<\!\-\-When\:[a-zA-Z]/ && $next eq "") { # Begin if (/\<\!\-\-When\:[a-zA-Z]/ && $next eq "")
			$end = $torem . "End";
			$_ =~ s/[\<\>\-\-\!]//g;
			$messageId = $_;
		}  # End if (/\<\!\-\-When\:[a-zA-Z]/ && $next eq "")
		if ($localized eq "" && $next eq "") { # Begin if ($localized eq "" && $next eq "")
			if (/End/) { # Begin if (/End/)
				print  "<tr>\n";
				print  "<td>\n";

				$nbwordOffSet = 100;
				$wordLength = 0;
				$max = length("$lineStored") ;
				$prev = ();
				while ($wordLength < $max) { # Begin while ($wordLength < $max)
					$str = substr($lineStored,$wordLength,$nbwordOffSet);
					#		    if ($str =~ m/\<cent(er\>){0,1}/i) { # Begin if ($str =~ m/\<cent(er\>){0,1}/i)
					#		      $str =~ s/(\<cent(er\>){0,1})/\<\!\-\-\ $1/i;
					#		      $prev = 1;
					#		    }  # End if ($str =~ m/\<cent(er\>){0,1}/i)
					#		    if ( $str =~ m/\<\/center\>/i ) { # Begin if ( $str =~ m/\<\/center\>/i )
					#		      $str =~ s/(\<\/center\>)/$1\ \-\-\>/i;
					#		      $prev = 0;
					#		    } # End if ( $str =~ m/\<\/center\>/i )
					if ($prev == 1 && $str =~ m/(\<td)/i) { # Begin if ($prev == 1 && $str =~ m/(\<td)/i)
						$prev = 0;
						$str =~ s/\<td/\-\-\>$1/g;
					} # End if ($prev == 1 && $str =~ m/(\<td)/i)
					print   $str  ;
					$wordLength += ($nbwordOffSet);
				}  # End while ($wordLength < $max)
				chomp($messageId);
				$messageId =~ s/[\ ]//g;
				$messageId =~ s/End//g;
				$lineStored = "";
				print "<td align=center valign=top>\n";
				print "<form action=\"login.cgi\" method=post>\n";
				print "<input type=hidden name=\"guest_book_name\" value=\"$guest_book_name\">\n";
				print "<input type=hidden name=\"old_guest_book_name\" value=\"$guest_book_name\">\n";
				print "<input type=submit value=\"Enlever message\nRemove message\">\n";
				print "<input type=hidden name=\"torem\" value=\"$messageId\">\n";
				print "<input type=hidden name=\"login\" value=\"$login\">\n";
				print "<input type=hidden name=\"password\" value=\"$password\">\n";
				print "<input type=hidden name=\"function\" value=\"admin\">\n";
				#		print  "<input type=hidden name=\"granted\" value=\"ok\">\n";
				#                print  "<input type=hidden name=\"guest_book_name\" value=\"$guest_book_name\">\n";
				print "</form>\n";
				print "</tr>\n";
			}  # End if (/End/)
			if (/When\:[a-zA-Z]/) { # Begin if (/When\:[a-zA-Z]/)
				chomp($_);
				$_ =~ s/\ //g;
				$toSave = $toSave . "<--" . $_ . "-->\n";
			}  # End if (/When\:[a-zA-Z]/)
			else { # Begin else
				$lineStored = $lineStored . $_;
			} # End else
		}  # End if ($localized eq "" && $next eq "")
		$next = "";
	}  # End while (<GUESTBOOK>)
	print  "</table>\n";
	close(GUESTBOOK) ||  die("Cannot close file $!");
	#    close(ADMIN) ||  die("Cannot close file $!");;
}  # End sub prints_messages_on_admin_screen


=head1 FUNCTION removeGuestBook

This function removes an old guest book.

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

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jul 11st 2006

- I<Last modification:> Jun 6th 2003

- I<Created on:> Feb 2003

=back

=cut

sub removeGuestBook { # Begin sub removeGuestBook
	if (@_[0] ne "") { # Begin if (@_[0] ne "")
		if ( $guest_book_name !~ m/TimerDelay/i) { # Begin if ( $guest_book_name !~ m/TimerDelay/i)
			open(GUESTBOOK_OLD, GUEST_BOOK_DIRECTORY_DEPOSIT . "body.my") || die("Can't open ". GUEST_BOOK_DIRECTORY_DEPOSIT ."body.my $!");
		}  # End if ( $guest_book_name !~ m/TimerDelay/i)
		else { # Begin else
			open(GUESTBOOK_OLD, GUEST_BOOK_DIRECTORY_DEPOSIT . "${guest_book_name}.guest_book.my") || die("Can't open ". GUEST_BOOK_DIRECTORY_DEPOSIT."${guest_book_name}.guest_book.my $!");
		}  # End else
		open(GUESTBOOK_TMP,">" . GUEST_BOOK_DIRECTORY_DEPOSIT . TEMPORARY_FILE . "${guest_book_name}") || die("Can't create ". GUEST_BOOK_DIRECTORY_DEPOSIT . TEMPORARY_FILE  .".${guest_book_name} $!");
		@lineBody = <GUESTBOOK_OLD>;
		$dateToRemove = "@_[0]";
		$dateToRemoveEnd = $dateToRemove . "End";
		$dateToRemoveFind = "";
		foreach $line (@lineBody) { # Begin foreach $line (@lineBody)
			if ($line =~ m/$dateToRemove/) { # Begin if ($line =~ m/$dateToRemove/)
				$dateToRemoveFind = ($dateToRemoveFind eq "" ) ? "ok" : "";
			}  # End if ($line =~ m/$dateToRemove/)
			else { # Begin else
				if ($dateToRemoveFind eq "") { # Begin if ($dateToRemoveFind eq "")
					print GUESTBOOK_TMP $line;
				}  # End if ($dateToRemoveFind eq "")
			}  # End else
		}  # End foreach $line (@lineBody)
		close(GUESTBOOK_OLD) ||  die("Cannot close file $!");
		close(GUESTBOOK_TMP) ||  die("Cannot close file $!");
		if ( $guest_book_name !~ m/TimerDelay/i) { # Begin if ( $guest_book_name !~ m/TimerDelay/i)
			open(GUESTBOOK_NEW,">". GUEST_BOOK_DIRECTORY_DEPOSIT."body.my") || die("Can't create ". GUEST_BOOK_DIRECTORY_DEPOSIT ." body.my $!");
		}  # End if ( $guest_book_name !~ m/TimerDelay/i)
		else { # Begin else
			open(GUESTBOOK_NEW,">". GUEST_BOOK_DIRECTORY_DEPOSIT ."${guest_book_name}.guest_book.my") || die("Can't create ". GUEST_BOOK_DIRECTORY_DEPOSIT ." ${guest_book_name}.guest_book.my $!");
		}  # End else
		open(GUESTBOOK_OLD2, GUEST_BOOK_DIRECTORY_DEPOSIT . TEMPORARY_FILE . "${guest_book_name}") || die("Can't open ". GUEST_BOOK_DIRECTORY_DEPOSIT . TEMPORARY_FILE .".$guest_book_name $!");
		@fileToTransfer = <GUESTBOOK_OLD2>;
		print GUESTBOOK_NEW @fileToTransfer;
		close(GUESTBOOK_NEW) ||  die("Cannot close file $!");
		close(GUESTBOOK_OLD2) ||  die("Cannot close file $!");
		my $file_tmp = TEMPORARY_FILE . "*";
		unlink GUEST_BOOK_DIRECTORY_DEPOSIT . TEMPORARY_FILE . "${guest_book_name}" || die("Can't remove ". GUEST_BOOK_DIRECTORY_DEPOSIT . TEMPORARY_FILE . "${guest_book_name} $!");
	}  # End if (@_[0] ne "")
} # End sub removeGuestBook


=head1 FUNCTION  head

Prints head for the page.

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

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Jun 6th 2003

- I<Created on:> Feb 2003

=back

=cut

sub head { # Begin sub head
	#print "Content-type: text/html\n\n";
	print "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\">\n";
	print "<!--\nCode written shark bait june 6th 2003\n-->\n";
	print "<html>\n";
	#    print "<body>\n";
}  # End sub head


=head1 FUNCTION  foot

Prints foot of the page.

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

=head2 STATUS

=over 4

Deprecated.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jun 6th 2003

- I<Created on:> Feb 2003

=back

=cut

sub foot { # Begin sub foot
	print "</body>\n";
	print "</html>\n";
}  # End sub foot


=head1 FUNCTION form_to_fill_guestbook

Creates a file that will print after a call the form.

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

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Aug 2sd 2006

- I<Last modification:> Jun 6th 2003


- I<Created on:> Feb 2003

=back

=cut

sub form_to_fill_guestbook { # Begin sub form_to_fill_guestbook
	print  "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\">\n<!--\nCode written by shark bait june 6th 2003\n<br>email:shark.bait\@laposte.net\n-->\n<html>\n";

	print <<END_JAVASCRIPT;
    <head>
      <style type="text/css">
		  #fill_action_help_menu {
			position: absolute;
			opacity:.85;
			top: 90px;
			left: 5px;
			width: 930px;
			height: 800px;
			border: solid .1em yellow;
			background: #353135;
		  }
		  #guest_book li {
		     display: inline;
		  }
		  a:link {

		     text-decoration: none;
		  }
		  a:hover {
		     background-color: blue;
		     color: white;
		  }
		  #authenticate {
			position: relative;
			opacity:.50;
			top: -10px;
			left: 2px;
			width: 300px;
			height: 100px;
END_JAVASCRIPT
	print '                        background: #6f726f;'. "\n";
	print <<END_JAVASCRIPT;
		 //       border: #DDD042 solid 0.5px ;
		  }
      </style>
      <script type="text/javascript">
	  <!--
	     function show(id) {
		var d = document.getElementById(id);
END_JAVASCRIPT
	print "                for (var i = 0; i <= " . ( $num_of_private_messages + $max_mess_page + 8 )." ; i++) {\n";
	print <<END_JAVASCRIPT;
			if (document.getElementById('manage_guest_book'+i)) {
			      document.getElementById('manage_guest_book'+i).style.display='none';
			}
		}
		if (d) {
		    d.style.display='block';
		}
	     }
	   -->
	</script>
    </head>

END_JAVASCRIPT
	$aranged = $url_stored;
	$aranged =~ s/\.\.\///g;
	print "<body bgcolor=\"black\" text=\"green\" onload=\"javascript:show()\" link=yellow>\n";

	print "<table width=100%>\n<tr>\n<td>";
	print "<form action=\"login.cgi\" method=\"post\">\n";
	print "<input type=hidden name=\"guest_book_name\" value=\"$guest_book_name\">\n";
	print "<input type=\"submit\" value=\"Retour arrière\nGo back\">\n";
	print "<input type=hidden name=\"function\" value=\"\">\n";
	print "<input type=hidden name=\"password\" value=\"\">\n";
	print "<input type=hidden name=\"login\" value=\"\">\n";
	print "<input type=hidden name=\"page\" value=\"$page\">\n";
	print "</form>\n";
	print "<td align=right valign=center>\n";
	print "<dl><dt onclick=\"javascript:show();javascript:show('manage_guest_book0');\"><font color=\"$color_text_stored\">Aide / </font><font color=orange>Help</font>\n</dt>\n";
	my $guest_book_name_old = $guest_book_name;
	$guest_book_name = "help";
	&prints_help_message_if_signing_up_guest_book;
	$guest_book_name = $guest_book_name_old;
	print "</dl></tr>\n</table>\n";
	print "<br>\n <center><font color=\"$color_text_stored\">Signer le livre d'or / </font><font color=orange>Sign up guest book </font> " . &print_title . "</center><br><br><br>";
	print "<form action=\"login.cgi\" method=\"post\">\n";
	print "<input type=hidden name=\"guest_book_name\" value=\"$guest_book_name_old\">\n";
	print "<input type=hidden name=\"page\" value=\"$page\">\n";
	print "<fieldset>\n";
	print "<legend><font color=\"$color_text_stored\">Entrez des informations générales /</font> <font color=orange>Set general information</font></legend>\n";
	print "<input type=hidden name=\"function\" value=\"post\"><br>\n";

	print "<table>\n";
	print "<tr><td>";
	print "<font color=\"$color_text_stored\">Auteur / </font></font><font color=orange>Author</font><font color=\"$color_text_stored\">:</font><td><input type=\"text\" name=\"author\"></tr>\n";
	print "<tr><td><font color=\"$color_text_stored\">Votre nom de site web / </font><font color=orange>Your website name</font><font color=\"$color_text_stored\">:</font><td><input type=\"text\" name=\"home_name\"></tr>\n";
	print "<tr><td><font color=\"$color_text_stored\">Entrer l'adresse du site web / </font><font color=orange>Your website address</font>:<td><input type=\"text\" name=\"home_url\" value=\"http://\"></tr>\n";
	print "<tr><td><font color=\"$color_text_stored\">Votre email / </font><font color=\"orange\">Your email</font><font color=\"$color_text_stored\">:</font><td><input type=\"text\" name=\"email\"></tr>\n";
	print "<tr><td><font color=\"$color_text_stored\">Lieu (ville+pays) / </font><font color=orange>Location (town+country)</font><font color=\"$color_text_stored\">:</font><td><input type=\"text\" name=\"loc\"></tr>\n";
	print "</table>\n";
	print "</fieldset>\n";
	print "<fieldset>\n";
	print "<legend><font color=\"$color_text_stored\">Entrez votre message / </font><font color=orange>Enter your message</font></legend><br>\n";
	print "<textarea name=mess cols=92% rows=5>Entrer texte ici / Enter text here</textarea><br>\n";
	print "</fieldset>\n";
	print "<table>\n";
	print "<tr>\n";
	print "<td>\n";
	print "<input type=submit  name=\"privateMess\" value=\"Envoyer\nSubmit\">\n";
	print "<input type=\"reset\" value=\"Effacer\nReset\">\n";
	print "<td>\n";
	print "<input type=submit name=\"privateMess\" value=\"Enregistrer en tant que message privé\nSubmit as private message\">\n";
	print "<input type=hidden name=\"page\" value=\"$page\">\n";
	print "<td>\n";
	print "</tr>\n";
	print "</table>\n";
	print "</form>\n</body>\n<!-- End sub form_to_fill_guestbook -->\n</html>\n";
}  # End sub form_to_fill_guestbook


=head1 FUNCTION selects_color

Select colors.

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

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Jun 6th 2003

- I<Created on:> Feb 2003

=back

=cut

sub selects_color { # Begin sub selects_color
	$returnedString = "";
	foreach $color ( @_ ) { # Begin foreach $color ( @_ )
		$returnedString = $returnedString .&selects_option_color($color);
	}  # End foreach $color ( @_ )
	return $returnedString;
} # End sub selects_color


=head1 FUNCTION selects_option_color

Creates option field on the admin menu for colors.

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

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Last modification:> Jun 6th 2003

- I<Created on:> Feb 2003

=back

=cut

sub selects_option_color { # Begin sub selects_option_color
	$colorValue = @_[0];
	if ($colorValue eq $color_text_stored) { # Begin if ($colorValue eq $color_text_stored)
		return "<option selected>$colorValue</option>";
	}  # End if ($colorValue eq $color_text_stored)
	return "<option>$colorValue</option>";
}  # End sub selects_option_color


=head1 FUNCTION show_guest_book

Prints guest book on the screen.

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

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jul 15 2011: change css

- I<Last modification:> Jul 26th 2006

- I<Last modification:> Jun 6th 2003

- I<Created on:> Feb 2003

=back

=cut

sub show_guest_book { # Begin sub show_guest_book
	my $is_pre_tag = 0;
	my $num_authen_menu = 0;
	my $gb_name = ( "$guest_book_name" eq  DEFAULT_NAME_FOR_GUEST_BOOK ) ?  DEFAULT_NAME_FOR_GUEST_BOOK : "${guest_book_name}.guest_book.my";
	my $num_of_private_messages = &number_of_private_messages($gb_name);

	print <<END_JAVASCRIPT;
  <html>
    <head>
      <style type="text/css">
     table.footer {
		       font-size: 12px;
		       text-align: right;
		       color: yellow;
		       link: yellow;
		       vlink: orange;
		       background-color: #353135;
		       opacity: .50;
		  }

		  #help_main_menu {
			-moz-border-radius:10px;
			-webkit-border-radius: 10px;
			border-radius: 10px;
			position: absolute;
			opacity:.85;
			top: 90px;
			left: 5px;
			width: 930px;
			height: 480px;
			border: solid .1em yellow;
			background: #353135;
		  }
		  #guest_book li {
		     display: inline;
		  }
		  a:link {
		     text-decoration: none;
		  }
		  a:hover {
		     color: white;
		  }
		  #authenticate {
			position: relative;
			opacity:.50;
			top: -10px;
			left: 2px;
			width: 300px;
			height: 100px;
END_JAVASCRIPT
	print '                        background: #6f726f;'. "\n";
	print <<END_JAVASCRIPT;
		 //       border: #DDD042 solid 0.5px ;
		  }
      </style>
      <script type="text/javascript">
	  <!--
	     function show(id) {
		var d = document.getElementById(id);
END_JAVASCRIPT
	print "                for (var i = 0; i <= " . ( $num_of_private_messages + $max_mess_page + 9)." ; i++) {\n";
	print <<END_JAVASCRIPT;
			if (document.getElementById('manage_guest_book'+i)) {
			      document.getElementById('manage_guest_book'+i).style.display='none';
			}
		}
		if (d) {
		    d.style.display='block';
		}
	     }
	   -->
	</script>
    </head>

END_JAVASCRIPT
	print "<body link=\"yellow\" vlink=\"red\" bgcolor=\"black\" text=\"green\" onload=\"javascript:show()\">\n";
	if ($guest_book_name !~ m/help/) { # Begin if ($guest_book_name !~ m/help/)
		print "<table width=100%>\n";
		#&TR;
		#&TD;
		#print "<a href=\"http://dorey.sebastien.free.fr/\">";
		#print "Page d'accueil/Home page\n";
		#print "</a><br>\n";
		#&TR_E;
		&TR;
		&TD;
		if (&is_file_date_not_over($guest_book_name) == 0) { # Begin if (&is_file_date_not_over($guest_book_name) == 0)
			print "<form action=\"login.cgi\" method=\"post\">\n";
			print "<input type=hidden name=\"guest_book_name\" value=\"$guest_book_name\">\n";
			print "<input type=hidden name=\"function\" value=\"fill\">\n";
			print "<input type=submit value=\"Signer / Sign \"><br>\n";
			print "<input type=hidden name=\"page\" value=\"$page\">\n";
			print "</form>\n";
		} # End if (&is_file_date_not_over($guest_book_name) == 0)
		&TR_E;
		&TR;
		&TD;
		print "<form action=\"login.cgi\" method=\"post\">\n";
		print "<input type=hidden name=\"function\" value=\"admin\">\n";
		print "<input type=submit value=\"Autres activités / Other stuff \"><br>\n";
		print "<input type=hidden name=\"guest_book_name\" value=\"$guest_book_name\">\n";
		print "<input type=hidden name=\"old_guest_book_name\" value=\"$guest_book_name\">\n";
		print "</form>\n";
		&TR_E;
		&TR;
		&TD;
		#print "<td align=right><dl><dt onclick='javascript:show();javascript:show(\"manage_guest_book0\")'>Aide <font color=orange>Help</font></dt>";
		print "<dt onclick='javascript:show();javascript:show(\"manage_guest_book0\")'>Aide <font color=orange>Help</font></dt>";
		&prints_help_for_main_menu;
		print "</dl>\n";
		&TR_E;
		&TABLE_END;
	} # End if ($guest_book_name !~ m/help/)
	else { # Begin else
		print "<a href=\"javascript:show()\"><font color=\"$color_text_stored\">Quitter l'aide / </font><font color=orange>Leave help</font></a><br>\n";
	}  # End else

	print "";

	if (-f  GUEST_BOOK_DIRECTORY_DEPOSIT . "$gb_name") { # Begin if (-f  GUEST_BOOK_DIRECTORY_DEPOSIT . "$gb_name")
		open(FILE_WHERE_BODY_OF_MESSAGE_STORED, GUEST_BOOK_DIRECTORY_DEPOSIT . "$gb_name") || die("Cannot open ". GUEST_BOOK_DIRECTORY_DEPOSIT."/$gb_name $!");
		$counter = 1;
		$blockNumber = 0;
		$lineStored = "";
		$nb_page = 0;
		$isprivate = "";
		my $private_mess_beg = ();

		while (<FILE_WHERE_BODY_OF_MESSAGE_STORED>) { # Begin while (<FILE_WHERE_BODY_OF_MESSAGE_STORED>)
			chomp($_);
			if (/\<\!\-\-When\:/) { # Begin if (/\<\!\-\-When\:/)
				#                       Case when a session starts
				$private_mess_beg = $_;
				chomp($private_mess_beg);

				if (/End/) { # Begin if (/End/)
					#            Case when a session ends
					if ($counter == ($max_message+1)) { # Begin if ($counter == ($max_message+1))
						$blockNumber++;
						%tab = (%tab,$blockNumber,"$lineStored");
						$lineStored = "";
						$counter = 1;
					}  # End if ($counter == ($max_message+1))
				}  # End if (/End/)
				else { # Begin else
					$counter++;
				}  # End else
			} # End if (/\<\!\-\-When\:/)
			else { # Begin else
				if (/\<\!\-\-privateMessage/ || /\<\!\-\-privateMessageEnd/) { # Begin if (/\<\!\-\-privateMessage/ || /\<\!\-\-privateMessageEnd/)
					if (/privateMessageEnd/) { # Begin if (/privateMessageEnd/)
						$isprivate = "";
					}  # End if (/privateMessageEnd/)
					else { # Begin else
						$isprivate = "ok";
					}  # End else
				}  # End if (/\<\!\-\-privateMessage/ || /\<\!\-\-privateMessageEnd/)
				else { # Begin else
					if ($separator_bar_stored =~ m!hrSPACE!) { # Begin if ($separator_bar_stored =~ m!<hr>!)
						$_ =~ s/\<[\ \n]*img[\n\ ]*src[\n\ ]*\=[\ \n]*\"([^\"\']*)[\ \n]*\"[\ \n]*\>/$1/i;
						$_ =~ s/_\&separator_bar_stored\&_/$separator_bar_stored/g;
						$_ =~ s/EQUAL/\=/g;
						$_ =~ s/SPACE/\ /g;
					}  # End if ($separator_bar_stored =~ m!<hr>!)
					else { # Begin else
						$_ =~ s/_\&separator_bar_stored\&_/$separator_bar_stored/g;
					} # End else
					if ($isprivate eq "") { # Begin if ($isprivate eq "")
						if ($_ =~ m!<pre>!i) { # Begin if ($_ =~ m!<pre>!i)
							$is_pre_tag = 1;
						}  # End if ($_ =~ m!<pre>!i)
						if ($_ =~ m!</pre>!i) { # Begin if ($_ =~ m!</pre>!i)
							$is_pre_tag = 0;
						}  # End if ($_ =~ m!</pre>!i)
						$lineStored = $lineStored . (($is_pre_tag == 1) ? "<br>" : "") . $_ ;
					}  # End if ($isprivate eq "")
					else { # Begin else
						if ($isprivate eq "ok") { # Begin if ($isprivate eq "ok")
							$num_authen_menu++;
							$isprivate = "okDucky";
							$lineStored = $lineStored .
							"<dl>\n<dt onclick='javascript:show();javascript:show(\"manage_guest_book". (7+$num_authen_menu) ."\")'>Message privé / <font color=orange>Private message</font></dt><br>\n<br>\n<br>\n" .
							&prints_authenticate( 7 + $num_authen_menu,$private_mess_beg) . "</dl>";
							$lineStored = $lineStored .
							"<!-- Begin script show private -->\n<script type=\"text/javascript\">\n" .
							"show('private_mess" . ($num_authen_menu + 7+ 20) ."');\n" .
							"</script>\n<!-- End script show private -->\n".
							(
								("$private_message" eq "$private_mess_beg")
								? &gets_string_css_private_message($gb_name,$private_message,($num_authen_menu + 7 + $max_mess_page ))
								: "<!-- nothing was found -->\n"
							);
						}  # End if ($isprivate eq "ok")
					}  # End else
				}  # End else
			} # End else
		}  # End while (<FILE_WHERE_BODY_OF_MESSAGE_STORED>)
		$blockNumber++;
		%tab = (%tab,$blockNumber,"$lineStored");
		$blockNumber++;
		print $tab{$page};
		close(FILE_WHERE_BODY_OF_MESSAGE_STORED) ||  die("Cannot close file $!");
		$countLine = 1;
		print "<table border=0>\n";
		&TR;
		$number_of_pge = 0;
		# Prints list of pages at the bottom of each pages
		if (1 < ( keys(%tab) ) ) { # Begin if (1 < ( keys(%tab) ) )
			foreach $key ( sort numeric (keys(%tab)) ) { # Begin foreach $key ( sort numeric (keys(%tab)) )
				$toWrite = $tab{$key};
				chomp($toWrite);
				if ($toWrite ne "") { # Begin if ($toWrite ne "")
					if (((10*$countLine)/$key) > 1) { # Begin if (((10*$countLine)/$key) > 1)
						&TD;
					}  # End if (((10*$countLine)/$key) > 1)
					else { # Begin else
						$countLine++;
						&TR_E;&TR;&TD;
					}  # End else
					print "<form action=\"login.cgi\" method=post>\n";
					if ($page == $key) { # Begin if ($page == $key)
						print "<input type=button name=\"page\" value=\"|". $key . "|\">\n";
					}  # End if ($page == $key)
					else { # Begin else
						print "<input type=submit name=\"page\" value=\"" . $key . "\">\n";
					} # End else
					print "<input type=hidden name=\"guest_book_name\" value=\"$guest_book_name\">\n";
					print "<input type=hidden name=\"function\" value=\"\">\n";
					print "</form>\n";
				}  # End if ($toWrite ne "")
			}  # End foreach $key ( sort numeric (keys(%tab)) )
		} # End if (1 < ( keys(%tab) ) )
		&TR_E;
		&TABLE_END;
	}  # End if (-f  GUEST_BOOK_DIRECTORY_DEPOSIT . "$gb_name")
	#  print "<br>----------------------<br>Written by <a href=\"mailto:shark.bait\@laposte.net\">shark bait</a></body></html>\n";
}  # End sub show_guest_book


=head1 FUNCTION show_guest_book_help

Prints guest book on the screen.

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

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Aug 1st 2006

- I<Created on:> Jul 31st 2006

=back

=cut

sub show_guest_book_help { # Begin sub show_guest_book_help
	my $is_pre_tag = 0;
	my $num_authen_menu = 0;
	my $gb_name = ( "$guest_book_name" eq  DEFAULT_NAME_FOR_GUEST_BOOK ) ?  DEFAULT_NAME_FOR_GUEST_BOOK : "${guest_book_name}.guest_book.my";
	my $num_of_private_messages = &number_of_private_messages($gb_name);

	if ($guest_book_name !~ m/help/) { # Begin if ($guest_book_name !~ m/help/)
		print "<table width=100% border=0>\n";
		if (&is_file_date_not_over($guest_book_name) == 0) { # Begin if (&is_file_date_not_over($guest_book_name) == 0)
			&TR;
			&TD;
			print "<form action=\"login.cgi\" method=\"post\">\n";
			print "<input type=hidden name=\"guest_book_name\" value=\"$guest_book_name\">\n";
			print "<input type=hidden name=\"function\" value=\"fill\">\n";
			print "<input type=submit value=\"Signer le livre d'or\nSign my guestbook\"><br>\n";
			print "</form>\n";
			&TD_E;
			&TR_E;
		} # End if (&is_file_date_not_over($guest_book_name) == 0)
		&TR;
		&TD;
		print "<form action=\"login.cgi\" method=\"post\">\n";
		print "<input type=hidden name=\"function\" value=\"admin\">\n";
		print "<input type=submit value=\"Autres activités du livre d'or\nOther stuff for guestbook\">\n";
		print "<input type=hidden name=\"guest_book_name\" value=\"$guest_book_name\">\n";
		print "<input type=hidden name=\"old_guest_book_name\" value=\"$guest_book_name\">\n";
		print "</form>\n";
		print "<td align=left><dl><dt onclick='javascript:show();javascript:show(\"manage_guest_book0\")'>Aide <font color=orange>Help</font></dt>";
		&prints_help_for_main_menu;
		print "</dl>\n";
		&TR_E;
		&TABLE_END;
	} # End if ($guest_book_name !~ m/help/)
	else { # Begin else
		print "<a href=\"javascript:show()\">Quitter l'aide <font color=orange>Leave help</font></a><br>\n";
	}  # End else

	print "<br>\n <center>Aide pour la signature du livre d'or / <font color=orange>Help for signing up guest book</font>\n</center>\n<br><br><br>";

	if (-f  GUEST_BOOK_DIRECTORY_DEPOSIT . "$gb_name") { # Begin if (-f  GUEST_BOOK_DIRECTORY_DEPOSIT . "$gb_name")
		open(FILE_WHERE_BODY_OF_MESSAGE_STORED, GUEST_BOOK_DIRECTORY_DEPOSIT . "$gb_name") || die("Cannot open ". GUEST_BOOK_DIRECTORY_DEPOSIT."/$gb_name $!");
		$counter = 1;
		$blockNumber = 0;
		$lineStored = "";
		$nb_page = 0;
		$isprivate = "";
		my $private_mess_beg = ();

		while (<FILE_WHERE_BODY_OF_MESSAGE_STORED>) { # Begin while (<FILE_WHERE_BODY_OF_MESSAGE_STORED>)
			chomp($_);
			if (/\<\!\-\-When\:/) { # Begin if (/\<\!\-\-When\:/)
				#                       Case when a session starts
				$private_mess_beg = $_;
				chomp($private_mess_beg);

				if (/End/) { # Begin if (/End/)
					#            Case when a session ends
					if ($counter == ($max_message+1)) { # Begin if ($counter == ($max_message+1))
						$blockNumber++;
						%tab = (%tab,$blockNumber,"$lineStored");
						$lineStored = "";
						$counter = 1;
					}  # End if ($counter == ($max_message+1))
				}  # End if (/End/)
				else { # Begin else
					$counter++;
				}  # End else
			} # End if (/\<\!\-\-When\:/)
			else { # Begin else
				if (/\<\!\-\-privateMessage/ || /\<\!\-\-privateMessageEnd/) { # Begin if (/\<\!\-\-privateMessage/ || /\<\!\-\-privateMessageEnd/)
					if (/privateMessageEnd/) { # Begin if (/privateMessageEnd/)
						$isprivate = "";
					}  # End if (/privateMessageEnd/)
					else { # Begin else
						$isprivate = "ok";
					}  # End else
				}  # End if (/\<\!\-\-privateMessage/ || /\<\!\-\-privateMessageEnd/)
				else { # Begin else
					if ($separator_bar_stored =~ m!hrSPACE!) { # Begin if ($separator_bar_stored =~ m!<hr>!)
						$_ =~ s/\<[\ \n]*img[\n\ ]*src[\n\ ]*\=[\ \n]*\"([^\"\']*)[\ \n]*\"[\ \n]*\>/$1/i;
						$_ =~ s/_\&separator_bar_stored\&_/$separator_bar_stored/g;
						$_ =~ s/EQUAL/\=/g;
						$_ =~ s/SPACE/\ /g;
					}  # End if ($separator_bar_stored =~ m!<hr>!)
					else { # Begin else
						$_ =~ s/_\&separator_bar_stored\&_/$separator_bar_stored/g;
					} # End else
					if ($isprivate eq "") { # Begin if ($isprivate eq "")
						if ($_ =~ m!<pre>!i) { # Begin if ($_ =~ m!<pre>!i)
							$is_pre_tag = 1;
						}  # End if ($_ =~ m!<pre>!i)
						if ($_ =~ m!</pre>!i) { # Begin if ($_ =~ m!</pre>!i)
							$is_pre_tag = 0;
						}  # End if ($_ =~ m!</pre>!i)
						$lineStored = $lineStored . (($is_pre_tag == 1) ? "<br>" : "") . $_ ;
					}  # End if ($isprivate eq "")
					else { # Begin else
						if ($isprivate eq "ok") { # Begin if ($isprivate eq "ok")
							$num_authen_menu++;
							$isprivate = "okDucky";
							$lineStored = $lineStored .
							"<dl>\n<dt onclick='javascript:show();javascript:show(\"manage_guest_book". (7+$num_authen_menu) ."\")'>Message privé / <font color=orange>Private message</font></dt><br>\n<br>\n<br>\n" .
							&prints_authenticate( 7 + $num_authen_menu,$private_mess_beg) . "</dl>";
							$lineStored = $lineStored .
							"<!-- Begin script show private -->\n<script type=\"text/javascript\">\n" .
							"show('private_mess" . ($num_authen_menu + 7+ 20) ."');\n" .
							"</script>\n<!-- End script show private -->\n".
							(
								("$private_message" eq "$private_mess_beg")
								? &gets_string_css_private_message($gb_name,$private_message,($num_authen_menu + 7 + $max_mess_page ))
								: "<!-- nothing was found -->\n"
							);
						}  # End if ($isprivate eq "ok")
					}  # End else
				}  # End else
			} # End else
		}  # End while (<FILE_WHERE_BODY_OF_MESSAGE_STORED>)
		$blockNumber++;
		%tab = (%tab,$blockNumber,"$lineStored");
		$blockNumber++;
		# -----------------------------------------
		# Prints messages according to page request
		# -----------------------------------------
		$tab{$page} =~ s!(<br>)!\n$1!g;
		$tab{$page} =~ s!<pre>!<p>!g;
		$tab{$page} =~ s!</pre>!</p>!g;
		$tab{$page} =~ s/(.)(If)/$1<br><font color=orange>$2/g;
		$tab{$page} =~ s!necessary.!necessary</font>!g;

		print "<!-- \n========\nBegin of help menu\n=========\n -->\n<table><tr>\n<td align=left valign=top>$tab{$page}</td>\n</tr></table>\n<!-- \n========\nEnd of help menu\n=========\n -->\n";
		close(FILE_WHERE_BODY_OF_MESSAGE_STORED) ||  die("Cannot close file $!");
		$countLine = 1;
		print "<table border=0>\n";
		&TR;
		$number_of_pge = 0;
		# Prints list of pages at the bottom of each pages
		if (1 < ( keys(%tab) ) ) { # Begin if (1 < ( keys(%tab) ) )
			foreach $key ( sort numeric (keys(%tab)) ) { # Begin foreach $key ( sort numeric (keys(%tab)) )
				$toWrite = $tab{$key};
				chomp($toWrite);
				if ($toWrite ne "") { # Begin if ($toWrite ne "")
					if (((10*$countLine)/$key) > 1) { # Begin if (((10*$countLine)/$key) > 1)
						&TD;
					}  # End if (((10*$countLine)/$key) > 1)
					else { # Begin else
						$countLine++;
						&TR_E;&TR;&TD;
					}  # End else
					print "<form action=\"login.cgi\" method=post>\n";
					if ($page == $key) { # Begin if ($page == $key)
						print "<input type=button name=\"page\" value=\"|". $key . "|\">\n";
					}  # End if ($page == $key)
					else { # Begin else
						print "<input type=submit name=\"page\" value=\"" . $key . "\">\n";
					} # End else
					print "<input type=hidden name=\"guest_book_name\" value=\"$guest_book_name\">\n";
					print "<input type=hidden name=\"function\" value=\"\">\n";
					print "</form>\n";
				}  # End if ($toWrite ne "")
			}  # End foreach $key ( sort numeric (keys(%tab)) )
		} # End if (1 < ( keys(%tab) ) )
		&TR_E;
		&TABLE_END;
	}  # End if (-f  GUEST_BOOK_DIRECTORY_DEPOSIT . "$gb_name")
	#  print "<br>----------------------<br>Written by <a href=\"mailto:shark.bait\@laposte.net\">shark bait</a></body></html>\n";
}  # End sub show_guest_book_help


=head1 FUNCTION  gets_string_css_private_message

This function creates script that prints private message.

=head2 PARAMETER(S)

=over 4

$gb_name: That's a given guest book

$private_message: That's the private message

$id: That's id

=back

=head2 RETURNED VALUE

=over 4

String that was generated with private message.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jul 20th 2006

- I<Created on:> Jul 19th 2006

=back

=cut

sub gets_string_css_private_message { # Begin sub gets_string_css_private_message
	my ($gb_name,$private_message,$id) = @_;
	my $s = "<!-- Begin private message -->\n";

	if ( "$login_private_message" eq "toto" ) { # Begin  if ( "$login_private_message" eq "toto" )
		if ("$password_private_message" eq "momo") { # Begin if ("$password_private_message" eq "momo")
			$s = "<dd id=\"private_mess$id\">\n<div id=\"private_message_from_gb$id\">\n<table border=0>\n<tr>\n<td>\n";
			$s .= &gets_private_message($gb_name,$private_message);
			$s .= "</tr>\n</table>\n</div>\n</dd>\n";
		} # End if ("$password_private_message" eq "momo")
		else { # Begin else 
			$s .= "<!-- No private message -->\n";
		} # End else
	} # End  if ( "$login_private_message" eq "toto" )
	else { # Begin else
		$s .= "<!-- No private message -->\n";
	} # End else
	$s .= "<!-- End private message -->\n";

	return $s;
}  # End sub gets_string_css_private_message

=head1 FUNCTION gets_private_message

This function is used to get a private message from a given guest book at a given date.

=head2 PARAMETER(S)

=over 4

$file: a given guest book

$begin: id of the private message.

=back

=head2 RETURNED VALUE

=over 4

String that contains the given private message, of the given guest book at a precise date ($begin).

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jul 22sd 2006

- I<Created on:> Jul 20st 2006

=back

=cut

sub gets_private_message { # Begin sub gets_private_message
	my ($file,$begin) = @_;
	my $private_message = ();
	my $tag_met =0;
	my $tag_private_mess = 0;

	#   print "--X- > [$file] at [$begin]<br>\n";
	open(R, GUEST_BOOK_DIRECTORY_DEPOSIT . "$file") || die("Cannot find ". GUEST_BOOK_DIRECTORY_DEPOSIT ."$file: $!");
	while(<R>) { # Begin while(<R>)
		chomp($_);
		if ($_ =~ m/$begin/i) { # Begin if ($_ =~ m/$begin/i)
			$tag_met++;
		}  # End if ($_ =~ m/$begin/i)
		elsif ($_ =~ m/${begin}End/i) { # Begin elsif ($_ =~ m/${begin}End/i)
			$tag_met = 0;
			close(R) || die("Cannot close $!");
			return $private_message;
		} # End elsif ($_ =~ m/${begin}End/i)
		elsif ($tag_met != 0) { # Begin elsif ($tag_met != 0)
			if ($_ =~ m/privatemessage/i) { # Begin if ($_ =~ m/privatemessage/i)
				$tag_private_mess++;
			} # End if ($_ =~ m/privatemessage/i)
			elsif ($_ =~ m/privatemessageend/i) { # Begin elsif ($_ =~ m/privatemessageend/i)
				$tag_private_mess = 0;
			}  # End elsif ($_ =~ m/privatemessageend/i)
			elsif ( $tag_private_mess != 1) { # Begin elsif ( $tag_private_mess != 1)
				$tag_met = 0;
			} # End elsif ( $tag_private_mess != 1)
			else { # Begin  else
				$private_message = $private_message . $_ . "\n";
			} # End  else
		} # End elsif ($tag_met != 0)
	}  # End while(<R>)
	close(R) || die("Cannot close $!");
	return $private_message;
} # End sub gets_private_message


=head1 FUNCTION prints_authenticate

This function is used to print authentication menu when private message is requested to be seen.

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

String that contains menu.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jul 17th 2006

- I<Created on:> Jul 12sd 2006

=back

=cut

sub prints_authenticate { # Begin sub prints_authenticate
	my ($num_gb_help,$private_mess_beg) = @_;
	$private_mess_beg =~ s/end//gi;

	return 
	"<dd id='manage_guest_book".$num_gb_help."'>\n" .
	"<div id='authenticate'>\n" .
	"<center>\n" .
	"<table border=0>\n" .
	'<form action="login.cgi" name="my_login" method="post">' . "<!-- Begin form message for Login and Password -->\n" .
	"<input type=hidden name=\"guest_book_name\" value=\"$guest_book_name\">\n" .
	"<input type=hidden name=\"page\" value=\"$page\">".
	'<tr>' . "\n" .
	'<td>Login<td><input type="text" name="login_private_message" maxlength="20" size="10">' . "\n" .
	'</tr>' . "\n" .
	'<tr>' . "\n" .
	'<td>Password<td><input type="password" name="password_private_message" maxlength="20" size="10">' . "\n" .
	'</tr>' . "\n" .
	'<tr>' . "\n" .
	'<td>' . "\n" .
	'<td align=center valign=center> <input type="submit" value="Submit" maxlength="20" size="10" >' . "\n" .
	'<input type="hidden" name="message" value="'.$private_mess_beg.'" maxlength="20" size="10" >' . "\n" .
	'</form>' . "<!-- End form message for Login and Password -->\n" .
	'<td align=center valign=center>' . "\n" .
	'<form action="javascript:show()" method="post">' . "<!-- Begin form for Goin back -->\n" .
	'<input type=hidden name="guest_book_name" value="body.my">' . "\n" .
	' <input type="submit" value="Go back" maxlength="20" size="10" >' . "\n" .
	'<input type="hidden" name="function" value="" maxlength="20" size="10" >' . "\n" .
	'</tr>' . "\n" .
	' </form> <!-- End form for Goin back -->' ."\n".
	'</table>' . "\n" .
	'</center>' . "\n" .
	"</div>\n" .
	"</dd>\n";
} # End sub prints_authenticate

=head1 FUNCTION numeric

This function is used to sort numeric information.

=head2 PARAMETER(S)

=over 4

That's a and b.

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

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jun 6th 2003

- I<Created on:> Feb 2003

=back

=cut

sub numeric { # Begin sub numeric
	$a <=> $b;
} # End sub numeric


=head1 FUNCTION  parse_form

Is used to parse url. In the near future status of this function will be unused.

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

=head2 STATUS

=over 4

Deprecated.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jun 6th 2003

- I<Created on:> Feb 2003

=back

=cut

sub parse_form { # Begin sub parse_form
	read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
	if (length($buffer) < 5) { # Begin if (length($buffer) < 5)
		$buffer = $ENV{QUERY_STRING};
	} # End if (length($buffer) < 5)
	@pairs = split(/&/, $buffer);
	foreach $pair (@pairs) { # Begin foreach $pair (@pairs)
		($name, $value) = split(/=/, $pair);	
		$value =~ tr/+/ /;
		$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;	
		$input{$name} = $value;
	}  # End foreach $pair (@pairs)
}  # End sub parse_form


=head1 FUNCTION giveDate

This function is there to create a date when a user enter a message.

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

String that holds date to store later on.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jun 6th 2003

- I<Created on:> Feb 2003

=back

=cut

sub giveDate { # Begin sub giveDate
	use POSIX qw(strftime);
	($sec,$min,$ho,$ye) = (localtime)[0,1,2,5];
	$ye = $ye + 1900;
	$day = (Sun,Mon,Tue,Wed,Thu,Fri,Sat)[(localtime)[6]];
	$nday = strftime "%e", gmtime;
	if ($nday =~ /1$/) { # Begin if ($nday =~ /1$/)
		$nday = $nday . "st";
	}  # End if ($nday =~ /1$/)
	elsif ($nday =~ /2$/) { # Begin elsif ($nday =~ /2$/)
		$nday = $nday . "sd";
	}  # End elsif ($nday =~ /2$/)
	elsif ($nday =~ /3$/) { # elsif ($nday =~ /3$/)
		$nday = $nday . "rd";
	} # elsif ($nday =~ /3$/)
	else { # Begin else
		$nday = $nday . "th";
	}  # End else
	$mo = (Jan,Feb,Mar,Apr,may,Jun,Jul,Aug,sep,Oct,Nov,Dec)[(localtime)[4]];

	$ti = strftime "%a %b %Y", gmtime;
	$ti2 = strftime " %k:%M:%S%p", gmtime;
	$final = "When\: ${ti} ${nday} ${ti2}";
	$final =~ s/AM/am/g;
	$final =~ s/PM/pm/g;
	return $final;
}  # End sub giveDate

=head1 FUNCTION giveLogDate

Gives the date of the log.

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

Returns new string that contains a new date format.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jun 6th 2003

- I<Created on:> Feb 2003

=back

=cut

sub giveLogDate { # Begin sub giveLogDate
	($sec,$min,$ho,$ye) = (localtime)[0,1,2,5];
	$ye = $ye + 1900;
	$day = (Sun,Mon,Tue,Wed,Thu,Fri,Sat)[(localtime)[6]];
	$nday = (localtime)[3];
	if ($nday =~ /1$/) { # Begin if ($nday =~ /1$/)
		$nday = $nday . "st";
	}  # End if ($nday =~ /1$/)
	elsif ($nday =~ /2$/) { # Begin elsif ($nday =~ /2$/)
		$nday = $nday . "sd";
	}  # End elsif ($nday =~ /2$/)
	elsif ($nday =~ /3$/) { # Begin elsif ($nday =~ /3$/)
		$nday = $nday . "rd";
	} # End elsif ($nday =~ /3$/)
	else { # Begin else
		$nday = $nday . "th";
	}  # End else
	$mo = (Jan,Feb,Mar,Apr,may,Jun,Jul,Aug,sep,Oct,Nov,Dec)[(localtime)[4]];
	return "$day $mo, $nday $ye $ho:$min:$sec";
}  # End sub giveLogDate

=head1 FUNCTION TABLE_BEGIN

Prints the tag table.

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

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jun 6th 2003

- I<Created on:> Feb 2003

=back

=cut

sub TABLE_BEGIN { # Begin sub TABLE_BEGIN
	print "<table width=80\% >\n";
} # End sub TABLE_BEGIN


=head1 FUNCTION TR

Print TR tag within table tag.

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

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jun 6th 2003

- I<Created on:> Feb 2003

=back

=cut


sub TR { # Begin sub TR
	print "<tr>\n";
}  # End sub TR

=head1 FUNCTION  TR_E

That's the end for TR tag.

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

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jun 6th 2003

- I<Created on:> Feb 2003

=back

=cut

sub TR_E { # Begin sub TR_E
	print "</tr>\n";
}  # End sub TR_E


=head1 FUNCTION TD

Prints tag TD.

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

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jun 6th 2003

- I<Created on:> Feb 2003

=back

=cut

sub TD { # Begin sub TD
	print "<td>\n";
} # End sub TD


=head1 FUNCTION  TD_E

Prints end for the TD.

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

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jun 6th 2003

- I<Created on:> Feb 2003

=back

=cut

sub TD_E {
	print "</td>\n";
}


=head1 FUNCTION  TABLE_END

Prints end tag table.

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

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jun 6th 2003

- I<Created on:> Feb 2003

=back

=cut

sub TABLE_END { # Begin sub TABLE_END
	print "</table>\n";
}  # End sub TABLE_END


=head1 FUNCTION gets_line_num

Get number of lines per pages.

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

Number of lines per page.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

=back

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jul 23rd 2006

- I<Last modification:> Jun 6th 2003

- I<Created on:> Feb 2003

=back

=cut

sub gets_line_num { # Begin sub gets_line_num
	if (-f  GUEST_BOOK_DIRECTORY_DEPOSIT . "conf.my") { # Begin if (-f  GUEST_BOOK_DIRECTORY_DEPOSIT . "conf.my")
		open(LINE, GUEST_BOOK_DIRECTORY_DEPOSIT . "conf.my") || die("Cannot open ". GUEST_BOOK_DIRECTORY_DEPOSIT ."conf.my");
		@lines = <LINE>;
		close(LINE) ||  die("Cannot close file $!");

		foreach $l (@lines) { # Begin foreach $l (@lines)
			chomp($l);
			$l =~ s/\ //g;
			if ($l =~ /numLine/) { # Begin if ($l =~ /numLine/)
				($var,$numVar) = split(/=/,$l);
				return ($numVar);
			}  # End if ($l =~ /numLine/)
		}  # End foreach $l (@lines)
		return (5);
	} # End if (-f  GUEST_BOOK_DIRECTORY_DEPOSIT . "conf.my")
	return 0;
}  # End sub gets_line_num


=head1 FUNCTION gets_line_colors_stored

Returns line color stored. Default is blue.

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

Returns the color set by administrator or if not blue as default for character color.

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

- I<Last modification:> Jul 23rd 2006

- I<Last modification:> Jun 6th 2003

- I<Created on:> Feb 2003

=back

=cut

sub gets_line_colors_stored { # Begin sub gets_line_colors_stored
	if (-f  GUEST_BOOK_DIRECTORY_DEPOSIT . "conf.my") { # Begin if (-f  GUEST_BOOK_DIRECTORY_DEPOSIT . "conf.my")
		open(LINE, GUEST_BOOK_DIRECTORY_DEPOSIT . "conf.my") || die("Cannot open " . GUEST_BOOK_DIRECTORY_DEPOSIT . "conf.my $!");
		@lines = <LINE>;
		close(LINE) ||  die("Cannot close file $!");

		foreach $l (@lines) { # Begin foreach $l (@lines)
			$l =~ s/\ //g;
			chomp($l);
			if ($l =~ /colorText/) { # Begin if ($l =~ /colorText/)
				($var,$numVar) = split(/=/,$l);
				return ($numVar);
			}  # End if ($l =~ /colorText/)
		} # End foreach $l (@lines)
	} # End if (-f  GUEST_BOOK_DIRECTORY_DEPOSIT . "conf.my")
	return ("Blue");
} # End sub gets_line_colors_stored


=head1 FUNCTION gets_separator_bar

Prints separator bar according to administrator choice.

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

- I<Last modification:> Jul 23rd 2006

- I<Last modification:> Jun 6th 2003

- I<Created on:> Feb 2003

=back

=cut

sub gets_separator_bar { # Begin sub gets_separator_bar
	if (-f GUEST_BOOK_DIRECTORY_DEPOSIT . "conf.my") { # Begin if (-f GUEST_BOOK_DIRECTORY_DEPOSIT . "conf.my")
		open(LINE, GUEST_BOOK_DIRECTORY_DEPOSIT . "conf.my") || die("Cannot open ". GUEST_BOOK_DIRECTORY_DEPOSIT . "conf.my $!");
		@lines = <LINE>;
		close(LINE) ||  die("Cannot close file $!");;

		foreach $l (@lines) { # Begin foreach $l (@lines)
			chomp($l);
			$l =~ s/\ //g;
			if ($l =~ /separator_bar/) { # Begin if ($l =~ /separator_bar/)
				($var,$numVar) = split(/=/,$l);
				return ($numVar);
			}  # End if ($l =~ /separator_bar/)
		}  # End foreach $l (@lines)
	} # End if (-f GUEST_BOOK_DIRECTORY_DEPOSIT . "conf.my")
	return "";
}  # End sub gets_separator_bar


=head1 FUNCTION gets_line_URL_back

Returns URL stored by administrator.

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

Returns either url stored or "" string.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jul 23rd 2006

- I<Last modification:> Jun 6th 2003

- I<Created on:> Feb 2003

=back

=cut

sub gets_line_URL_back { # Begin sub gets_line_URL_back
	if (-f  GUEST_BOOK_DIRECTORY_DEPOSIT . "conf.my") { # Begin  if (-f  GUEST_BOOK_DIRECTORY_DEPOSIT . "conf.my")
		open(LINE, GUEST_BOOK_DIRECTORY_DEPOSIT . "conf.my") || die("Cannot open ".GUEST_BOOK_DIRECTORY_DEPOSIT . "conf.my :$!");
		@lines = <LINE>;
		close(LINE) ||  die("Cannot close file $!");

		foreach $l (@lines) { # Begin foreach $l (@lines)
			chomp($l);
			$l =~ s/\ //g;
			if ($l =~ /backGround/) { # Begin if ($l =~ /backGround/)
				($var,$url) = split(/=/,$l);
				return ($url);
			}  # End if ($l =~ /backGround/)
		}  # End foreach $l (@lines)
	} # End  if (-f  GUEST_BOOK_DIRECTORY_DEPOSIT . "conf.my")
	return "";
}  # End sub gets_line_URL_back


=head1 FUNCTION create_new_guest_book_name

Creates a new guest book if it does not exist.

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

0 if created otherwise -1

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Aug 2sd 2006

- I<Created on:> Jul 2nd 2006

=back

=cut

sub create_new_guest_book_name { # Begin sub create_new_guest_book_name
	my $time = &get_digital_date_format . "TimerDelay$timer$period";

	$time =~ s/\//\:/g;
	${new_Guest_book_name} =~ s/\ /\-\-\-\-/g;
	${new_Guest_book_name} =~ s/\_/MY\-UNDERSCORE\-TAG/g;
	$time =~ s/\ /\-/g;
	if ( ! -f GUEST_BOOK_DIRECTORY_DEPOSIT . "guest_book_list.my") { # Begin if ( ! -f "guest_book_list.my")
		open(NEW_GUEST_BOOK,">". GUEST_BOOK_DIRECTORY_DEPOSIT."guest_book_list.my") || die("Can't create file ". GUEST_BOOK_DIRECTORY_DEPOSIT."guest_book_list.my $!");
		print NEW_GUEST_BOOK "${new_Guest_book_name}_$time\n";
		close(NEW_GUEST_BOOK) ||  die("Cannot close file $!");
		open(NEW_GUEST_BOOK,">". GUEST_BOOK_DIRECTORY_DEPOSIT."${new_Guest_book_name}_$time.guest_book.my") || die("Can't create file ". GUEST_BOOK_DIRECTORY_DEPOSIT."${new_Guest_book_name}_$time.guest_book.my  $!");
		print NEW_GUEST_BOOK "";
		close(NEW_GUEST_BOOK) ||  die("Cannot close file ". GUEST_BOOK_DIRECTORY_DEPOSIT ."${new_Guest_book_name}_$time.guest_book.my $!");

		#print "Content-type: text/html\n\n";
		print "Le fichier ". GUEST_BOOK_DIRECTORY_DEPOSIT ."$new_Guest_book_name a été crée <br>\n<font color=orange>". GUEST_BOOK_DIRECTORY_DEPOSIT."$new_Guest_book_name file created</font><br>\n";
		return 0;
	}  # End if ( ! -f "guest_book_list.my")
	else { # Begin else
		my $already_in = 0;

		if ( $already_in == 0 ) { # Begin if ( $guest_book_name == 0 )
			#                         once check the list of album in the guest_book_list.my file and new entry does not exist
			#                         we create a new entry in the album
			open(NEW_GUEST_BOOK,">>". GUEST_BOOK_DIRECTORY_DEPOSIT."guest_book_list.my") || die("Can't create file ". GUEST_BOOK_DIRECTORY_DEPOSIT."guest_book_list.my $!");
			print NEW_GUEST_BOOK "${new_Guest_book_name}_$time\n";
			close(NEW_GUEST_BOOK) ||  die("Cannot close file $!");

			open(NEW_GUEST_BOOK,">". GUEST_BOOK_DIRECTORY_DEPOSIT."${new_Guest_book_name}_$time.guest_book.my") || die("Can't create file ". GUEST_BOOK_DIRECTORY_DEPOSIT ."${new_Guest_book_name}.guest_book.my  $!");
			print NEW_GUEST_BOOK "";
			close(NEW_GUEST_BOOK) ||  die("Cannot close file $!");

			#print "Content-type: text/html\n\n";
			print "Le fichier $new_Guest_book_name a été crée <br> <font color=orange>$new_Guest_book_name file created</font><br>\n";
		}  # End if ( $guest_book_name == 0 )
		else {  # Begin else
			return -1;
		}  # End else
		return 0;
	}  # End else
} # End sub create_new_guest_book_name


=head1 FUNCTION sub removes_old_guest_book_name

Removes a new guest book if it does exist.

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

0 if removed otherwise -1

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jul 4th 2006

- I<Created on:> Jul 2nd 2006

=back

=cut

sub removes_old_guest_book_name { # Begin sub remove_old_guest_book_name
	open(GUEST_BOOK_LIST, GUEST_BOOK_DIRECTORY_DEPOSIT . "guest_book_list.my") || die("Can't read file ". GUEST_BOOK_DIRECTORY_DEPOSIT."guest_book_list.my $!");
	my @new_list = ();
	my $is_in = 0;

	foreach my $name (<GUEST_BOOK_LIST>) { # Begin foreach my $name (<GUEST_BOOK_LIST>)
		chomp($name);
		if ("$name" ne "$old_Guest_book_name") { # Begin if ("$name" eq "$old_Guest_book_name")
			@new_list = (@new_list,$name);
		} # End if ("$name" eq "$old_Guest_book_name")
	} # End foreach my $name (<GUEST_BOOK_LIST>)
	close(GUEST_BOOK_LIST) ||  die("Cannot close file $!");
	open(GUEST_BOOK_LIST_NEW,">". GUEST_BOOK_DIRECTORY_DEPOSIT ."guest_book_list.my") || die("Can't read file ". GUEST_BOOK_DIRECTORY_DEPOSIT."guest_book_list.my $!");
	foreach my $alb_del (@new_list) {
		chomp($alb_del);
		print GUEST_BOOK_LIST_NEW "$alb_del\n";
	}
	close(GUEST_BOOK_LIST_NEW) ||  die("Cannot close file " . GUEST_BOOK_DIRECTORY_DEPOSIT ."guest_book_list.my $!");
	if (${old_Guest_book_name} =~ m/TRIGGERED/) {
		($old,${old_Guest_book_name}) = split(/TRIGGERED/,${old_Guest_book_name});
	}
	if (-f GUEST_BOOK_DIRECTORY_DEPOSIT . "${old_Guest_book_name}.guest_book.my") { # Begin if (-f GUEST_BOOK_DIRECTORY_DEPOSIT . "${old_Guest_book_name}.guest_book.my")
		unlink( GUEST_BOOK_DIRECTORY_DEPOSIT . "${old_Guest_book_name}.guest_book.my") || die(GUEST_BOOK_DIRECTORY_DEPOSIT . "${old_Guest_book_name}.guest_book.my cannot be removed");
	}  # End if (-f GUEST_BOOK_DIRECTORY_DEPOSIT . "${old_Guest_book_name}.guest_book.my")
	return 0;
}  # End sub remove_old_guest_book_name

=head1 FUNCTION number_of_private_messages

This function returns the number of messages that are private in a given guest book.

=head2 PARAMETER(S)

=over 4

$file_to_open: that's the given guest book

=back

=head2 RETURNED VALUE

=over 4

Returns the number of private messages that are stored in a given guest book.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jul 22sd 2006

- I<Created on:> Jul 22sd 2006

=back

=cut

sub number_of_private_messages { # Begin sub number_of_private_messages
	my ($file_to_open) = @_;
	my $private_message_counter = 0;

	if (-f  GUEST_BOOK_DIRECTORY_DEPOSIT . "$file_to_open") { # Begin if (-f  GUEST_BOOK_DIRECTORY_DEPOSIT . "$file_to_open")
		open(R, GUEST_BOOK_DIRECTORY_DEPOSIT . "$file_to_open") || die("Cannot open ". GUEST_BOOK_DIRECTORY_DEPOSIT ."$file_to_open $!");
		foreach my $line (<R>) { # Begin foreach my $line (<R>)
			chomp($line);
			if ($line =~ m!--privatemessage-->!i) { # Begin if ($line =~ m!--privatemessage-->!i)
				$private_message_counter++;
			} # End if ($line =~ m!--privatemessage-->!i)
		}  # End foreach my $line (<R>)
		close(R) || die("Cannot close ". GUEST_BOOK_DIRECTORY_DEPOSIT."$file_to_open $!");
		return $private_message_counter + 7;
	}  # End if (-f  GUEST_BOOK_DIRECTORY_DEPOSIT . "$file_to_open")
	return 0;
}  # End sub number_of_private_messages




=head1 FUNCTION checks_if_album_exists

This function checks if album exists.

=head2 PARAMETER(S)

=over 4

$file: that's the given guest book

=back

=head2 RETURNED VALUE

=over 4

Returns 0 if given album exists otherwise -1.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jul 22sd 2006

- I<Created on:> Jul 22sd 2006

=back

=cut

sub checks_if_album_exists { # Begin sub checks_if_album_exists
	my ($file) = @_;

	chomp($file);
	if ( GUEST_BOOK_DIRECTORY_DEPOSIT . "$file" eq  GUEST_BOOK_DIRECTORY_DEPOSIT . "body.my") { # Begin if ("$file" eq "body.my")
		return 0;
	} # End if ("$file" eq "body.my")
	elsif (-f  GUEST_BOOK_DIRECTORY_DEPOSIT . "${file}.guest_book.my") { # Begin elsif (-f "$file")
		return 0;
	}  # End elsif (-f "$file")
	return -1;
} # En sub checks_if_album_exists


=head1 FUNCTION creates_Guest_Book_directory

This function creates directory if album does not exists already.
It creastes too, a file conf.my that contains the following information:
					    numLine=5
					    backGround=../images/arcade.jpg
					    separator_bar=../images/bow.gif
					    colorText=Yellow

Within the function 2 other functions are added. One that check images and other that checks packages that are needed to this file (login.cgi).

By the way: another file body.my that contains list of future messages is created.

=head2 PARAMETER(S)

=over 4

$file: that's the given guest book

=back

=head2 RETURNED VALUE

=over 4

Returns 0 if given album exists otherwise -1.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jul 22sd 2006

- I<Created on:> Jul 22sd 2006

=back

=cut

sub creates_Guest_Book_directory { # Begin sub creates_Guest_Book_directory
	if ( ! -d GUEST_BOOK_DIRECTORY_DEPOSIT) { # Begin if ( ! -d GUEST_BOOK_DIRECTORY_DEPOSIT)
		mkdir GUEST_BOOK_DIRECTORY_DEPOSIT , 0755;
		open(W,">".GUEST_BOOK_DIRECTORY_DEPOSIT . "body.my") || die("Cannot create ".GUEST_BOOK_DIRECTORY_DEPOSIT . "body.my $!");
		print W "";
		close(W) || die("Cannot close ".GUEST_BOOK_DIRECTORY_DEPOSIT . "body.my $!");

		open(W,">".GUEST_BOOK_DIRECTORY_DEPOSIT . "conf.my") || die("Cannot create ".GUEST_BOOK_DIRECTORY_DEPOSIT . "conf.my $!");
		print W "numLine=5\n";
		print W "backGround=". IMAGE_DIRECTORY_DEPOSIT ."arcade.jpg\n";
		print W "separator_bar=". IMAGE_DIRECTORY_DEPOSIT ."bow.gif\n";
		print W "colorText=Yellow\n";
		close(W) || die("Cannot close ".GUEST_BOOK_DIRECTORY_DEPOSIT . "conf.my $!");

		io::MyUtilities::checks_file_dependencies("check_files",
			GUEST_BOOK_DIRECTORY_DEPOSIT,
			(
				PACKAGE_DIRECTORY . "MyTime.pm",
				PACKAGE_DIRECTORY . "MyUtilities.pm"
			)
		);
		io::MyUtilities::checks_file_dependencies("check_images",
			GUEST_BOOK_DIRECTORY_DEPOSIT,
			(
				IMAGE_DIRECTORY_DEPOSIT . "my_lovely_pict.gif",
				IMAGE_DIRECTORY_DEPOSIT . "bkg.gif",
				IMAGE_DIRECTORY_DEPOSIT . "arcade.jpg",
				IMAGE_DIRECTORY_DEPOSIT . "bow.gif",
				IMAGE_DIRECTORY_DEPOSIT . "hruler13.gif",
				IMAGE_DIRECTORY_DEPOSIT . "wavy.gif"
			)
		);
		&create_help_file;
	} # End if ( ! -d GUEST_BOOK_DIRECTORY_DEPOSIT)
}  # End sub creates_Guest_Book_directory


=head1 FUNCTION create_help_file

This function creates help file when user want to sign up a guest book

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

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Aug 3rd 2006

- I<Created on:> Aug 3rd 2006

=back

=cut

sub create_help_file { # Begin sub create_help_file
	open(W,">".GUEST_BOOK_DIRECTORY_DEPOSIT . "help.guest_book.my") || die(GUEST_BOOK_DIRECTORY_DEPOSIT . "help.guest_book.my cannot be created");
	print W "<!--When:SatJul200629th3:09:59am-->\n";
	print W "<!--privateMessage-->\n";
	print W "<i><b>This is a private message</b><br></i>\n";
	print W "Posted on Sat Jul 2006 29th   3:09:59am<br>\n";
	print W "<pre>\n";
	print W "Message privé / Private message\n";
	print W "</pre>\n";
	print W "<br>\n";
	print W "<!--privateMessageEnd-->\n";
	print W "<center>\n";
	print W '<img width="90\%" src="_&separator_bar_stored&_">'."\n";
	print W "</center>\n";
	print W "<br>\n";
	print W "<!--When:SatJul200629th3:09:59amEnd-->\n";
	print W "<!--When:SatJul200629th3:09:16am-->\n";
	print W "Posted on Sat Jul 2006 29th   3:09:16am<br>\n";
	print W "<pre>\n";
	print W "Si vous pressez le bouton  [Enregistrer en tant que message privé] apres avoir écrit ce message vous aurez <br>le message ci-dessus d'affiché (Message privé).\n";
	print W "Votre message est privé et est protégé par un mot de passe.\n";
	print W "If you push the button [Submit as pivate message] you will get the upper message printed (Private message).\n";
	print W "Your message is private and to access it a password is necessary.\n";
	print W "</pre>\n";
	print W "<br>\n";
	print W "<center>\n";
	print W '<img width=\"90\%\" src="_&separator_bar_stored&_">'."\n";
	print W "<center>\n";
	print W "<br>\n";
	print W "<!--When:SatJul200629th3:09:16amEnd-->\n";
	print W "<!--When:SatJul200629th3:04:25am-->\n";
	print W "Posted on Sat Jul 2006 29th   3:04:25am<br>\n";
	print W "<pre>\n";
	print W "Si vous pressez le bouton Envoyer/Submit aprés avoir écrit ce message vous aurez ce message d'affiché.\n";
	print W "If you push the button Submit you will get this message printed.\n";
	print W "</pre>\n";
	print W "<center>\n";
	print W '<img width=\"90\%\" src="_&separator_bar_stored&_">'."\n";
	print W "</center>\n";
	print W "<br>\n";
	print W "<!--When:SatJul200629th3:04:25amEnd-->\n";
	close(W)  || die(GUEST_BOOK_DIRECTORY_DEPOSIT . "help.guest_book.my cannot be closed");
} # End sub create_help_file

=head1 FUNCTION sub print_title

This function prints guest book title (user side) according to the file where are stored information.

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

Returns string for the guest book title according to guest book.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Aug 3rd 2006

- I<Created on:> Jul 22sd 2006

=back

=cut

sub print_title { # Begin sub print_title
	my ($title,$date) = split(/\_/,$guest_book_name);

	$title =~ s/MY-UNDERSCORE-TAG/\_/g;
	$title =~ s/----/\ /g;
	if ($title !~ m/^body.my$/i) { # Begin if ($title !~ m/^body.my$/i)
		$date =~ s/([0-9]{2})\:([0-9]{2})\:([1-9][0-9]{3})\-/$1\/$2\/$3  /g;

		if (&is_file_date_not_over($guest_book_name) == 0) { # Begin if (&is_file_date_not_over($guest_book_name) == 0)
			$date =~ s/TimerDelay([0-9]+)/ expirera dans \/ <font color=orange>will expire in <\/font>$1/g;
			$date =~ s/d$/ jour\(s\) \/ <font color=orange>day\(s\)<\/font>/g;
		} # End if (&is_file_date_not_over($guest_book_name) == 0)
		else { # Begin else
			$date =~ s/TimerDelay([0-9]+).*/<br>Livre d\'or fermé <font color=orange>Guest book closed<\/font>/g;
		}  # End else
		return "$title<br>Ouvert le / <font color=orange>Opened on</font> $date";
	} # End if ($title !~ m/^body.my$/i)
	else { # Begin else
		$title =~ s!body.my!!g;
		return "$title<br>";
	} # End else
}  # End sub print_title


=head1 FUNCTION sub prints_help_message_if_signing_up_guest_book

This function prints guest book sign option help.

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

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jul 29th 2006

- I<Created on:> Jul 28th 2006

=back

=cut

sub prints_help_message_if_signing_up_guest_book { # Begin sub prints_help_message_if_signing_up_guest_book
	print "<dd id='manage_guest_book0'>\n";
	print "<div id='fill_action_help_menu'>\n";
	print "<table width=100% border=0>\n<tr>\n<td>\n";
	&show_guest_book_help;
	print "\n</tr></table>\n";
	print "</div>\n";
	print "</dd>\n";
} # End sub prints_help_message_if_signing_up_guest_book


=head1 FUNCTION sub prints_help_for_main_menu

This function prints guest book sign option help.

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

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jul 29th 2006

- I<Created on:> Jul 28th 2006

=back

=cut

sub prints_help_for_main_menu { # Begin sub prints_help_for_main_menu
	print "<dd id='manage_guest_book0'>\n";
	print "<div id='help_main_menu'>\n";
	print "<a href=\"javascript:show()\">Quitter l'aide <font color=orange>Leave help</font></a><br><br><br>\n";
	print "<table border=1 width=100%>\n";
	print "<tr><td align=right width=10% align=center><img width=\"90\%\" src=\"". IMAGE_DIRECTORY_DEPOSIT ."my_lovely_pict.gif\" >\n";
	print "<td align=center>Aide / <font color=orange>Help</font></tr></table><br><br>\n";
	print "<table width=100% border=0>\n";
	#print "<tr><td align=right valign=top>Page d'acceuil:<td align=left valign=top> retour à la page d'accueil du site web.</td></tr>\n";
	print "<tr><td align=right valign=top><font color=orange>Home page:</font><td align=left valign=top> <font color=orange>back to home page.</font></td></tr>\n";
	print "<tr><td align=right valign=top>Signer le livre d'or:<td align=left valign=top> écrire un message dans le livre d'or.</td></tr>\n";
	print "<tr><td align=right valign=top><font color=orange>Sign my guest book:</font><td align=left valign=top> <font color=orange>write a message in the guest book.</font></td></tr>\n";
	print "<tr><td align=right valign=top>Autres activités livre d'or:<td align=left valign=top> c'est le modérateur du livre qui s'occupe de gérer les messages dans le livre d'or.</td></tr>\n";
	print "<tr><td align=right valign=top><font color=orange>Other stuff for guest book:</font><td align=left valign=top> <font color=orange>that's the moderator of the guest book that manage messages within guest book.</font></td></tr>\n";
	print "<tr><td align=right valign=top>Format de la date:<td align=left valign=top>mois/jour/année</tr>\n";
	print "<tr><td align=right valign=top><font color=orange>Date format is:</font><td align=left><font color=orange>month/day/year</font></tr>\n";
	print "<tr><td align=left><br><br>Merci pour être passé.</tr>\n";
	print "<tr><td align=left><font color=orange>Thanks for coming.</font></tr>\n";
	print "\n</table>\n";
	print "</div>\n";
	print "</dd>\n";
}  # End sub prints_help_for_main_menu


=head1 FUNCTION  is_time_over

Function that checks is according to current date, a date that is creation of the guest book file is over.

=head2 PARAMETER(S)

=over 4

$file_name: that's the file name of the guest book. For instance "test----4_08:30:2006-14:00:53TimerDelay42d.guest_book.my".

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

- I<Last modification:> Jul 30th 2006

- I<Created on:> Jul 30th 2006

=back

=cut

sub is_file_date_not_over { # Begin sub is_file_date_not_over
	my ($file_name) = @_;
	my  $local_time = io::gets_formated_date;

	# That's when admin said no limit in time
	if ($file_name =~ /n$/) { # Begin if ($file_name =~ /n$/) 
		return 0;
	}  # End if ($file_name =~ /n$/)
	elsif ($file_name =~ /^body.my$/) { # Begin elsif ($file_name =~ /^body.my$/)
		#    print "case 2<br>\n";
		return 0;
	} # End elsif ($file_name =~ /^body.my$/)
	my ($file_name,$schedule) = split(/\_/,$file_name);
	my ($date,$time) = split(/\-/,$schedule);
	$time =~ s/TimerDelay/ /g;
	my ($time,$lag) = split(/\ /,$time);
	$lag =~ s/[md]$//g;

	my ($month,$day,$year) = split(/\:/,$date);
	#    print "case 3<br>\n";
	$month =~ s/0([0-9])/$1/;
	my $one_date = add_days($year,$month,$day,$lag);
	$one_date =~ s/\ \ /\ $time\ UTC\ /;
	my $l = &are_dates_greater($one_date,$local_time);
	#  print "__${l}__" . ((&are_dates_greater($one_date,$local_time) == 0) ? "ok" : "nok") . "__($one_date,$local_time)";
	return &are_dates_greater($one_date,$local_time);
}  # End sub is_file_date_not_over



=head1 FUNCTION create_translate_time_to_trigger

Function that translates url (name of guest book) to proper file.

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

0 if operation is ok otherwise -1.

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

- I<Last modification:> Aug 4th 2006

- I<Created on:> Aug 3rd 2006

=back

=cut

sub create_translate_time_to_trigger { # Begin sub create_translate_time_to_trigger
	if (-f  GUEST_BOOK_DIRECTORY_DEPOSIT ."guest_book_list.my") { # Begin if (-f  GUEST_BOOK_DIRECTORY_DEPOSIT ."guest_book_list.my")
		my @deposit = ();
		my $changed = 0;

		if ($guest_book_name =~ m/TimerDelay[0-9]+t/) {
			my $file_to_remove = ();
			open(R_GB, GUEST_BOOK_DIRECTORY_DEPOSIT ."guest_book_list.my") || die( GUEST_BOOK_DIRECTORY_DEPOSIT . "guest_book_list.my cannot be found $!");
			foreach my $file_name (<R_GB>) { # Begin foreach my $file_name (<R_GB>)
				chomp($file_name);
				if ($file_name =~ m/$guest_book_name/) { # Begin if ($file_name =~ m/$guest_book_name/)
					if ($file_name !~ m/TRIGGERED/) { # Begin if ($file_name !~ m/TRIGGERED/)
						my $time =  &get_digital_date_format ;
						chomp($time);
						$time =~ s/\//\:/g;
						${new_Guest_book_name} =~ s/\ /\-\-\-\-/g;
						${new_Guest_book_name} =~ s/\_/MY\-UNDERSCORE\-TAG/g;
						$time =~ s/\ /\-/g;
						unlink(GUEST_BOOK_DIRECTORY_DEPOSIT . "${file_name}.guest_book.my") || die("Cannot remove ". GUEST_BOOK_DIRECTORY_DEPOSIT . "${file_name}.guest_book.my $!");
						$changed++;
						$file_name =~ m/([0-9]+)t$/;
						my ($title,$o) = split(/\_/,$file_name);

						my $new_file_name = $title . "_${time}TimerDelay$1" . "d";
						$guest_book_name = "${file_name}TRIGGERED${new_file_name}";
						@deposit = (@deposit,"$guest_book_name");
						#	    print "---> $guest_book_name created<br>";
					} # End if ($file_name !~ m/TRIGGERED/)
					else { # Begin else
						my ($old,$guest_book_name_tmp) = split(/TRIGGERED/,$file_name);
						$guest_book_name = $guest_book_name_tmp;
						#	    print "found ===> $guest_book_name / $file_name<br>\n";
						return 0;
					} # End else
				} # End if ($file_name =~ m/$guest_book_name/)
				else { # Begin else
					@deposit = (@deposit,$file_name);
				} # End else
			}  # End foreach my $file_name (<R_GB>)
			close(R_GB) ||  die("Cannot close file $!");
			if ($changed) { # Begin if ($changed)
				my ($old,$new) = split(/TRIGGERED/,$guest_book_name);
				open(C_GB, ">".GUEST_BOOK_DIRECTORY_DEPOSIT ."$new.guest_book.my") || die("cannot create ". GUEST_BOOK_DIRECTORY_DEPOSIT ."$new.guest_book.my  $!");
				print C_GB "";
				close(C_GB) || die("Cannot close ". GUEST_BOOK_DIRECTORY_DEPOSIT ."$guest_book_name.guest_book.my  $!");
				#	print "Content-type: text/html\n\n";
				open(W_GB,">". GUEST_BOOK_DIRECTORY_DEPOSIT ."guest_book_list.my") || die( GUEST_BOOK_DIRECTORY_DEPOSIT . "guest_book_list.my cannot be found $!");
				foreach my $line (@deposit) { # Begin foreach my $line (@deposit)
					print W_GB "$line\n";
					#	  print "$line<br>\n";
				} # End foreach my $line (@deposit)
				close(W_GB) || die( GUEST_BOOK_DIRECTORY_DEPOSIT . "guest_book_list.my cannot be closed $!");
				#	my ($old,$guest_book_name_tmp) = split(/TRIGGERED/,$file_name);
				$guest_book_name = $new;
				return 0;
			} # End if ($changed)
		} # End if (-f  GUEST_BOOK_DIRECTORY_DEPOSIT ."guest_book_list.my")
	} # End if ($guest_book_name =~ m/TimerDelay[0-9]+t/)
	return -1;
} # Begin sub create_translate_time_to_trigger

=head1 AUTHOR

Current maintainer: M. Flotilla Reindeer, <flotilla.reindeer@laposte.net>

=cut


