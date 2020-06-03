# #!/opt/local/bin/perl

package io::MyConstantBase;

use Sys::Hostname;
use Socket;

# ------------------------------------------------------
q##//q#
* Created By : sdo
* File Name : MyConstantBase.pm
* Creation Date : Sun Aug 19 22:51:08 2018
* @modify date 2020-06-02 23:46:48
* Email Address : sdo@linux.home
* Version : 0.0.5.12
* License:
*       Permission is granted to copy, distribute, and/or modify this document under the terms of the Creative Commons Attribution-NonCommercial 3.0
*       Unported License, which is available at http: //creativecommons.org/licenses/by- nc/3.0/.
* Purpose : Accessing constants from another package/file. - PERL Miscellaneous
#;
# ------------------------------------------------------

use strict;
use warnings;
use CGI;
use io::MyUtilities;

use vars qw($mip);
use Exporter qw(import);

our @EXPORT = qw( do_untaint );

# $mip variable declared in the main package

my $mycgi=CGI->new;
our $toto="testing";
my $privateToto="testing";

use constant MANAGER       => sub { 'landing net'; };   # manager's name
use constant AUTHOR        => sub { 'flotilla reindeer'; };   # Author's name
use constant COMPAGNY      => sub { 'shark bait'; };         # That's for fun
use constant ROOT_DEPOSIT  => sub { '../'; }; # To store information

use constant AMOUNT_OF_INFO_TO_READ => sub { ( 2096 * 7 ); }; # That's the amount bite read each time src files read (slot)

#use constant MY_WEBSITE    => sub { 'http://dorey.sebastien.free.fr'; }    # That's author's url

#  album.cgi's file to modify
#  my $album_directory="album";
#  my $configuration_file="conf.file";
#  my $url_demo="http://storm.prohosting.com/dorey/cgi-bin/${main_prog}";

use constant LOCAL_HOSTS_FILE => "/etc/hosts"; # For security issur where to check hosts files
use constant PROTO_USED => sub { ($mycgi->https()=~m/on/) ? "https://" : "http"; } ;
use constant LOCAL_HOSTED_BY_URL => sub { inet_ntoa((gethostbyname(hostname))[4]) ; }; # That's the local url/ip address to reach website
use constant DISTANT_HOSTED_BY_URL => sub { "dorseb.hopto.org"; }; # That's the local url/ip address to reach website
use constant WEB_ACCOUNT => sub { '/~sdo/'; }; # Account where to access website 
use constant HOSTED_BY_URL => sub{ PROTO_USED->() . DISTANT_HOSTED_BY_URL->(). WEB_ACCOUNT->(); }; # That's the url of host name
use constant HOSTED_BY => sub{  "hopto.org";  }; # That's the host name
use constant CHECK_PID_SESSION => sub{ 'album/pid'; }; # Checks previous pid to garanty the session
use constant MAP_VER_IN_USE => sub { "3-0"; }; # Version of the map in use
use constant MAP_PROG => sub { "g3ogle.cgi"; };
use constant EADM => sub{ 'dorey.sebastien@free.fr'; }; # Email 

# We define a boolean value OK=0
use constant OK  => sub{ 0; };
use constant NOK => sub{ ! OK ->(); };

