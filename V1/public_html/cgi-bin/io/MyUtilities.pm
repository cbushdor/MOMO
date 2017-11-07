package io::MyUtilities;

# +-------------------------------+
# | MyUtilities.pm                |
# | Last update on Oct 1st  2016  |
# | Created     on Oct 13rd 2005  |
# +-------------------------------+

require Exporter;

# @inc=(@inc "packages");

use CGI::Carp qw(fatalsToBrowser); 
#use strict;
use IO::Socket;
#use URI;

# use strict;

my $VERSION    = '1.1.25.24';
$VERSION    = eval $VERSION;
my @ISA    = qw( Exporter );
my @EXPORT = qw(
		finds_directory_where_are_stored_images
		checks_file_dependencies      footer
		gets_private_stuff_for_administrator
		check_password 		   getUrlFromFile
		getsXML getsXMLFromString
		googHead loadFile
		setUrlFile 		   remove_ip
		isEqualedValue
		getsDocVers 		myPing
	    );

use constant MANAGER       => 'landing net';    # manager's name
use constant AUTHOR        => 'flotilla reindeer';    # Author's name
use constant COMPAGNY      => 'shark bait';         # That's for fun
use constant MY_WEBSITE    => 'http://dorey.sebastien.free.fr';    # That's author's url
use constant ROOT_DEPOSIT  => '../'; # To store information

=head1 NAME

io::MyUtilities.pm

$VERSION    = '1.1.25.25'

=head1 ABSTRACT

This packages helps user to have basic functions.

=head2 LIST OF FUNCTIONS

=over 4

check_password 
checks_file_dependencies 
finds_directory_where_are_stored_images 
footer 
getUrlFromFile
gets_private_stuff_for_administrator 
getsXML
getsXMLFromString
googHead
loadFile 
isEqualedValue
remove_ip
setUrlFile

=back

=head2 STATUS

=over 4

In used.

=back

=head2 HISTORY OF MODIFICATIONS

=over 4

- I<Last modification: v1.1.25.25> 20161001 see googHead 

- I<Last modification: v1.1.25.24> 20142230 see setUrlFile

- I<Last modification: v1.1.25.21> 20140206 see footer

- I<Last modification: v1.1.25.13> 20140206 see googHead

- I<Last modification: v1.1.21.0> 20110815 see googHead

- I<Last modification: v1.1.20.0> 20110813 getsXML added
getDocVers changed to getsDocVers

- I<Last modification: v1.1.19.0> Jun 21st see footer

- I<Last modification: v1.1.17.1> see setUrlFile

- I<Last modification: v1.1.17.0> Jan 10th 2011: myPing() added.

- I<Last modification: v1.1.16.15> Oct 5th 2010: modification see getsDocVers()

- I<Last modification: v1.1.16.14> Oct 5th 2010: modification see getsDocVers()

- I<Last modification: v1.1.16.13> Oct 3rd 2010: modification see getsVers() to getsDocVers()

- I<Last modification: v1.1.16.12> Oct 1st 2010: modification see getsVers()

- I<Last modification: v1.1.16.10> Oct 1st 2010: modification see getsVers()

- I<Last modification: v1.1.16.5> Sep 25th 2010: modification see getsVers()

- I<Last modification: v1.1.16.0> Sep 20th 2010: see getsVers()

- I<Last modification: v1.1.15.4> Mar 04th 2010: see setUrlFile()

- I<Last modification: v1.1.10.13> Aug 08th 2009: Shift margin to right.

- I<Last modification: v1.1.1.0> May 23rd 2009: Read modif done at this date.

- I<Last modification: v1.1.0.0> Jun 05th 2008: Read modif done at this date.

- I<Last modification: v1.0.7.1> Mar 03rd 2008: Read modif done at this date.

- I<Last modification: v1.0.6.6> Sep 3rd 2006: Read modif done at this date.

- I<Last modification: v1.0.0.0.5)> Jul 25th 2006; Read modif done at this date.

- I<Last modification: v1.0.0.0> Jul 25th 2006: Read modif done at this date.

=back

=head2 WATCHOUT

=over 4

Some dates does not match right with the given date below. This is just because dates above correspond to the creation of the package and the dates within other functions were copied from other program that was written by current maintainer.

=back

=cut

=head1 sub  finds_directory_where_are_stored_images(...)

This function returns the path where are stored images.

