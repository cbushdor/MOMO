#!/opt/local/bin/perl

# ------------------------------------------------------
q##//q#
* Created By : sdo
* File Name : MyConstantBase.pm
* Creation Date : Sun Aug 19 22:51:08 2018
* Last Modified : Fri Oct 26 22:00:30 2018
* Email Address : sdo@macbook-pro-de-sdo.home
* Version : 0.0.0.0
* License:
*       Permission is granted to copy, distribute, and/or modify this document under the terms of the Creative Commons Attribution-NonCommercial 3.0
*       Unported License, which is available at http: //creativecommons.org/licenses/by- nc/3.0/.
* Purpose : Accessing constants from another package/file. - PERL Miscellaneous
#;
# ------------------------------------------------------

use strict;
use warnings;
use io::MyUtilities;

use vars qw($mip);

# $mip variable declared in the main package

our $toto="testing";
my $privateToto="testing";

use constant LOCAL_HOSTS_FILE => "/etc/hosts"; # For security issur where to check hosts files
use constant HOSTED_BY_URL => sub{ "https://dorseb.hopto.org/~sdo/" }; # That's the url of host name
#use constant HOSTED_BY_URL => sub{ "$ENV{REQUEST_SCHEME}://$ENV{SERVER_NAME}$ENV{CONTEXT_PREFIX}" }; # That's the url of host name
use constant HOSTED_BY => sub{  "hopto.org"  }; # That's the host name
#use constant HOSTED_BY => sub{  (split(/\//,HOSTED_BY_URL->()))[2] }; # That's the host name

# We define a boolean value OK=0
use constant OK  => sub{ 0; };
use constant NOK => sub{ ! OK ->(); };

# Where pictures are going to be when upload action is done
use constant DIRECTORY_DEPOSIT 		=> sub{ io::MyUtilities::finds_directory_where_are_stored_images; };
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

=head1 LOCAL_HOSTED_BY_URL

Check if it local or not local ip.
That's the url of local host name

=head2 PARAMETER(S)

=over 4

=over 4

none

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

Returns IP address otherwise an empty string. Checks field error returned otherwise.

=back

=back

=head2 ERRROR RETURNED

=over 4

=over 4

$mip is not defined
	Message received "$mip does not exists: $!"

$mip is defined but does not contains IP address.
	Message received "\$mip does exists but not initialized: $!" 

=back

=back

=head2 BUG(S) KNOWN

=over 4

=over 4

None.

=back

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

=over 4

- I<Last modification:> Aug 20 2018

- I<Created on:> Aug 15 2018

=back

=back

=cut

use constant LOCAL_HOSTED_BY_URL => sub {
	# Sanitized tests
	die "\$mip does not exists: $!" if ! defined $mip;
	die "\$mip does exists but not initialized: $!" if $mip =~ m/io::MyNav::gets_ip_address/;

	#open(RHF,"$_[0]") || die("Error: $!\n"); # On the file that contains hosts file 
	# my $o = 
	open(RHF,LOCAL_HOSTS_FILE) || die("Error: $! '$_'\n"); # On the file that contains hosts file 
	print "\$_->'$_'=length(".length("$_")."), error:$!<br>";
	foreach(<RHF>){
		close(RHF) || die("Error: $!\n") if ($_ =~ m/^$mip\ +/); 
		return "$mip"   if ($_ =~ m/^$mip\ +/); 
	}
	close(RHF) || die("Error: $!\n");
	return "";
};

sub printTest{
	print "hello world<br>";
}

sub titi {
	print "hello world useTestPrint<br>";
}
our $useTestPrint = \&titi;
my $usePrivateTestPrint = \&titi;

return 1;