# Where pictures are going to be when upload action is done
use constant DIRECTORY_DEPOSIT 		=> sub{ &io::MyUtilities::finds_directory_where_are_stored_images() };
use constant TRIP_NAME           	=> sub{ "trips"; }; # Album trips
use constant TESTED_WITH_BROWSERS    	=> sub{ 'Firefox V27.0.1,Safari V5.1.7,Opera V11.64'; };  # That's browsers tested
use constant MAX_PAGE_PER_LINE_INDEX 	=> sub{ 20; };  # That's max of page in browser that shows up on one line.
use constant MAX_COL_NUMBER 		=> sub{ 10 ; }; # Add cols till MAX_COL_NUMBER in DB
use constant MAX_IMAGES_PER_PAGE     	=> sub{ 5; };  # Maximum of images per page
use constant LANGUAGES               	=> sub{ ( "French", "English" ); };  # Languages used
use constant PRIVATE_INFO_DIRECTORY  	=> sub{ "private/"; }; # that's where private info are stored
use constant ALBUM_INFO_DIRECTORY  	=> sub{ "album/"; };  # that's where album info are stored
use constant ALBUM_INFO_HIST_DIRECTORY 	=> sub{ ALBUM_INFO_DIRECTORY ->() . "hist/"; }; # Where to store history (log for i.e)
use constant ALBUM_HISTORY_INFO_FILE  	=> sub{ "history"; }; # that's where album history info file is stored
use constant MPWD 			=> sub{ "M!gn0n3 411ons si l4 R0s3"; }; # that's the master password to crypt session
use constant LOOP 			=> sub{ "loop"; }; # maximum packet size
use constant SHOW_PICTURES_ADMIN     	=> sub{ 0 ; }; # Prints on admin menu picture (!0) or not
use constant ALLOWED_FILE_FORMAT_TYPE 	=> sub{ "jpeg|jpg|gif|png|mp4|3gp|mpeg|mov|dat|mp3|avi"; }; # Allowed file format to be uploaded
use constant ALLOWED_SOCIAL_NETWORK 	=> sub{ "http\:\/\/www.youtube.com"; }; # Url to reach youtube website for i.e
use constant GOOGLE_MAP_SCRIPT_VERSION	=> sub{ "3"; }; # Script version to reach google map
use constant PATH_GOOGLE_MAP_ID 	=> sub{ "private/id.googlemap.v". GOOGLE_MAP_SCRIPT_VERSION ->(); }; # Where to store info
use constant PATH_GOOGLE_MAP_TRIP 	=> sub{ "album/trips/"; }; # Where to reach trips
use constant PATH_GOOGLE_MAP_OPT 	=> sub{ "-0"; }; # Extra option check documentation or comments
use constant PATH_TO_SENDMAIL_OPT	=> sub{ "|/usr/sbin/sendmail -t"; }; # Path to send mail with sendmail and options
use constant BODY_MESS_TO_SEND		=> sub{ ALBUM_INFO_DIRECTORY->() . "myMessToSend.txt" ; }; # File that old the message to send
use constant PATH_FOR_CALENDAR_ICS	=> sub{ ALBUM_INFO_DIRECTORY->() . "myICal_BranNew.ics"; }; # Path where to store ics calendar 
#"/Users/sdo/Sites/cgi-bin/myICal.ics"

# Unused
use constant MAXIMUM_SIZE_FILE 		=> sub{ (1_048_576 * 5); };    # 1 deposit = 1Mo * 5
use constant MAXIMUM_DIRECTORY_SIZE_THAT_CAN_CONTAIN_FILE => sub{ 100 * MAXIMUM_SIZE_FILE->(); }; # Size of directory that can contains files
use constant MAXIMUM_FILE_OPENED                          => sub{ 100; }; # Maximum file opened

sub do_untaint { # Begin sub do_untaint
	my ($myvar) = @_;
	unless ($myvar =~ m/^(.*)$/) { #allow filename to be [a-zA-Z0-9_]
		die("Tainted $myvar $!");
	} return $1;
} # End sub do_untaint

sub is_tainted { # Begin sub is_tainted
	my $taint;

	if ( $] >= 5.008 ) { # Begin if ( $] >= 5.008 )
		$taint = eval '${^TAINT}';
	} # End if ( $] >= 5.008 )
	else { # Begin else
		# some work around ...
	} # End else
	$taint;
} # End sub is_tainted

sub printTest{
	print "hello world<br>";
}

sub titi {
	print "hello world useTestPrint<br>";
}

#our $my_untaint=\&do_untaint;
our $useTestPrint = \&titi;
my $usePrivateTestPrint = \&titi;

return 1;