=head2 PARAMETER(S)

=over 4

=over 4

None.

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

Returns directory path from a predefined list. If the predefined path does not exist then a path s.a ../images/ is given. The previous path is created if not found.

=back

=back

=head2 ERRROR RETURNED

=over 4

=over 4

None.

=back

=back

=head2 BUG KNOWN

=over 4

=over 4

None.

=back

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

=over 4

- I<Last modification:> Jul 25th 2006

- I<Last modification:> Jan 04 2006

- I<Created on:> Jan 04 2006

=back

=back

=cut

sub finds_directory_where_are_stored_images {  # begin sub finds_directory_where_are_stored_images
	#my $directory_where_are_stored_imagess=ROOT_DESPOSIT;

	if ( -d "../img/" ) {             # begin if (-d "../img/")
		return ROOT_DEPOSIT . "img/";
	}    # End if (-d "../img/")
	elsif ( -d "../image/" ) {    # begin elsif (-d "../image")
		return ROOT_DEPOSIT . "image/";
	}    # End elsif (-d "../image")
	elsif ( -d "../images/" ) {    # begin elsif (-d "../images")
		return ROOT_DEPOSIT . "images/";
	}    # End elsif (-d "../images")
	elsif ( -d "../Image/" ) {    # begin elsif (-d "../Image")
		return ROOT_DEPOSIT . "image/";
	}    # End elsif (-d "../Image")
	elsif ( -d "../IMAGE/" ) {    # begin elsif (-d "../IMAGE")
		return ROOT_DEPOSIT . "IMAGE/";
	}    # End elsif (-d "../IMAGE")
	elsif ( -d "../IMAGES" ) {    # begin elsif (-d "../IMAGES")
		return ROOT_DEPOSIT . "IMAGES/";
	}    # End elsif (-d "../IMAGES")
	elsif ( -d "../Image" ) {    # begin elsif (-d "../Image")
		return ROOT_DEPOSIT . "Image/";
	}    # End elsif (-d "../Image")
	elsif ( -d "../Images" ) {    # begin elsif (-d "../Images")
		return ROOT_DEPOSIT . "Images/";
	}    # End elsif (-d "../Images")
	else {    # begin else
		# That's the case where no directory was found under the above names.
		# Case where directory does not exist. we create a directory where all images will be stored.
		# &error_raised("can't find a directory to store images");

		mkdir( ROOT_DEPOSIT . "images/", 0755 );
		return ROOT_DEPOSIT . "images/";
	}    # End else
} # End sub finds_directory_where_are_stored_images

=head1 sub checks_file_dependencies(...)

This function checks if all necessary files are stored in a given path. If everything is fine, then it creates a file specfied by parameter $file of this function in a path specified by the parameter $application_name.  Hence it puts the list of all files that are missing or not. If everything is fine, then this file is changed with the same name and the extension ok is added. Hence this test is not performed any more till the file with the extension ok is not removed.

=head2 PARAMETER(S)

=over 4

$file: this is where the application name is.

$application_name: that's application name

@file_dependencies: file are stored there.

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

- I<Last modification:> Jul 25 2006

- I<Created on:> Feb 17 2006

=back

=cut

sub checks_file_dependencies {    # begin sub checks_file_dependencies
	my ($file,$application,@file_dependencies) = @_;

	if (!-f "$application/$file.ok") { # begin if (-f "$application/check_file.ok")
		my $error = 0;
		my @files = ();

		open(W,">$application/$file") || die("$application/check_file cannot be created");
		foreach (@file_dependencies) { # begin foreach (@file_dependencies)
			if (! -f  "$_") { # begin if (! -f PACKAGE_DIRECTORY . "MyUtilities.pm")
				@files = (@files,$_);
				$error++;
				print W "$_ nok\n";
			}  # End if (! -f PACKAGE_DIRECTORY . "MyUtilities.pm")
			else { # begin else
				print W "$_ ok\n";
			} # End else
		}# End foreach (@file_dependencies)
		close(W) || die("Cannot close $application/check_file");
		if ($error != 0) { # begin if ($error != 0)
			print "Content-type: text/html\n\n";
			print "<body bkground=black>\n";
			foreach (@files) { # begin foreach (@files)
				print  "$_ not found<br>" ;
			} # End foreach (@files)
			exit;
		} # End if ($error != 0)
		open(W,">$application/$file.ok") || die("$application/check_file.ok cannot be created");
		open(R,"$application/$file") || die("$application/check_file cannot be read");
		foreach (<R>) { # begin foreach (<R>)
			chomp($_);
			print W "$_\n";
		}  # End foreach (<R>)
		close(R) || die("$application/$file cannot be closed");
		close(W) || die("$application/$file.ok cannot be closed");
		unlink("$application/$file") || die("$application/$file cannot be unlinked");
	} # End if (-f "$application/check_file.ok")
}    # End sub checks_file_dependencies

=head1 sub footer(...)

This function standardizes footer within menus.

=head2 PARAMETER(S)

=over 4

$doc: that's object new CGI

$image_used: That's the image name

$link_with_image: that's link that is ude with image.

$version: that's version of the script.

$browsers: that's browser's name that were tested.

$hosted_url: url of the hoster

$hosted_by: hoster name

=back

=head2 RETURNED VALUE

=over 4

New footer string.

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

- I<Last modification:> Feb 20 2014. field html validator removed.

- I<Last modification:> Jun 21 2011. bug add two last args about url

- I<Last modification:> Aug 08 2009. Shift margin to right.

- I<Last modification:> Aug 5th 2006

- I<Last modification:> Jan 27th 2006

- I<Created on:> Jan 27th 2006

=back

=cut

sub footer {    # begin sub footer
  my ($doc,$image_used,$image_encryption,$link_with_image,$version,$browsers
  ,$hosted_url
  ,$hosted_by
  ) = @_;
  # Checks footer url
  my $chkf= <<CHECK;
  <script>
  	var murl="https://validator.w3.org/check?uri=";
	document.write("<a href='"+murl+encodeURI(document.URL)+"'>Syntax validator</a>");
  </script>
CHECK
  return 
    "	<div id=\"my_footer\">\n".
    "<!-- <script>document.write('hello');</script> -->\n".
      $doc->table(
		  {
		   -class => "footer",
		   -border => "0",
		   -width => '100%'
		  }, "\n" .
		  $doc->Tr("\n".
			   $doc->td(
				    {
				     -align  => 'left',
				     -valign => 'top'
				    },
				    "\n<i><u id='pr'>R</u>esponzible f<u id='po'>o</u>r the <u id='pp'>P</u>roj<u id='pe'>e</u>ct</i>"
				    . "\n" . $doc->a(
					      {
					       -href =>
					       'mailto:esse.dho@laposte.net?subject=Album of pictures'
					      },
					      MANAGER
					     )
				    . 
				    "; Designed by "
				    . $doc->a(
					      {
					       -href =>
					       'mailto:shark.bait@laposte.net?subject=Album of pictures'
					      },
					      COMPAGNY
					     )
				    . "; Written by "
				    . $doc->a(
					      {
					       -href =>
					       'mailto:flotilla.reindeer@laposte.net?subject=Album of pictures'
					      },
					      AUTHOR
					     )
				    . $doc->br
				    . "<font class=\"footer\">Script version "
				    . $version . $doc->br
				    #. "Tested with browsers: "
				    #. $browsers . "."
				    . "</font>\n<br />" 
				    #. "<script>document.write('<a href=\"https://validator.w3.org/check?uri=');</script>\n"
				    . "$chkf\n" .
					"\n"
				   ),"\n".
			   $doc->td(
				    {
				     -align  => 'right',
				     -valign => 'bottom'
				    }, "\n".
					    $doc->img( { -border => 0,
								-alt => "",
					    -src => $image_encryption } )
				    . "\n"
				    ),"\n"
				   .
			   $doc->td(
				    {
				     -align  => 'right',
				     -valign => 'bottom'
				    }, "\n".
				    $doc->a(
					    { 
					    -href => $link_with_image 
					    } ,"\n" . $doc->img( { 
					    			-border => 0,
								-alt => "",
								-src => $image_used } )
					   )
				    . $doc->br
				    . "\nHosted by "
				    . $doc->a(
					      { 
					      -href => $hosted_by }, $hosted_url
					     )
				    . "\n")
			  . "\n")
			  . "\n"
		 ) .
	   "\n";
}    # End sub footer

=head1 sub gets_private_stuff_for_administrator(...)

This function gets info related to administrator to be identified.

=head2 PARAMETER(S)

=over 4

$an_action: action that was asked by user

$private_info_directory: that's a constant that admin set to store login and password.

$my_param_login: login

$my_param_password: password

=back

=head2 RETURNED VALUE

=over 4

Returns $login, and $passwd values.

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

- I<Last modification:> Sep 2sd 2006

- I<Last modification:> Feb 16 2006

- I<Last modification:> Jan 04 2006

- I<Created on:> Jan 04 2006

=back

=cut

sub gets_private_stuff_for_administrator {    # begin sub gets_private_stuff_for_administrator
	my ($an_action,$private_info_directory,$my_param_login,$my_param_password) = @_;
	my ( $login, $passwd ) = ();

	if ( $an_action ne "record_modify" ) {    # begin if ($an_action ne "record_modify")
		if ( -f "$private_info_directory/pswd.txt" ) {    # begin if (-f "private/pswd.txt")
			open( R, "$private_info_directory/pswd.txt" )
			|| die( "Cannot find file "
			    . $private_info_directory
			    . "/pswd.txt $!\n" );
			my @p = <R>;
			chomp( $p[0] );
			chomp( $p[1] );
			$login  = $p[0];
			$passwd = $p[1];
			close(R);
			chomp($login);
			chomp($passwd);

			if ( $login eq "" || $passwd eq "" ) {
				$login  = $my_param_login;
				$passwd = $my_param_password;
				open( W, ">$private_info_directory/pswd.txt" )
					|| die( "Cannot find file "
					      . $private_info_directory
					      . "/pswd.txt when being created $!\n" );
				print W "$login\n";
				print W "$passwd\n";
				close(W);
			}
		}    # End if (-f "private/pswd.txt")
		else {    # begin else
			if ( !-d "$private_info_directory" ) {     # begin if (!-d "$album_directory")
				mkdir( "$private_info_directory", 0700 )
					|| die("Cannot create $private_info_directory\n");
			}    # End if (!-d "$album_directory")
			open( W, ">$private_info_directory/pswd.txt" )
			|| die( "Cannot find file "
				  . $private_info_directory
				  . "/pswd.txt when being created $!\n" );
			print W "\n";
			print W "\n";
			close(W);
		} # End else
	} # End if ($an_action ne "record_modify")
	return ( $login, $passwd );
} # End sub gets_private_stuff_for_administrator

=head1 sub check_password(...)

This function checks password for admin.

=head2 PARAMETER(S)

=over 4

$my_pid: previous pid gotten from parameters.

$service_from_param: service gotten from parameter

$service_value: according to a given service do actions.

$prev_pid_from_param: 

$user_login: login given by the user by the interface.

$login: login used to acces admin menu.

$user_password: password given by the user by the interface.

$password: password used to acces admin menu.

$doc: that's the objet CGI.

$album_pid_file: that's the album file name where is stored pid. Very usefull it is used to check if previous session was not hacked.

=back

=head2 RETURNED VALUE

=over 4

0 if ok otherwise -1.

=back

=head2 ERRROR RETURNED

=over 4

-1 is returned and means that a problem occured.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Sep 3rd 2006

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back

=cut

# work to do creates parameters according to variables within function below.

sub check_password {    # begin sub check_password
	my ($my_pid,
	$service_from_param,
	$service_value,
	$prev_pid_from_param,
	$user_login,
	$login,
	$user_password,
	$password,
	$doc,
	$album_pid_file)=@_;

	if ( "$service_from_param" eq "$service_value" ) { # begin if ( "$service_from_param" eq "$service_value" )
		#print "ok 1<br>";
		if ( "$prev_pid_from_param" eq "" ) { # begin if ( $doc->param('prev_pid_from_param') eq "")
			#print "ok 2 ---|$user_login---$login<<<<<br>";
			if ( "$user_login" eq "$login" ) { # begin if ( "$user_login" eq "$login" )
				#print "ok 3<br>";
				if ( "$user_password" eq "$password" ) { # begin if ("$user_password" eq "$password")
					#print "ok 4<br>";
					open( PID, ">$album_pid_file" ) || die("Can't create $album_pid_file: $!");
					print PID $$;
					close(PID);
					return 0;
				} # End if ("$user_password" eq "$password")
				#print "ok 3bis<br>";
			} # End if ($user_login eq "$login")
			#print "ok 2bis<br>";
		} # End if ( $doc->param('prev_pid_from_param') eq "")
		else { # begin else
			#print "ok 1bis<br>";
			open( OLD_PID, "$album_pid_file" ) || die("Can't open $album_pid_file: $!");
			my $pid;
			foreach (<OLD_PID>) { # begin foreach (<OLD_PID>)
				#print "pid list $_<br>\n";
				chomp($_);
				$pid .= $_;
			} # End foreach (<OLD_PID>)
			close(OLD_PID);

			if ( $my_pid != $pid ) { # begin if ($my_pid != $pid)
				#print "bad<br>";
				return -1;
			} # End if ($my_pid != $pid)
			open( PID, ">$album_pid_file" ) || die("Can't create $album_pid_file: $!");
			print PID $$;
			close(PID);
			return 0;
		} # End else
	} # End if ( "$service_from_param" eq "$service_value" )
	else {    # begin else
		#print "$service_from_param eq $service_value aaaaaaaaa<br>";
	} # End else
	#print "BAD<br>";
	return -1;
} # End sub check_password



=head1 sub getUrlFromFile(...)

This function creates url list file in album direcory (within cgi-bin dir). returns the list of urls allowed.

=head2 PARAMETER(S)

=over 4

none.

=back

=head2 RETURNED VALUE

=over 4

list url separated by comas.

=back

=head2 ERRROR RETURNED

=over 4

none.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Created on:> Jun 05 2008

- I<Created on:> Mar 03 2008

=back

=cut

sub getUrlFromFile{
	my $urls="127.0.0.1,";
	my $f="urls";
	my $locdep="album";

	if(!-f "$locdep/$f") { mkdir($locdep); open(URL,">$locdep/$f"); print URL "$urls"; close(URL); }
	else { open(URL,"$locdep/$f"); $urls=<URL>; close(URL); }
#print "oooooooooooo>$urls(rrrrrrrrr<br>";
	return $urls; 
}

=head1 sub remove_ip(...)

This function removesz from url list an IP address given. (NOT USED YET)

=head2 PARAMETER(S)

=over 4

$rem address to remove

@oth list of IP addresses

=back

=head2 RETURNED VALUE

=over 4

None

=back

=head2 ERRROR RETURNED

=over 4

none.

=back

=head2 BUG KNOWN

=over 4

Stuck when removing an IP address.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Modified on:> Jun 09 2008

- I<Created on:> Jun 03 2008

=back

=cut

sub remove_ip{ # begin sub remove_ip
	my ($rem,@oth)=@_;
	my $f="urls";
	my $locdep="album";

#	open(URL,">$locdep/$f") || die("$locdep/$f $!");
	foreach my $i (@oth){ # begin foreach my $i (@oth)
		chomp($i);
#		if($rem!~/$i/){ print URL "$i,"; }
		if($rem!~/$i/){ print "+++>ok $i<br>\n"; }
		else { print "===>to be removed $i<br>\n"; }
	} # End foreach my $i (@oth)
#	close(URL) || die("$locdep/$f $!");
	return 0;
} # end sub remove_ip

=head1 sub setUrlFile(...)

This function creates url list file in album direcory (within cgi-bin dir).

=head2 PARAMETER(S)

=over 4

$p : that's the IP address

$f : that's the file where to store info

$locdep: path

=back

=head2 RETURNED VALUE

=over 4

None

=back

=head2 ERRROR RETURNED

=over 4

none.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification on:> Dec 30 2014: removed dead code

- I<Last modification on:> Feb 18 2011: removes lock

- I<Last modification on:> Mar 04 2010: adds lock

- I<Created on:> Jun 01 2008

=back

=cut

sub setUrlFile{ # begin setUrlFile
	my ($p,$f,$locdep)=@_;#$p:line,$f:file where to store;path
	my $d=();

#	print "Content-type: txt/html\n\n";
	chomp($p);
	if( !-d "$locdep"){# begin if( !-d "$locdep")
		print "$locdep does not exist<br>";
		for (split(/\//,$locdep)){# begin for (split(/\//,$locdep))
			$d.=$_;
			if( !-d "$d"){# begin if( !-d "$d")
				mkdir("$d");
			}# end if( !-d "$d")
			$d.="/";	
		}# end for (split(/\//,$locdep))
	}# end if( !-d "$locdep")
	else{# begin else
		open(URL,">>$locdep/maop-$f") or die("$locdep/maop-$f");
		print URL "$p," ;
		close(URL); 
	}# end else
} # End setUrlFile


=head1 sub isEqualedValue(...)

Looks if values are equal.

=head2 PARAMETER(S)

=over 4

$v1=value 1

$v2=value 2

=back

=head2 RETURNED VALUE

=over 4

result of == operation.

=back

=head2 ERRROR RETURNED

=over 4

none.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Modified on:> May 03 2009

- I<Created on:> May 03 2009

=back

=cut

sub isEqualedValue{ # begin sub isEqualedValue
	my ($v1,$v2)=@_;
	return ($v1==$v2);
} # end sub isEqualedValue

=head1 sub getsDocVers(...)

Makes html file for the verstion number of main file.

=head2 PARAMETER(S)

=over 4

$orpath original path with file

$vpath destination path with file 

$version version

=back

=head2 RETURNED VALUE

=over 4

none

=back

=head2 ERRROR RETURNED

=over 4

none.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Modified on:1.1.20.0> Aug 14th 2011 name changed from getDocVers to getsDocVers

- I<Modified on:1.1.16.13> Oct 5th 2010 modification

- I<Modified on:1.1.16.12> Oct 1st 2010 modification

- I<Modified on:1.1.16.10> Oct 1st 2010 modification date for document ._.html 

- I<Modified on:1.1.16.5> Sep 25 2010 modification

- I<Created on: 1.1.16.0> Sep 20 2010 creation

=back

=cut

sub getsDocVers{# Begin sub getsDocVers
	my ($orpath,$version)=@_;

	open(R,"${orpath}");
	@ooo=<R>;
	close(R);
	$oo=join(/\n/,@ooo);
	@oob=split(/=head2 HISTORY OF MODIFICATIONS/,$oo);
	@z=split(/=over 4/,$oob[1]);
	$oo=join(/\n/,$z[1]);
	@z=split(/=back/,$oo);
	$oo=join(/\n/,$z[0]);
	$oo=~s/I<Last modification:\ *(v[0-9]{1,9}.[0-9]{1,9}.[0-9]{1,9}.[0-9]{1,9})([^\ >]*)> /$1<font color=white><b>$2<\/b><\/font>|/g;
	$oo=~s/\n/<br>/g;
	return "$oo<br>\n";
}# End sub getsDocVers

=head1 sub myPing(...)

That's a ping.

=head2 PARAMETER(S)

=over 4

$emp: address IP 

=back

=head2 RETURNED VALUE

=over 4

none

=back

=head2 ERRROR RETURNED

=over 4

if there is an error with the connexion it will be told.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Modified on:1.1.16.13> Oct 5th 2010 modification

=back

=cut

sub myPing{ # begin sub myPing
	my ($emp)=@_;# IP address
	my $u1 = URI->new("$emp"); 
	my $ho=$u1->host();
	my $po=$u1->port();
	my $pa=$u1->path();

	print "$ho $po $pa\n";

	my $socket=new IO::Socket::INET(PeerAddr => $ho,
					PeerPort => $po,
					Proto => 'tcp') or 
					die "impossible connexion";

	$socket->autoflush(1);

	print $socket "GET $pa HTTP/1.1\n",
			"Host: $ho\n\n";
	print while (<$socket>);
	$socket->close();
} # end sub myPing


=head1 sub getsXML(...)

From an XML file stored returns its correcponding associative array.

=head2 PARAMETER(S)

=over 4

$dir:  path to file (inclueded).

=back

=head2 RETURNED VALUE

=over 4

Associative array.

=back

=head2 ERRROR RETURNED

=over 4

none.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Modified on:1.1.20.0> Aug 13rd 2011

=back

=cut

sub getsXML{ # begin sub getsXML
	my ($dir)=@_;# that's the path to the file (inclueded)
	my %dta=();# data stored:
	my $lin=0;# line number

	open(R,"$dir") || die("error open $!");# open file
	my @a=<R>;# store the file
	close(R) || die("error close $!");# close file
	my $o=$a[0];# get file content

	while($o=~m{(\<[^\<\>]*\>)([^\<\>]*)}g){ # begin while($o=~m{(\<[^\<\>]*\>)([^\<\>]*)}g)
		my $f=$1; # field content between open and close braquet

		if($1=~m{(\<\/[^\<\>]*\>)}){
		# begin if($1=~m{(\<\/[^\<\>]*\>)})
			$lin++;
			$dta{"$lin-$f"}=$2;
		} # end if($1=~m{(\<\/[^\<\>]*\>)})
		else{ # begin else
			$lin++;
			$dta{"$lin-$f"}=$2;
		} # end else
	} # end while($o=~m{(\<[^\<\>]*\>)([^\<\>]*)}g)

	my @r=sort { $a <=> $b ; } keys %dta;
	return @r;
} # end sub getsXML

=head1 sub getsXMLFromString(...)

From an XML stored in a string returns its correcponding associative array.

=head2 PARAMETER(S)

=over 4

$o: that's the string that contains xml

=back

=head2 RETURNED VALUE

=over 4

Associative array.

=back

=head2 ERRROR RETURNED

=over 4

none.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Modified on:1.1.20.0> Aug 13rd 2011

=back

=cut

sub getsXMLFromString{ # begin sub getsXML
	my ($o)=@_;# that's the string that contains xml
	my %dta=();# data stored:
	my $lin=0;# line number

	while($o=~m{(\<[^\<\>]*\>)([^\<\>]*)}g){ # begin while($o=~m{(\<[^\<\>]*\>)([^\<\>]*)}g)
		my $f=$1; # field content between open and close braquet

		if($1=~m{(\<\/[^\<\>]*\>)}){
		# begin if($1=~m{(\<\/[^\<\>]*\>)})
			$lin++;
			$dta{"$lin-$f"}=$2;
		} # end if($1=~m{(\<\/[^\<\>]*\>)})
		else{ # begin else
			$lin++;
			$dta{"$lin-$f"}=$2;
		} # end else
	} # end while($o=~m{(\<[^\<\>]*\>)([^\<\>]*)}g)

	my @r=sort { $a <=> $b ; } keys %dta;
	return @r;
} # end sub getsXML


=head1 sub googHead

Header for google stuff.

=head2 PARAMETER(S)

=over 4

$idgoog: identifier to allow using googlemap stuff

=back

=head2 RETURNED VALUE

=over 4

String that contains google id.

=back

=head2 ERRROR RETURNED

=over 4

none.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Modified on:1.1.25.14> Oct 1st 2016
added $ilws parameter which tells if it is local website or not

- I<Modified on:1.1.25.13> Feb 6th 2014
added the param $gmv

- I<Modified on:1.1.21.0> Jan 14th 2014

- I<Modified on:1.1.21.0> Aug 15th 2011

=back

=cut

sub googHead{ # begin sub googHead
	my ($idgoog,$gmv,$ilws)=@_; # $idgoog: $idgoog: Google id for one page, $gmv: google map version used,$ilws: is local web site (thats for tests)
	my $r=();# that's for the header

	#print "parameters ($idgoog,\n$gmv)\n<br>";
	if($gmv == 3){
		if($ilws==1){ # Begin if($ilws==1)
			# Distant website case
			$r=<<R;
			<script type="text/javascript"
				src="https://maps.googleapis.com/maps/api/js?sensor=true">
			</script>
R
		} # End if($ilws==1)
		else{ # Begin else
			# Local website case
			$r=<<R;
			<script type="text/javascript"
				src="https://maps.googleapis.com/maps/api/js?sensor=false">
			</script>
R
		} # End else
#		<script type="text/javascript"
#		      src="https://maps.googleapis.com/maps/api/js?key=${idgoog}&sensor=false">
#		</script>
	} else {
		$r=<<R;
			<script src="http://maps.google.com/maps?file=api&amp;v=2&amp;sensor=false&amp;key=${idgoog}" type="text/javascript"></script>
R
	}
	return $r;
} # end sub googHead

=head1 sub googHead

Loads a file.

=head2 PARAMETER(S)

=over 4

$fn: that's the file to load

=back

=head2 RETURNED VALUE

=over 4

String that contains the file.

=back

=head2 ERRROR RETURNED

=over 4

none.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Modified on:1.1.21.0> Aug 15th 2011

=back

=cut

sub loadFile{# begin loadFile
	my ($fn)=@_; # File name

	open(R,"$fn");
	my @r=<R>;# fle content
	close(R);
	return join("",@r);
}# end loadFile

1;


=head1 SEE ALSO

=cut

=head1 AUTHOR

Current maintainer: M. Flotilla Reindeer, <flotilla.reindeer@laposte.net>

=cut

