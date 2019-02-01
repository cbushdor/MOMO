#!/usr/bin/perl-5.28.1 -T
#/opt/local/bin/perl 

# ------------------------------------------------------
q##//q#
* Created By : sdo
* File Name : album.cgi
* Creation Date : Mon Feb 3 22:51:08 2003
* Last Modified : Fri Feb  1 23:06:35 2019
* Email Address : sdo@macbook-pro-de-sdo.home
* License:
*       Permission is granted to copy, distribute, and/or modify this document under the terms of the Creative Commons Attribution-NonCommercial 3.0
*       Unported License, which is available at http: //creativecommons.org/licenses/by- nc/3.0/.
* Version : 1.6.16.500
* Purpose :
#;
# ------------------------------------------------------

use CGI;

my $doc;
#my $rtrip="white"; # We record or not just by color
my $rtrip; # We record or not just by color
BEGIN {
	push @INC,"/Users/sdo/Sites/cgi-bin/"; # We add a new path to @INC
	# A bug was solved and that's it was "...but still, the newly generated form has al the values from the previous form...".
	$doc=$CGI::Q ||= new CGI; # It is using the special internal $CGI::Q object, rather than your 'my $doc' object that's why we do this.
	$rtrip="blue"; # We don't record trip
}
END {
	$doc->delete_all(); # We clean all variables and parameters when the script is over
}

use strict;
use warnings;

use Socket;
use JSON;
use File::stat;
use locale;
use MIME::Base64;
use CGI::Carp qw(fatalsToBrowser); 
use LWP::Simple;
use XML::Simple;
use Data::Dumper;
use Time::localtime;
#use File::stat;
use Time::Local;
use Try::Tiny;
use Cwd;
use POSIX qw(strftime);
use Encode;
use URI::Escape;
use HTTP::Tiny;

use DateTime;
use DateTime::TimeZone;
use DateTime::Format::Strptime;

use Data::ICal;
use Data::ICal::Entry::Event;
use Date::ICal;

my $debug=0;# 0=false for no debug;1=true for debug
my $id=();
my $trips="var tripListJSON=[";
my $lot="var lot= new Array('--',"; # List of trips
my $lotList="<select name='maop_operationokdelete' onChange='listToDelete()'>"; # List of trips
my $lotList2="<select name='maop_operationokdelete' onChange='listToList()'>"; # List of trips

# Security issue
#&loadDataTrips; # put security control

if($debug==1){ # Begin if($debug==true)
	#print "case 1";
	if( !-f "album/_debug_album_DO_NOT_REMOVE"){ # Begin if( !-f "album/_debug_album_DO_NOT_REMOVE")
		if( !-f "album/debug_album_DO_NOT_REMOVE"){ # Begin if( -f "album/debug_album_DO_NOT_REMOVE")
			open(W,">album/debug_album_DO_NOT_REMOVE") or die("error $!");
			close(W) or die("error $!");
		} # End if( -f "album/debug_album_DO_NOT_REMOVE")
	} # End if( !-f "album/_debug_album_DO_NOT_REMOVE")
	else{ # Begin else
		rename("album/_debug_album_DO_NOT_REMOVE","album/debug_album_DO_NOT_REMOVE");
	} # End else
} # End if($debug==true)
else{ # Begin else
	#print "case 2";
	if( !-f "album/debug_album_DO_NOT_REMOVE"){ # Begin if( !-f "album/debug_album_DO_NOT_REMOVE")
		if( !-f "album/_debug_album_DO_NOT_REMOVE"){ # Begin if( !-f "album/_debug_album_DO_NOT_REMOVE")
			open(W,">album/_debug_album_DO_NOT_REMOVE") or die("error $!");
			close(W) or die("error $!");
		} # End if( -f "album/_debug_album_DO_NOT_REMOVE")
	} # End if( !-f "album/debug_album_DO_NOT_REMOVE")
	else{ # Begin else
		if( !-f "album/_debug_album_DO_NOT_REMOVE"){ # Begin if( !-f "album/debug_album_DO_NOT_REMOVE")
			rename("album/debug_album_DO_NOT_REMOVE","album/_debug_album_DO_NOT_REMOVE");
		} # End if( !-f "album/debug_album_DO_NOT_REMOVE")
	} # End else
} # End else

my $MyFile=();
my $locdep="album";# where are stored informations
my $myuri="$ENV{SERVER_NAME}";
my $myport= ($ENV{SERVER_PORT}=~m/[0-9]+/) ? ":$ENV{SERVER_PORT}/" : "/";
my $myscript= $ENV{REQUEST_URI};
$myscript=~s/\?.*$//;
$myscript=~s/album.cgi/maop.cgi/;
#print "Content-Type: text/html ; charset=UTF-8\n\n";

eval "use io::gut::machine::MyFile";
if ($@){
	eval "use io::gut::machine::MyFileRescue";
	if($@){
		print "No io::MyFileRescue";
		exit (-1);
	}
#	else{ $MyFile="packges::MyFileRescue";}
}
#print "Content-Type: text/html\n\n";
#my $timsec=localtime;
#my $final2 = io::gut::machine::MyFile::my_upload($doc, $doc->param("maop_file_name_img"), &io::MyConstantBase::DIRECTORY_DEPOSIT->(), "${timsec}$$",&io::MyConstantBase::ALLOWED_FILE_FORMAT_TYPE->());

use io::MyTime;
use io::MyConstantBase;
use io::MyUtilities;
use io::MyNav;

use io::MySec;

our $mip=io::MyNav::gets_ip_address;
chomp($mip);

use constant ALBUM_VER               	=> '1.6'; # Album version
use constant ALBUM_REL               	=> '16.500'; # Album release
use constant ALBUM_VERSION           	=> ALBUM_VER . '.' . ALBUM_REL; # Album version


my $vnl=100; # calculate version number length (number of characters in string)
my $main_prog="maop.cgi"; #(split(/[\\\/]/,"$0"))[scalar(split(/[\\\/]/,"$0"))-1]; # gets program name
#my $loc_margin="        ";
my $loc_margin="";

#my $ipAddr=io::MyNav::gets_ip_address;
my $furls="urls"; # fichier de sauvegarde urls
# Next 3 lines are used to suffix new file name to save in the album.
my @month=( "Jan", "Fev", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec" );
my @proc                  = gmtime;
my $suffix_for_image_file =
	 $mip
	. "||";

my $fn="album/hist/${mip}";

# This is usefull when pb occurs and file being open
# use IO;

#import bar.cgi;

=head1 NAME

album.cgi

$VERSION=1.6.16.500

=head1 ABSTRACT

This file creates an album on the net of different pictures that have different formats. Formats can be jpeg or jpg or gif (can be others but these format are mostly used). Size of the picture (length,width) does not matter but file size yes (look my_upload function).

=head2 LIST OF FUNCTIONS

=over 4

=over 4

accessAdminPicture
accessToPicture
add_new_col 
admin_menu 
auth_menu 
cascade_style_sheet_definition 
clean_pictures 
create_dir 
create_new_page 
create_table_for_navigator 
error_raised_visit 
extra_comments 
general_css_def 
get_first_page_authorized 
getsTagsFromIpAllowed
gets_current_images_information_from_current_album 
gets_first_page_number 
go_back 
help_menu_with_css 
ipAddressGranted
ipAddressRemoved
is_ok_page_num 
javaScript 
loadDataTrips
look_for_images_used 
look_if_page_authorized 
main_help_menu_css 
main_menu 
manage_position 
menu_admin_title 
menu_leave_admin 
menu_page_title 
menu_admin_GoogleMap_ID
myrec
my_wait
number_of_pages 
numbers 
print_date_of_picture_put_on_album 
print_info_picture 
print_page 
print_pictures 
my_promptA
my_promptB
put_url_line 
raised_upload_window 
rank_right_navigator_bar_range 
record 
remove_picture 
return_info_picture 
setGoogleID
set_history
set_language 
set_link 
set_select_tag 
set_upload 
showsStats
shows_list_pictures 
shows_page_not_taken_yet 
split_links 
switch_from_a_specified_character_to_tag 
switch_from_a_specified_tag_to_characters 
tag_div_comment 
under_construction_prompt 

=back

=back

=head2 HISTORY OF MODIFICATIONS

=over 4

- I<Last modification:v1.6.16.500> Jan 30 2019 This is perl 5, version 24, subversion 3 (v5.24.3) built for darwin-thread-multi-2level to This is perl 5, version 28, subversion 1 (v5.28.1) built for darwin-2level (with 1 registered patch, see perl -V for more detail).

- I<Last modification:v1.6.16.234> Dec 15 2018 Now pictures are printed.

- I<Last modification:v1.6.16.200> Dec 02 2018 Map legend improved now date+time+tip name added. To reach the map extra param was added in Visitor map menu.

- I<Last modification:v1.6.16.196> Nov 28 2018 Physical messages replaced by color values.

- I<Last modification:v1.6.16.195> Nov 28 2018 A mail is send to EADM when first time finger print is taken.

- I<Last modification:v1.6.16.193> Nov 27 2018 Finger print implemented.

- I<Last modification:v1.6.16.191> Nov 26 2018 Finger print implemented.

- I<Last modification:v1.6.16.190> Nov 23 2018 TZ in second unit added+better indent in mail for trip created

- I<Last modification:v1.6.16.189Hc> Nov 22 2018 Form is cleaned and localtion for TZ preset.

- I<Last modification:v1.6.16.189Hb> Nov 22 2018 Form is cleaned properly. Trip name does not support now # and  / characters. Trip name encoding was removed or commented.

- I<Last modification:v1.6.16.189Ha> Nov 20 2018 Form is cleaned properly. Trip name does not support or bare / character.

- I<Last modification:v1.6.16.189H> Nov 20 2018 Form is cleaned properly. Now ICS file created but not enclosed in email. Not created in proper directory.

- I<Last modification:v1.6.16.189G> Nov 17 2018 Form is cleaned properly. TZ loaded properly but still need to be taken.


- I<Last modification:v1.6.16.189F> Nov 09 2018 old data staid in the form even if the content of it is new. This bug was solved in the field BEGIN and END.

- I<Last modification:v1.6.16.189D> Nov 08 2018 Tainted mode finally added to the program and tested. Some corrections were made to make te prgram work agaain as the original.

- I<Last modification:v1.6.16.189C> Nov 05 2018 Tainted mode finally added to the program.

- I<Last modification:v1.6.16.189B> Nov 04 2018 use warnings; added. Try to avoid old value in memory to stay. Hope it will be ok. Slight change done in the code to make it works with these prerequisites.

- I<Last modification:v1.6.16.189A> Nov 04 2018 use strict; added. Try to avoid old value in memory to stay. Hope it will be ok. Slight change done in the code to make it works with these prerequisites.

- I<Last modification:v1.6.16.189> Nov 04 2018 hash added %credentials to check_passord

- I<Last modification:v1.6.16.156> Oct 27 2018 Tests+updates of the dates

- I<Last modification:v1.6.16.151> Oct 26 2018 Starting + finishing putting all constants in a single file: io/MyConstantBase.pm

- I<Last modification:v1.6.16.145> Oct 26 2018 Starting putting all constants in a single file: io/MyConstantBase.pm

- I<Last modification:v1.6.16.140> Apr 21 2018 Compiler version change from  5.8.8 to 5.24.3. Slight modification were made read note Last modification:v1.6.16.140.

- I<Last modification:v1.6.16.112> Apr 07 2018 Due to portage configuration from previous config were not modified. There are still some but for the ime being it does not shows up. Couldn't check local config but ok for distant tests. This lack was modified hopefully hope it is ok now.
Early bird: when link is sent within email bad IP address send. Now it is ok.

- I<Last modification:v1.6.16.100> Jan 31 2018 due to a breakdown to web host new to to update program. Install web server (or update) and mail server. Program my album of picture used was not up to date so took last version that was buggy and made correction of bugs and try to update it.

- I<Last modification:v1.6.15.238> Apr 8 2016 minor bug noticed during tests at the public place. Spaces in the trip name was bathering the map printings. Regexp was added to remove this checks sub setGoogleID

- I<Last modification:v1.6.15.234> Mar 3 2016 minor bug noticed during tests at the public place. Byug solved. Tested merely need some more tests see <DATETIME>.

- I<Last modification:v1.6.15.233> Feb 26 2016 minor bug noticed during tests at the theatre. Bug event occur before it was expected 
s.a lon lat calculated

- I<Last modification:v1.6.15.230> Feb 26 2016 minor bug noticed. If trip name is Test 6 #20160225 trip is not recorded

- I<Last modification:v1.6.15.219> Feb 26 2016 weird behavior lost param value due to order of input tag

- I<Last modification:v1.6.15.215> Feb 15 2016 html page title enhanced now trip name added if one exists

- I<Last modification:v1.6.15.214> Feb 15 2016 see sub setGoogleID

- I<Last modification:v1.6.15.210> Feb 11 2016 see sub menu_admin_GoogleMap_ID

- I<Last modification:v1.6.15.200> Feb 11 2016 see sub menu_admin_GoogleMap_ID

- I<Last modification:v1.6.15.197> Feb 06 2016 see sub menu_admin_GoogleMap_ID

- I<Last modification:v1.6.15.190> Jan 30 2016 see sub menu_admin_GoogleMap_ID

- I<Last modification:v1.6.15.188> Jan 24 2016 due to add to maop_ infront of each var name in input tag some data were lost.
see sub menu_admin_GoogleMap_ID

- I<Last modification:v1.6.15.170> Dec 07 2015 due to add to maop_ infront of each var name in input tag some data were lost.
		Try to debug and rmove these lack by adding maop_ to var name where they were missing.

- I<Last modification:v1.6.15.145> Nov 06 2015 added extra info to myrec printed tests not inside the function but messages printed from outside

- I<Last modification:v1.6.15.129> Nov 06 2015 added extra info to myrec s.a current working directory path
		Trip name is bolded

- I<Last modification:v1.6.15.124> Aug 29 2015 that's the line my $oppp=time(); #io::MyTime::gets_formated_date;
		The bug came from that granularity was not goot with a formated date

- I<Last modification:v1.6.15.105> Aug 17 2015 tests added on geo coordinate format 
		if(! defined($lat)||length($lat)==0||$lat!~m/^[\-\+]{0,1}[0-9]{1,}\.[0-9]{1,}$/){ # Begin if(!defined($lat)||length($lat)==0||$lat!~m/^[\-\+]{0,1}[0-9]{1,}\.[0-9]{1,}$/)
		                                               ^^^^


- I<Last modification:v1.6.15.80> Jan 20 2015 extra test to avoid user cheating

- I<Last modification:v1.6.15.65> Dec 24 2014 see setGoogleID

- I<Last modification:v1.6.15.60> Dec 23 2014 see set set_history

- I<Last modification:v1.6.15.48> May 10 2014 see set set_history

- I<Last modification:v1.6.15.45> Feb 24 2014 see menu_admin_GoogleMap_ID

- I<Last modification:v1.6.15.40> Feb 23 2014 see menu_admin_GoogleMap_ID

- I<Last modification:v1.6.15.30> Feb 21 2014 see menu_admin_GoogleMap_ID

- I<Last modification:v1.6.15.25> Feb 20 2014 io::MyUtilities::footer information modified.

- I<Last modification:v1.6.15.14> Feb 18 2014 Removed parameters. Caused problems with google map.

- I<Last modification:v1.6.13.13> Feb 11 2014 Add the constant &io::MyConstantBase::PATH_GOOGLE_MAP_OPT->()

- I<Last modification:v1.6.13.12> Jan 18 2014 put the trip name in history
			&io::MyConstantBase::GOOGLE_MAP_SCRIPT_VERSION->() added.

- I<Last modification:v1.6.13.10> Jul 17 2012 see accessToPicture

- I<Last modification:v1.6.13.9> Jul 15 2012 see manage_position , record

- I<Last modification:v1.6.10.6> Jul 4 2012 see set_link

- I<Last modification:v1.6.10.1>  Feb 02 2012 see set_history

- I<Last modification:v1.6.10.1>  Nov 6 2011 see print_page

- I<Last modification:v1.6.10.0>  Nov 4 2011 shows date of inscription (put on) of the picture in the album.
at the begining the choice was not to print it but for different reasons this was changed.

- I<Last modification:v1.6.9.3>  Oct 31 2011 see record

- I<Last modification:v1.6.8.33>  Aug 27 2011: see ipAddressGranted

- I<Last modification:v1.6.8.0>  Aug 25 2011: see print_page see record

- I<Last modification:v1.6.7.0>  Aug 24 2011: see print_page 

- I<Last modification:v1.6.6.0>  Aug 21 2011: see record
see menu_admin_GoogleMap_ID

- I<Last modification:v1.6.5.1>  Aug 17 2011: see io::MySec

- I<Last modification:v1.6.5.0>  Jul 22 2011: MIME::Base64 encoding used.

- I<Last modification:v1.6.4.49>  Jun 22 2011: bug solve go_back(...)

- I<Last modification:v1.6.4.48> Jun 06 2011 documentation revised+extra bugs.

- I<Last modification:v1.6.4.0> Apr 22 2011 documentation revised.

- I<Last modification:v1.6.3.5> Apr 17 2011 check shows_list_pictures 

- I<Last modification:v1.6.3.0> Apr 15 2011 check print_page

- I<Last modification:v1.6.2.32> Apr 11 2011 check ipAddressGranted

- I<Last modification:v1.6.2.0> Apr 10 2011 check print_date_of_picture_put_on_album

- I<Last modification:v1.6.0.0> Apr 07 2011 DB changed due to admin problem

- I<Last modification:v1.5.12.39> Apr 06 2011 default was not printed by default if no page selected by default (he first from the list).
check shows_page_not_taken_yet
check remove_picture
check clean_pictures
check shows_list_pictures

- I<Last modification:v1.5.12.0> Mar 15 2011: check for sub print_page.
check for sub shows_list_pictures.
check for sub record.

- I<Last modification:v1.5.11.23> Mar 14 2011: check for sub print_page and sub record.

- I<Last modification:v1.5.11.0> Mar 13 2011: check sub record.

- I<Last modification:v1.5.10.0> Feb 26 2011: check sub record.

- I<Last modification:v1.5.9.20> Feb 25 2011: print_page, record.

- I<Last modification:v1.5.9.15> Feb 24th 2011: see print_page, record.

- I<Last modification:v1.5.9.3> Feb 22 2011: see io::gut::machine::MyFile::my_upload
see manage_position

- I<Last modification: v1.5.9.0> Feb 18 2011: ipAddressGranted modified
history structure modified.

- I<Last modification: v1.5.8.1> Feb 17 2011: see io::MyUtilies::setUrlFile

- I<Last modification: v1.5.8.0>  Feb 11 2011: setGoogleID added.

- I<Last modification: v1.5.7.0>  Feb 10 2011:  see io::MyNav

- I<Last modification: v1.5.6.0> Jan 31 2011: seee packages::MyFile.pm.

- I<Last modification: v1.5.4.10> Jan 21 2011. Better ip address format management IPV4 & IPV6.

- I<Last modification: v1.5.4.0> Nov 23rd 2010. Better management of module added.

- I<Last modification: v1.5.3.1> Nov 22 2010. Problem with storing in data base.

- I<Last modification: v1.5.3.0> Nov 22 2010. Error management added for file format.
see package::MyFile::my_upload(...).

- I<Last modification: v1.5.2.0> Nov 21 2010. flv format replaced by mp3 format.

- I<Last modification: v1.5.1.20> Nov 02 2010: Segmentation packet done in a different way.
Extra tests were done.

- I<Last modification: v1.5.1.10> Nov 02 2010: Segmentation packet done in a different way.

- I<Last modification: v1.5.1.0> Oct 28th 2010: previous operation canceled. Segmentation packet done instead.

- I<Last modification: v1.5.0.2> Oct 27th 2010: characters for html tags replaced.

- I<Last modification: v1.5.0.0> Oct 16th 2010: crypto system added on service versioning, verDoc.

- I<Last modification: v1.4.18.0> Oct 15th 2010: Function added in io::MyNav.pm

- I<Last modification: v1.4.17.12> Oct 15th 2010: Tests about how to make documentation.

- I<Last modification: v1.4.17.11> Oct 5th 2010: modification see io::MyUtilities.pm.
New $service verDoc added.

- I<Last modification: v1.4.17.10> Oct 5th 2010: modification see io::MyUtilities.pm.

- I<Last modification: v1.4.17.9> Oct 4th 2010: bug on tests upon optimisation of 2 transactions to 1. 
Bug fixed.

- I<Last modification: v1.4.17.5> Oct 4th 2010: optimisation of 2 transactions to 1. 
(go and back)*2 optimised to (go and back)*1
See io::MyUtilities.pm

- I<Last modification: v1.4.17.0> Oct 3rd 2010: $service==versionning added.
Only updates version number datum.

- I<Last modification: v1.4.16.4> Oct 1 2010: see MyUtilities.
Add unlink for *._.html doc * already done.
 
- I<Last modification: v1.4.16.2> Oct 1 2010: see MyUtilities.

- I<Last modification: v1.4.16.0> Oct 1 2010: and $main_prog=$0 variable added.
Extra tests were done to remove trailing path with separator / or \.
\ not tested yet.

- I<Last modification: v1.4.15.23> Sep 25 2010: test

- I<Last modification: v1.4.15.22> Sep 25 2010: modification function getVers() see packag::MyUtilities 
Creation of the log book.
This page is the log book.

- I<Last modification: v1.4.15.30> Sep 24 2010: function getVers() added to package::MyUtilities

- I<Last modification: v1.4.15.1> Jun 15 2010: see package::MySec::myGetsUrl()

- I<Last modification: v1.4.14.5> Mar 04 2010: see albun.cgi main_menu;menu modiffied log book admin menu;package::MyUtilities::setUrlFile()

- I<Last modification: v1.4.14.1> Dec 5 2009: help_menu_with_css, general_css_def

- I<Last modification: v1.4.14.0RC> Oct 29 2009: see  ipAddressGranted.

- I<Last modification: v1.4.13.9> Oct 24 2009: mp4 or dat or flv file format added.

- I<Last modification: v1.4.13.1> Oct 18 2009: &io::MyConstantBase::SHOW_PICTURES_ADMIN->() added.

- I<Last modification: v1.4.12.0> Oct 04 2009: read comment io::MyNav.pm.

- I<Last modification: v1.4.11.0> Sep 27 2009: read comment of cascade_style_sheet_definition.

- I<Last modification: v1.4.8.0> Sept 26 2009: read comment of accessToPicture.

- I<Last modification: v1.4.4.0> Sept 24 2009: Add CGI:: beautifuller. Auto conf html tags.

- I<Last modification: v1.4.3.0> Sept 20 2009: page_list.

- I<Last modification: v1.4.2.0> Sep 17 2009: read io::MyNav.pm  .

- I<Last modification: v1.4.1.20> Sep 13 2009: see shows_list_pictures .

- I<Last modification: v1.4.1.11> Sep 10 2009: see auth_menu,menu_page_title.

- I<Last modification: v1.4.1.10c> Sep 08 2009: see io::MyNav.pm .

- I<Last modification: v1.4.1.10b> Sep 07 2009: see io::MyNav.pm firstChoicetMenuadmin .

- I<Last modification: v1.4.1.10aTryOut> Sep 03 2009: switch recPid value from ok to none value.

- I<Last modification: v1.4.1.8> Aug 31 2009: Link tag shows up on .mov .3gp movie format. Correction done. When asks to put left side image and allowed to be printed a link tag shows up corection done no link shows up now.

- I<Last modification: v1.4.1.7> Jul 29 2009: Html code reformated see help_menu_with_css, groupAndStuff,firstChoicetMenuadmin.

- I<Last modification: v1.4.1.6> Jul 25 2009: Intermediate menu added. Change was done in menu_leave_admin.

- I<Last modification: v1.4.1.5> Jul 21 2009: Moved from album.cgi to  io::MySec::urlsAllowed .

- I<Last modification: v1.4.1.0> Jul 20 2009: Look at function accessToPicture, urlsAllowed.

- I<Last modification: v1.4.0.3> Jul 19 2009: Look at functions print_page, extra_comments.

- I<Last modification: v1.4.0.0> Jun 27 2009: Checks function where modif were done.

- I<Last modification: v1.3.7.0> Nov 30 2008: Checks function where modif were done.

- I<Last modification: v1.0.5.0> Apr 20 2008: Checks function where modif were done.

- I<Last modification: v1.0.0.0> Jan 27 2006: Checks function where modif were done.

- I<Last modification: v0.4.0.0> Mar 03 2005: Checks function where modif were done.

- I<Last modification: v0.4.0.0FirstShot> Nov 10 2004: Checks function where modif were done.

=back

=cut

# Url(s) that are allowed to ptnt insert picture option in navigator bar
my @urlAllowed=split(/\,/, io::MyUtilities::getUrlFromFile);
# Checks if url is allowed.
my ($allow,$authorized)=io::MySec::urlsAllowed;

# --------------------------------------------------------------------------
# --------- Modifications can be done in the zone below --------------------
# --------------------------------------------------------------------------

# This is directory where all be stored
my $album_directory="album";

# That's where the file that contains info for building pages are stored
my $configuration_file="conf.file";

# send to another site when under construction for a demo
my $url_demo="http://storm.prohosting.com/dorey/cgi-bin/${main_prog}";

# --------------------------------------------------------------------------
# --------- End of zone ----------------------------------------------------
# --------------------------------------------------------------------------

$|=1;

#use CGI::Pretty qw( :html4 );

$CGI::Pretty::LINEBREAK="\n\n";
$CGI::Pretty::INDENT="\t\t";

use Fcntl qw( :DEFAULT :flock);

# create temporary file
if( ! -d "tmp"){mkdir("tmp");}
if( ! -d &io::MyConstantBase::PATH_GOOGLE_MAP_TRIP->() ){mkdir(&io::MyConstantBase::PATH_GOOGLE_MAP_TRIP->());}


# This is document which will help to deal with CGI information
binmode STDOUT, ':utf8';
print $doc->header(-type => 'text/html',
	                   -charset => 'utf-8');


my $timsec=uri_unescape($doc->param("timsec"));
my $mgidt=uri_unescape($doc->param("maop_googid")); #my google id  trip
$mgidt=~s/[\n\t\ ]*$//g;
my $tn=&io::MyConstantBase::PATH_GOOGLE_MAP_TRIP->().$mgidt ."-".&io::MyConstantBase::TRIP_NAME->(); # Trip name
my $an_action=();
my $lok=uri_unescape($doc->param("maop_login"));
my $lon=uri_unescape($doc->param("maop_lon"));
my $lat=uri_unescape($doc->param("maop_lat"));
my $param_trip=uri_unescape($doc->param("maop_TRIP_ID"));
my $bdaytime=uri_unescape($doc->param("maop_bdaytime"));
my $edaytime=uri_unescape($doc->param("maop_edaytime"));
my $logfile=uri_unescape($doc->param("maop_log"));

#@chomp($param);
chomp($logfile);
#print "Content-type:text/html ; charset=UTF-8\n\n";
#my $c=(${^TAINT}) ? "Tainted<br>\n":"Not tainted<br>\n";
#print "<br>------->$c<br>\n";
#print "---->$bdaytime<br>========>$edaytime<br>";

if(-f "debug"){ # Begin if(-f "debug")
	$id="AIzaSyDoz8j1983lLAncsYMjXLeemy5ks3DkfM8";
} # End if(-f "debug")
else{ # Begin else
	$id=io::MyUtilities::loadFile("private/id.googlemap.v3");	
} # End else

my $mparam=();

	#my $gurl =();# google url get data time zone name for instance
	#my $gjson=();# json object return from get with $gurl
	#my $json_obj = ();# json object
	#my #$pperl = ();# gjson decoded to perl hash
	my $mtzg=();# My Time Zone Global

# Saving parametters
foreach my $p ($doc->param){ # Begin foreach my $p ($doc->param)
	#print ">>>>>>>$p<br>";
	if($p=~m/^maop\_/){ # Begin if($p=~m/^maop\_/)
		if($p!~m/^maop_lon$/&&
		   $p!~m/^maop_lat$/&&
		   $p!~m/^maop_prog$/&&
		   $p!~m/^maop_log$/){ # Begin if($p!~m!maop_lon!&&$p!~m!maop_lat!&&$p!~m!maop_prog!&&$p!~m!maop_log!)
			my $ull=uri_unescape($doc->param($p));
			#print "<br>PARAMS-------------->$p:$ull<br>";
			$mparam.="&$p=".uri_escape($ull);
		}  # End if($p!~m!maop_lon!&&$p!~m!maop_lat!&&$p!~m!maop_prog!&&$p!~m!maop_log!)
	} # End if($p=~m/^maop\_/)
} # End foreach my $p ($doc->param)
#print "iiiiiioooooooooo>$mparam<br>";
$mparam=~s/^\&//;
#print "oooooooooo>$mparam<br>";
#exit(1);

	my $url=();
	my $mltmp=&io::MyConstantBase::LOCAL_HOSTED_BY_URL->(); # my local tmp
	#print "Content-Type: text/html ; charset=UTF-8\n\n";
	#print "case 2<br>";exit(1);
	if(! defined($mip)||$mip=~m/^127\.0\.0\.1/i||$mip=~m!localhost!){ # Begin if(! defined($mip)||$mip=~m/^127\.0\.0\.1/i||$mip=~m!localhost!)
		#print "oooiiiiiiii>case 1-";
		$url="http://localhost/~sdo/cgi-bin/maop.cgi\?$mparam";
		#print "*************CHECK******>$url<br>";
	} # End if(! defined($mip)||$mip=~m/^127\.0\.0\.1/i||$mip=~m!localhost!)
	elsif(! defined($mip)||$mip=~m/^$mltmp/||$mip=~m!example2.dev!){ # Begin elsif(! defined($mip)||$mip=~m/^${\&io::MyConstantBase::LOCAL_HOSTED_BY_URL}/||$mip=~m!example2.dev!)
		#print "iiiiiiii>case 3xxx-";
		$url="https://$mltmp/~sdo/cgi-bin/maop.cgi\?$mparam";
		#print "</br>$url<br>";
		#print "</br>IP---->$mip<br>defined:" . defined($mip) . "<br>${\&io::MyConstantBase::LOCAL_HOSTED_BY_URL} ? match example2.dev :". ($mip=~m!example2.dev!) ."<<br>";
		#sleep(15);
		#exit(-1);
	} # End elsif(! defined($mip)||$mip=~m/^${\&io::MyConstantBase::LOCAL_HOSTED_BY_URL}/||$mip=~m!example2.dev!)
	else{ # Begin else
		#print "iiiiiiii>case 2-";
		$url = 'http';
		if ("$ENV{HTTPS}" eq "on") {
			$url .= "s";
		}
		$url .= "://";
		$url.= $ENV{"HTTP_HOST"} . $ENV{REQUEST_URI}. "\?$mparam"; # url where website is hosted
		$url=~s/album\.cgi/maop\.cgi/;
	} # End else
	# ------------------------------------------------------------------------------------------
	#print "<br>#########################>$url<br>";

	#exit(0);

if(! defined($logfile)||length($logfile)==0||$logfile!~m/^album\_hist\_log-[0-9]{1,}(\.[0-9]{1,}){3}\-[0-9]{3,}$/){ # Begin if(! defined($logfile)||length($logfile)==0||$logfile!~m/^album\_hist\_log-[0-9]{1,}(\.[0-9]{1,}){3}\-[0-9]{3,}$/)
	print &my_promptA("<!--<u>part 1 ($logfile):</u> <b></u>$url</b>-->" ."<!-- accordeoniste -->");
	exit(0);
} # End if(! defined($logfile)||length($logfile)==0||$logfile!~m/^album\_hist\_log-[0-9]{1,}(\.[0-9]{1,}){3}\-[0-9]{3,}$/)

$logfile=~s/\_/\//g;
if(!-f "$logfile"){ # Begin if(!-f "$logfile")
	print &my_promptA("part 2 (does not exist $logfile): ");
	exit(0);
} # End if(!-f "$logfile") 
else{ # Begin else
	#print "azerty 3<br>";
	if( -e "$logfile"){ # Begin if( -e "$logfile")
		$logfile=&do_untaint($logfile);
		unlink("$logfile");
	} # End if( -e "$logfile")
	chdir("album");chdir("hist");
	opendir(ARD,".") || die(". $!");# open current directory
	my @dr= grep { $_ ne '.' and $_ ne '..' and $_ !~ m/pl$/i and $_ !~ m/cgi$/i and $_=~m!^log-!} readdir(ARD);# parse current directory
	closedir(ARD) || die(". $!");# close directory
	#print "Content-Type: text/html ; charset=UTF-8\n\n";
	my $c=0;
	for my $o (@dr){ # Begin for my $o (@dr)
		my $uuu= time - stat($o)->ctime;
		if( $uuu > 5*60*60){ # Begin if( $uuu > 5*60*60)
			#print ">".$c++ . "--------------ooo)" . ( time - $uuu )  ;
			if( -e "$o"){ # Begin if( -e "$o")
				#print "removing $o<br>";
				$o=&do_untaint($o);
				unlink("$o");
			} # End if( -e "$o")
		} # End if( $uuu > 5*60*60)
	} # End for my $o (@dr)
	chdir(".."); chdir("..");
} # End else

if(! defined($lat)||length($lat)==0||$lat!~m/^[\-\+]{0,1}[0-9]{1,}\.[0-9]{1,}$/){ # Begin if(!defined($lat)||length($lat)==0||$lat!~m/^[\-\+]{0,1}[0-9]{1,}\.[0-9]{1,}$/)
	#print "Content-Type: text/html ; charset=UTF-8\n\n";
	# &myrecmyrec("Case 3 ($lon - $lat) latitude exists and as proper format <i>$url</i>","../error.html","(! defined($lat)||length($lat)==0||$lat!~m/^[0-9]{1,}\.[0-9]{1,}$/)");
	#print "azerty 4<br>";
	#print $c. "<!-- azerty -->";
	exit(0);
} # End if(!defined($lat)||length($lat)==0||$lat!~m/^[\-\+]{0,1}[0-9]{1,}\.[0-9]{1,}$/)

#my $locweaf=&io::MyConstantBase::ALBUM_INFO_HIST_DIRECTORY->() ."wfc_data.$lon.$lat.$$.".time().".xml";# file for local weather
my $locweaf=&io::MyConstantBase::ALBUM_INFO_HIST_DIRECTORY->() ."wfc_data-$$-".time().".xml";# file for local weather

# ----------------------------------------------------------------------------------------------
# format solved - missing but need to check if lon lat can have negative values
if(! defined($lon)||length($lon)==0||$lon!~m/^[\-\+]{0,1}[0-9]{1,}\.[0-9]{1,}$/){ # Begin if(!defined($lon)||length($lon)==0||$lon!~m/^[\-\+]{0,1}[0-9]{1,}\.[0-9]{1,}$/)
	my $url=();

	# -------------------------------------------------------
	# --------------------- BEGINING ------------------------
	# -------- case when local but this case now is rare ----
	$url = 'http';
	if ("$ENV{HTTPS}" eq "on") {
		$url .= "s";
	}
	$url .= "://";
	$url.= $ENV{"HTTP_HOST"} . $ENV{REQUEST_URI}. "\?$mparam"; # url where website is hosted
	$url=~s/album\.cgi/maop\.cgi/;
	# -------- case when local but this case now is rare ----
	# ---------------------- END ----------------------------
	# -------------------------------------------------------
	
	#print "Content-Type: text/html ; charset=UTF-8\n\n";
	my $t="* <u>($lon)</u> ======== * defined(lon):".((defined($lon)) ? " defined" : " not defined")." <b>=====</b> "
		."* length(lon)==0: ".((length($lon)==0) ? " length is zero ":" length is not zero ")." <b>=====</b> "
		."* lon!~m/^[\-\+]{0,1}[0-9]{1,}\.[0-9]{1,}$/".(($lon!~m/^[\-\+]{0,1}[0-9]{1,}\.[0-9]{1,}$/) ? " not defined for this reg exp " : " defined for this reg exp ")." <b>=====</b> ";
		print $t;
	print &my_promptB("Tests B");
	#print $c . "<!-- plustot -->";
	exit(0);
} # End if(!defined($lon)||length($lon)==0||$lon!~m/^[\-\+]{0,1}[0-9]{1,}\.[0-9]{1,}$/)
else{ # Begin else
} # End else

#if($url=~m/dorey/||$url=~m!${\&io::MyConstantBase::LOCAL_HOSTED_BY_URL}!){ # Begin if($url=~m/dorey/||$url=~m!${\&io::MyConstantBase::LOCAL_HOSTED_BY_URL}!)
if($url=~m/$ENV{SERVER_NAME}/){ # Begin if($url=~m/$ENV{SERVER_NAME}/)
	# Note Last modification:v1.6.16.140
	# We want to get time zone Id from param
	$mtzg=uri_unescape($doc->param("maop_myLocalTZ")); # my time zone from google
	#$pperl->{timeZoneId};
} # End if($url=~m/$ENV{SERVER_NAME}/)
# &myrecmyrec("Case 10 ($lon - $lat) logfile format <i>$url</i>","../error.html","------------------everything is fine-----------------------------");

# Password for login
my ( $login, $password )=io::MyUtilities::gets_private_stuff_for_administrator($an_action,
									       &io::MyConstantBase::PRIVATE_INFO_DIRECTORY->(),
									       uri_unescape($doc->param("maop_login")),
									       uri_unescape($doc->param("maop_password")));

# We need PID tO make a little security
my $my_pid=uri_unescape($doc->param('maop_prev_id'));
chomp($my_pid);

# This is where configuration file is
# This is a table. In the new future this will be manage by io::MyDB.pm 
# For the time being io::MyDB.pm is under construction
# It is managed by hand (hard coded in this cgi)
my $file_conf_to_save="$album_directory/$configuration_file";
chomp($file_conf_to_save);

	#print "Content-Type: text/html ; charset=UTF-8\n\n";
# That's the service
my $service=uri_unescape($doc->param("maop_service"));
chomp(${service});
#print "eeeeeeeeeeeee)$service<br />";

if( -f "album/debug_album_DO_NOT_REMOVE"){ # Begin if( -f "album/debug_album_DO_NOT_REMOVE")
	#print "Content-Type: text/html ; charset=UTF-8\n\n";
	#print "ooooooo)$service<br />";
	#print "-------->" . $mip."\n<br />";
	#print "oooooo->$name<br />";
} # End if( -f "album/debug_album_DO_NOT_REMOVE")
else{# Begin else
	if( !-f "album/_debug_album_DO_NOT_REMOVE"){ # Begin if( -f "album/debug_album_DO_NOT_REMOVE")
		open(W,">album/_debug_album_DO_NOT_REMOVE") or die("error $!");
		close(W) or die("error $!");
	} # End if( -f "album/debug_album_DO_NOT_REMOVE")
	#print "Content-Type: text/html ; charset=UTF-8\n\n";
	#print "Pragma: no-cache \n\n";
	#print "oooooo->$name<br />";
} # End else

if($service eq "verDoc"){ # Only entire documentation + version is asked
	#print "Content-Type: text/html ; charset=UTF-8\n\n";
	my $res=io::MyUtilities::getsDocVers("${main_prog}",ALBUM_VERSION);
	#print $res;
	my $cres=jcode(MPWD->(),$res);
	$res=encode_base64($cres);
	print "$res";
	exit(&io::MyConstantBase::OK->());# Exit that's it
}elsif($service eq "versioning"){ # Only version is asked
	#print "Content-Type: text/html ; charset=UTF-8\n\n";
	my $cres=jcode(MPWD->(),ALBUM_VERSION);
	#print "$cres(---------)<br />";
	my $res=encode_base64($cres);
	print "$res";
	exit(&io::MyConstantBase::OK->());# Exit that's it
}elsif($service eq "ver"){ # Only version is asked
	#print "Content-Type: text/html ; charset=UTF-8\n\n";
	#my $cres=jcode(MPWD->(),ALBUM_VERSION);
	print ALBUM_VERSION;
	exit(&io::MyConstantBase::OK->());# Exit that's it
}elsif($service=~m/geoLoc/){ # only history is asked
	my $u=ALBUM_INFO_DIRECTORY->() . ALBUM_HISTORY_INFO_FILE->();
	#print "Content-Type: text/html ; charset=UTF-8\n\n";
	#print "Content-Type: text/html\n\n";
	if(  -f "$u" ){ # Begin if(  -f "$u" )
		print "error";
		exit(&io::MyConstantBase::OK->());
	} # End if(  -f "$u" )
	open(R,$u) || die("error $u $!"); 
	my $hist=<R>;
	close(R)|| die("error ".ALBUM_INFO_DIRECTORY->() . ALBUM_HISTORY_INFO_FILE->());
	my $cres=jcode(ALBUM_INFO_DIRECTORY->() . MPWD->() . ALBUM_INFO_DIRECTORY->(),$hist);
	my $res=encode_base64($cres);
	print "$res";
	exit(&io::MyConstantBase::OK->());
}# End elsif($service=~m/geoLoc/)

# That's the pid to record
my $recPid=uri_unescape($doc->param("maop_recPid"));
chomp($recPid);

# That's the pid to remove
my $remPid=uri_unescape($doc->param("maop_remPid"));
chomp($remPid);

# Upload granted or not
my $upload=uri_unescape($doc->param("maop_upld"));
chomp($upload);

# That's the user login from the url
my $user_login=uri_unescape($doc->param("maop_login"));
chomp($user_login);

# That's the user password from the url
my $user_password=uri_unescape($doc->param("maop_password"));
chomp($user_password);

# Modify or remove lines for album
$an_action=uri_unescape($doc->param("maop_action"));
chomp($an_action);

# That's info stored when we want to modify it
my @info_on_picture=();


# necessary images
my @images_used=(
	&io::MyConstantBase::DIRECTORY_DEPOSIT->() . "new_cross.gif",
	&io::MyConstantBase::DIRECTORY_DEPOSIT->() . "under_construction10.gif",
	&io::MyConstantBase::DIRECTORY_DEPOSIT->() . "my_lovely_pict.gif",
	&io::MyConstantBase::DIRECTORY_DEPOSIT->() . "chair1-a.gif",
	&io::MyConstantBase::DIRECTORY_DEPOSIT->() . "powered.gif"
	);

my $date_ticket=uri_unescape($doc->param("maop_date"));
#print "Content-Type: text/html;charset=utf-8;\n"; print "Pragma: no-cache \n\n";

	#------------------------------------------------------------------------
my $mtfn=();# my trip file name

if(-f "$tn"){ # Begin if(-f "$tn")
	# =================================================================================================
	# ============================ We calculate if the trip is on schedule ============================
	# ===================== We have the name of the trip dates: begining and, end of the trip =========
	# ===================== We have the time zone where the trip starts and end =======================
	# ===================== <DATETIME> ================================================================
	# =================================================================================================

	my $dt3 = DateTime->from_epoch( epoch => time() );# Current date format DateTime

	open(RTN,"$tn") or die ("$tn error $!");my @rtn=<RTN>;close(RTN) or die("$tn close error"); # RTN: read trip name file (contains Begin and end of trip)
	if (@rtn<2){ 
		print "<br><u>We didn't record yet the device finger print in <b>$tn</b></u>\n<br>";
		$tn=&do_untaint($tn);
		open(my $WOO,'>>'."$tn") || die("error $!");
		print $WOO "\n";
		print $WOO io::MySec::getsDFP;
		close($WOO) or die("$tn close error"); # RTN: read trip name file (contains Begin and end of trip)
		print "<br><u>We recorded the device finger print in <b>$tn</b></u>\n<br>";
		open(RTN,"$tn") or die ("$tn error $!");@rtn=<RTN>;close(RTN) or die("$tn close error"); # RTN: read trip name file (contains Begin and end of trip)

		# Email sent
		$ENV{PATH}='/bin:/usr/bin:/usr/local/bin';
		my $from = 'Bot from MAOP<shark.b@laposte.net>';
		my $to=&io::MyConstantBase::EADM->();
		my $subject = "Trip / Voyage: report/rapport " . uri_unescape($doc->param('maop_googid')); 
		$to=&do_untaint($to);
		$from=&do_untaint($from);
		$subject=&do_untaint($subject);
		my $mypath=&io::MyConstantBase::PATH_TO_SENDMAIL_OPT->();
		$mypath=&do_untaint($mypath);
		my $mylstrft= strftime '%Y-%m-%dT%H:%M:%S',gmtime;
		#strftime "%a %b %e %H:%M:%S %Y", localtime;# my local strft
		open(MAIL,"$mypath") || die("Error: $!");
		# Email Header
		print MAIL "To: $to\n";
		#print MAIL "To: sebastien.dorey\@laposte.net\n";
		print MAIL "From: $from\n";
		print MAIL "Subject: $subject\n";
		print MAIL "Content-Type: multipart/mixed; boundary=frontier\n";
		print MAIL "--frontier\n";
		print MAIL "Content-Type: text/html; charset=us-ascii\n";
		print MAIL "MIME-Version: 1.0\n\n";
		print MAIL "\n\n$mylstrft\n\n";
		print MAIL "<br>\n" ;
		print MAIL io::MySec::getsDFP ;
		print MAIL "<br>\n" . "Friendly yours,<br>Bot from MAOP";
		close(MAIL) || die("Error: $!");

		print "A mail to $to is being sent...\n<br>";
	}
	chomp($rtn[0]);my ($brtn,$ertn,$tntz_b,$tntz_e)=split(/\#/,$rtn[0]); # begining r... trip name,end r... trip name,trip name (time) zone begining,trip name (time) zone end
	my $my_finger_print=$rtn[1];chomp($my_finger_print);
	my $anal = DateTime::Format::Strptime->new( pattern => '%Y-%m-%dT%H:%M' ); # Analyzer
	my $dtb = $anal->parse_datetime( $brtn );

	# We set internal clock as the same time zone as the begining of the trip time zone
	$dt3->set_time_zone($tntz_b);

	if($dtb>$dt3){ # Begin if($dtb>$dt3)
		# date is not yet arrived
		print ">>>>>>>>>>>>>>>>>>>>>>>>>>> <u>$dt3</u><$dtb not passed\n";
		$rtrip='red'; # We record 
		$mtfn="_-" . &io::MyConstantBase::TRIP_NAME->(); 
	} # End if($dtb>$dt3)
	else{ # Begin else $dtb<=$dt3
		my $anal2 = DateTime::Format::Strptime->new( pattern => '%Y-%m-%dT%H:%M' ); # Analyzer
		my $dte = $anal2->parse_datetime( $ertn );

		# We set intenal clock as the same time zone as the end of the trip time zone
		$dt3->set_time_zone($tntz_e);

		if($dte<$dt3){ # Begin if($dte<$dt3)
			# date is passed
			$mtfn="_-" . &io::MyConstantBase::TRIP_NAME->(); 
		} # End if($dte<$dt3)
		else { # Begin  $dte>=$dt3
			my $dcfp = io::MySec::getsDFP;# We get the device finger print that is connecting

			if($dcfp eq $my_finger_print) { # Begin if($dcfp eq $my_finger_print)
				#print "<h1>We record $dtb<$dt3<$dte</h1></br>";
				$rtrip='#808080'; # We record 
				$mtfn="${mgidt}-" . &io::MyConstantBase::TRIP_NAME->(); 

				try { # Begin try
					# Getting info from the Weather center
					my $wfcu="http://api.wunderground.com/auto/wui/geo/WXCurrentObXML/index.xml?query=$lat,$lon";
					my $xml = new XML::Simple;
					my $wfc=get("$wfcu");

					open(my $WOO,'>'."$locweaf") || die("error $!");
					print $WOO $wfc;
					close($WOO) || die("error $!");
					#print "XXXXXXXXXXXXXXXXXXX><br>$wfc<br><XXXXXXXXXXXXXXXXXXXX<br>\n";
					my $data = $xml->XMLin("$locweaf") or die("error $locweaf $!");
				} # End try
				catch { # Begin catch
					if( -e "$locweaf"){ # Begin if( -e "$locweaf")
						unlink("$locweaf") or die("error $!");
					} # End if( -e "$locweaf")
				}; # End catch
			} # End if($dcfp eq $my_finger_print)
			else {
				$rtrip='red'; # We record 
				#print"<br>no record for this device<br>";
			}
		} # End  $dte>=$dt3
	} # End else $dtb<=$dt3
} # End if(-f "$tn")
else{ # Begin else
	#print uri_unescape($doc->param("maop_date"))." usual record\n<br>";
	$mtfn="_-" . &io::MyConstantBase::TRIP_NAME->(); 
} # End else
#------------------------------------------------------------------------

print "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n";
print "<html xmlns=\"http://www.w3.org/1999/xhtml\">\n";
print $doc->start_head();
#print "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=iso-8859-15\" />\n";
print "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" />\n";
print $doc->meta({
			-name=>"title",
			-content=>"Album of pictures/Album photos"
		})."\n";
print $doc->meta({ 
			-name=>"description", 
			-content=>"Album of pictures generated with a script/Album genere avec un script"
		})."\n" ;
print $doc->meta({ 
			-name=>"keywords", 
			-content=>"Merci, Thanks"
		})."\n" ;
#print $doc->meta({ 
		#-name=>"keywords", 
		#-content=>"quelque part sur la toile,somewhere on the net, album picture, album photo Sebastien Dorey, mere denis"
		#}) ;
print $doc->meta({ 
			-name=>"author", 
			-content=>"Sebastien DOREY aka shark bait"
		})."\n" ;

#print "++++===><br />";
my ($resPing,$ipOk)=(0,0); # stub io::MySec::checksRevIpAdd($mip,io::MySec::getsAllIPReceived); # Checks ping address
my %credentials;
$credentials{"my_pid"}=$my_pid;
$credentials{"service_from_param"}=uri_unescape($doc->param("maop_service")); # It is from prams
#print "(service_from_param,maop_service)=(".$credentials{"service_from_param"}.",".uri_unescape($doc->param("maop_service")).")<br>\n"; # It is from prams
$credentials{"service_value"}='check'; # It is from server
$credentials{"prev_pid_from_param"}=$my_pid;
$credentials{"user_login"}=$user_login;
$credentials{"login"}=$login;
$credentials{"user_password"}=$user_password;
$credentials{"password"}=$password;
$credentials{"doc"}= $doc;
$credentials{"album_pid_file"}=&io::MyConstantBase::CHECK_PID_SESSION->();

#print "<u>param to checks:</u> $my_pid,".uri_unescape($doc->param("maop_service")).", check, $my_pid, $user_login, $login, $user_password, $password, $doc,".&io::MyConstantBase::CHECK_PID_SESSION->()."\n<br>";
#my $resAuth=io::MyUtilities::check_password($my_pid,uri_unescape($doc->param("maop_service")), "check", "$my_pid", $user_login, $login, $user_password, $password, $doc,&io::MyConstantBase::CHECK_PID_SESSION->());
#print "Content-Type: test/html\n\n";
my $resAuth=io::MyUtilities::check_password(%credentials);
&loadDataTrips; # put security control
print &cascade_style_sheet_definition;

my @auaf=io::MyNav::gets_all_user_agent_fields;
if ( $an_action eq "modify" ){ # Begin if ($an_action eq "modify")
	# We print the administration menu of the album of pictures to modify a feature
	@info_on_picture=&return_info_picture;
} # End if ($an_action eq "modify")

# We get info from URL
my (
	$modify_page_position_in_album, $modify_position_in_page,
	$my_addrip,
	$modify_file_name,
	$modify_vertical_text, 		$modify_horizontal_text,        
	$modify_french_comment, 	$modify_english_comment,        
	$modify_halign,                 $modify_valign, 		
	$modify_position_from_the_image ,	$uris,
	$grant,				$tag	
) = @info_on_picture;

	#my $o=0; print "LIST<br>";foreach (@info_on_picture){ print "<u>$o.</u> $_<br>"; $o++; } print "<br>";


#print "<!-- 3 https://developer.mozilla.org/en/User_Agent_Strings_Reference    -->\n";
my $rul=uri_unescape($doc->param("rul")); # return of my upload

#print "<!-- 3.0 https://developer.mozilla.org/en/User_Agent_Strings_Reference    -->\n";
my @all_file=();
#print "<!-- 3.1212 https://developer.mozilla.org/en/User_Agent_Strings_Reference    -->\n";

#print "<!-- 3.2 https://developer.mozilla.org/en/User_Agent_Strings_Reference    -->\n";
#print "<script>document.write(\"connected with\"+navigator.userAgent);</script>\n";
if( -f "album/debug_album_DO_NOT_REMOVE"){ # Begin if( -f "album/debug_album_DO_NOT_REMOVE")
	#print "<br />\n---->res ping($resPing,$ipOk) for $mip<br />---$service---<br />";
} # End if( -f "album/debug_album_DO_NOT_REMOVE")
use Net::Domain qw(hostname hostfqdn hostdomain);
         
my @resa=split(/\n/,io::MySec::getsCoordinates(${mip}));# from ip address gets geoloc coordinates
#print "<!-- 3.3 https://developer.mozilla.org/en/User_Agent_Strings_Reference    -->\n";
my $l=();
foreach (@resa){
	chomp($_); # must desapeared (non sense due to previous split
	$l.="#$_"; # we create a line with fields separate with  ended with ,
}
@resa=split(/\#/,$l);
my $co=(split(/\:/,$resa[2]))[1];
my $cn=(split(/\:/,$resa[3]))[1];
my $cr=(split(/\:/,$resa[6]))[1];
my $ct=(split(/\:/,$resa[7]))[1];
my $lo=(split(/\:/,$resa[8]))[1];
my $la=(split(/\:/,$resa[9]))[1];
my $locid="$co/$cn/$cr/$ct/$lo/$la";
#print "The host name is $l --->$co-$cn-$cr-$ct-lo-la\n";


# print "Content-Type: text/html ; charset=UTF-8\n\n";


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

#print "<br>$$ >>>>>+++++>>>>>>>$resAuth<<<<<<<<br>$resPing<------delim<br>";
{
	open(REC,">>../rec.html")||die("Error $!");
	my $tft=gmtime(); #time for test
	print REC "<br>BEGIN < $0 > $tft<br>";
	foreach my $p ($doc->param){ # begin foreach my $p ($doc->param)
		print REC "($my_pid,$$)>>>>>>>$p --->".$doc->param($p)."<br>";
	} # end foreach my $p ($doc->param)
	print REC "<br>END < $0 > $tft<br>";
	close(REC)||die("Error:$!");
}
			
if ( ($resPing==0) && ($resAuth==0) ){ # Begin if ( ($resPing==0) && ($resAuth==0) ) 
	$user_password=""; # we remove password because of pid and prev pid
	$password=""; # we remove password because of pid and prev pid
	print $doc->title("album ${service} admin interface");
	print $doc->end_head();
	my $recor=uri_unescape($doc->param("maop_recording"));
	chomp($recor);
	open( R, "$file_conf_to_save" ) || error_raised( $doc, "File [$file_conf_to_save] not found!!!" );
	@all_file=<R>;
	close(R)||die("Error: $!");
	print '<body onload="JavaScript:show();">'."\n".  '<div id="myDemo">popoopopo</div>'."\n" ;
	&main_menu(
		"Menu pour administration. / Administration menu.",
		"Choisir une page et un rang pour placer l'image. / Choose a page and a raw for the image.",
		"Choisir une image. / Choose an image.",
		"Entrer le(s) mot(s) (versions Français et Anglais) et &agrave; cot&eacute; son lien pour que ce dernier aparaissent dans le Cyber Album sous forme de lien dans le commentaire. / Enter words to link in message (French, English versions) in order to make links show up in message when Cyber Album is watched.",
		"Choisir les options de placement. / Choose options for positions.",
		"Mettre les commentaires. / Write comments."
		);

	my $ssection=uri_unescape($doc->param("maop_ssection")) ; # Gets login
	chomp($ssection);
	if(length($ssection)==0){ # Begin if(length($$section)==0)
		#print "1111111111111111111111111></br>";
		&firstChoicetMenuadmin ; # Create a pre admin first menu choice
	} # End if(length($$section)==0)
	elsif($ssection=~m/adminGroup/){ # Begin elsif($ssection=~m/adminGroup/)
		print "00000000000000000000></br>";
		&setGoogleID(&io::MyConstantBase::PATH_GOOGLE_MAP_ID->(),uri_unescape($doc->param("maop_googid"))) ; # Stuff about google ID map
		&groupAndStuff ; # Stuff about groups
	} # End elsif($ssection=~m/adminGroup/)
	elsif($ssection=~m/adminGroupModif/){ # Begin elsif($ssection=~m/adminGroup/)
		&setGoogleID(&io::MyConstantBase::PATH_GOOGLE_MAP_ID->(),uri_unescape($doc->param("maop_googid"))) ; # Stuff about google ID map
		&groupAndStuff ; # Stuff about groups
	} # End elsif($ssection=~m/adminGroupModif/)
	elsif($ssection=~m/adminGoogleID/){ # Begin elsif($ssection=~m/adminGoogleID/)
		#print "toto 2 l er ret";
		&setGoogleID(&io::MyConstantBase::PATH_GOOGLE_MAP_ID->(),uri_unescape($doc->param("maop_googid"))) ; # Stuff about google ID map
		&firstChoicetMenuadmin ; # Create am pre admin first menu choice
	} # End elsif($ssection=~m/adminGoogleID/)
	elsif($ssection=~m/adminPict/){ # Begin elsif($ssection=~m/adminPict/)
		# That's where info are uploaded
		if ( $an_action ne "record_modify" ){ # Begin if ($an_action ne "record_modify")
			if ( $upload eq "ok" ){ # Begin if ($upload eq "ok")
				my $type_upload=uri_unescape($doc->param("maop_type_of_upload"));

				# We use this option in order to make a difference between an image linked to a web site and an image localy uploaded
				if ( $type_upload eq "Local" ){ # Begin if ($type_upload eq "Local")
					    # When upload raised a new window with info
				    #open( W, ">album/dec" ) || error_raised( $doc, "File [$file_conf_to_save] not found!!!" );
				    #	print W ".";
				    #	close(W);
					##&raised_upload_window;
					if(length(uri_unescape($doc->param("maop_file_name_img")))>0){ # Begin if(length(uri_unescape($doc->param("maop_file_name_img")))>0)
						# watch out case for youtube
						$rul=$doc->param('maop_final2');
						#	io::gut::machine::MyFile::my_upload($doc, uri_unescape($doc->param("maop_file_name_img")), &io::MyConstantBase::DIRECTORY_DEPOSIT->(), "${timsec}$$",&io::MyConstantBase::ALLOWED_FILE_FORMAT_TYPE->());
					} # End if(length(uri_unescape($doc->param("maop_file_name_img")))>0)
				} # End if ($type_upload eq "Local")
			} # End if ($upload eq "ok")
		} # End if ($an_action ne "record_modify")

		# Record information on disk
		if ((( uri_unescape($doc->param("maop_file_name_img")) ne "" ) && ( uri_unescape($doc->param("maop_file_name_img2")) eq "" ) )
			|| (( uri_unescape($doc->param("maop_file_name_img2")) ne "" ) && ( uri_unescape($doc->param("maop_file_name_img")) eq "" ) )
			|| ( $an_action eq "record_modify" ) ){ #  Begin if ( (uri_unescape($doc->param("maop_file_name_img")) ne "") || ($an_action eq "record_modify") )
			if ( $recor eq "check" ){ #  Begin if ($recor eq "check")
				if($rul==0){ # Begin if($rul==0) 
					&record;
				} # End if($rul==0)
				else{ # Begin else
					print "<br />Picture not recorded<br />"
				} # End else
			} # End if ($recor eq "check")
		} # End if ( (uri_unescape($doc->param("maop_file_name_img")) ne "") || ($an_action eq "record_modify") )
		else{ # Begin else
			print "<br />Picture not recorded<br />"
		} # End else
		
		# We remove a feature from the list
		if ( $an_action eq "remove" ){ # Begin if ($an_action eq "remove")
			print $doc->p( "<br /><br /><br /><br />Picture will be removed from page "
				. uri_unescape($doc->param("maop_page"))
				. " line "
				. uri_unescape($doc->param("maop_line")) );
			# transcodint char - to ascii value
			#$file_name=~s!\-!&#45;!g;
			&remove_picture(uri_unescape($doc->param("maop_page")),uri_unescape($doc->param("maop_line")));
		} # End if ($an_action eq "remove")

		&menu_admin_title();
		&menu_leave_admin;
		
		print "\n<form action='${main_prog}?maop_service=auth\&maop_upld=ok' method='post' name=\"adminMenu\"  enctype='multipart/form-data'>\n";
		print "<input type='hidden' name='maop_prev_id' value='$$' />";
		print "<table width=\"100%\" border=\"0\">\n" . 
			"<tr>\n<td width=22% bgcolor='#CFD3F6' align='left' valign='top'>\n";

		# We show the list of pictures that are already taken
		print &accessToPicture;
		&shows_page_not_taken_yet;
		print "<td align='left' valign='top' bgcolor='#CFD3F6'>\n";

		print 
		      $doc->start_table( 
					{-width=>"100%" , -border=>0},
		            $doc->Tr(
			    		[
					   $doc->td(
					             { 
					              -class=>"configuration"
						     },
						     "Configure image position"
						    )
				        ]
				      ) ) ; #</tr></table>\n";
		&admin_menu( "Set position of the image in compartment", "Set position of the text from the image in compartment" );
		print $doc->br() . $doc->start_center();
		&go_back;
		print $doc->end_center();

		# We show the list of pictures of the album with caracteristics
		&shows_list_pictures;
		print $doc->end_table($doc->end_Tr());
		print "</tr>\n</table>\n";
	} # End elsif($ssection=~m/adminPict/)
} # End if ( ($resPing==0) && ($resAuth==0) )
elsif ( 
	    ($resPing==0) && 
	(${service} eq "auth")
      ){
          # Begin elsif (
	  #              ($resPing==0) && 
          #              ( $resPing==0 && ${service} eq "auth" )
	  #             )
	print $doc->title("album ${service}");
	#print "    </head>\n";
	print $doc->end_head();
	print "<body onload=\"JavaScript:show()\">\n";
	&main_menu(
			"Aide pour l'authentification / Authentication menu help",
			"Entrer l'identifiant et le mot de passe. / Enter login and password."
		);

	# We print the main title of authentication menu
	&auth_menu;
} # End elsif (
  #              (io::MyNav::checksRevIpAdd("${mip}")==0) && 
  #              ( $resPing==0 && ${service} eq "auth" )
  #             )
elsif ( ${service} eq "showPict" ){ # Begin elsif ( ${service} eq "showPict" )
	# shows picture enlarged
	my $separator=uri_unescape($doc->param("maop_comments"));

	$separator=~s!SEPARATOR!] / [!g;
	print "\n    <title>album ${service} section; comment [${separator}] pict enlarged</title>\n";
	print "    </head>\n";
	&main_help_menu_css;
	print '<body onload="JavaScript:show();" <!-- toto 2 le retour --> >'."\n";
	# We print the choosen picture on the screen, with comments.
	&print_pictures;
	if("$authorized" eq "ok"){ # Begin if("$authorized" eq "ok")
		print io::MyTime::gets_formated_date."<br />\n";
		print "<script  language=\"javascript\" type=\"text/javascript\">\nvar d = new Date();\ndocument.write(d);\n</script>\n";
	} # End if("$authorized" eq "ok")
} # End elsif ( ${service} eq "showPict" )
else { # Begin else 
#print "<!-- 5 https://developer.mozilla.org/en/User_Agent_Strings_Reference    -->\n";
	my $u="";
	my $locpa=((uri_unescape($doc->param("maop_page"))=~m/[0-9]+/) ? uri_unescape($doc->param("maop_page")) : 1 );

	&create_dir;# Creates infrastructure directories,...
	# We create a directory if it does not exists
#print "<!-- 94111115 https://developer.mozilla.org/en/User_Agent_Strings_Reference    -->\n";
	my ($a,$main_page)=&print_page;
#print "<!-- 44111115 https://developer.mozilla.org/en/User_Agent_Strings_Reference    -->\n";
	#print $doc->script( { -language => "javascript" ,
	print "<script language=\"javascript\" type=\"text/javascript\" >";
	print "//<![CDATA[\nfunction listOfPages(){\n".'document.write("' . $a . '");'."\n}\n//]]>\n".
	      "\n</script>\n" . $doc->title("album's page ".uri_unescape($doc->param('maop_googid'))) ; 
#	) .
	#$doc->end_head() .
	#print "\n</script>";
	print "</head>";
	print "<body onload=\"JavaScript:show();\" >" ;
	#&create_dir;# Creates infrastructure directories,...
	#print "<!-- 2111115 https://developer.mozilla.org/en/User_Agent_Strings_Reference    -->\n";
	&main_help_menu_css("$u");
#print "<!-- 1111115 https://developer.mozilla.org/en/User_Agent_Strings_Reference    -->\n";
	print $main_page;
	my $oppp=io::MyTime::gets_formated_date;
	my $llll_l="";
	#print "------------weather----------------->$locweaf<br>";
	my @llll_res=($lon,$lat,$mtfn,(-e "$locweaf") ? "$locweaf" : "-",$date_ticket);# from ip address gets geoloc coordinates, trip name,weather stuff
	foreach (@llll_res){ # Begin foreach (@llll_res)
		chomp($_);# must desapeared (non sense due to previous split
		if (length($llll_l)==0){ # Begin if (length($llll_l)==0) 
			$llll_l.="$_";# fill fields + concatenation with previous data
		} # End if (length($llll_l)==0) 
		else{ # Begin else
			$llll_l.="#$_";# fill fields + concatenation with previous data
		} # End else
	} # End foreach (@llll_res)
	#$llll_res[6]=~s/[^:]*://g;
	#$llll_res[7]=~s/[^:]*://g;
	set_history(${mip}, $oppp,$locpa ,"$mip",$llll_l,&io::MyConstantBase::ALBUM_INFO_HIST_DIRECTORY->());
	# Dealing with tweeter
	#my $llll_inf="[$llll_res[6],$llll_res[7]]";
	#system("`pwd`/tweet.sh \"Sh4rkb41t\" \"lakpwr\"  \"[album] $oppp page:$locpa $llll_inf\""); 
	if("$authorized" eq "ok"){ # Begin if("$authorized" eq "ok")
		print DateTime::TimeZone->new( name => 'local' )->name() ; 
		print "<script  language=\"javascript\" type='text/javascript'>\nvar d = new Date();\ndocument.write(d+' '+d.getTimezoneOffset()+\"<br>\");\n</script>\n";
	} # End if("$authorized" eq "ok")
} # End else

#print "<!-- 000000000005 https://developer.mozilla.org/en/User_Agent_Strings_Reference    -->\n";
# Footer is here because it is printed from here on all pages without modifying other page structures
#&showsStats;
#print "zzzzzzzzzzzzzzzzzz<br />";
print "<br /><br />" . io::MyUtilities::footer($doc, 
						 &io::MyConstantBase::DIRECTORY_DEPOSIT->() . "powered.gif",
						 &io::MyConstantBase::DIRECTORY_DEPOSIT->() . "jangada.gif",
						 "http://www.perl.org",
						 ALBUM_VERSION,
						 &io::MyConstantBase::TESTED_WITH_BROWSERS->(),
						 &io::MyConstantBase::HOSTED_BY->(),
						 &io::MyConstantBase::HOSTED_BY_URL->());
print <<EE;
</div>

</body>
</html>
EE

=head1 sub raised_upload_window(...)

When the upload action is done, a new window is raised on the screen with info related to upload. This info now is the upload percent of the image file processing to directory.

=head2 PARAMETER(S)

=over 4

=over 4

None.

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

Returns directory path.

=back

=back

=head2 ERRROR RETURNED

=over 4

=over 4

-1

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

- I<Last modification:> Mar 04 2005

- I<Created on:> Mar 03 2005

=back

=back

=cut

sub raised_upload_window { # Begin raised_upload_window
	print "<script  language=\"javascript\" type=\"text/javascript\">\nwindow.open('bar.cgi','smallwin','bgcolor=blue,width=550,height=200,status=no,resizable=no');\n</script >\n";
} # End sub raised_upload_window

=head1 sub menu_leave_admin(...)

This function helps user to leave admin menu by creating a button on the screen.

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

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jul 25 2009: intermediate menu added. Go back to intermediate menu.

- I<Last modification:> Feb 25 2006

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back

=cut

sub menu_leave_admin { # Begin menu_leave_admin
	my $login=uri_unescape($doc->param("maop_login")) ; # Gets login
	my $password=uri_unescape($doc->param("maop_password")) ; # Gets login

	print <<MENU;
<form action='${main_prog}?maop_service=auth&maop_upld=ok' method='post' name="maop_adminMenu" enctype='multipart/form-data'>
	<input type='hidden' name='maop_prev_id' value='$$' />
	<input type='hidden' name='maop_login' value='$login' />
	<input type='hidden' name='maop_remPid' value='ok' />
	<input type='hidden' name='maop_service' value='check' />
	<input type='submit' value='Retour au menu principal/Back to main menu' />
</form>
MENU
} # End sub menu_leave_admin

=head1 sub print_info_picture(...)

This function is used to print information related to picture.

=head2 PARAMETER(S)

=over 4

$rank: that's the rank of the picture in the page of one album.

$img: that's the image name.

=back

=head2 RETURNED VALUE

=over 4

None.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Oct 14 2006

- I<Created on:> Oct 14 2006

=back

=cut

sub print_info_picture { # Begin print_info_picture
	my ($rank,$img)=@_;
	return "";
	my $comment=uri_unescape($doc->param('maop_comments'));
	my ( $french, $english )=split( /SEPARATOR/, $comment );
	my $uuu= &io::MyConstantBase::DIRECTORY_DEPOSIT->() ."$img";
	chomp($uuu);
	my (@stat_img)= stat $uuu;
	my ($num_of_pict,$size_of_all_picture_gathered)=&gets_current_images_information_from_current_album("$file_conf_to_save");

	my $return1 =
	#	"Nom photo/<font color='#822942'>Picture name</font> $img<br />" .
	"* Taille photo sur &eacute;cran/<font color='#822942'>Picture size on the screen</font> \" + document.images[ $rank - 1].width + \"x\"+ document.images[ $rank - 1].height + \" px<br />" .
	"* Taille fichier/<font color='#822942'>File size</font> $stat_img[7] byte(s).<br />";

	return $return1;
} # End sub print_info_picture

=head1 sub print_pictures(...)

This function is used to print bigger picture.

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

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Sep 05 2006

- I<Last modification:> Fev 14 2006

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back

=cut

sub print_pictures { # Begin print_pictures
	my $img     = uri_unescape($doc->param('maop_pict'));
	my $comment=uri_unescape($doc->param('maop_comments'));
	my ( $french, $english )=split( /SEPARATOR/, $comment );
	my (@stat_img)=stat $img;

print "<!-- 22221 https://developer.mozilla.org/en/User_Agent_Strings_Reference    -->\n";

	$french=&switch_from_a_specified_tag_to_characters($french);
	$english=&switch_from_a_specified_tag_to_characters($english);

	if("$authorized" eq "ok"){ # Begin if("$authorized" eq "ok")
		print "<br /><br /><br /><center><img src='$img' alt='p' /><br />$french\n ";
		print "<br />/<br /><font color='#822942'>$english</font>\n";
	} else {
		print "<br /><br /><br /><center>Image innaccessible<br />\n ";
		print "<br />/<br /><font color='#822942'>Picture unreachable</font>\n";
	}
	print "</center>\n";
print "<!-- 22221 https://developer.mozilla.org/en/User_Agent_Strings_Reference    -->\n";
	print "<script  language=\"javascript\" type=\"text/javascript\">\n";
	print "   document.write(\"<br /><p style='font-size: 10pt; font-weight: lighter; font-style: oblique;'>\");\n";

	print "   document.write(\"Hauteur/<font color='#822942'>Height</font> \" + document.images[1].height + \"px; \");\n";
	print "   document.write(\"Largeur/<font color='#822942'>Width</font> \" + document.images[1].width + \"px.<br />\");\n";
	print "   document.write(\"Taille/<font color='#822942'>Size</font> $stat_img[7]byte(s).</p>\");\n";
	print "</script>\n";
	my ($num_of_pict,$size_of_all_picture_gathered)=&gets_current_images_information_from_current_album("$file_conf_to_save");
	print "</p><br /><br /><br />\n<a  href='javaScript:history.back()'  >Back</a> previous page\n<br />";
} # End sub print_pictures

=head1 sub create_new_page(...)

This function is called when a new page is asked to be created.

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

New page created.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:>  Nov 10 2004

- I<Created on:> Nov 10 2004

=back

=cut

sub create_new_page { # Begin create_new_page
	open( R, "$file_conf_to_save" ) or error_raised("File $file_conf_to_save does not exists");
	my @f=<R>;
	close(R) or error_raised("File $file_conf_to_save does not exists");
	my $line=();

	if ( scalar(@f) != 0 ){ # Begin if (scalar(@f) != 0)
		my $value_not_exist=1;

		foreach (@f){ # Begin foreach (@f)
			$line=$_;
		} # End foreach (@f)
		chomp($line);

		my @tmp_line=split( /\/\//, $line );
		$tmp_line[0]++;
		return "$tmp_line[0]||1";
	} # End if (scalar(@f) != 0)
	else { # Begin else
		return "1||1";
	} # End else
} # End sub create_new_page


=head1 sub add_new_col(...)

This function is creates new column in db

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

none.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:>  Jul 05 2008

- I<Created on:> May 25 2008

=back

=cut

sub add_new_col { # Begin add_new_col
	my $col;
	if( ! -f "$file_conf_to_save.nb_col" ){ # Begin if( ! -f "$file_conf_to_save.nb_col" )
		open( W, ">$file_conf_to_save.nb_col" ) or error_raised("File $file_conf_to_save does not exists");
		print W MAX_COL_NUMBER->();
		close(W) or error_raised("File $file_conf_to_save does not exists");
	} # End if( ! -f "$file_conf_to_save.nb_col" )
	else { # Begin else
		open( R, "$file_conf_to_save.nb_col" ) or error_raised("File $file_conf_to_save does not exists");
		my @u=<R>;
		close(R) or error_raised("File $file_conf_to_save does not exists");
		$col=(split(/\n/,@u))[0];
	} # End else
	if($col<MAX_COL_NUMBER->()){ # Begin if($col<MAX_COL_NUMBER->())
		open( R, "$file_conf_to_save" ) or error_raised("File $file_conf_to_save does not exists");
		my @f=<R>;
		close(R) or error_raised("File $file_conf_to_save does not exists");
		my $line=();

		if ( scalar(@f) != 0 ){ # Begin if (scalar(@f) != 0)
			my $value_not_exist=1;
			my @k=();

			open( W, ">$file_conf_to_save.ok" ) or error_raised("File $file_conf_to_save does not exists");
			foreach (@f){ # Begin foreach (@f)
				chomp($_);
				$line=$_;
				my @z=split(/\|\|/,$_);
				my $nb=scalar(@z)-1;
				if($nb>0){ # Begin if($nb>0)
					for(my $i=$nb;$i<=MAX_COL_NUMBER->();$i++){ # Begin for(my $i=$nb;$i<MAX_COL_NUMBER->();$i++)
						$line="$line||.";
					} # End for(my $i=$nb;$i<MAX_COL_NUMBER->();$i++)
					print W "$line\n";
				} # End if($nb>0)
			} # End foreach (@f)
			close(W) or error_raised("File $file_conf_to_save does not exists");
			open( D, "$file_conf_to_save.ok" ) or error_raised("File $file_conf_to_save does not exists");
			my @v=<D>;
			close(D) or error_raised("File $file_conf_to_save does not exists");
			open( M, ">$file_conf_to_save" ) or error_raised("File $file_conf_to_save does not exists");
			foreach (@v){ # Begin foreach (@v)
				#print  "-->$_";
				print M "$_";
			} # End foreach (@v)
			close(M) or error_raised("File $file_conf_to_save does not exists");
		} # End if (scalar(@f) != 0)
	} # End if($col<MAX_COL_NUMBER->())
	return 0;
} # End sub add_new_col

=head1 sub number_of_pages(...)

This function calculates number of pages to show on the screen when a user inserts, or modifies a picture.

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

Number of pages.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Nov 10 2004

- I<Created on:>  Nov 10 2004

=back

=cut

sub number_of_pages { # Begin number_of_pages
	open( R, "$file_conf_to_save" );
	my @all_file=<R>;
	close(R);
	my $num=( ( split( /\|\|/, $all_file[ scalar(@all_file) - 1 ] ) )[0] );
	return ( ( "$num" eq "" ) ? 0 : $num );
} # End sub number_of_pages

=head1 sub go_back(...)

This function helps the user to go back on a previous page.

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

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:>  Jun 22 2011: bug solved

- I<Last modification:>  Feb 25 2006

- I<Last modification:>  Nov 10 2004

- I<Created on:> Nov 10 2004

=back

=cut

sub go_back { # Begin go_back
	print <<MNU;
	<form action='${main_prog}' method='post'>
		<input type='hidden' name='maop_prev_id' value='$$' />
		<input type='hidden' name='maop_login' value='$login' />
		<input type='hidden' name='maop_remPid' value='ok' />
		<input type='hidden' name='maop_service' value='check' />
		<input type='submit' value='Menu principal / Go back to main menu' />
	</form>
MNU
} # End sub go_back

=head1 sub menu_page_title(...)

This function sets up the menu page title.

=head2 PARAMETER(S)

=over 4

$title: Enter title of the menu.

=back

=head2 RETURNED VALUE

=over 4

The title.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Sep 10 2009: refarmatted the html code.

- I<Last modification:> Jan 27 2006

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back

=cut

sub menu_page_title { # Begin menu_page_title
	my ( $title, $num_page )=@_;

	return $doc->center(
				"<h1>$title<br/>\n$num_page</h1>"
				) . "<br /><br />" ;
} # End sub menu_page_title

=head1 sub menu_admin_title(...)

This function creates menu admin.

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

Admin menu.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 NOTES

=over 4

Name's changed from menu_admin to menu_admin_title.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jan 27 2006.

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back

=cut

sub menu_admin_title { # Begin menu_admin_title
	print &menu_page_title( $doc->br() . "ADMINISTRATION DES PHOTOS" . $doc->br() . $doc->font( { -color => 'blue' } , "ADMINISTRATION OF PICTURES") . $doc->br .'<p id="inf"></p>');
} # End sub menu_admin_title

=head1 sub  admin_menu(...)

This function manages the menu in order to insert a new page. A page must have a fixed length of image per it.

=head2 PARAMETER(S)

=over 4

@line_title: that's the line title for each pictures.

=back

=head2 RETURNED VALUE

=over 4

None.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Fev 25 2006

- I<Last modification:> Jan 20 2005

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back

=cut

sub admin_menu { # Begin admin_menu
	my (@line_title)=@_;
	my ($num_of_pict,$size_of_all_picture_gathered)=&gets_current_images_information_from_current_album("$file_conf_to_save");

	print "<p style='font-size: 10pt; font-weight: lighter; font-style: oblique;'>\n";
	print "Somme de toutes les tailles des images de l'album / <font color='#822942'>Sum of all picture sizes in the album</font> $size_of_all_picture_gathered byte(s)\n<br />\n";
	print "$num_of_pict photo(s) stokee(s) / <font color='#822942'>picture(s) stored</font>.\n";
	print "<table border=\"1\">\n";
	&set_upload;
	&set_link;
	if ( $an_action ne "modify" ){ # Begin  if ($an_action ne "modify")
		my $num=&number_of_pages;
		foreach my $l_title (@line_title){ # Begin foreach @line_title
			print "<tr>\n<td align='left' valign='top'>\n";
			&manage_position( 
						(&number_of_pages),
						$l_title ,
						( # position of image
							(length($modify_valign)==0) ?
								uri_unescape($doc->param("maop_vertical")):
								$modify_valign
						),
						( # position of image
							(length($modify_halign)==0) ?
								uri_unescape($doc->param("maop_horizontal")):
								$modify_halign
						),
						( # position of text from image (separated compartment)
							(length($modify_position_from_the_image)==0) ?	
								uri_unescape($doc->param("maop_Set_position_of_the_text_from_the_image_in_compartment")): 
								$modify_position_from_the_image
						),
						( # position of text in its compartment
							(length($modify_vertical_text)==0) ?
								uri_unescape($doc->param("maop_vertical_text")):
								$modify_vertical_text
						),
						(
							(length($modify_horizontal_text)==0) ?
								uri_unescape($doc->param("maop_horizontal_text")):
								$modify_horizontal_text
						)
					);
			#            &manage_position( (&number_of_pages), $l_title );
			print "</tr>\n";
		} # End foreach @line_title
	} # End  if ($an_action ne "modify")
	else { # Begin  else of if ($an_action ne "modify")
		my $num=&number_of_pages;
		foreach my $l_title (@line_title){ # Begin foreach @line_title
			print "<tr>\n<td align='left' valign='top'>\n";
			&manage_position( 
						(&number_of_pages),
						$l_title ,
						( # position of image
							(length($modify_valign)==0) ?
								uri_unescape($doc->param("maop_vertical")):
								$modify_valign
						),
						( # position of image
							(length($modify_halign)==0) ?
								uri_unescape($doc->param("maop_horizontal")):
								$modify_halign
						),
						( # position of text from image (separated compartment)
							(length($modify_position_from_the_image)==0) ?	
								uri_unescape($doc->param("maop_Set_position_of_the_text_from_the_image_in_compartment")): 
								$modify_position_from_the_image
						),
						( # position of text in its compartment
							(length($modify_vertical_text)==0) ?
								uri_unescape($doc->param("maop_vertical_text")):
								$modify_vertical_text
						),
						(
							(length($modify_horizontal_text)==0) ?
								uri_unescape($doc->param("maop_horizontal_text")):
								$modify_horizontal_text
						)
					);
			#            &manage_position( (&number_of_pages), $l_title );
			print "</tr>\n";
		} # End foreach @line_title
		print "<input type='hidden' name='maop_page' value='$modify_page_position_in_album' />\n";
		print "<input type='hidden' name='maop_line' value='$modify_position_in_page' />\n";
		print "<input type='hidden' name='maop_file_name_img' value='$modify_file_name' />\n";
	} # End  if ($an_action ne "modify")
	&set_language(&io::MyConstantBase::LANGUAGES->());
	print $doc->Tr(
		$doc->td( {align=>'right'},"\n".
			#$doc->input({ type=>'hidden', name=>'maop_prev_id', value=>"$$"})."\n<!-- myabbaracada -->",
			$doc->input({ type=>'hidden', name=>'maop_login', value=>uri_unescape($doc->param("maop_login"))})."\n",
			$doc->input({ type=>'hidden', name=>'maop_remPid', value=>'ok'})."\n",
			$doc->input({ type=>'hidden', name=>'maop_service', value=>'check'})."\n",

			$doc->input({ type=>'hidden', name=>'maop_upld', value=>'ok'})."\n",
			$doc->input({ type=>'hidden', name=>'maop_Set_page_position_in_the_album', value=>"Page #$modify_page_position_in_album @ row #$modify_position_in_page"})."\n",
			$doc->input({ type=>'hidden', name=>'maop_ssection', value=>'adminPict'})."\n",
			$doc->input({ type=>'hidden', name=>'maop_recording', value=>'check' })."\n",
			$doc->input({ type=>'submit', value=>'Envoyer la requete / Send query' } ))."\n",
		$doc->td($doc->input({ type=>'reset', value=>'Annuler / Reset'})))."\n";
	print "</table>\n";
	print "</form>\n";
} # End sub admin_menu

=head1 sub set_upload(...)

This function sets upload button in menu. It manages all upload.

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

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Sept 21 2008

- I<Last modification:> Aug 20 2008

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back

=cut

sub set_upload { # Begin set_upload
	if ( $an_action ne "modify" ){ # Begin if ($an_action ne "modify")
		print "<tr>\n<td>Enter file name to upload from\n" .
															$doc->popup_menu(
																	 -name=>'maop_type_of_upload',
																	 -values=>[
																			'Local',
																			'http:/'
																		  ],
																	 -defaults=>[
																			'Local'
																		    ]
																       ) .
															"<td><input type=\"file\" name='maop_file_name_img' size='50' />\n";

		print "<script language='javascript' type='text/javascript'>\n";
		print "gti();";
		print "</script>\n";
		print "<tr>\n<td>Enter URL here if http option above is choosen<td><input type=\"text\" name='maop_file_name_img2' size='50' />\n";
		print "Printed/Imprime<select name=\"maop_youtubeln\"><option selected>normal</option><option>link/lien</option></select>";
	} # End if ($an_action ne "modify")
} # End sub set_upload

=head1 sub set_link(...)

This function sets a link (optional) within French text or English text when asked in admin menu.

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

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jul 4 2012 $info_on_picture[11] changed befaore it was 10 

- I<Last modification:> Feb 2 2006

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back

=cut

sub set_link { # Begin set_link
	chomp( $info_on_picture[11] );
	$info_on_picture[11]=~s/[\(\)]//g;
	my ( $fr, $eng )=split( /\;/, $info_on_picture[11] ); # we take last field (french and english comment and link)
	my ( $words,     $link )     = split( /\,/, $fr );
	my ( $words_eng, $link_eng )=split( /\,/, $eng );

	print "<tr>\n<td valign='top' aglign=left>Enter a name to link within the text for French comment </td><td><table><tr>\n<td><input name='maop_name_to_link' value='$words' /><td>Enter the related link<input type='text' name='maop_link' value='$link' /></tr>\n</table>\n</tr>\n";
	print "<tr>\n<td valign='top' aglign=left>Enter a name to link within the text for English comment</td>\n<td>\n<table><tr>\n<td><input name='maop_name_to_link_eng' value='$words_eng' /></td><td>Enter the related link for eng<input type='text' name='maop_link_eng' value='$link_eng' /></tr>\n</table>\n</tr>\n";
} # End sub set_link

=head1 sub set_language(...)

This function sets language(s).

=head2 PARAMETER(S)

=over 4

@languages: that's the list of languages that can be set up.

=back

=head2 RETURNED VALUE

=over 4

None.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back

=cut

sub set_language { # Begin set_language
	my @languages=@_;
	my $comment   = ();

	foreach my $lng (@languages){ # Begin foreach @languages
		if ( $lng=~m/french/i ){ # Begin if ($lng=~m/french/i)
			$comment=$modify_french_comment;
		} # End if ($lng=~m/french/i)
		elsif ( $lng=~m/english/i ){ # Begin elsif ($lng=~m/english/i)
			$comment=$modify_english_comment;
		} # End elsif ($lng=~m/english/i)
		$comment=&switch_from_a_specified_tag_to_characters($comment);
		$comment=~s/\'/\&\#145/g;
		$comment=~s/\"/\&\#147/g;
		print "<tr>\n<td>Comment of the picture in $lng </td>\n<td><input type='text' size=50 name='maop_lang_${lng}_comment' value=\"$comment\" /></tr>\n<br />\n";
	} # End foreach @languages
	if ( $an_action eq "modify" ){ # Begin if ($an_action eq "modify")
		print "<input type='hidden' name='maop_action' value='record_modify' />\n";
	} # End if ($an_action eq "modify")
} # End sub set_language

=head1 sub manage_position(...)

This function manages different positions in the picture album.

=head2 PARAMETER(S)

=over 4

$number_of_page: that's the number of page.

$line: that's the line.

$image_vertical: possible position values are top middle bottom.

$image_horizontal: possible position values are left center right.

$text_position: that's the position from the image.

$vertical_text_position: position possible values are top middle bottom.

$horizontal_text_position: position possible values are left center right.

=back

=head2 RETURNED VALUE

=over 4

None.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jul 15 2012 Synchro with data base not up to snuff. Correction done but still yet error(s) occur(s).

- I<Last modification:> Sep 08 2011 problem with positionnning added.

- I<Last modification:> Sep 08 2006

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back

=cut

sub manage_position { # Begin manage_position
	my (
		$number_of_page,
		$line,
		$image_vertical,
		$image_horizontal,
		$text_position,
		$vertical_text_position,
		$horizontal_text_position)=@_;
	my $select_name=$line;

	#    print "$line,$image_vertical,$image_horizontal,$text_postion,$vertical_text_position,$horizontal_text_position<br />\n";

	$select_name=~s/\ +/_/g;
	print "$line<td>\n";
	print "<table border=\"0\" width=\"100%\">\n<tr>\n<td valign='top' align='right'>";
	if( $line=~m!text from the image! ){ # Begin if ($line=~m!text from the image!)
		print "<select name='maop_$select_name'>\n";
		if ($text_position =~ m/Left side of the image/){ # Begin if ($text_position =~ m/Left side of the image/)
			print 
				"<option selected>Left side of the image</option>\n" .
				"<option>Right side of the image</option>\n" .
				"</select></tr>\n";
		} # End if ($text_position =~ m/Left side of the image/)
		else { # Begin else
			print 
				"<option selected>Right side of the image</option>\n" .
				"<option>Left side of the image</option>\n" .
				"</select></tr>\n";
		} # End else
		print "<tr>\n<td align='left' valign='top'>${image_vertical}--- Vertical ";
		print "<select name='maop_vertical_text'>\n";
		if ($image_vertical !~ m/(top|middle|bottom)/i){ # Begin if ($image_vertical !~ m/(top|middle|bottom)/i)
			print "<option selected>top</option>\n";
			print "<option>middle</option>\n";
			print "<option>bottom</option>\n";
		} # End if ($image_vertical !~ m/(top|middle|bottom)/i)
		else { # Begin else
			print "<option".&set_select_tag('top'   ,"$image_vertical").">top</option>\n";
			print "<option".&set_select_tag('middle',"$image_vertical").">middle</option>\n";
			print "<option".&set_select_tag('bottom',"$image_vertical").">bottom</option>\n";
		} # End else
		print "</select>\n<td>\n";
		print "Horizontal ";
		print "****$image_horizontal***---<select name='maop_horizontal_text'>\n";
		if ($image_horizontal !~ m/(left|center|right)/i){ # Begin if ($image_vertical !~ m/(left|center|right)/i)
			print "<option selected>left</option>\n";
			print "<option>center</option>\n";
			print "<option>right</option>\n";
			print "<option>justify</option>\n";
		} # End if ($image_vertical !~ m/(left|center|right)/i)
		else { # Begin else
			print "<option".&set_select_tag('left'  ,"$image_horizontal").">left</option>\n";
			print "<option".&set_select_tag('center',"$image_horizontal").">center</option>\n";
			print "<option".&set_select_tag('right' ,"$image_horizontal").">right</option>\n";
			print "<option>justify</option>\n";
		} # End else
		print "</select>\n";
	} # End if ($line=~m!text from the image!)
	elsif ( $line=~m!position of the image!i ){ # Begin elsif ( $line=~m!position of the image!i )
		print "<td valign='top' align='left'>Vertical ";
		print "-------$vertical_text_position-----<select name='maop_vertical'>\n";
		if ($vertical_text_position !~ m/(top|middle|bottom)/i){ # Begin if ($vertical_text_position !~ m/(top|middle|bottom/i)
			print "<option selected>top</option>\n";
			print "<option>middle</option>\n";
			print "<option>bottom</option>\n";
		} # End if ($vertical_text_position !~ m/(top|middle|bottom/i)
		else { # Begin else
			print "<option".&set_select_tag('top'   ,"$vertical_text_position").">top</option>\n";
			print "<option".&set_select_tag('middle',"$vertical_text_position").">middle</option>\n";
			print "<option".&set_select_tag('bottom',"$vertical_text_position").">bottom</option>\n";
		} # End else
		print "</select>\n\n";
		print "<td valign='top' align='left'>Horizontal ";
		print "----------------$horizontal_text_position------<select name='maop_horizontal'>\n";
		if ($horizontal_text_position !~ m/(left|center|right)/i){ # Begin if ($horizontal_text_position !~ m/(left|center|right)/i)
			print "<option selected>left</option>\n";
			print "<option>center</option>\n";
			print "<option>right</option>\n";
		} # End if ($horizontal_text_position !~ m/(left|center|right)/i)
		else { # Begin else
			print "<option".&set_select_tag('left'  ,"$horizontal_text_position").">left</option>\n";
			print "<option".&set_select_tag('center',"$horizontal_text_position").">center</option>\n";
			print "<option".&set_select_tag('right' ,"$horizontal_text_position").">right</option>\n";
		} # End else
		print "</select>\n";
	} # End if ($line=~m!text from the image!)
	print "</tr>\n</table>\n";
} # End sub manage_position

=head1 sub set_select_tag(...)

This function that set flag selected or not. It is selected $val1 match $val2.

=head2 PARAMETER(S)

=over 4

$val1: string 1.

$val2: string 2.

=back

=head2 RETURNED VALUE

=over 4

None.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Sep 08 2006

- I<Created on:>  Sep 08 2006

=back

=cut

sub set_select_tag { # Begin set_select_tag
	my ($val1,$val2)=@_;
	chomp($val1);
	chomp($val2);

#	print "$val1 === $val2";
	return (($val2=~m/$val1/i) ? " selected" : "");
} # End sub set_select_tag


=head1 sub auth_menu(...)

This function manages the Authentication menu.

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

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Sep 10 2009: refarmatted the html code.

- I<Last modification:> Jan 27 2006

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back

=cut

sub auth_menu { # Begin auth_menu
	my $color='red';
	print $doc->br
		. &menu_page_title(
			"Bienvenue sur l'album photos<br /><font color='blue'>Welcome to the album of pictures</font>",
			"Authentifiez vous pour administrer l'album photos" . $doc->br . "\n" .
			"<font color='blue'>Authenticate to administrate the album of pictures</font>", 
			"\n" .
			ALBUM_VERSION
			);

	print <<MENU;
<center>
<table class=\"main_auth\" >
<tr>
<td align='center' valign='middle'>
<br />
<form action='${main_prog}' method='post'>
<table class="auth">
<tr>
<td>
Enter login
</td> 
<td>
<input type='text' name='maop_login' />
</td>
</tr>
<tr>
<td>
Enter password
</td>
<td>
<input type='password' name='maop_password' />
<input type='hidden' name='maop_service' value='check' />
</td>
</tr>
<tr>
<td>
<br />
<input type='submit' value='Soumettre :) / Submit :)' />
</td>
<td>
<input type='reset' value='Annuler / Reset' />
<br />
</td>
</tr>
</table>
</form>
<br />
MENU
	&go_back;
	print <<MENU;
</td>
</tr>
</table>
</center>
MENU
	print $doc->br
		. $doc->br
		. $doc->br
		. $doc->br
		. $doc->br
		. $doc->br
		. $doc->br;
} # End sub auth_menu


=head1 sub numbers(...)

This function sorts numbers when it is used with the sort function.

=head2 PARAMETER(S)


=over 4


$a: value to sort.

$b: value to sort.

=back

=head2 RETURNED VALUE

=over 4

None.

=back

=head2 ERRROR RETURNED

=over 4

-1 if $a smaller that $b,0 is $a equals to $b, else 1

=back

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back

=cut

sub numbers { # Begin numbers
	my @la=split( /\|\|/, $a );
	my @lb=split( /\|\|/, $b );

	if ( $a ne $b ){ # Begin if ($a ne $b)
		( $la[0] <=> $lb[0] ) || ( $la[1] <=> $lb[1] );
	} # End if ($a ne $b)
} # End sub numbers

=head1 sub record(...)

This function records information into a file named $file_conf.

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

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jan 18 2014 keep the trip name in parameter to follow from page to page

- I<Last modification:> Jul 15 2012 Synchro with data base not up to snuff. Correction done but still yet error(s) occur(s).

- I<Last modification:> Oct 31 2011. Modification for youtube to be accepted with url and then print it as if it was embeded.

- I<Last modification:> Aug 25 2011. Modification for youtube size now standardized 200x180 (wxh)

- I<Last modification:> Aug 21 2011. Modification for youtube

- I<Last modification:> Mar 15 2011. String format bug still persistant. Correction done hopefully: <object> tag used.

- I<Last modification:> Mar 14 2011. String format bug. Correction done hopefully: <embed> tag used.

- I<Last modification:> Mar 13 2011. URL for youtube can be used. iframe can be too.

- I<Last modification:> Feb 26 2011. iframe added

- I<Last modification:> Feb 25 2011. Transtypage added but there were bugs. Correction done.

- I<Last modification:> Feb 24 2011. new type of data that's from youtube.
Transtypage added

- I<Last modification:> Jun 28 2009

- I<Last modification:> Jul 17 2006

- I<Last modification:> Mar 29 2006

- I<Last modification:> Feb 16 2006

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back

=cut

sub record { # Begin record
	my (
		$file_name,               $page_position_in_album,
		$valign,                  $halign,
		$french_comment,          $english_comment,
		$vertical_text,           $horizontal_text,
		$position_from_the_image, $link_name,
		$link,                    $link_name_eng,
		$link_eng
	)=(
		(length(uri_unescape($doc->param("maop_file_name_img")))>0) ? "$timsec" . uri_unescape($doc->param("maop_file_name_img")) : (uri_unescape($doc->param("maop_file_name_img2"))=~m/\<\ *iframe\ *title\ *\=/i) ?  uri_unescape($doc->param("maop_file_name_img2")) : uri_unescape($doc->param("maop_file_name_img2"))
		,
		uri_unescape($doc->param("maop_Set_page_position_in_the_album")),
		uri_unescape($doc->param("maop_vertical")),
		uri_unescape($doc->param("maop_horizontal")),
		uri_unescape($doc->param("maop_lang_French_comment")),
		uri_unescape($doc->param("maop_lang_English_comment")),
		uri_unescape($doc->param("maop_vertical_text")),
		uri_unescape($doc->param("maop_horizontal_text")),
		uri_unescape($doc->param("maop_Set_position_of_the_text_from_the_image_in_compartment")),
		uri_unescape($doc->param("maop_name_to_link")),
		uri_unescape($doc->param("maop_link")),
		uri_unescape($doc->param("maop_name_to_link_eng")),
		uri_unescape($doc->param("maop_link_eng")),
	);
	my $page_num=(); # no comment that's the page number
	my $grantPictur=uri_unescape($doc->param("maop_grantPicture"));
	chomp($grantPictur);
	my $grantPicture=($grantPictur=~m!Public granted!) ? "ok" : (($grantPictur=~m!Admin granted!) ? "adm" : "ko") ;

	print "<br>------------------>record($grantPictur):$grantPicture<br>";
	my $type_upload=uri_unescape($doc->param("maop_type_of_upload"));
	my @save_result=();
	if($file_name=~m/www.youtube.com/){ # Begin if($file_name=~m/www.youtube.com/)
		print "<!-- oCROCOoooooooooooooooooooooo)$file_name(mmmmmmmmmmm=======>$file_name<br -->";
		if($file_name=~m/\<iframe/){
			$file_name=~s/width\=\"\d+\"/width\=\"200\"/;
			$file_name=~s/height\=\"\d+\"/height\=\"180\"/;
		}
		elsif($file_name=~m/\/watch\?/){ # Begin elsif($file_name=~m/www.youtube.com\/watch\?/)
				my $tmp="<iframe width=\"200\" height=\"180\" src=\"";
				$file_name=~s/\/watch\?v\=/\/embed\//;
				$file_name=~s/\&feature\=related//;
				$file_name.='"';
				$tmp.=$file_name . " frameborder=\"0\" allowfullscreen></iframe>";
				#print "<!-- ZOZOZIZOZO $file_name \n\n $tmp -------->";
				$file_name=$tmp;
		} # End elsif($file_name=~m/www.youtube.com\/watch\?/)
	} # End if($file_name=~m/www.youtube.com/)
	
	print $doc->p( "<br /><br /><br /><br />Information recorded. granted:  $grantPicture" .  $doc->br );

	if ( uri_unescape($doc->param("maop_Set_page_position_in_the_album")) eq "" ){ # Begin if (uri_unescape($doc->param("maop_Set_page_position_in_the_album")) eq "" )
		error_raised( $doc,
		"No page position set in the previous menu here is the value ["
		. uri_unescape($doc->param("maop_Set_page_position_in_the_album"))
		. "]" );
	} # End if (uri_unescape($doc->param("maop_Set_page_position_in_the_album")) eq "" )

	# We check if file has the following format
	# <drive name>:\d1\d1\f1.gif where d[num] is a directory and and f1.gif an image file name
	# then we take only the image file name

	my @l_file_scat=split( /\//, io::gut::machine::MyFile::reformat($file_name) );
	my $file_name_saved_at_server_side=();
	if(scalar(@l_file_scat)>0){# Begin if(scalar(@l_file_scat)>0)
		io::gut::machine::MyFile::reformat($l_file_scat[ scalar(@l_file_scat) - 1 ]);
	}# End if(scalar(@l_file_scat)>0)
	# We create a file into a path where to store new image file
	my $file_to_upload=&io::MyConstantBase::DIRECTORY_DEPOSIT->() . "/${suffix_for_image_file}${file_name_saved_at_server_side}";

	# That's the end of session at the end this session will be remove

	$page_position_in_album=~s/\ *\@\ */\|\|/g;
	$page_position_in_album=~s/\ *(Page|[\#]|row)\ *//g;
	if ( $page_position_in_album=~m/create/i ){ # Begin if ( $page_position_in_album=~m/create/)
		$page_position_in_album=&create_new_page;
	} # End if ( $page_position_in_album=~m/create/i)
	# Case we want to save info but no modification is required
	if ( $an_action ne "record_modify" ){ # Begin if ($an_action ne "record_modify")
		#                                  Begin if record modify action not requested

		#	print $doc->p("case 1");
		# if file exists then we get its content then we sort it and then save it
		if ( -f "$file_conf_to_save" ){ # Begin if case where all info related to files are stored and already exists
			my $pages_num=0;

			open( CHECK, "$file_conf_to_save" );
			@save_result=<CHECK>;
			close(CHECK);
			@save_result=sort numbers @save_result;

			my $position_in_page=();# no comments
			foreach (@save_result){ # Begin foreach @save_result
				# format of BD:
				# PAGE||RANK||ADDRIP||FILE_NAME||COMMMENT_POSY||COMMMENT_POSX||F_COMMENT||E_COMMENT||IMG_POSX||IMG_POSY||POS_COMMENT_FROM_IMG||TAG||GRANT
				chomp($_);

				my @in_file=split( /\|\|/, $_ );
				my $page_num=$in_file[0];
				if ( $position_in_page=~/last/i ){ # Begin  if ($position_in_page=~/last/i)
					if ( $page_position_in_album == $page_num ){ # Begin if ($page_position_in_album == $page_num)
						if ( $in_file[1] == &io::MyConstantBase::MAX_IMAGES_PER_PAGE->() ){ # Begin if ($in_file[1] == &io::MyConstantBase::MAX_IMAGES_PER_PAGE->())
							error_raised( $doc, "Maximum of images reached per page which is " . &io::MyConstantBase::MAX_IMAGES_PER_PAGE->() );
						} # End if ($in_file[1] == &io::MyConstantBase::MAX_IMAGES_PER_PAGE->())
					} # End if ($page_position_in_album == $page_num)
				} # End if ($position_in_page=~/last/i)
				if ($page_position_in_album == $in_file[0] && $position_in_page == $in_file[1] ){ # Begin if ( $page_position_in_album == $in_file[0] && $position_in_page == $in_file[1] )
					error_raised( $doc, "This place is already taken by another picture [(pos in album=$page_position_in_album == $page_num=page number),(row in page = $in_file[1] == " . &io::MyConstantBase::MAX_IMAGES_PER_PAGE->() . "max row(s) per page)]" );
				} # End if ( $page_position_in_album == $in_file[0] && $position_in_page == $in_file[1] )
			} # End foreach (@save_result)
		} # End if case where all info related to files are stored and already exists
		# Code not in use anymore
		if ( $page_position_in_album=~m/create/i ){ # Begin if ($page_position_in_album=~m/create/i)
			$page_position_in_album = $page_num + 1;
		} # End if ($page_position_in_album=~m/create/i)
		# End of code not in use
		$french_comment  = ( $french_comment  eq "" ) ? "." : $french_comment;
		$english_comment = ( $english_comment eq "" ) ? "." : $english_comment;
		$page_position_in_album=uri_unescape($doc->param("maop_Set_page_position_in_the_album"));
		$page_position_in_album=~s/\ *\@\ */\|\|/g;
		$page_position_in_album=~s/\ *(Page|[\#]|row)\ *//g;
		if ( $page_position_in_album=~m/create/i ){ # Begin if ( $page_position_in_album=~m/create/)
			$page_position_in_album = &create_new_page;
		} # End if ( $page_position_in_album=~m/create/i)

		$valign=uri_unescape($doc->param("maop_vertical"));
		$halign=uri_unescape($doc->param("maop_horizontal")),
		$valign=~tr/[A-Z]/[a-z]/;
		$halign=~tr/[A-Z]/[a-z]/;
		$vertical_text=uri_unescape($doc->param("maop_vertical_text"));
		$horizontal_text=uri_unescape($doc->param("maop_horizontal_text"));
		$vertical_text=~tr/[A-Z]/[a-z]/;
		$horizontal_text=~tr/[A-Z]/[a-z]/;
		my $commFr=uri_unescape($doc->param("maop_lang_French_comment"));
		my $commEng= uri_unescape($doc->param("maop_lang_English_comment"));
		#print "uuuuuuuuuuuuuuuuuuu)$file_name<br />";
		# do same thing with the minimum of MyFile.pm
		# string transformation
		#$file_name=~s!\-!&#45;!g;
		$file_name_saved_at_server_side=io::gut::machine::MyFile::reformat($file_name);
		$file_name_saved_at_server_side=~s!\_!\&\#95;!g;
		#	print "<br />hhhhhhhhhhhhhhhhhhhh)". $file_name_saved_at_server_side ."(eeeeeeeeeeee<br />";
		$file_name=~s!\_!\&\#95;!g;
		
		my $obj=();
		if($file_name!~m!www.youtube.com!i){ # Begin if($file_name!~m!www.youtube.com!i)
			$obj="${suffix_for_image_file}$file_name_saved_at_server_side";
		} # End if($file_name!~m!www.youtube.com!i)
		else{ # Begin else
			$obj="${suffix_for_image_file}${file_name}";
		} # End else
		
                #print "before --------------------->file name:$obj<br>";
		if($commFr=~m!http://www.youtube.com!){$obj=();}
		if($commEng=~m!http://www.youtube.com!){$obj=();}
                #print "after --------------------->file name:$obj<br>";
		my $line_pos=$page_position_in_album . "||"
			. $obj . "||" 
			. $valign . "||"
			. $halign . "||"
			. &switch_from_a_specified_character_to_tag($commFr)
			. "||"
			. &switch_from_a_specified_character_to_tag($commEng)
			. "||"
			. $horizontal_text . "||"
			. $vertical_text . "||"
			. uri_unescape($doc->param( "maop_Set_position_of_the_text_from_the_image_in_compartment"))
			. "||" . "("
			. uri_unescape($doc->param("maop_name_to_link")) . ","
			. uri_unescape($doc->param("maop_link")) . ")" . ";" . "("
			. uri_unescape($doc->param("maop_name_to_link_eng")) . ","
			. uri_unescape($doc->param("maop_link_eng")) . ")"
			. "||$grantPicture"
			. "||" . uri_unescape($doc->param("maop_youtubeln"));
		#print "oooo)$line_pos<br />";
		if($line_pos!~m/^\|\|/){# Begin if($line_pos!~m/^\|\|/)
				@save_result = (@save_result,$line_pos);
				@save_result = sort numbers @save_result;
		}# End if($line_pos!~m/^\|\|/)
	} # End if ($an_action ne "record_modify")
	else { # Begin else
		#    Else record modify action requested
		my $local_page = uri_unescape($doc->param("maop_page"));
		my $local_line = uri_unescape($doc->param("maop_line"));

		#	print $doc->p("case 2");
		open( R, "$file_conf_to_save" ) || error_raised( $doc, "File [$file_conf_to_save] not found!!!" );
		my @all_file = <R>;
		close(R);
		my @tmp=();
		foreach (@all_file){ # Begin foreach (@all_file)
			chomp($_);
			my (
				$page_position_in_album, $position_in_page,
				$ipaddr,$file_name,
				$valign, $halign,
				$french_comment, $english_comment,
				$horizontal_text,$vertical_text, 
				$position_from_the_image,
				$related_link,
				$grantPictur,$my_tag
			)= split( /\|\|/, $_ );
			if ( $page_position_in_album eq $local_page ){ # Begin if ( $page_position_in_album eq $local_page)
				if ( $position_in_page eq $local_line ){ # Begin if ( $position_in_page eq $local_line )
					print "position found and changed: ($related_link ,$grantPictur)<br />";
					#$grantPictur=($grantPictur=~m!Public granted!) ? "ok" : (($grantPictur=~m!Admin granted!) ? "adm" : "ko") ;
					#print "<br>ooooo><table border=1><tr><td>$_</td></tr></table>"; print "<ooooooooooooooooooo<br>";

					my $l =
						"$page_position_in_album||$position_in_page||$ipaddr||$file_name||"
						. uri_unescape($doc->param("maop_vertical")) . "||"
						. uri_unescape($doc->param("maop_horizontal")) . "||"
						. uri_unescape($doc->param("maop_lang_French_comment")) . "||"
						. uri_unescape($doc->param("maop_lang_English_comment")) . "||"
						. uri_unescape($doc->param("maop_horizontal_text")) . "||"
						. uri_unescape($doc->param("maop_vertical_text")) . "||"
						. uri_unescape($doc->param("maop_Set_position_of_the_text_from_the_image_in_compartment")) . "||"
						. "("
							. uri_unescape($doc->param("maop_name_to_link")) . "," . uri_unescape($doc->param("maop_link")) 
						. ")" 
						. ";"
						. "("
							. uri_unescape($doc->param("maop_name_to_link_eng")) . "," . uri_unescape($doc->param("maop_link_eng")) 
						. ")"
						. "||$grantPicture||$my_tag";
					if($l!~m/^\|\|/){# Begin if($l!~m/^\|\|/)
						$_=$l;
					}# End if($l!~m/^\|\|/)
				} # End if ( $position_in_page eq $local_line )
				else { # Else of if ( $position_in_page eq $local_line )
					@tmp = ( @tmp, "$_" );
				} # End if ( $position_in_page eq $local_line )
			} else { # Else if ( $page_position_in_album eq $local_page)
				@tmp = ( @tmp, "$_" );
			} # End if ( $page_position_in_album eq $local_page)
		} # End foreach (@all_file)
		@save_result = @all_file;
	} # End else
	# End if Record modify action requested

	open( S_CONF, ">$file_conf_to_save" ) or error_raised( $doc, "File [$file_conf_to_save] does not exist !!!" );
	foreach my $in (@save_result){ # Begin foreach @save_result
		chomp($in);
		print S_CONF "$in\n";
	} # End foreach @save_result
	close(S_CONF);
} # End sub record

=head1 sub create_dir(...)

This function creates a directory in order to store all information related to album info.

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

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back

=cut

sub create_dir { # Begin create_dir
	my @o=(); # no comments
	if ( !-d "$album_directory" ){ # Begin if (!-d "$album_directory")
		#       mkdir("$album_directory",0700) || die("Cannot create $album_directory\n");
		`mkdir $album_directory`;
		`chmod 700 $album_directory`;
	} # End if (!-d "$album_directory")
	if ( !-f "$file_conf_to_save" ){ # Begin if (!-f "$file_conf_to_save")
		open( W, ">$file_conf_to_save" ) || die("Cannot create $file_conf_to_save\n");
		print W "";
		close(W);
	} # End if (!-f "$file_conf_to_save")
	open( F, "$file_conf_to_save" );
	my @local_f  = <F>;
	my $num_line = 0;
	if ( scalar(@local_f) < 2 && scalar(@local_f) > 0 ){ # Begin if (scalar(@local_f) < 2 && scalar(@local_f) > 0)
		foreach (@local_f){ # Begin foreach (@local_f)
			chomp($_);
			@o = split( /\|\|/, $_ );

			$_=~s/\ *//;
			if ( $_ eq "" ){ # Begin if ($_ eq "")
				&under_construction_prompt;
			} # End if ($_ eq "")
		} # End foreach (@local_f)
		close(F);
	} # End if (scalar(@local_f) < 2 && scalar(@local_f) > 0)
	elsif ( scalar(@local_f) == 0 ){ # Begin elsif (scalar(@local_f) == 0)
		&under_construction_prompt;
	} # End elsif (scalar(@local_f) == 0)
} # End sub create_dir

=head1 sub under_construction_prompt(...)

This function prints under construction prompt (picture) on the screen.

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

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back

=cut

sub under_construction_prompt { # Begin under_construction_prompt
	print "<br /><br /><br /><br /><center>\n";
	print "<table border=\"0\">\n<tr>\n<td align='right'>\n";
	&look_for_images_used;
	print "<td>\n<center>\n";
	print "<br />\n<br />\n<br />\n";
	print "<br /><br /><b><a href='${main_prog}?maop_service=auth'  >Administrer le Cyber Album</a></b> /\n";
	print "<font color='gray42'><b><a href='${main_prog}?maop_service=auth'  >Administrate Cyber Album</a></b></font>\n<br />\n<br />\n";
	print "<img src='"
				. &io::MyConstantBase::DIRECTORY_DEPOSIT->()
				. "under_construction10.gif' alt='y' />\n<br />";
	#print "<br />\n<br />\nAller <a href='$url_demo'  >version</a> precedente / <font color='gray42'>Go to previous <a href='$url_demo'  >version</a>.\n</font><br />\n"
		#. $doc->br
		#. $doc->br
	print $doc->img( { -src => &io::MyConstantBase::DIRECTORY_DEPOSIT->() . 'powered.gif' } )
		. $doc->br
		. "Hosted by "
		. $doc->a( { -href => &io::MyConstantBase::HOSTED_BY_URL->() }, &io::MyConstantBase::HOSTED_BY->() )
		. "</center>\n";
	print "</table>\n";
	exit(-1);
} # End sub under_construction_prompt

=head1 sub error_raised_visit(...)

This function generates an error message when problem occurs.

=head2 PARAMETER(S)

=over 4

$doc: that's an implementation of the object CGI (new CGI to be precised).

$explaination: explaination of the error.

=back

=head2 RETURNED VALUE

=over 4

None.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back

=cut

sub error_raised_visit { # Begin error_raised_visit
	my ( $doc, $explaination ) = @_;
	print $doc->start_html("Error"),
		$doc->h1("Error"),
		$doc->p("Your visit was not successful because of the following error: "),
		$doc->p( $doc->i($explaination) ),
		$doc->p("<center><img src=\"../img/wheel.gif\" alt='h' /></center><br />"),
		$doc->p("<a href=\"JavaScript:history.back()\"  >go back</a>"),
		$doc->end_html;
	exit(-1);
} # End sub error_raised_visit

=head1 sub  shows_page_not_taken_yet(...)

This function showss pages that are taken.

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

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Apr 06 2011 default was not printed by default if no page selected by default (he first from the list).

- I<Last modification:> Mar 28 2006

- I<Last modification:> Feb 16 2006

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back

=cut

sub shows_page_not_taken_yet { # Begin shows_page_not_taken_yet
	my @line=(); #no comments
	my $add=(); #no comments
	open( SHOW, "$file_conf_to_save" ) or error_raised("File $file_conf_to_save does not exists");
	my @save_info = <SHOW>;
	close(SHOW);
	my $script_page_taken = "<table width='100%' border='0'><tr>\n<td bgcolor='#CF6748' align=center>Nouvelles postions / New positions</tr>\n<tr><td align='center' valign='middle'><select name='maop_Set_page_position_in_the_album' size=12>\n"
	; # Final script to print
	my $lmax = ( split( /\|\|/, $save_info[ scalar(@save_info) - 1 ] ) )[0] ; # Max of lines
	my $s =
	()
	; # String that store all pages in order to create option list with true missing pages and rows
	my $first_pass = 0; # used when option need to be selected as default

	# Problem solve as in this way: a matrix (page, line). Enumerate all possibilities in a list.
	# read page already saved. Remove from the list page already saved. And print the matrix of page not taken.
	for ( my $l = 1 ; $l != ( $lmax + 1 ) ; $l++ )
	{ # Begin for (my $l = 1;$l != ($lmax+1);$l++)
	for ( my $c = 1 ; $c != ( &io::MyConstantBase::MAX_IMAGES_PER_PAGE->() + 1 ) ; $c++ )
	{ # Begin for ($c = 1; $c != (&io::MyConstantBase::MAX_IMAGES_PER_PAGE->()+1); $c++)
	$s .= "$l $c;";
	} # End for ($c = 1; $c != (&io::MyConstantBase::MAX_IMAGES_PER_PAGE->()+1); $c++)
	} # End for (my $l = 1;$l != ($lmax+1);$l++)

	foreach (@save_info){ # Begin foreach (@save_info)
	@line = split( /\|\|/, $_ ); #save_info
	$add = $line[0] . " " . $line[1] . ";";
	$s=~s/$add//;
	} # End foreach (@save_info)

	foreach ( split( /\;/, $s ) ){ # Begin foreach (split(/\;/,$s))
		my ( $p, $l ) = split( /\ /, $_ );

		if ( $first_pass == 0 ){ # Begin if ($first_pass == 0)
			$script_page_taken .= "<option selected>Page #$p @ row #${l}</option>\n";
			$first_pass++;
		} # End if ($first_pass == 0)
		else { # Begin else
			$script_page_taken .= "<option>Page #$p @ row #${l}</option>\n";
		} # End else
	} # End foreach (split(/\;/,$s))

	if($script_page_taken=~m!<option selected>!i){ # Begin if($script_page_taken=~m!<option selected>!i)
		$script_page_taken .= "<option>\nCreate a new page\n</option>\n</select></tr>\n</table>\n";
	} # End if($script_page_taken=~m!<option selected>!i)
	else{ # Begin else
		$script_page_taken .= "<option selected>\nCreate a new page\n</option>\n</select></tr>\n</table>\n";
	} # End else

	print $script_page_taken;
} # End sub shows_page_not_taken_yet

=head1 sub shows_list_pictures(...)

This function showss the list of pictures.

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

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Apr 17 2011: bug due to data base file format changed

- I<Last modification:> Apr 06 2011: bug prints info according to file format.

- I<Last modification:> Mar 15 2011: prints info according to file format.

- I<Last modification:> Sep 13 2009: switch image to image name admin menu (option to optmize data transfert).

- I<Last modification:> Jun 28 2009

- I<Last modification:> Feb 6 2006

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back

=cut

sub shows_list_pictures { # Begin shows_list_pictures
	open( SHOW, "$file_conf_to_save" ) or error_raised("File $file_conf_to_save does not exists");
	my @save_info = <SHOW>;
	close(SHOW) or error_raised("File $file_conf_to_save does not exists");

	print "<fieldset><legend align='top'>\nPicture(s) already set</legend>\n<ol>\n";
	print "<table><tr><td align='center' valign='middle' bgcolor='#D0EFE6'>\n";
	print "<table border=\"0\"><tr>\n";
	print "<td width=90% valign='top' align='left' bgcolor='#9CDCCA'>\nComments\n";
	print "<td width=90% valign='top' align='left' bgcolor='#9CDCCA'>\nWhere is comment\n";
	print "<td valign='top' align='center' bgcolor='#9CDCCA'>Page\n";
	print "<td valign='top' align='center' bgcolor='#9CDCCA'>Line\n";
	print "<td valign='top' align='center' bgcolor='#9CDCCA'>Text position\n";
	print "<td valign='top' align='center' bgcolor='#9CDCCA'>Image position\n";
	print "<td valign='top' align='center' bgcolor='#9CDCCA'>Image view\n";
	print "<td valign='top' align='center' bgcolor='#9CDCCA'>Link on word(s)\n";
	print "<td valign='top' align='center' bgcolor='#9CDCCA'>URL\n";
	print "<td valign='top' align='center' bgcolor='#9CDCCA'>Grant/Accorder\n";
	print "<td valign='top' align='center' bgcolor='#9CDCCA'>Modify/Modifier\n";
	print "<td valign='top' align='center' bgcolor='#9CDCCA'>Remove/Enlever\n";
	print "<td valign='top' align='center' bgcolor='#9CDCCA'>(Link/Lien) Youtube\n";
	print "<td valign='top' align='center' bgcolor='#9CDCCA'>Operations</tr>\n";

	my @line=();
	my ( $word, $link, $word_eng, $link_eng) = ();
	my $counter_p=1;
	foreach my $one_line (@save_info){ # Begin foreach my $one_line (@save_info)
		@line=();
		if($counter_p>1){ # Begin if($counter_p>1)
			@line = split( /\|\|/, $one_line );
			( $word, $link, $word_eng, $link_eng) = &split_links( $line[11] );
			my $granted=$line[12] ; # granted
			print "<form action='${main_prog}' method='post'>\n";
			print "<tr><td valign='top' align='left'>\n<li>"
				. &switch_from_a_specified_tag_to_characters( ($line[6]=~m!http://www.youtube.com!) ? "<img src='".&io::MyConstantBase::DIRECTORY_DEPOSIT->()."/youtube.gif' alt='q' />" :$line[6] ) . "<br /><font color='#822942'>"
				. &switch_from_a_specified_tag_to_characters( ($line[7]=~m!http://www.youtube.com!) ? "<img src='".&io::MyConstantBase::DIRECTORY_DEPOSIT->()."/youtube.gif' alt=':' />":$line[7]  )
				. "</font></li></td>\n";# field 1
			print "<td align='center' valign='top'>\n$line[10]</td>\n";# field 2
			print "<td align='center' valign='top'>\n$line[0]</td>\n";# field 3
			print "<td align='center' valign='top'>$line[1]</td>\n";#field 4
			print "<td align='center' valign='top'>\n$line[8]/$line[9]</td>\n";# field 5
			print "<td align='center' valign='top'>\n$line[4]/$line[5]</td>\n";# field 6

			if ( $line[3] !~ m/^http\:\/\//i ){ # Begin if ($line[3] !~ m/^http\:\/\//i)
				if(&io::MyConstantBase::SHOW_PICTURES_ADMIN->()!=0){ # Begin if(&io::MyConstantBase::SHOW_PICTURES_ADMIN->()!=0)
					print "<td align='center' valign='middle'>\n";
					print "<img src='"
						. &io::MyConstantBase::DIRECTORY_DEPOSIT->()
						. "$line[3]' width='75'  height='75' alt='xx' />\n</td>";# field 7
				} # End if(&io::MyConstantBase::SHOW_PICTURES_ADMIN->()!=0)
				else { # Begin else
					print "<td align='left' valign='top'>\n";# field 7
					
					#-------------------------------------
					# get info from file
					chdir("../img");
					if(-f "$line[3]"){ # Begin if(-f "$line[3]")
						#print "----------ooooo)$line[3]";
						open(my $R,"$line[3]");
						my $dta=stat($R);
						print "<br /><u><b>At/A:</b></u> " ;
						print scalar localtime $dta->mtime ;
						close($R);
						print "\n<br />";
					} # End if(-f "$line[3]")
					chdir("../cgi-bin");
					print "<u><b>IP/IP:</b></u>$line[2]\n<br />";
					if($line[3]=~m/www.youtube.com/i){ # Begin if($line[2]=~m/www.youtube.com/i)
							$line[3]=~s!_!\&\#95;!g;# _ transformed in &#95; because of date format $line[2]
							$line[3]=~s!'!\&\#39;!g;
							$line[3]=~s!\"!\&\#34;!g;
							$line[3]=~s!\<!\&\#60;!g;
							$line[3]=~s!\>!\&\#62;!g;
							$line[3]=~s!_!&#95;!g;
					} # End if($line[2]=~m/www.youtube.com/i)
					if($line[3]=~m/(jpg|jpeg|gif|png)$/i){ # Begin if($line[3]=~m/(jpg|jpeg|gif|png)$/i)
						print "<u><b>Img:</b></u>$line[3]\n<br />";
					} # End if($line[3]=~m/(jpg|jpeg|gif|png)$/i)
					else{ # Begin else
						print "<u><b>Video:</b></u>$line[3]\n<br />";
					} # End else
				} # End else
			} # End if ($line[2] !~ m/^http\:\/\//i)
			else { # Begin else
				print "<td align='center' valign='middle'>\n<img src='$line[3]' width='75'  height='75' alt='bbb' />\n";
			} # End else

			if(length($word)>0||length($word_eng)>0){
				# field 8,9 values
				print "<td align='center' valign='middle'>\n$word<br /><font color='#822942'>$word_eng</font></td>\n".
					"<td align='center' valign='middle'>$link<br /><font color='#822942'>$link_eng</font>\n</td>\n";
			} else {
				# field 8,9 substitute no value
				print "<td align='center' valign='middle'>\n</td>\n";
				print "<td align='center' valign='middle'>\n</td>\n";
			}
			# ---------------------
			print "<td align='center' valign='middle'>\n";
			print "$granted</td>";
			print "\n<form action='${main_prog}?maop_service=auth&maop_upld=ok' method='post' enctype='multipart/form-data'>\n";
			print "<input type='hidden' name='maop_prev_id' value='$$' />\n";
			print "<td align='center' valign='middle'>\n";
			print "<input type='radio' name='maop_action' value='modify' />\n";
			print "<td align='center' valign='middle'>\n";
			print "<input type='radio' name='maop_action' value='remove' />\n";
			print "<td align='center' valign='middle'>\n";
			print "<!-- input type='radio' name='maop_action' value='youtuberightslink' --> $line[13]\n";
			print "<td align='center' valign='middle'>\n";
			print "<input type='hidden' name='maop_login' value='" . uri_unescape($doc->param("maop_login")) . "' />\n";
			print "<input type='hidden' name='maop_page' value='$line[0]' />\n";
			print "<input type='hidden' name='maop_ssection' value='adminPict' />";
			print "<input type='hidden' name='maop_line' value='$line[1]' />\n";
			print "<input type='hidden' name='maop_vertical' value='$line[8]' />\n";
			print "<input type='hidden' name='maop_horizontal' value='$line[7]' />\n";
			print "<input type='hidden' name='maop_Set_position_of_the_text_from_the_image_in_compartment' value='$line[9]' />\n";
			print "<input type='hidden' name='maop_vertical_text' value='$line[3]' />\n";
			print "<input type='hidden' name='maop_horizontal_text' value='$line[4]' />\n";
			print "<input type='hidden' name='maop_service' value='check' />\n";
			print "<input type='submit'  value='Soumettre :) / Submit :)' />\n";
			print "</form></tr>\n";
		} # End if($counter_p>1)
		else{ # Begin else
			$counter_p++;
		} # End else
	} # End foreach my $one_line (@save_info)
	print "</table>\n\n</fieldset>\n";
	print "</table>\n";
} # End sub shows_list_pictures

=head1 sub split_links(...)

This function split links in a given string ($language). That's what it is returned from $language ($word_to_link,$link,$word_to_link_eng,$link_eng).

=head2 PARAMETER(S)

=over 4

$language: that's the list of possible languages.

=back

=head2 RETURNED VALUE

=over 4

$word_to_link: word to link in French.

$link: that's the link for French.

$word_to_link_eng: word to link in English.

$link_eng: that's the link.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back

=cut

sub split_links { # Begin split_links
	my ( $fr_l,             $en_l )     = split( /\;/, $_[0] );
	my ( $word_to_link,     $link )     = split( /\,/, $fr_l );
	my ( $word_to_link_eng, $link_eng ) = split( /\,/, $en_l );

	$word_to_link    =~s/\(//g;
	$link            =~s/\)//g;
	$word_to_link_eng=~s/\(//g;
	$link_eng        =~s/\)//g;
	return ( $word_to_link, $link, $word_to_link_eng, $link_eng );
} # End sub split_links

=head1 sub remove_picture(...)

This function gets a picture to be removed. A line and, a page number are necesessary to know the location of the picture. These information are taken with uri_unescape($doc->param('...')) function that's why no parameters are used.

=head2 PARAMETER(S)

=over 4

$page: page number to remove

$line: line in page to remove

=back

=head2 RETURNED VALUE

=over 4

None.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Apr 06 2011 file format changed need to do modifications to make it work!!!

- I<Last modification:> Jul 06 2006

- I<Last modification:> Aug 23 2006

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back

=cut

sub remove_picture { # Begin remove_picture
	my @tmp            = ();
	my @all_file       = ();
	#my $local_page     = uri_unescape($doc->param("maop_page"));
	#my $local_line     = uri_unescape($doc->param("maop_line"));
	my $file_to_remove = ();
	my ($local_page, $local_line)=@_;

	open( R, "$file_conf_to_save" ) || error_raised( $doc, "File [$file_conf_to_save] not found!!!" );
	@all_file = <R>;
	close(R);

	# We remove a line from a given page from the album
	foreach (@all_file){ # Begin foreach (@all_file)
		chomp($_);
		my @line = split( /\|\|/, $_ );
		if ( $line[0] eq $local_page ){ # Begin if ($line[0] eq $local_page)
			if ( $line[1] eq $local_line ){ # Begin if ( $line[1] eq $local_line )
				$file_to_remove = $line[3];
				#print "---> Line <b>$_</b> removed.<br />";
			} # End if ( $line[1] eq $local_line )
			else { # Else of if ( $line[1] eq $local_line )
				@tmp = ( @tmp, "$_" );
			} # End if ( $line[1] eq $local_line )
		} # End if ($line[0] eq $local_page)
		else { # Else of if ($line[0] eq $local_page)
			@tmp = ( @tmp, "$_" );
		} # End if ($line[0] eq $local_page)
	} # End foreach (@all_file)

	if ( scalar(@all_file) > scalar(@tmp) ){ # Begin if (scalar(@all_file) > scalar(@tmp))
		@all_file = @tmp;
	} # End if (scalar(@all_file) > scalar(@tmp))

	# We check if the picture to remove is not use into another comment of picture before destroying it.
	my $linked_to_other_comment = 0;
	my @list_file = ();

	foreach (@all_file){ # Begin foreach (@all_file)
		my @line = split( /\|\|/, $_ );
		@list_file = (@list_file,&io::MyConstantBase::DIRECTORY_DEPOSIT->() . $line[2]);
	} # End foreach (@all_file)

	# We create the new file_conf
	open( W, ">$file_conf_to_save" ) || error_raised( $doc, "File [$file_conf_to_save] not found!!!" );
	flock( W, LOCK_EX | LOCK_SH );
	foreach (@tmp){ # Begin foreach (@tmp)
		print W "$_\n";
	} # End foreach (@tmp)
	close(W) || error_raised( $doc, "File [$file_conf_to_save] not found!!!" );

	# remove encoding to find file &#45; to - character
	#$file_to_remove=~s!&#45;!\-!g;
	#$file_to_remove=~s!&#95;!\_!g;
	# We remove the image that goes with the associated comment if no more use than once in the album otherwise it is not removed
	my $local_dir = &io::MyConstantBase::DIRECTORY_DEPOSIT->() . "$file_to_remove";
	$local_dir=&do_untaint($local_dir);
	if (-f "$local_dir"){ # Begin if (-f "$local_dir")
		unlink("$local_dir") || die("$local_dir cannot be removed");
		$local_dir=~s/\</&#60;/g;
		$local_dir=~s/\>/&#62;/g;
		$local_dir=~s/\"/&#34;/g;
		print "+ File $local_dir removed from the disk<br />\n";
		print "--->File removed from the disk<br />\n";
	} # End if (-f "$local_dir")
	elsif ($local_dir=~m/frame/){ # Begin elsif ($local_dir=~m/frame/)
		#unlink("$local_dir") || die("$local_dir cannot be removed");
		$local_dir=~s/^[^<]*//g;
		$local_dir=~s/\</&#60;/g;
		$local_dir=~s/\>/&#62;/g;
		$local_dir=~s/\"/&#34;/g;
		print "+ Link $local_dir removed from the table<br />\n";
		#print "Picture removed from the disk<br />\n";
	} # End elsif ($local_dir=~m/frame/)
	else{ # Begin else
		$local_dir=~s/\</&#60;/g;
		$local_dir=~s/\>/&#62;/g;
		$local_dir=~s/\"/&#34;/g;
		print "+ File $local_dir cannot be removed from the disk<br />\n";
	} # End else
	&clean_pictures(@list_file);
} # End sub remove_picture

=head1 sub clean_pictures(...)

This function cleans pictures. The picrures removed are the pictures that are not anymore in the album.

=head2 PARAMETER(S)

=over 4

@list: that's the list of pictures that are in the album.

=back

=head2 RETURNED VALUE

=over 4

None.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Apr 06 2011 file format changed need to do modifications to make it work!!!

- I<Last modification:> Aug 22 2006

- I<Created on:> Aug 22 2006

=back

=cut

sub clean_pictures { # Begin clean_pictures
	my (@list) = @_;
	my $dir =  &io::MyConstantBase::DIRECTORY_DEPOSIT->() . "200*";
	print "------>$dir<-------------<br>";
	$ENV{PATH}='/bin:/usr/bin:/usr/local/bin';
	my $s="ls $dir";
	$s=&do_untaint($s);
	my @l = `$s`;

	# if (!-f "${album_directory}/to_clean_pictures_according_album_of_pictures_remove_me"){ # Begin if (!-f "${album_directory}/to_clean_pictures_according_album_of_pictures_remove_me")
	#print "I will try to clean all pictures that were recorded and,<br />removed from the album but that are still on the disk...<br />\n";
	foreach my $list_pict (@l){ # Begin foreach my $list_pict (@l)
		my $is_ok = 0;
		chomp($list_pict);
		foreach my $elem_pict (@list){ # Begin foreach my $elem_pict (@list)
			chomp($elem_pict);

			if ($list_pict eq $elem_pict){ # Begin if ($list_pict eq $elem_pict)
				$is_ok = 1;
			} # End if ($list_pict eq $elem_pict)
		} # End foreach my $elem_pict (@list)
		if (!$is_ok){ # Begin if (!$is_ok)
			unlink("$list_pict") || die("$list_pict cannot be removed");
			print "o file $list_pict removed from the disk<br />\n";
		} # End if (!$is_ok)
	} # End foreach my $list_pict (@l)
	#print "Pictures removed :)<br />";
	# } # End if (!-f "${album_directory}/to_clean_pictures_according_album_of_pictures_remove_me")
} # End sub clean_pictures

=head1 sub return_info_picture(...)

This function returns info related to picture. At this time, looks in the file where info are stored, then returns line concerned, if it exists.

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

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back

=cut

sub return_info_picture { # Begin return_info_picture
	my @tmp            = ();
	my @all_file       = ();
	my $local_page     = uri_unescape($doc->param("maop_page"));
	my $local_line     = uri_unescape($doc->param("maop_line"));
	my $file_to_remove = ();

	open( R, "$file_conf_to_save" ) || error_raised( $doc, "File [$file_conf_to_save] not found!!!" );
	@all_file = <R>;
	close(R) || error_raised( $doc, "File [$file_conf_to_save] not found!!!" );

	# We remove a line from a given page from the album
	foreach (@all_file){ # Begin  foreach (@all_file)
		chomp($_);
		my @line = split( /\|\|/, $_ );
		if ( $line[0] eq $local_page ){ # Begin if ($line[0] eq $local_page)
			if ( $line[1] eq $local_line ){ # Begin if ( $line[1] eq $local_line )
				#print "<br>iiiiiiiiiii>"; print "@line"; print "<br><<<<<<<<<<<<<<<<<\n<br>";
				return @line;
			} # End if ( $line[1] eq $local_line )
			else { # Begin else
				@tmp = ( @tmp, "$_" );
			} # End else
		} # End if ($line[0] eq $local_page)
		else { # Begin else
			@tmp = ( @tmp, "$_" );
		} # End else
	} # End foreach (@all_file)
} # End sub return_info_picture

=head1 sub put_url_line(...)

When we print info on screen we put url if there is a link.

=head2 PARAMETER(S)

=over 4

$word_to_link: that's the word to link.

$line: that's the line to look for the word(s) to link.

$url: that's the url to link to the word(s).

=back

=head2 RETURNED VALUE

=over 4

Returns the linked string.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Sep 06 2006

- I<Last modification:> Feb 16 2006

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back

=cut

sub put_url_line { # Begin put_url_line
	my $word_to_link = $_[0];
	my $line         = $_[1];
	my $url          = $_[2];
	chomp($word_to_link);
	chomp($line);
	chomp($url);

	# Extra test if it is only a word in the sentence
	if ($line=~m/^($word_to_link)$/gi){ # Begin if ($line=~m/^($word_to_link)$/gi)
		$line=~s/^($word_to_link)$/\<a href=\"$url\"  \>$1\<\/a\>$2/gi;
		return $line;
	} # End if ($line=~m/^($word_to_link)$/gi)

	if ($line=~m/([\ \,\.\'\;\:\!\?\"\)\(])($word_to_link)([\ \,\.\'\;\:\!\?\"\(\)])/gi){ # Begin if ($line=~m/([\ \,\.\'\;\:\!\?\"\)\(])($word_to_link)([\ \,\.\'\;\:\!\?\"\(\)])/gi)
		$line =~
		s/([\ \,\.\'\;\:\!\?\"\)\(])($word_to_link)([\ \,\.\'\;\:\!\?\"\(\)])/$1\<a href=\"$url\"  \>$2\<\/a\>$3/gi;
		return $line;
	} # End if ($line=~m/([\ \,\.\'\;\:\!\?\"\)\(])($word_to_link)([\ \,\.\'\;\:\!\?\"\(\)])/gi)

	# Had to do a second time because when ([\ \,\.\'\;\:\!\?\"\)])($word_to_link) is used then sencond occurence of that does not work
	# We need to do it a sencond time
	if ($line=~m/([\ \,\.\'\;\:\!\?\"\)\(])($word_to_link)([\ \,\.\'\;\:\!\?\"\(\)])/gi){ # Begin  if ($line=~m/([\ \,\.\'\;\:\!\?\"\)\(])($word_to_link)([\ \,\.\'\;\:\!\?\"\(\)])/gi)
		$line =~
		s/([\ \,\.\'\;\:\!\?\"\)\(])($word_to_link)([\ \,\.\'\;\:\!\?\"\(\)])/$1\<a href=\"$url\"  \>$2\<\/a\>$3/gi;
		return $line;
	} # End  if ($line=~m/([\ \,\.\'\;\:\!\?\"\)\(])($word_to_link)([\ \,\.\'\;\:\!\?\"\(\)])/gi)

	# Look at the begining of string
	if ($line=~m/^($word_to_link)([\ \,\.\'\;\:\!\?\"\(])/){ # Begin if ($line=~m/^($word_to_link)([\ \,\.\'\;\:\!\?\"\(])/)
		$line =~
		s/^($word_to_link)([\ \,\.\'\;\:\!\?\"\(])/\<a href=\"$url\"  \>$1\<\/a\>$2/gi;
		return $line;
	} # End if ($line=~m/^($word_to_link)([\ \,\.\'\;\:\!\?\"\(])/)

	$line=~s/([\ \,\.\'\;\:\!\?\"\(])($word_to_link)$/$1\<a href=\"$url\"  \>$2\<\/a\>/gi;
	return $line;
} # End sub put_url_line

=head1 sub print_page(...)

This function returns an HTML page for the album. There's automatic link to the next page(s).

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

Two strings. Pge navigation and sttructure of page with images.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:v1.6.10.1>  Nov 6 2011 bug related to file name translation solved by changing the coding o,nce stored in memory.

- I<Last modification:v1.6.10.0>  Nov 4 2011 prints date when datum entered for the first time (no modification time printed).

- I<Last modification:v1.6.8.0> Aug 25 2011. bug solved when url to youtube enterer but does not contains <iframe> tag ask then to print link or message to this link.

- I<Last modification:v1.6.7.0> Aug 24 2011. bug solved when multiple links to youtube on same page (one per image).

- I<Last modification:> Apr 15 2011. First line skipped because name of the fields

- I<Last modification:> Mar 15 2011. String format bug. Correction done hopefully. Transformation of the char to encoded char.

- I<Last modification:> Mar 14 2011. String format bug. Correction done hopefully.

- I<Last modification:> Feb 25 2011. Transtypage added but there were bugs. Correction done.

- I<Last modification:> Feb 24 2011. new type of data that's from youtube.
Transtypage added

- I<Last modification:> Nov 21 2010. flv fomat replaced by mp3 format.

- I<Last modification:> Sept 20 2009. Returns page script+navigator html script. Used for gathering pags and privacy.

- I<Last modification:> Aug 31 2009. Link tag shows up on .mov movie format. Correction done. When asks to put left side image and allowed to be printed a link tag shows up corection done no link shows up now.

- I<Last modification:> Jul 19 2009. Stats removed if IP not allowed, hence cannot enlarge picture.

- I<Last modification:> Jul 18 2009

- I<Last modification:> Jun 30 2009

- I<Last modification:> Mar 22 2008

- I<Last modification:> Jan 27 2008

- I<Last modification:> Oct 14 2006

- I<Last modification:> Mar 7 2006

- I<Last modification:> Fev 6 2006

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back

=cut

sub print_page { # Begin print_page
	my $page_asked                = uri_unescape($doc->param("maop_page"));
	my $print_my_page_script_head = ();
	my $print_my_page_script   = ();
	my @all_file               = ();
	my $list_page_beg          = "  ";
	my $list_page              = "<table border='0'><tr>";
	my $prev                   = 1;
	my $prev_page              = ();
	my $next_page              = ();
	my @line                   = ();
	chomp($page_asked);
	my $div = $page_asked / &io::MyConstantBase::MAX_IMAGES_PER_PAGE->();
	my ( $word_to_link,     $my_link )     = ();
	my ( $word_to_link_eng, $my_link_eng ) = ();
	my $date_of_picture_put_on_css = "font-weight: lighter;font-size: 10pt; font-style: oblique;";
	my $my_image = 0;
	my $my_image_per_page = 2;

	#print "----------------->$page_asked<<br>))))))))))))$div<<br>";
	$div = ( split( /\./, $div ) )[0];

	# We setup min range and max range of page number to show up on the navigator menu of the album.
	my $RANK_MIN_PICT_SHOW = ( ( $div < 1.0 ) ? 1 : ( $div * &io::MyConstantBase::MAX_IMAGES_PER_PAGE->() ));

	# We set up min range and max range of page number to show up on the navigator menu of the album.
	my $RANK_MAX_PICT_SHOW = &rank_right_navigator_bar_range( $RANK_MIN_PICT_SHOW + ( &io::MyConstantBase::MAX_IMAGES_PER_PAGE->() - 1 ) );

	#print "--------->$file_conf_to_save<br>";
	open( R, "$file_conf_to_save" ) || error_raised( $doc, "File [$file_conf_to_save] not found!!!" );
	@all_file = <R>;
	close(R) || error_raised( $doc, "File [$file_conf_to_save] not found!!!" );

	# This line was added because of case empty page (no number of page). If so, page asked is the first one
	#print "---------------->$page_asked<----->".&gets_first_page_number."<-------<br />";
	$page_asked = ( "$page_asked" eq "" || "$page_asked" eq "0" ) ? &gets_first_page_number : $page_asked;

	$print_my_page_script = "<table border=\"0\" width='75\%'>\n";

	my @list_of_existing_pages = ();
	my $my_prev=();
	# ------------------------------------------
	# Begin Creates navigator menu
	my $cpt_l=1;
	foreach (@all_file){ # Begin foreach (@all_file)
		#print "<u>line:</u>$_<br>\n";
		if($cpt_l!=0){ # Begin if($cpt_l!=0)
			chomp($_);
			# next line to be removed in the near future
			$_=~s/\&\#95\;/\_/g;# Transforms data in order not to be delete later
			#print "WWWWWWWWWWWWWWWW>$_<br>";
			my @line = split(/\|\|/,$_);
			my $d = $line[3];
			my $ppj=();

			#my ($date_se,@other) = split(/\-/,$d);
			# case we want to print link to youtube video and not the video itself
			if( $line[3]=~m!www.youtube.com!i){ # Begin if( $line[3]=~m!www.youtube.com!i)
				if($line[13]=~m/link\/lien/){ # Begin if($line[13]=~m/link\/lien/)
					if($line[3]=~m/src=\"([^\"]*)\"/){
						$line[3]="Lien vers/Link to <a href=\"$1\"  >Youtube</a>";
					}
					else{ # Begin else
						my $ppin=$line[3];# save link

						$line[3]="Lien vers/Link to <a href='${ppin}' >Youtube</a>";# modify printing
					} # End else
					#print "encounter youtube $line[3] $cpt_l<br />";
				} # End if($line[13]=~m/link\/lien/)
			} # End if( $line[3]=~m!www.youtube.com!i)
			if( $line[3]!~m!www.youtube.com!i && $line[3]!~m!iframe!i){ # Begin if( $line[3]!~m!www.youtube.com!i && $line[3]!~m!iframe!i)
				# do some cleaning in case that something went wrong during delete picture
				if(-f &io::MyConstantBase::DIRECTORY_DEPOSIT->() . "$line[3]"){ # Begin if(-f &io::MyConstantBase::DIRECTORY_DEPOSIT->() . "$line[3]")
					#print "------>$line[3]<br />";
					open(my $R, &io::MyConstantBase::DIRECTORY_DEPOSIT->() . "$line[3]");
					my $dta=stat($R);
					$ppj= scalar localtime $dta->mtime ;
					close($R);
				} # End if(-f &io::MyConstantBase::DIRECTORY_DEPOSIT->() . "$line[3]")
				else{ # Begin else
					if( $line[3]!~m!www.youtube.com!i){ # Begin if( $line[3]!~m!www.youtube.com!i)
						my $o=$line[3];
						$o=~s!\;!\&\#59;!g;
						$o=~s!\'!\&\#39;!g;
						$o=~s!\"!\&\#34;!g;
						$o=~s!\-!\&\#45;!g;
						$o=~s!\<!\&\#60;!g;
						$o=~s!\>!\&\#62;!g;

						#print "oooooooooooooo>$o<br />";
						if($line[0]=~/^[0-9]+$/ && $line[1]=~/^[0-9]+$/){ # Begin if($line[0]=~/^[0-9]+$/ && $line[1]=~/^[0-9]+$/)
							print "does not exist ------>$line[3]<br />";
							&remove_picture($line[0],$line[1]);
						} # End if($line[0]=~/^[0-9]+$/ && $line[1]=~/^[0-9]+$/)
					} # End if( $line[3]!~m!www.youtube.com!i)
				} # End else
			} # End if( $line[3]!~m!www.youtube.com!i && $line[3]!~m!iframe!i)

			# checks if it is not a fake number, page does not exists, ...
			# if it can be seen from ip address ...
			if(&look_if_page_authorized($line[0])==0 ){ # Begin if(&look_if_page_authorized($line[0])==0)
				#print "^^^^^^^^^^^:w authorize $line[3]<br />";
				# we get word to link in order to make on screen a link on other web sites. This is done for French and English version.
				( $word_to_link, $my_link, $word_to_link_eng, $my_link_eng ) =
				&split_links( $line[11] );
				
				# that's comments of the picture left or right
				if ( $word_to_link ne "" && $word_to_link_eng ne "" ){ # Begin if ($word_to_link ne "" && $word_to_link_eng ne "")
					chomp($my_link);
					chomp($my_link_eng);

					$line[6] = &put_url_line( $word_to_link, $line[6], $my_link );
					$line[7] = &put_url_line( $word_to_link_eng, $line[7], $my_link_eng );
				} # End if ($word_to_link ne "" && $word_to_link_eng ne "")
				else { # Begin else
					$line[6] = &switch_from_a_specified_tag_to_characters( $line[6] );
					$line[7] = &switch_from_a_specified_tag_to_characters( $line[7] );
				} # End else
				@list_of_existing_pages = ( @list_of_existing_pages, $line[0] );

				# nicely prints page list of album
				if ( $my_prev != $line[0] ){ # Begin if ($my_prev != $line[0])
					if ( $page_asked != $line[0] ){ # Begin if ($page_asked != $line[0])
						if ( ( $my_prev != 1 ) ){ # Begin if ( ( $my_prev != 1 ) )
							if ( ( $line[0] % &io::MyConstantBase::MAX_PAGE_PER_LINE_INDEX->() ) < ( $my_prev % &io::MyConstantBase::MAX_PAGE_PER_LINE_INDEX->() ) ){ # Begin if ( ( $line[0] % &io::MyConstantBase::MAX_PAGE_PER_LINE_INDEX->() ) < ( $my_prev % &io::MyConstantBase::MAX_PAGE_PER_LINE_INDEX->() ) )
								$list_page .= " </td><!-- blue jean --></tr><!-- balaaaaa -->\"\n+\"<tr>";
							} # End if ( ( $line[0] % &io::MyConstantBase::MAX_PAGE_PER_LINE_INDEX->() ) < ( $my_prev % &io::MyConstantBase::MAX_PAGE_PER_LINE_INDEX->() ) )
							$list_page .= "<td align='center'><a href='${main_prog}?maop_page=$line[0]".
								"&maop_googid=".uri_unescape($doc->param("maop_googid"))."&maop_gmv=".&io::MyConstantBase::GOOGLE_MAP_SCRIPT_VERSION->(). &io::MyConstantBase::PATH_GOOGLE_MAP_OPT->() .
								"'>x</a></td><!-- <wwblablablablo -->\"+\n\"";
						} # End if ($my_prev != 1)
						else { #  Begin else 
							if ( ( $line[0] % &io::MyConstantBase::MAX_PAGE_PER_LINE_INDEX->() ) == 0 ){ # Begin if ( ( $line[0] % &io::MyConstantBase::MAX_PAGE_PER_LINE_INDEX->() ) == 0 )
								$list_page .= "<td align='center'></td><!-- pantalon --></tr>\"\n+\"<tr>";
							} # End if ( ( $line[0] % &io::MyConstantBase::MAX_PAGE_PER_LINE_INDEX->() ) == 0 )
							#    First element in the list
							$list_page .= "<td align='center'><a href='${main_prog}?maop_page=$line[0]".
							"&maop_googid=".uri_unescape($doc->param("maop_googid")). "&maop_gmv=".&io::MyConstantBase::GOOGLE_MAP_SCRIPT_VERSION->(). &io::MyConstantBase::PATH_GOOGLE_MAP_OPT->() .
							"'>x</a></td><!-- lolololozutzutyyyyyyyy -->\"+\n\"";
						} # End if ( ($my_prev != 1) && (($line[0] % (&io::MyConstantBase::MAX_IMAGES_PER_PAGE->()+1)) != 0) )
						$my_prev = $line[0];
					} # End if ($page_asked != $line[0])
					else { # Begin else
						$my_prev = $line[0];
						if ( ( $my_prev != 1 ) && ( ( $line[0] % ( &io::MyConstantBase::MAX_IMAGES_PER_PAGE->() + 1 ) ) != 0 ) ){ # Begin if (($my_prev != 1) && (($line[0] % (&io::MyConstantBase::MAX_IMAGES_PER_PAGE->()+1)) != 0) )
							if ( ( $line[0] % &io::MyConstantBase::MAX_PAGE_PER_LINE_INDEX->() ) == 0 ){ # Begin if ($line[0] % 10 == 0)
								$list_page .= " </td><!-- short en bermuda --></tr>\"\n+\"<tr>";
							} # End if ($line[0] % 10 == 0)
							$list_page .= "<td align='center'><i><font color='#CE3030'>X</font></i></td><!-- zutzutyyyyyyyy -->\"\n+\"";
						} # End if (($my_prev != 1) && (($line[0] % (&io::MyConstantBase::MAX_IMAGES_PER_PAGE->()+1)) != 0) )
						else { # Begin else
							if ( ( $line[0] % &io::MyConstantBase::MAX_PAGE_PER_LINE_INDEX->() ) == 0 ){ # Begin if ( ( $line[0] % &io::MyConstantBase::MAX_PAGE_PER_LINE_INDEX->() ) == 0 )
								$list_page .= "</td><!-- tshirt moulant --></tr>\"\n+\"<tr>";
							} # End if ( ( $line[0] % &io::MyConstantBase::MAX_PAGE_PER_LINE_INDEX->() ) == 0 )
							$list_page .= "<td align='center'><font color='#CE3030'>X</font></td><!-- zout machine -->\"+\n\"";
						} # End else
					} # End else
				} # End if ($my_prev != $line[0])
				if($line[12]=~m/ok/){ $authorized="ok" ; } else { ($allow,$authorized)=io::MySec::urlsAllowed; } 
				if ( $page_asked eq $line[0] ){ # Begin if ($page_asked eq $line[0])
					if("$authorized" eq "ok"){ # Begin if("$authorized" eq "ok")
						if ( $line[10]=~m/left/i ){ # Begin if ($line[10]=~m/left/i)
							#print "dddddddd: ".(io::MySec::urlsAllowed)[1]." :ddddddddssss$line[2]<br />";
							$print_my_page_script .=
										"<tr>\n<td align='$line[8]' valign='$line[9]' width='50\%'> \n$line[6]<br />\n<font color='#822942'>$line[7]</font><br />"
										."</td>\n<td valign='$line[4]'  align='$line[5]' width='50\%'>";
							# checks if the user is authorised
							if((io::MySec::urlsAllowed)[1] eq "ok" ){ # Begin if((io::MySec::urlsAllowed)[1] eq "ok" )
						#		print "bboboboobooooooo:io::MySec::urlsAllowed)[1]<br />";
								
								if($line[3]!~/.(mp4|3gp|mpeg|mov|dat|mp3|avi|www.youtube.com)$/i){ # Begin if($line[3]!~/.(mp4|3gp|mpeg|mov|dat|mp3|avi)/i)
									if( $line[3]!~m!www.youtube.com!i && $line[3]!~m!iframe!i){ # Begin if( $line[3]!~m!www.youtube.com!i && $line[3]!~m!iframe!i)
										$print_my_page_script .= 
											"\n<!-- momo and toto --><a  href='${main_prog}?maop_service=showPict&maop_pict="
											. &io::MyConstantBase::DIRECTORY_DEPOSIT->()
											. "$line[3]&maop_comments="
											. &switch_from_a_specified_character_to_tag(
														"$line[6]SEPARATOR$line[7]")
										. "'>\n";
									} # End if( $line[3]!~m!www.youtube.com!i && $line[3]!~m!iframe!i)
									else { # Begin else
										#$print_my_page_script .= $line[3]. "<!-- carotttttttttttttte -->";
										$print_my_page_script .=  "<!-- carotttttttttttttte -->";
									} # End else
								} # End if($line[3]!~/.(mp4|3gp|mpeg|mov|dat|mp3|avi)/i)
							} # End if((io::MySec::urlsAllowed)[1] eq "ok" )
							if($line[3]=~/.(mp4|3gp|mpeg|mov|dat|avi)$/i){ # Begin if($line[3]=~/.(mp4|3gp|mpeg|mov|dat|avi)/i)
								#print "ggggggg<br />";
								$print_my_page_script .= 
										  "<embed src='"
										. &io::MyConstantBase::DIRECTORY_DEPOSIT->()
										. "$line[3]'  height=360 width=450 border=1 autoplay=false>\n";
							} # End if($line[3]=~/.(mp4|3gp|mpeg|mov|dat|avi)/i)
							else { # Begin else
								if($line[3]!~/.(mp3)$/i&&$line[3]!~/www.youtube.com/){ # Begin if($line[3]!~/.(mp3)$/i&&$line[3]!~/www.youtube.com/)
									#print "eeeeeeeeiiiie<br />";	
									$print_my_page_script .= 
										  "\n<img src='"
										. &io::MyConstantBase::DIRECTORY_DEPOSIT->()
										#. "$line[3]'  height='72' border='0' alt='knn' />\n";
										. "$line[3]'  height='72' border='0' alt='knn' />\n</td></tr>";
								} # End if($line[3]!~/.(mp3)$/i&&$line[3]!~/www.youtube.com/)
								elsif($line[3]=~m!www.youtube.com!){ # Begin elsif($line[3]=~m!www.youtube.com!)
									#print "eeeeeeeeeeeeeeeeeqqqq<br />";
									#my $loca= (split(/\-/,$line[3]))[1];

									#$print_my_page_script .= $loca . "<!-- azer qwer -->";
									$print_my_page_script .= $line[3] . "<!-- azer qwer -->";
								}# End elsif($line[3]=~m!www.youtube.com!)
							#print "endend<br />";
							} # End else
							if((io::MySec::urlsAllowed)[1] eq "ok" ){ # Begin if((io::MySec::urlsAllowed)[1] eq "ok" )
								#print "eeeeeeeeeeeeeee<br />";
								if($line[3]!~/.(mp4|3gp|mpeg|mov|dat|mp3|avi)$/i){ # Begin if($line[3]!~/.(mp4|3gp|mpeg|mov|dat|mp3|avi)$/i)
									$print_my_page_script .= "</a>\n";
								} # End if($line[3]!~/.(mp4|3gp|mpeg|mov|dat|mp3|avi)$/i)
								elsif($line[3]=~/.(mp3)$/i){ # Begin if($line[3]=~/.(mp3)$/i)
							#	    print "tttttttt<br />";
									$print_my_page_script .= 
												  "<embed src='"
												. &io::MyConstantBase::DIRECTORY_DEPOSIT->()
												. "$line[3]'  height=100 width=200 border=0 autoplay=false>\n";
								} # End if($line[3]=~/.(mp3)$/i)
								elsif($line[3]=~m!www.youtube.com!i){# Begin elsif($line[3]=~m!www.youtube.com!)
							#		print "uuuuuuuuuu$line[3]<br />";
									$print_my_page_script .= $line[3]. "<!-- bobobobobozo le clown -->";
								}# End elsif($line[3]=~m!www.youtube.com!)
								$print_my_page_script .= 
											 &extra_comments("left",
													"left",
													$line[0],
													$line[1],
													"<p align=left style='font-weight: lighter;font-size: 10pt; font-style: oblique;'>" .
													&print_date_of_picture_put_on_album($ppj,$date_of_picture_put_on_css,'(stat(&io::MyConstantBase::DIRECTORY_DEPOSIT->() .$line[2]))[9]',$line[12],$line[2],$line[3]) .
											&print_info_picture((($my_image_per_page == 2) ? 2 :($my_image_per_page)) ,"$line[3]") 
										       ) ."</td><!-- vouiiiii --></tr>\n";
									$print_my_page_script .= "</td></tr>";
							} # End if((io::MySec::urlsAllowed)[1] eq "ok" )
							else{ # Begin else
								#$print_my_page_script .= "<br />$ppj<!-- date of first time --></td></tr>";
							} # End else
							$my_image_per_page += 2;
						} # End if ($line[scalar(@line)-1]=~m/left/i)
					else { # Begin else
						#print "ooooooooooooobabbbbbb$line[2]<br />";
						$print_my_page_script .= "<tr>\n<td valign='$line[4]'  align='$line[5]' width='50\%'>\n";
						if($line[3]=~/.(mp4|3gp|mpeg|mov|dat|avi)$/i){# BEGIN if($line[3]=~/.(mp4|3gp|mpeg|mov|dat|avi)$/i)
							$print_my_page_script .=
							"<embed src='"
							. &io::MyConstantBase::DIRECTORY_DEPOSIT->()
							. "$line[3]'  height=360 width=450 border=0 autoplay=false>\n";
						} # End if($line[3]=~/.(mp4|3gp|mpeg|mov|dat|avi)$/i)
						elsif($line[3]=~/.(mp3)$/i){ # Begin if($line[3]=~/.(mp3)/i)
								$print_my_page_script .= 
										  "<embed src='"
										. &io::MyConstantBase::DIRECTORY_DEPOSIT->()
										. "$line[3]'  height=100 width=200 border=0 autoplay=false>\n";
						} # End if($line[3]=~/.(mp3)/i)
						elsif($line[3]=~/www.youtube.com/i){ # Begin if($line[3]=~/www.youtube.com/i)
	#print "=============>$line[2]<br />";
							my ($loca)=$line[3];
	#print "OOOOOOOO>$loca<br />";
							$print_my_page_script.=$loca;
						}  # End if($line[3]=~/www.youtube.com/i)
						else { # BEGIN else
							if( $line[3]!~m!www.youtube.com!i && $line[3]!~m!iframe!i){ # Begin if( $line[3]!~m!www.youtube.com!i && $line[3]!~m!iframe!i)
								if((io::MySec::urlsAllowed)[1] eq "ok" ){ # Begin if((io::MySec::urlsAllowed)[1] eq "ok" )
									$print_my_page_script.="<a   href='${main_prog}?maop_service=showPict&maop_pict="
										. &io::MyConstantBase::DIRECTORY_DEPOSIT->()
										. "$line[3]&maop_comments="
										. &switch_from_a_specified_character_to_tag(
										"$line[6]SEPARATOR$line[7]")
										. "'>\n";
								} # End if((io::MySec::urlsAllowed)[1] eq "ok" )
								$print_my_page_script .= "<img src='" . &io::MyConstantBase::DIRECTORY_DEPOSIT->() . "$line[3]'  height='72'  border='0' alt='oook' />\n" ;
								if((io::MySec::urlsAllowed)[1] ne "ok" ){ # Begin if((io::MySec::urlsAllowed)[1] ne "ok" )
									#$print_my_page_script .= "<br />$ppj<!-- date of first time -->" ;
								}

								if((io::MySec::urlsAllowed)[1] eq "ok" ){ # Begin if((io::MySec::urlsAllowed)[1] eq "ok" )
									$print_my_page_script.="</a>\n";
								} # End if((io::MySec::urlsAllowed)[1] eq "ok" )
							} # End if( $line[3]!~m!www.youtube.com!i && $line[3]!~m!iframe!i)
							else{ # Begin else
								$print_my_page_script .= "<!-- clearfield -->\n" ;
							} # End else
						} # End else
						$print_my_page_script .=
							&extra_comments("left",
								"left",
								$line[0],
								$line[1],
								"<p align=left style='font-weight: lighter;font-size: 10pt; font-style: oblique;'>" .
								&print_date_of_picture_put_on_album($ppj,$date_of_picture_put_on_css,(stat(&io::MyConstantBase::DIRECTORY_DEPOSIT->() .$line[3]))[9],$line[12]," ",$line[2],$line[3]) .
								&print_info_picture((($my_image_per_page==2 ) ? 2 :($my_image_per_page)),"$line[3]") .
								"</p>"
						       )
							."</td><td align='$line[8]' valign='$line[9]' width='50\%'>".
((length($line[6])>0||length($line[7])>0) ? "\n$line[6]<br />\n<font color='#822942'>$line[7]</font>\n" : "")  . "</td><!-- Burette et tout ce qu'il faut --></tr>\n";
							$my_image_per_page += 2;
						} # End else
					} # End if("$authorized" eq "ok") 
					else { # Begin else
						#$print_my_page_script .= "<tr><td><br />\nNe peut être vu de $locip / <font color='#822942'>Cannot be seen from $locip</font></td></tr>\n";
			#			$print_my_page_script .= "<tr><td><br /> <table><tr><td>\n<!--<img src=\"". &io::MyConstantBase::DIRECTORY_DEPOSIT->() . "/sorry.jpg\" > -->\n</td><td valign=middle align=left><!--La photo ne peut être vue de cette machine <br />\n<font color='#822942'> This picture cannot be seen from this machine</font> --></td></tr></table></td></tr>\n";
						$my_image_per_page += 2;
					} # End else
				} # End if ($page_asked eq $line[0])
				$my_image++;
			} # End if(&look_if_page_authorized($line[0])==0)
		} # Begin if($cpt_l!=0)
		else{ # Begin else
			print "not authorize<br />";
			$cpt_l++;
		} # End else
	} # End foreach (@all_file)
	$print_my_page_script .= "</table>\n";
	if ( &is_ok_page_num( $page_asked, @list_of_existing_pages ) == &io::MyConstantBase::NOK->() )  { # Begin if ( &is_ok_page_num($page_asked,@list_of_existing_pages) == &io::MyConstantBase::NOK->())
		print error_raised( $doc, "Page asked [$page_asked] does not exist!!!!" );
	} # End if ( &is_ok_page_num($page_asked,@list_of_existing_pages) == &io::MyConstantBase::NOK->())

	$list_page .= "<!-- meueuuuuuuu --></tr></table>";

	# ------------------------------------------
	# Begin to Create navigator menu
	my $navigator_menu = &create_table_for_navigator($list_page_beg,$prev_page,"<script language='javascript' type='text/javascript'>listOfPages();</script>", $next_page );
	# End to Create navigator menu
	# ------------------------------------------

	my $page_result=
		$doc->br . $doc->br . $doc->table(
		{
		-border => 0,
		-width  => "100%"
		},
		"\n",
		$doc->Tr(
		$doc->td(
			{ -bgcolor => '#CFD3F6' },
			"\n",
			$doc->table(
				{
				-width  => "100%",
				-border => 0
				},
				"\n",
				$doc->Tr(
				$doc->td(
				{
				    -valign => "top",
				    -align  => "left",
				    -width  => "48%",
				},
				[$navigator_menu]
				),
				"\n",
				$doc->td(
					{
					    -align => 'center',
					    #										-bgcolor => '#F7C5C5'
					},"\n",
						),
				"\n",
				$doc->td(
					{
					    -align  => 'right',
					    -valign => 'top',
					} , $allow , "\n"
				), "\n"
				), # End of one line
				"\n"
				)
			) # End of one column
			)
			)
			. "\n"
			. $doc->table(
				{
					-border => 0,
					-class => "xxx",
					-width  => "100%"
				},
				"\n",
			$doc->Tr(
				$doc->td(
					{
					-align  => 'center',
					-valign => 'middle',
					-bgcolor => '#B4C4BD'
					},
					&menu_page_title( "Bienvenue sur l'album photos<br /><font color='$rtrip'>Welcome to the album of pictures</font>", "Merci d'&ecirc;tre pass&eacute;.<br /><font color='$rtrip'>Thanks for your visiting.</font>")
				),
				"\n"
			),
			"\n",
			$doc->Tr(
				$doc->td(
					{
						-align  => 'center',
						-valign => 'middle'
					},
					$doc->br,
					$doc->br,
					$doc->br,
					$print_my_page_script,
					"\n"
					)
				),
			"\n"
			)
		. $print_my_page_script_head
	;
	return ($list_page,$page_result);
} # End sub print_page

=head1 sub print_date_of_picture_put_on_album(...)

This function reformat information from the file name to print on the screen (see extra comments function).

=head2 PARAMETER(S)

=over 4

$date_set: date when picture was created.

$date_of_picture_put_on_css: that's css stuff.

$file_name_dt: that's the file name date (when it was created more or less according to doc) in case we don't get any info about image file stored. This will get info from system.

$ok

$ipa: ip address

=back

=head2 RETURNED VALUE

=over 4

New string formated with IP address and date when file was created.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 SEE ALSO

=over 4

extra_comments

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Apr 10 2011

- I<Last modification:> Jun 28 2009

- I<Last modification:> Oct 16 2006

- I<Last modification:> Mar 7 2006

- I<Created on:> Mar 5 2006

=back

=cut

sub print_date_of_picture_put_on_album { # Begin print_date_of_picture_put_on_album
	my ($date_set,$date_of_picture_put_on_css,$file_name_dt,$ok,$ipa,$nap) = @_;
	my @local_proc = gmtime($file_name_dt);
	my ($num_of_pict,$size_of_all_picture_gathered) = &gets_current_images_information_from_current_album("$file_conf_to_save");

	my ${taken} =
	"* $nap<br />" .
	"* Nombre de photo(s) ds album / <font color='#822942'>Number of pictures within album</font> $num_of_pict<br />" .
	"* Photo mise le / <font color='#822942'>Picture put on</font> $date_set<br />".
	"* @ IP trouv&eacute;e / <font color='#822942'>IP @ available</font>$ipa<br />";
	return ${taken};
} # End sub print_date_of_picture_put_on_album

=head1 sub rank_right_navigator_bar_range(...)

This function is there to calculate right the navigator bar menu for pages (enumerates all page number(s)).

=head2 PARAMETER(S)

=over 4

$rank_max: maximum rank.

=back

=head2 RETURNED VALUE

=over 4

Returns max_rank in one page (to check better).

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back

=cut

sub rank_right_navigator_bar_range { # Begin rank_right_navigator_bar_range
	my ${rank_max} = $_[0];

	while ( ( ${rank_max} % &io::MyConstantBase::MAX_IMAGES_PER_PAGE->() ) != 0 ){ # Begin while ((${rank_max} % &io::MyConstantBase::MAX_IMAGES_PER_PAGE->()) != 0)
		${rank_max}++;
	} # End while ((${rank_max} % &io::MyConstantBase::MAX_IMAGES_PER_PAGE->()) != 0)
	return ${rank_max};
} # End sub rank_right_navigator_bar_range

=head1 sub is_ok_page_num(...)

This function checks if page asked is in the page rank.

=head2 PARAMETER(S)

=over 4

$page_asked:page asked.

@list_of_existing_pages: list of pages.

=back

=head2 RETURNED VALUE

=over 4

&io::MyConstantBase::OK->(): ok.

&io::MyConstantBase::NOK->(): not ok.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back

=cut

sub is_ok_page_num { # Begin is_ok_page_num
	my ( $page_asked, @list_of_existing_pages ) = @_;

	if ( $page_asked !~ m/^\d+$/ ){ # Begin  if ($page_asked !~ m/^\d+$/)
		error_raised_visit( $doc, "Page format number not correct!!!! [$page_asked]" );
	} # End  if ($page_asked !~ m/^\d+$/)
	elsif ( $page_asked <= $list_of_existing_pages[ scalar(@list_of_existing_pages) - 1 ] ){ # Begin if ($page_asked <= $list_of_existing_pages[scalar(@list_of_existing_pages)-1])
		return &io::MyConstantBase::OK->();
	} # End if ($page_asked <= $list_of_existing_pages[scalar(@list_of_existing_pages)-1])
	else { # Begin else
		#	print $doc->p("&io::MyConstantBase::NOK->() value is [$page_asked]");
		return &io::MyConstantBase::NOK->();
	} # End else
} # End sub is_ok_page_num

=head1 sub create_table_for_navigator(...)

We create a table for navigation menu that's it.

=head2 PARAMETER(S)

=over 4

$list_page_beg
$prev_page
$list_page
$next_page

=back

=head2 RETURNED VALUE

=over 4

String of table for navigator.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jan 29 2006

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back

=cut

sub create_table_for_navigator { # Begin create_table_for_navigator
	print "<!-- Beginint-->\n";
	return $doc->table(
		$doc->Tr(
			$doc->td(
				{
				},
				"\n",
				$doc->table(
					{ -border => 0 },
					"\n",
					$doc->Tr(
						$doc->td(
						{
							-align  => 'left',
							-valign => 'top'
						},
						#($_[0]=~m/[A-Z0-9]*/i) ? "$_[0]" : ""
							($_[0]=~m/[A-Z0-9]*/i) ? "" : ""
						),
						"\n",
						$doc->td(
						{
							-align  => 'left',
							-valign => 'top'
						},
							#"$_[1]"
							($_[1]=~m/[A-Z0-9]*/i) ? "$_[1]" : ""
						),
						"\n",
						$doc->td(
						{
							-align  => 'left',
							-valign => 'top'
						},
							#"$_[2]"
							($_[2]=~m/[A-Z0-9]*/i) ? "$_[2]" : ""
						),
						"\n",
						$doc->td(
						{
							-align  => 'left',
							-valign => 'top'
						},
							($_[3]=~m/[A-Z0-9]*/i) ? "$_[3]" : ""
						),
						"\n",
						),
					"\n"
					),
				"\n"
			),
			"\n"
		)
	);
} # End sub create_table_for_navigator


=head1 sub cascade_style_sheet_definition(...)

This function creates a cascade style sheet for the whole program.

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

Returns String formated for style sheet.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Sep 27 2009: add $doc object

- I<Last modification:> Jan 27 2006

- I<Created on:> Jan 27 2006

=back

=cut

sub cascade_style_sheet_definition { # Begin cascade_style_sheet_definition
	return &javaScript($_[0]) . "\n".
		$doc->style({ -type=>'text/css' },
		"\n/*<![CDATA[*/\n<!--\n" . 
		&general_css_def
		. "-->\n/*]]>*/"
		);
} # End sub cascade_style_sheet_definition

=head1 sub javaScript(...)

This function creates a java script section.

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

Returns string formated of section in Java Script code.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Sept 21 2008

- I<Last modification:> Feb 10 2006

- I<Created on:> Feb 10 2006

=back

=cut

sub javaScript { # Begin javaScript
	my $u=<<R;
//<![CDATA[
		<!--
			function print_info(title,mess){ /* Begin function print_info(title,mess) */
				var x = document.getElementById("myDemo"); 
				x.innerHTML = "<div id='paragHeader'>"+title+"</div>" + "<div id='paragBody'>"+mess+"</div>" ;
			} /* End function print_info(title,mess) */

			function add_print_info(mess){ /* Begin add_function print_info(mess) */
				var x = document.getElementById("myDemo"); 
				x.innerHTML +=  mess;
			} /* End function add_print_info(mess) */

			function go_to(url){ /*  Begin function go_to(url) */
				location= url;
			}  /*  End function go_to(url) */

			function show(id){ /*  Begin function show(id) */
				var d = document.getElementById(id);

				for (var i = 1; i<=10; i++){ /*  Begin for (var i = 1; i<=10; i++) */
					if (document.getElementById('smenu'+i)){ /*  Begin if (document.getElementById('smenu'+i)) */
						document.getElementById('smenu'+i).style.display='none';
					} /*  End if (document.getElementById('smenu'+i)) */
				} /*  End for (var i = 1; i<=10; i++) */
				if (d){ /*  Begin if (d) */
					d.style.display='block';
				} /*  End if (d) */
			} /*  End function show(id) */

			/*
				The aim is to creates / moved all js functions in this field
				try to field functions wisely ${lot},...
			*/

	function paramEncode(a){
		var x = document.getElementById(a);
		for (i = 0 ; i < x.elements.length ; i++) {
			document.getElementById("demo").innerHTML += x.elements[i].name + " === " + x.elements[i].value + "<br>";
			x.elements[i].value = encodeURIComponent(x.elements[i].value) ;
			document.getElementById("demo").innerHTML += x.elements[i].name + " === " + x.elements[i].value + "<br>";
		}
	}

function timeCalculusB(value){
	var mtz=decodeURIComponent(value); // my time zone
	var formISO='YYYY-MM-DDTHH:mm';
	//var d=new Date();
	var nowMoment=moment();

	if (value==""){ // Begin if (value=="")
		document.myform.maop_bdaytime.value = "--";
		document.getElementById('err').innerHTML = manageError(
									"Error/Erreur",
									"Begin trip:Select a time zone first.",
									"Début voyage:Selectionnez un fuseau horaire en premier.");
	} // End if (value=="")
	else{ // Begin else
		document.myform.maop_bdaytime.value = nowMoment.tz(mtz).add(5,'minutes').format(formISO);
		//document.getElementById('err').innerHTML = document.myform.maop_bdaytime.value;
	} // End else
}

function timeCalculusE(value){
	var mtz=decodeURIComponent(value); // my time zone
	var formISO='YYYY-MM-DDTHH:mm';
	var d=new Date();
	var nowMoment=moment();

	if (value==""){ // Begin if (value=="")
		document.myform.maop_edaytime.value = "--";
		document.getElementById('err').innerHTML = manageError(
									"Error/Erreur",
									"End of trip: select a time zone first.",
									"Fin du voyage: selectionnez un fuseau horaire en premier.");
	} // End if (value=="")
	else{ // Begin else
		document.myform.maop_edaytime.value = nowMoment.tz(mtz).add(5,'minutes').format(formISO);
	} // End else
}

function manageError(header,eEn,eFr){/* Begin function manageError(header,eEn,eFr) */
	return "<div name='errFrame' style='border: thin solid black;border-radius: 5px;'>"+ 
			"<div name='errFrame' style='border: thin solid #33ccff;border-radius: 5px;'>"+ 
				"<div name='errFrame' style='border: thin solid black; background: repeating-linear-gradient(to bottom,#33ccff,#0033cc); '>"+
					"<center><h3>"+header+"</h3></center>"+
				"</div>"+
				"<p>"+
					eEn+"<br>"+eFr+
				"</p>"+
			"</div>"+
		"</div>"  ;
} /* End function manageError(header,eEn,eFr) */

function calc(){ /*  Begin function calc() */
	$lot
	var trip=decodeURIComponent(document.myform.maop_googid.value);// Trip name
	var d1; // date with JS (will be be deprecated pretty soon in this code
	var d2; // date with JS (will be be deprecated pretty soon in this code
	var num1=decodeURIComponent(document.myform.maop_bdaytime.value);// date+time local begining of the trip
	var num2=decodeURIComponent(document.myform.maop_edaytime.value);// date+time local ending of the trip
	var comp1=decodeURIComponent(document.myform.maop_ltzn_b.value);// time zone begining of the trip
	var comp2=decodeURIComponent(document.myform.maop_ltzn_e.value);// time zone ending of the trip
	var myurl=new String("$myuri$myport/$myscript?maop_googid="+trip+"&maop_gmv=3-0"); // <<<<<<<< here to check for url and ip @
	var r="https://"+myurl.replace(/[\/]{2,}/g,"/"); /*  Regexp used to eliminate bugs while printing URL   ... */
	var myForms = document.forms["myform"];
	var bot=moment(num1); // date+time begining of trip ; add one minute to the begining of the trip because of he cell bug
	var eot=moment(num2); // date+time ending of trip 
	var formISO='YYYY-MM-DDTHH:mm';

	bot.tz(comp1,true); // Begin of trip: we don't change date but set time zone to it (date and time)
	var mbot1=bot; // Begin of trip: we don't change date but set time zone to it (date and time)
	var mbot2=bot.clone(); // clone date+time at the begining of the trip
	mbot2.tz(comp2); // we set mbot2 to local time=end of the trip
	var meot1=eot.tz(comp2,true); // End of trip: we don't change date but set time zone to it (date and time)
	// begin test not good enougth need to be improved
	// current date is>=begin of trip?
	var cdt=moment().format('YYYY-MM-DDTHH:MM'); // current date
	var mbot3=bot.clone(); // clone date+time at the begining of the trip
	mbot3.tz(cdt); // we set mbot3 to local time=current date of the trip
	// end test not good enougth need to be improved


	if (new String(trip).valueOf() == new String("").valueOf()) { /* Begin if (new String(trip).valueOf() == new String("").valueOf()) */
		document.getElementById('err').innerHTML = manageError(
									"Error/Erreur",
									"No trip name specified.",
									"Pas de nom de voyage spécifié.");// + "<br>" + myForms.elements.length;
	} /* End if (new String(trip).valueOf() == new String("").valueOf()) */
	else if (document.myform.maop_bdaytime.value=="--" ){ /* Begin else if (document.myform.maop_bdaytime.value=="--" ) */
		document.getElementById('err').innerHTML = manageError(
									"Error/Erreur",
									"<u><b>Begining of the trip:</u></b> select a time zone first.",
									"<br><u><b>Début du voyage:</b></u> selectionnez un fuseau horaire en premier.");
	} /* End else if (document.myform.maop_bdaytime.value=="--" ) */
	else if (mbot3>=meot1){
		// test not good enougth need to be improved
		document.getElementById('err').innerHTML = manageError(
									"Error/Erreur",
									"Time zone end and dates <= time zone begining and dates.",
									"Fuseaux horaires et heures d'arrivées <= Fuseaux horaires et heures de départ.");
	}
	else if (document.myform.maop_edaytime.value=="--" ){ /* Begin else if (document.myform.maop_edaytime.value=="--" ) */
		document.getElementById('err').innerHTML = manageError(
									"Error/Erreur",
									"<u><b>End of the trip:</u></b> select a time zone first.",
									"<u><b>Fin du voyage:</u></b> selectionnez un fuseau horaire en premier.");
	} /* End else if (document.myform.maop_edaytime.value=="--" ) */
	else { /*  Begin else */
		if( lot.indexOf(trip+ "-trips",0)>=0){ /* Begin if( lot.indexOf(trip+ "-trips",0)>=0) */
			document.getElementById('err').innerHTML = manageError(
										"Error/Erreur",
										"The trip name [<b>" + trip + "</b>] already exists.",
										"Le nom [<b>" + trip + "</b>] déjà existtant.");
		} /*  End if( lot.indexOf(trip+ "-trips",0)>=0) */
		else{ /*  Begin else */
			if (meot1>mbot1) {
				var lag=0;
				document.getElementById('err').innerHTML = "<input type='submit' onclick='validForm();'>"+
										"<input type='hidden' name='maop_url' value='"+r+"'/>";
										/*
										+ "----->"+getTimeZone()+ "<-----"+
										"<input type='hidden' name='maop_tz_offset' value='"+lag+"'/>";
										*/

				// function validForm() not working fine : not called in the input field above
				function validForm(){ // Begin function validForm()
					for (var i = 0; i < myForms.elements.length; i++) { // Begin for (var i = 0; i < myForms.elements.length; i++)
						if(myForms.elements[i].value != "Checks dates"){ // Begin if(myForms.elements[i].value != "Checks dates")
							myForms.elements[i].value=encodeURIComponent(myForms.elements[i].value);
						} // End if(myForms.elements[i].value != "Checks dates")
					} // End for (var i = 0; i < myForms.elements.length; i++)
				} // End function validForm()
			}
			else{ /*  Begin else */
				document.getElementById('err').innerHTML = manageError( "Error/Erreur",
											"(d1,t1) > (d2,t2)",
											"(d1,t1) > (d2,t2)");
			} /*  End else */
		} /*  End else */
	} /*  End else */
	/*
		document.getElementById('err').innerHTML += "   --------- "+ trip 
						+" ooooooooo <br><b>"+ meot1.format(formISO) 
						+'  >  '+ mbot1.format(formISO) +"</b><===>"+mbot2.format(formISO)
						+" ======== "+ (meot1>mbot1) + " or "+(meot1>mbot2);
	*/
} /*  End function calc() */

function listToModification(){ /*  Begining function listToModification() */
	$trips
	alert("hello world "+tripListJSON.length+" " +tripListJSON[1].TripName);
} /*  End function function listToModification() */

function listToList(){ /*  Begining function listToList() */
	$trips
	var e = document.myform.maop_operationokdelete.selectedIndex;
	var choice = document.myform.maop_operationokdelete.options[e].innerHTML;
	var myurl=new String("$myuri$myport/$myscript?maop_googid="+choice+"&maop_gmv=3-0");
	var r="https://"+myurl.replace(/[\/]{2,}/g,"/"); /*  Regexp used to eliminate bugs while printing URL   .... */

	var i = 0;
	var strUser = document.myform.maop_operationokdelete.options[e].text;
	while(i<tripListJSON.length&&tripListJSON[i].TripName!=strUser)i++;
	document.getElementById('err').innerHTML = "<br><b><u>Tip name:</u></b>"+tripListJSON[i].TripName +
			"<br><b><u>Begining of the trip:</u></b>"+tripListJSON[i].btd+" --- "+tripListJSON[i].btzn +
			"<br><b><u>End of the trip:</u></b>"+tripListJSON[i].etd+" --- "+tripListJSON[i].etzn +
			"<br><b><u>URL to trace the trip:</u></b><a href='"+encodeURI(r)+"'>"+encodeURI(r)+"</a>";
} /*  End function listToList() */

function listToListSend(){ /*  Begining function listToListSend() */
	$trips
	var e = document.myform.maop_operationokdelete.selectedIndex;
	var choice = document.myform.maop_operationokdelete.options[e].innerHTML;
	var myurl=new String("$myuri$myport/$myscript?maop_googid="+choice+"&maop_gmv=3-0");
	var r="https://"+myurl.replace(/[\/]{2,}/g,"/"); /*  Regexp used to eliminate bugs while printing URL   .... */

	var i = 0;
	var strUser = document.myform.maop_operationokdelete.options[e].text;
	while(i<tripListJSON.length&&tripListJSON[i].TripName!=strUser)i++;
	document.getElementById('err').innerHTML = "<br><b><u>Tip name:</u></b>"+tripListJSON[i].TripName +
	"<br><b><u>Begining of the trip:</u></b>"+tripListJSON[i].btd +
	"<br><b><u>End of the trip:</u></b>"+tripListJSON[i].etd +
	"<br><b><u>URL to trace the trip:</u></b>"+r;
} /*  End function listToListSend() */

function getTimeZone() { /*  Begin function getTimeZone() */
	return /\((.*)\)/.exec(new Date().toString())[1];
} /*  End function getTimeZone() */
		-->
//]]>
R
	my $r= $doc->script( { -type=>"text/javascript" } , "\n" . $u) ;
	return $r;
} # End sub javaScript

=head1 sub general_css_def(...)

This function creates a cascade style sheet definition for the 'a' html tag.

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

Returns String formated for style sheet for 'a' tag.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Dec 5 2009: change #help_content to .help_content and make square angle to round angle according to browser (of couse).

- I<Last modification:> Mar 9 2006

- I<Last modification:> Feb 1 2006

- I<Created on:> Jan 27 2006

=back

=cut

sub general_css_def { # Begin general_css_def
	return "body {\n"
		. "color: #07396E;\n"
		. "font-family: Courier New;\n"
		. "}\n"
		. "dl {\n"
		. "display: block;\n"
		. "width: 100%;\n"
		. "}\n"
		. "dt {\n"
		. "float: left;\n"
		. "text-align: center;\n"
		. "border: 1px solid;\n"
		. "background-color: #BEC3E5;\n"
		. "width: 14em;\n"
		. "height: 2em;\n"
		. "padding-top: 0.25em;\n"
		. "}\n"
		. "dd {\n"
		. "display: none;\n"
		. "margin: 2.0;\n"
		. "height: 12;\n"
		. "}\n"
		. "font.footer {\n"
		. "font-size: 12.0px;\n"
		. "font-style: italic;\n"
		. "}\n"
		. "P.footer {\n"
		. "border-width: 1;\n"
		. "border: double;\n"
		. "border-color: blue;\n"
		. "background-color: #E5E3FF;\n"
		. "font-family: Courier New;\n"
		. "}\n"
		. "ul.main_menu {\n"
		. "text-align: left;\n"
		. "background-color: #ABAFCE;\n"
		. "color: black;\n"
		. "border-color: #807CA5;\n"
		. "color: black;\n"
		. "}\n"
		. "#myDemo {\n"
		. "color: black;\n"
		. "margin-top: 0px;\n"
		. "padding: 5px;\n"
		. "background: grey;\n"
		. "width: 500px;\n"
		. "font-size: 12px;\n"
		#. "height: 200px;\n"
		. "position: absolute;\n"
		. "left: 500px;\n"
		. "top: 100px;\n"
		. "border-width:1px;\n"
		. "border-style: double;\n"
		. "border-radius: 25px;\n"
		. "z-index: 24;\n"
		. "}\n"
		. "#paragHeader{\n"
		. "position: relative;\n"
		#. "border-radius: 25px;\n"
		#. "top: 0px;\n"
		. "background: green;\n"
		. "height: 15%;\n"
		. "width: 100% 15%;\n"
		. "}\n"
		. "div.paragBody{\n"
		. "position: relative;\n"
		#. "color: yellow;\n"
		. "}\n"
		. "li {\n"
		. "margin-left: 2px;\n"
		. "display: inline;\n"
		. "}\n". "li.help_menu_content {\n".
		"color: red;\n"
		. "}\n"
		. "b.taken {\n"
		. "color: red;\n"
		. "}\n"
		. "table.footer {\n"
		. "font-size: 12px;\n"
		. "text-align: right;\n"
		. "color: black;\n"
		. "background-color: #D2D2FF;\n"
		. "border: double;\n"
		. "border-color: blue;\n"
		. "}\n"
		. "table.main_auth {\n"
		. "text-align: right;\n"
		. "background-color: #D2D2FF;\n"
		. "color: black;\n"
		. "font-weight: bolder;\n"
		. "border: double;\n"
		. "border-color: #807CA5;\n"
		. "}\n"
		. "table.auth {\n"
		. "text-align: right;\n"
		. "background-color: #D8D7FF;\n"
		. "color: black;\n"
		. "font-weight: bolder;\n"
		. "}\n"
		. "td.configuration {\n"
		. "vertical-align: top;\n"
		. "text-align: center;\n"
		. "background-color: #33127F;\n"
		. "color: white;\n"
		. "font-weight: bolder;\n"
		. "}\n"
		. "img {\n"
		. "border: 0;\n"
		. "}\n"
		. "h1 {\n"
		. "color: #000067;\n"
		. "font-family: Courier New;\n"
		. "}\n"
		. "i {\n"
		. "color: #07396E;\n"
		. "}\n"
		. "a.toto {\n"
		. "color: #822942;\n"
		. "font-style: italic;\n"
		. "font-weight: bold;\n"
		. "text-decoration: none;\n"
		. "}\n"

		. "a {\n"
		. "color: black;\n"
		. "font-style: italic;\n"
		. "font-weight: bold;\n"
		. "text-decoration: none;\n"
		. "}\n"

		. ".help_content {\n"
		. "-moz-border-radius:10px;\n"
		. "-webkit-border-radius: 10px;\n"
		. "border-radius: 10px;\n"
		. "color: yellow;\n"
		. "position: absolute;\n"
		. "left: 242px;\n"
		. "top: 130px;\n"
		. "width: 600px;\n"
		. "height: 500px;\n"
		. "border: 1.42px;\n"
		. "border-color: #011438;\n"
		. "border-style: double;\n"
		. "background: #1a1731;\n"
		. "opacity: .95;\n"
		. "z-index: 950;\n"
		. "}\n"
		. "#image_help {\n"
		. "background:  #7e85c1;\n"
		. "opacity: .1;\n"
		#	  . "background-image: url(\""
		#	    . &io::MyConstantBase::DIRECTORY_DEPOSIT->()
		#	      . "/my_lovely_pict.gif\");\n"
		#		. "background-repeat: no-repeat;\n"
		. "background-position: left top;\n"
		. "}\n"
		. "#parag_help {\n"
		. "position: relative;\n"
		. "text-indent: 40px;\n"
		. "left: 10px;\n"
		. "right: 10px;\n"
		. "width: 500px;\n"
		. "margin-left: 90px;\n"
		. "margin-right: 10px;\n"
		.

		#	"text-align: justify;\n".
		"}\n". "#title_help {\n".

		#	"position: absolute;\n".
		"text-align: center;\n"
		. "top: 5px;\n"
		. "width: 100%;\n"
		. "border-bottom: 2px solid #D9D073;\n"
		. "}\n"
		. "#my_face_help {\n"
		. "position: absolute;\n"
		. "left: 5px;\n"
		. "top: 5px;\n"
		. "width: 80px;\n"
		. "}\n"
		. "#err {\n"
		. "width: 40\%;\n"
		. "}\n"
		.

		#	"dl {display: block;}".
		"a:hover {\n".

		#	"zindex: 100;".
		#	"color: #4E5293;\n".
		"color: #C49209;\n".

		#	"font-size: 20px;\n".
		#	"font-family: courier;\n".
		"}\n".
		"xxx { z-index: 40; position: absolute; left: 0px;top: 120px;}\n".
		"expl_1_4 { position: absolute; left: 5px; top: 2px; z-index: 2; }\n"; 
} # End sub general_css_def

=head1 sub main_menu(...)

This function creates a general menu.

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

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jan 18 2014 add to map the trip id parameter

- I<Last modification:> Mar 04 2010: new feature... visitor map

- I<Last modification:> Feb 25 2006

- I<Created on:> Feb 1 2006

=back

=cut

sub main_menu { # Begin main_menu
	my ( $title, @help_feature ) = @_;

	#print "<![CDATA[\n";
	print "<dl><!-- begin dl -->\n";
	print "<dt>\n<a  href='JavaScript:go_to(\""
		. "http://dorey.sebastien.free.fr"
		. "\");'>My website</a>\n</dt>\n";
	#print "<dt>Other albums</dt>\n";
	print "<dt><a href=\"maop.cgi?maop_prog=g".&io::MyConstantBase::GOOGLE_MAP_SCRIPT_VERSION->()."ogle.cgi" . 
		"&maop_googid=".uri_unescape($doc->param("maop_googid"))."&maop_gmv=".&io::MyConstantBase::GOOGLE_MAP_SCRIPT_VERSION->(). &io::MyConstantBase::PATH_GOOGLE_MAP_OPT->() . "&maop_lon=$lon&maop_lat=$lat&maop_googid=".uri_unescape($doc->param('maop_googid')). "\">Visitor map</a></dt>\n";
	print "<dt onclick=\"javascript:show('smenu2');\" onmouseout=\"javascript:show();\">Help</dt>";
	print "\n<dd id=\"smenu2\"><!-- begin dd smenu2 -->\n";
	&help_menu_with_css( $title, @help_feature );
	print "</dd><!-- end dd smenu2 -->\n";
	print "</dl><!-- end dl -->\n";
} # End sub main_menu

=head1 sub help_menu_with_css(...)

This function creates a menu for help.

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

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Dec 5 2009: change to class. 

- I<Last modification:> Jul 29 2009. Html code reformated

- I<Last modification:> Feb 8 2006

- I<Created on:> Feb 8 2006

=back

=cut

sub help_menu_with_css { # Begin help_menu_with_css
	my ( $title, @info ) = @_;
	@info = (
	"Suivre attentivement les instructions dessous. / Follow carefully instructions below.",
	@info
	);
	my $img="<img src=\"" . &io::MyConstantBase::DIRECTORY_DEPOSIT->() . "/my_lovely_pict.gif\" style=\"float: right;padding-top: 25px;\" alt='+' />";

	print <<MENU;
<div class="help_content"> <!-- begin div help_content -->
<div id="title_help"> <!-- begin div title_help -->
$title
</div> <!-- end div title_help -->
<div id="my_face_help"> <!-- begin div my_face_help -->
$img
</div> <!-- end div my_face_help -->
<div id="parag_help"><!-- begin div parag_help -->
MENU

	foreach my $feature (@info){ # Begin foreach my $feature (@info)
		$feature=~s/(\/)(.*)/$1\<font color=\"#b05800\"\>$2\<\/font\>/g;
		print <<MENU;
<p>+ $feature</p>
MENU
	} # End foreach my $feature (@info)

	#    print "</p>\n";
	print <<MENU;
</div><!-- end div parag_help -->
</div> <!-- end div help_content -->
MENU
} # End sub help_menu_with_css

=head1 sub switch_from_a_specified_character_to_tag(...)

This function changes some specified character to a tag in order not to avoid miss-understanding in local Data Base when reading it.

=head2 PARAMETER(S)

=over 4

$string: that's the string to reformat.

=back

=head2 RETURNED VALUE

=over 4

New srting formated.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jan 27 2008

- I<Last modification:> Feb 6 2006

- I<Created on:> Feb 5 2006

=back

=cut

sub switch_from_a_specified_character_to_tag { # Begin switch_from_a_specified_character_to_tag
	my ($string) = @_;
print "<!-- ZOZO $string -->";
	#$string=~s/\'/\_\_TAG\_COT\_\_/g;
	#$string=~s/\"/\_\_TAG\_DCOT\_\_/g;

	#    $string=~s/\_/\_\_TAG\_UNDERSCORE\_\_/g;
	#$string=~s/\;/\_\_TAG\_SEMI\_COLUMN\_\_/g;
	$string=~s!\'!\&\#39;!g;
	$string=~s!\"!\&\#34;!g;
	$string=~s!\-!\&\#45;!g;
	$string=~s!\<!\&\#60;!g;
	$string=~s!\>!\&\#62;!g;
	$string=~s!\;!\&\#59;!g;
	
	return $string;
} # End sub switch_from_a_specified_character_to_tag

=head1 sub switch_from_a_specified_tag_to_characters(...)

This function changes some specified character tag to a character in order not to avoid miss-understanding in local Data Base when reading it.

=head2 PARAMETER(S)

=over 4

$string: that's the string to reformat.

=back

=head2 RETURNED VALUE

=over 4

New srting formated.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jan 27 2008

- I<Last modification:> Feb 6 2006

- I<Created on:> Feb 5 2006

=back

=cut

sub switch_from_a_specified_tag_to_characters { # Begin switch_from_a_specified_tag_to_characters
	my ($string) = @_;

	#$string=~s/\_\_TAG\_COT\_\_/\'/g;

	#$string=~s/\_\_TAG\_DCOT\_\_/\"/g;

#	$string=~s/\_\_TAG\_UNDERSCORE\_\_/\_/g;
#	$string=~s/\_\_TAG\_SEMI\_COLUMN\_\_/\;/g;
	$string=~s!\&\#39;!\'!g;
	$string=~s!\&\#34;!\"!g;
	$string=~s!\&\#45;!\-!g;
	$string=~s!\&\#60;!\<!g;
	$string=~s!\&\#62;!\>!g;
	$string=~s!\&\#59;!\;!g;

	return $string;
} # End sub switch_from_a_specified_tag_to_characters

=head1 sub look_for_images_used(...)

This function check if all necessary images are stored in the path where images are stored.

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

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Mar 27 2006

- I<Last modification:> Feb 17 2006

- I<Created on:> Feb 17 2006

=back

=cut

sub look_for_images_used { # Begin look_for_images_used
	if ( !-f "private/image_checked" )
	{ # Begin if (!-f "private/image_checked")
		my $counter = 0;
		print "<center><b>Checks</b>\n";
		print "</center>\n";
		print "<table>\n";
		print
		"	<tr><td align='left'><font color='blue'><b>Status</b></font></td>\n<td align='right'><font color='blue'><b>Image</b></font></td></tr>\n";
		foreach (@images_used){ # Begin foreach (@images_used)
			if ( -f "$_" ){ # Begin if (-f &io::MyConstantBase::DIRECTORY_DEPOSIT->() . "$_")
				$counter++;
				print
				"	<tr><td align='left'><b><font color='green'>ok</font></b></td>\n<td align='right'>$_</td></tr>\n";
			} # End if (-f &io::MyConstantBase::DIRECTORY_DEPOSIT->() . "$_")
			else { # Begin else
				print
				"<tr><td align='left'> N'existe pas / <font color='blue'>does not exist !!!</font><b></td>\n<td align='right'>$_</td></tr>\n";
			} # End else
		} # End foreach (@images_used)
		print "</table>\n";
		if ( ($counter) == scalar(@images_used) )
		{ # Begin if (($counter+1) == scalar(@images_used))
			open( W, ">private/image_checked" )
			|| die("Can't create private/image_checked file $!\n");
			print W "";
			close(W);
			print "All images are present in the directory "
			. &io::MyConstantBase::DIRECTORY_DEPOSIT->()
			. "<br />\n";
		} # End if (($counter+1) == scalar(@images_used))
		else { # Begin else
			exit(-1);
		} # End else
	} # End if (!-f "private/image_checked")
} # End sub look_for_images_used

=head1 sub  gets_first_page_number(...)

We got the first page that is stored. Usefull if fake page number is given.

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

Returns first page number stored in album DB file.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Mar 09 2006

- I<Created on:> Mar 09 2006

=back

=cut

sub gets_first_page_number { # Begin gets_first_page_number
	my @line =(); # Initialize
	open( R, "$file_conf_to_save" ) or error_raised("File $file_conf_to_save does not exists");
	my @f = <R>;
	close(R);
	@line = split( /\|\|/, $f[1] ); # creates 
	return &get_first_page_authorized($line[0]);
} # End sub gets_first_page_number

=head1 sub  main_help_menu_css(...)

We print help menu just for main page.

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

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Mar 27 2006

- I<Created on:> Mar 27 2006

=back

=cut

sub main_help_menu_css { # Begin main_help_menu_css
	&main_menu(
		"Aide / Help",
		"Projet commenc&eacute; en F&eacute;vrier 2003 (avec modifications succ&eacute;ssives pour rester alive). / Project started on February 2003 (many modifications have been processed since then).",
		"Les liens apparaissent en fonc&eacute;. D&eacute;s qu'ont les survolent ils changent de couleur. Cliquez dessus pour suivre le lien. / Links show up in dark color. When overfew by the mouse, color changes hence click on it to follow the link.",
		#"Les images peuvent &ecirc;tre agrandies si on clique dessus (si permission accordi&eacute;e). / Images can be enlarged if we click on it (when granted).",
		"On peut changer les pages en pressant les croix en haut &agrave; gauche. / Pages can be switched when x character at left top are clicked.",
		"Merci pour votre venue :) / Thanks for your coming :)<br /><br /><font color='LightBlue'>Remerciements &agrave; DrPc et PrimaNet pour m'avoir permis de faire des tests chez eux </font><br /><font color='red'>Thanks to DrPc and PrimaNet allowing me to do short test period of time for the album.</font>"
	);
} # End sub main_help_menu_css


=head1 sub gets_current_images_information_from_current_album(...)

When the upload action is done, a new window is raised on the screen with info related to upload. This info now is the upload percent of the image file processing to directory.

=head2 PARAMETER(S)

=over 4

=over 4

None.

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

Returns directory path.

=back

=back

=head2 ERRROR RETURNED

=over 4

=over 4

-1

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

- I<Last modification:> Mar 04 2005

- I<Created on:> Mar 03 2005

=back

=back

=cut

sub gets_current_images_information_from_current_album { # Begin gets_current_images_information_from_current_album
	my ($file_album) = @_;
	my $size_within_album_of_all_images = 0;
	open( R, "$file_album" ) || error_raised( $doc, "File [$file_album] not found!!!" );
	my @all_file = <R>;
	close(R);
	my $max_of_image_that_are_stored = scalar(@all_file);

	foreach my $line_of_album (@all_file){ # Begin foreach my $line_of_album (@all_file)
		chomp($line_of_album);
		my ($p,$l,$img_name,@others) = split(/\|\|/,$line_of_album);

		$size_within_album_of_all_images += (stat  &io::MyConstantBase::DIRECTORY_DEPOSIT->() . "$img_name")[7];
	} # End foreach my $line_of_album (@all_file)
	return ($max_of_image_that_are_stored,$size_within_album_of_all_images);
} # End sub gets_current_images_information_from_current_album


=head1 sub extra_comments(...)

Put extra comments for a psecific picture.

=head2 PARAMETER(S)

=over 4

=over 4

$current_horizontal_pos: that's current horizontal pos (param will be removed in future).

$check_with_horizontal_pos: check value with the previous field (param will be removed too).

$page: that's page value in the album.

$line: that's line value in the album.

$comment: that's the comments. All extra info to be printed to related picture.

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

Returns string that is used to print infoarmation.

=back

=back

=head2 ERRROR RETURNED

=over 4

=over 4

None.

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

- I<Last modification:> Jul 19 2009. Stats removed if IP not allowed.

- I<Last modification:> Oct 13 2006

- I<Created on:> Oct 11 2006

=back

=back

=cut

sub extra_comments { # Begin extra_comments
	if((io::MySec::urlsAllowed)[1] eq "ok" ){ # Begin if((io::MySec::urlsAllowed)[1] eq "ok" )
		if("$authorized" eq "ok"){ # Begin if("$authorized" eq "ok")
			my ($current_horizontal_pos,$check_with_horizontal_pos,$page,$line,$comment) = @_;
			#  my $javascript_f = "<script  language=\"javascript\" type=\"text/javascript\" >\nfunction comment_print_${page}_${line}(){ \nreturn new String(\"$comment\");\n } \n</script>\n";
			my $javascript_f = "<script  language=\"javascript\" type=\"text/javascript\">\nfunction comment_print_${page}_${line}(){ // Begin function comment_print_${page}_${line}\nreturn new String(\"$comment\");\n } // End function comment_print_${page}_${line} \n</script>\n";

			if ($current_horizontal_pos=~m/$check_with_horizontal_pos/i ){ # Begin if ($current_horizontal_pos=~m/$check_with_horizontal_pos/i )
				return "$javascript_f <a onclick='k=document.getElementById(\"expl_" . $page . "_". $line . "\");document.getElementById(\"expl_" . $page . "_". $line . "\").style.display=\"none\"; k.innerHTML=comment_print_${page}_${line}(); k.style.display=\"block\";'  onmouseout=\"document.getElementById('expl_" . $page . "_". $line . "').style.display='none';\">\n"
				. "\n<img src='". &io::MyConstantBase::DIRECTORY_DEPOSIT->() ."/new_cross.gif' title=\"Cliquez moi / Click me\" alt='o' />\n"
				. "</a>"
				. &tag_div_comment($page,$line);
			} # End if ($current_horizontal_pos=~m/$check_with_horizontal_pos/i )
		} # End if("$authorized" eq "ok")
	} # End if((io::MySec::urlsAllowed)[1] eq "ok" )
	return " ";
} # End sub extra_comments

=head1 sub tag_div_comment(...)

Put a tag that is used to print comments about pictures s.a pict. size, when where it was posted ...

=head2 PARAMETER(S)

=over 4

=over 4

None.

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

Returns string that format comments.

=back

=back

=head2 ERRROR RETURNED

=over 4

=over 4

None.

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

- I<Last modification:> Oct 14 2006

- I<Created on:> Oct 13 2006

=back

=back

=cut

sub tag_div_comment { # Begin tag_div_comment
	my ($page,$line) = @_;

	return 	 '<div style="width=150;height=10;background:#F9FFE5" id="expl_'. $page . "_" . $line . '"></div>';
} # End sub tag_div_comment

=head1 sub ipAddressGranted(...)

Gets IP adress from a given file.

=head2 PARAMETER(S)

=over 4

=over 4

None.

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

None.

=back

=back

=head2 ERRROR RETURNED

=over 4

=over 4

None.

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

- I<Last modification:> Aug 27 2011: $locIdName added

- I<Last modification:> Apr 11 2011: menu bug ip address granted.

- I<Last modification:> Feb 18 2011: menu modified log book admin menu.

- I<Last modification:> Mar 04 2010: menu modified log book admin menu.

- I<Last modification:> Oct 29 2009: size added to select option.

- I<Last modification:> Jul 04 2009

- I<Last modification:> Jul 14 2008

- I<Last modification:> Jul 12 2008

- I<Created on:> May Jun 2008

=back

=back

=cut

sub ipAddressGranted{ # Begin ipAddressGranted
	my $ipad=uri_unescape($doc->param("maop_urls")); # gets_ip_address ; # get IP address in order to print the right stuff on the screen 
	chomp($ipad); # Separator crlf

	# Records ip address if user agreed
	if($recPid=~m/ok/){ # Begin if($recPid=~m/ok/)
		$recPid="";
		my $url=join(/\n/,io::MyUtilities::getUrlFromFile); # pick up url from the file
		#print "zozozo$ipad<br />$url<br />";
		if($url!~/$ipad\|/){ # Begin if($url!~/$ipad\|/)
			chomp($ipad); # Remove crlf
			$ipad.="||" ; # Separator
			my $pad=uri_unescape($doc->param("maop_locIdName")); 
			#$pad=~s!\,!__COMA__!g; # replaces ; by a tag
			$ipad.=$pad;
			$ipad.="||" ; # Separator
			my $pad=uri_unescape($doc->param("maop_grantAdministration")); # grant administration of album
			chomp($pad); # Remove crlf
			$ipad.=$pad;
			#printf "---)${recPid}(-->${url}<---->${ipad}<----";
			#io::MyUtilities::setUrlFile($ipad,"${furls}");# that's for visitor
			open(R,"album/$furls") or die("album/$furls $!");
			my @t=<R>;
			close(R) or die("album/$furls $!");
			$t[0].=",$ipad";
			#print "oooooooooo)$t[0]<br />";
			$ipad=$t[0];
			$ipad=~s!,,!,!g;
			open(W,">album/$furls") or die("album/$furls $!");
			print W "$ipad";
			close(W) or die("album/$furls $!");
		} # End if($url!~/$ipad\|/)
		@urlAllowed=split(/\,/, io::MyUtilities::getUrlFromFile); # refresh list
	} # End if($recPid=~m/ok/)

	#my $sen=io::MyNav::gets_server_name;

# -------------------------autorize ip address---------
	print <<MENU;
	<fieldset>
		<legend>Administration of IP address</legend>
		<form action='${main_prog}?maop_service=auth&maop_upld=ok' method='post' enctype='multipart/form-data'>
			<input type='hidden' name='maop_prev_pid' value='$$' />
			<input type='hidden' name='maop_login' value='$lok' />
			<input type='hidden' name='maop_recPid' value='ok' />
			<input type='hidden' name='maop_maop_service' value='check' />
			IP address:<input type='text' name='maop_urls' value='$mip' /><br />
			<input type='hidden' name='maop_ssection' value='adminGroup' />
			Given name:<input type='text' name='maop_locIdName' value='$locid' />
MENU
		&accessAdminPicture;
		print <<MENU;
			<input type='submit' value='Autoriser cette adresse IP / Authorize this IP adress' />
			<input type='hidden' name='maop_ssection' value='adminGroup' />
		</form>
	</fieldset>
</td></tr><tr><td valign=top algin=left>Log book/Journal de log
MENU
	if( -d "album/hist"){ # Begin if(-d "album/hist")
		chdir("album");chdir("hist");
		
		opendir(ARD,".") || die(". $!");
		my @dr= grep { $_ ne '.' and $_ ne '..' } readdir(ARD);
		closedir(ARD) || die(". $!");
#		print "=====".scalar(@dr)." @dr <<<<br />";
		#print "<select name=\"access\" size=10>\n";
		print "<select name=\"access\">\n";
#		my @nr=();
		foreach (@dr){ # Begin foreach (@dr)
			if(length("$_")>0){# Begin if(length("$_")>0)
				#print "---->$_<<br />";
				open(R,"$_") || die("$_ $!"); my $b=<R>;close(R) || die("$_ $!");
				
				foreach my $m (reverse split(/\,/,$b)){ # Begin foreach my $m (reverse split(/\,/,$b))
					$m=~s!#!\n<br />\&nbsp\;<br />!g;
					print "<option>$m</option>\n";
				} # End foreach my $m (reverse split(/\,/,$b))
			}# End if(length("$_")>0)
		} # End foreach (@dr)
		chdir("..");chdir("..");
		print "</select>\n";
	} # End if(-d "album/hist")
} # End ipAddressGranted

=head1 sub menu_admin_GoogleMap_ID(...)

Gives authorisation to different intern application s.a googlemap, youtube

=head2 PARAMETER(S)

=over 4

=over 4

None.

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

None.

=back

=back

=head2 ERRROR RETURNED

=over 4

=over 4

None.

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

- I<Last modification:> Feb 11 2016: encodeURIComponent() added to encode trip name

- I<Last modification:> Feb 06 2016: Mail feature added when trip name created and sent to a user

- I<Last modification:> Jan 30 2016: List feature completed and finished

- I<Last modification:> Jan 24 2016: Due to to the add of prefix to variables to enhance geolocation coordinate value a regression bug was noticed. The maop_ prefix was not revised to all variables that were passed. Now it is done for this function.

- I<Last modification:> Feb 24 2014: Deletion of trip name complete. Traces in files that contains coordinates are not yet removed.

- I<Last modification:> Feb 23 2014: Infobox alert in deletion trip information added

- I<Last modification:> Feb 21 2014: menu trip added

- I<Last modification:> Aug 21 2011: menu youtube added

- I<Last modification:> Apr 11 2011: menu googlemap added

- I<Created on:> May Jun 2008

=back

=back

=cut


sub menu_admin_GoogleMap_ID{# Begin menu_admin_GoogleMap_ID
	#my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
	#my $now = sprintf("%04d-%02d-%02dT%02d:%02d:%02d", $year+1900, $mon, $mday, $hour, $min, $sec);
	my $dt=DateTime->now;#
	#$dt->set_time_zone($mtgz);
	my $nowMyFormat=join 'T', $dt->ymd, $dt->hms;
	#print "******************>$nowMyFormat\n";
	# --------------google id
	#chomp($mtzg);
	# ---------------done---------------------------------------------------------------------------------- Ruler
	my $ltznb=" Time zone/Fuseau horaire <select name='maop_ltzn_b' onchange='timeCalculusB(this.value)' >"; # List of time zone names for the begining of the trip
	my $ltzne=" Time zone/Fuseau horaire <select name='maop_ltzn_e' onchange='timeCalculusE(this.value)' >"; # List of time zone names for the end of the trip
	my $tmpltznb="";
	my $tmpltzne="";
	$ltznb.="<option value='' selected>--</option>";
	$ltzne.="<option value='' selected>--</option>";
	foreach (@{DateTime::TimeZone->all_names}){
		chomp($_);
		my $tzfe=uri_escape("$_"); # time zone field encoded
		if($_=~m/$mtzg/){
			$ltznb.="<option value='$tzfe'>$_</option>";
			$ltzne.="<option value='$tzfe'>$_</option>";
		} else{
			 $tmpltznb.="<option value='$tzfe'>$_</option>";
			 $tmpltzne.="<option value='$tzfe'>$_</option>";
		}
	}
	$tmpltznb.="</select>";
	$tmpltzne.="</select>";
	$ltznb.=$tmpltznb;
	$ltzne.=$tmpltzne;
	# ---------------done---------------------------------------------------------------------------------- Ruler
	my $tzField="<input type='hidden' name='maop_myLocalTZ' value='".uri_escape(DateTime::TimeZone->new( name => 'local' )->name())."'>";
	my $emailADM=&io::MyConstantBase::EADM->();
	print <<MENU;
<fieldset>
<legend>Google</legend>
<form action='${main_prog}?maop_service=auth&maop_upld=ok' method='post' enctype='multipart/form-data'>
<input type='hidden' name='maop_prev_id' value='$$' />
<input type='hidden' name='maop_login' value='$lok' />
<input type='hidden' name='maop_recPid' value='ok' />
<input type='hidden' name='maop_service' value='check' />
Google ID:<input type='text' name='maop_googid' />
<input type='hidden' name='maop_ssection' value='adminGoogleID' />
<input type="hidden" name="maop_TRIP_ID" value="no">
<br><input type='submit' value='Autorisation google ID map/ Authorized google ID map' />
</form>
</fieldset>	
<fieldset>
<legend>Trip operations/Opérations sur les voyages</legend>

<script  language="javascript"  type="text/javascript">

function listToDelete(){ /* Begin function listToDelete() */
	var idx = document.myform.maop_operationokdelete.selectedIndex;
	var choice = document.myform.maop_operationokdelete.options[idx].innerHTML;
	var r=confirm("Press OK button to delete ["+choice+"] trip name. Press Cancel button to avoid ["+choice+"] deletion.");

	if (r==true) {
		document.myform.submit(); 
	} else { 
		x="You pressed Cancel!"; 
	}
} /*  End function listToDelete() */

function myList(){ /*  Begin function myList() */
	var idx = document.myform.operation.selectedIndex;
	var choice = document.myform.operation.options[idx].innerHTML;
	document.getElementById('tripList').innerHTML = "in myList()";

	if(choice.match("Delete")){ /*  Begin if(choice.match("Delete")) */
		document.getElementById('tripList').innerHTML = "Trip list: $lotList" +
		"${tzField}"+
		"<input type='hidden' name='maop_prev_id' value='$$' />" +
		"<input type='hidden' name='maop_lon' value='$lon' />" +
		"<input type='hidden' name='maop_lat' value='$lat' />" +
		"<input type='hidden' name='maop_login' value='$lok' />" +
		"<input type='hidden' name='maop_recPid' value='ok' />" +
		"<input type='hidden' name='maop_service' value='check' />" +
		"<input type='hidden' name='maop_ssection' value='adminGroup' />" +
		"<input type='hidden' name='maop_TRIP_ID' value='ok' />" +
		"<input type='hidden' name='maop_TRIP_ID_DELETE' value='ok' />" +
		"<input type='button' value='confirm' onClick='listToDelete()' >";
	} /*  End if(choice.match("Delete")) */
	else if(choice.match("List")){ /*  Begin if(choice.match("List")) */
		document.getElementById('tripList').innerHTML = "Trip list: $lotList2" +
		"<input type='hidden' name='maop_prev_id' value='$$' />" +
		"${tzField}"+
		"<input type='hidden' name='maop_login' value='$lok' />" +
		"<input type='hidden' name='maop_recPid' value='ok' />" +
		"<input type='hidden' name='maop_service' value='check' />" +
		"<input type='hidden' name='maop_ssection' value='adminGroup' />" +
		"<input type='hidden' name='maop_TRIP_ID' value='ok'>" +
		"<input type='hidden' name='maop_lon' value='$lon' />" +
		"<input type='hidden' name='maop_lat' value='$lat' />" +
		"<input type='button' value='confirm' onClick='listToList()' >" +
		'<div id="err"></div>';
	} /*  End if(choice.match("List")) */
	else if(choice.match("Send")){ /*  Begin if(choice.match("Send")) */
		document.getElementById('tripList').innerHTML = "Trip list: $lotList2" +
		"<input type='hidden' name='maop_prev_id' value='$$' />" +
		"<input type='hidden' name='maop_login' value='$lok' />" +
		"${tzField}"+
		"<input type='hidden' name='maop_recPid' value='ok' />" +
		"<input type='hidden' name='maop_service' value='check' />" +
		"<input type='hidden' name='maop_ssection' value='adminGroup' />" +
		"<input type='hidden' name='maop_TRIP_ID' value='ok'>" +
		"<input type='hidden' name='maop_lon' value='$lon' />" +
		"<input type='hidden' name='maop_lat' value='$lat' />" +
		"<input type='button' value='confirm' onClick='listToListSend()' >" +
		'<div id="err"></div>';
	} /*  End if(choice.match("Send")) */
	else if(choice.match("Modification")){ /*  Begin if(choice.match("Modification")) */
		document.getElementById('tripList').innerHTML = "<!--zeub $lotList2 --> Trip list: $lotList2" +
		"<input type='hidden' name='maop_prev_id' value='$$' />" +
		"${tzField}"+
		"<input type='hidden' name='maop_login' value='$lok' />" +
		"<input type='hidden' name='maop_recPid' value='ok' />" +
		"<input type='hidden' name='maop_service' value='check' />" +
		"<input type='hidden' name='maop_ssection' value='adminGroupModif' />" +
		"<input type='hidden' name='maop_TRIP_ID' value='ok'>" +
		"<input type='hidden' name='maop_lon' value='$lon' />" +
		"<input type='hidden' name='maop_lat' value='$lat' />" +
		"<input type='button' value='confirm' onClick='listToModification()' >";
	} /*  End if(choice.match("Modification")) */
	else if(choice.match("Add")){ /*  Begin else if(choice.match("Add")) */
		//var myurl=new String("$myuri$myport/$myscript?maop_googid="+choice+"&maop_gmv=3-0");
		//var r="http://"+myurl.replace(/[\/]{2,}/g,"/"); /*  Regexp used to eliminate bugs while printing URL   ... */
		document.getElementById('tripList').innerHTML = "<input type='hidden' name='maop_lon' value='$lon' />" +
		"<input type='hidden' name='maop_lat' value='$lat' />" +
		"<input type='hidden' name='maop_prev_id' value='$$' />" +
		"${tzField}"+
		"<input type='hidden' name='maop_login' value='$lok' />" +
		"<input type='hidden' name='maop_recPid' value='ok' />" +
		"<input type='hidden' name='maop_service' value='check' />" +
		"<input type='hidden' name='maop_ssection' value='adminGroup' />" +
		"<input type='hidden' name='maop_TRIP_ID' value='ok' />" +
		"Trip name/Nom du voyage:<input type='text' name='maop_googid' pattern='[a-zA-Z0-9 ]+' /> " +
		"<br>Email address to send / Addresse mail pour envoie de courriel: <input type='email' name='maop_email' value='$emailADM'>" +
		"<br>Begining of the trip/Début du voyage<input type='datetime-local' name='maop_bdaytime' value='--' onchange='calc()'>"+
		"$ltznb" +
		"<br>End of the trip/Fin du voyage<input type='datetime-local' name='maop_edaytime' value='--' onchange='calc()'>"+
		"$ltzne" +
		"<br><input type='button' onclick='calc()' value='Checks dates oki ducky'>" +
		'<div id="err"></div>';
	} /*  End else if(choice.match("Add")) */
	else{ /*  Begin else */
		document.getElementById('tripList').innerHTML = "";
	} /*  End else */
} /*  End function myList() */

</script>

<form name="myform" method='post' enctype='multipart/form-data'>
<!-- Operation <select name="operation" onChange="myList();"> -->
Operations/Opérations <select name="operation" onChange="myList();">
<option default>--</option>
<option>Add</option>
<option>List</option>
<option>Modification</option>
<option>Send</option>
<option>Delete</option>
</select> 
<div id="tripList"></div>
</form>
</fieldset>	
<style tyle="text/css">
/*<![CDATA[*/
#notimplemented{
	-moz-transform: rotate(5deg);
	-webkit-transform: rotate(5deg);
	-o-transform: rotate(5deg);
	font-family: Courier New;
	font-size: 20px;
	color: Black;
	position: absolute;
	top: 10px;
	left: 200px;
}
div.protect {
	height:10%;
	background-color: #-1;
	position: absolute;
	filter: alpha(opacity = 55);
	opacity: .50;
	z-index: 33;
}
</style>
<div class="protect">
<div id="notimplemented">
<b>not implemented</b>
</div>
</div>
<fieldset>
<legend>Youtube</legend>
<form action='${main_prog}?maop_service=auth&maop_upld=ok' method='post' enctype='multipart/form-data'>
<input type='hidden' name='maop_prev_id' value='$$' />
<input type='hidden' name='maop_login' value='$lok' />
<input type='hidden' name='maop_recPid' value='ok' />
<input type='hidden' name='maop_service' value='check' />
<input type='hidden' name='maop_ssection' value='adminYoutubeAppearance' />
<select name="maop_youtubeAppearance"><!--  begin select youtubeAppearance -->
<option selected>Visual/Visuel</option>
<option selected>Link/Lien</option>
</select><!--  end select youtubeAppearance -->
<input type='submit' value='Autoriser/Authorize youtube' />
<!--input type='hidden' name='maop_ssecgoo' value='adminGroup'-->
</form>
</fieldset>	
MENU
	# ------------------------------------------------------------------------------------------------- Ruler
} # End menu_admin_GoogleMap_ID

=head1 sub ipAddressRemoved(...)

Remove IP from a given file ip.

=head2 PARAMETER(S)

=over 4

=over 4

None.

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

None.

=back

=back

=head2 ERRROR RETURNED

=over 4

=over 4

None.

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

- I<Last modification:> Jan 21 2011 better IP address management: IPV4, IPV6

- I<Last modification:> Jul 10 2009

- I<Last modification:> Jul 12 2008

- I<Created on:> May Jun 2008

=back

=back

=cut

sub ipAddressRemoved{ # Begin ipAddressRemoved
	if("$remPid" eq "ok"){ # Begin if("$remPid" eq "ok") remove ip address if user agreed
		my $locRemIpInf=uri_unescape($doc->param("maop_remAddrIp"));
		chomp($locRemIpInf);
		my $locRemIp=(split(/\|\|/,$locRemIpInf))[0];

		#print "$locRemIp<<<<<br />";
		if(($locRemIp=~/[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/) || ($locRemIp=~/[0-9a-z]{0,}\:[0-9a-z]{0,}\:[0-9a-z]{0,}/i))
		{ # Begin if(($locRemIp=~/[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/) || ($locRemIp=~/[0-9a-z]{0,}\:[0-9a-z]{0,}\:[0-9a-z]{0,}/i))


			#print "(URL,>$locdep/$furls<";
				open(URL,">$locdep/$furls") || die("$locdep/$furls $!");
				foreach my $m (@urlAllowed){ # Begin foreach my $i (@oth)
					my $i=(split(/\|\|/,$m))[0];
					#print "oooo>$i has to be removed from <$locRemIp><br />";
					chomp($i);
					if($locRemIp=~/$i/){ 1 ; print "removed $locRemIp<br />";}
					elsif($locRemIp=~/^\ *[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\ *$/){ # Begin elsif($locRemIp=~/^\ *[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\ *$/)
						print URL "$m,"; }# End elsif($locRemIp=~/[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/)
				} # End foreach my $i (@oth)
				close(URL) || die("$locdep/$furls $!");
				@urlAllowed=split(/\,/, io::MyUtilities::getUrlFromFile); # refresh list
			} # End if(($locRemIp=~/[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/) || ($locRemIp=~/[0-9a-z]{0,}\:[0-9a-z]{0,}\:[0-9a-z]{0,}/i))
		} # End if("$remPid" eq "ok")

		my $log=uri_unescape($doc->param("maop_login"));
		print <<MENU;
<form action='${main_prog}?maop_service=auth&maop_maop_upld=ok' method='post' enctype='multipart/form-data'>
<input type='hidden' name='maop_prev_id' value='$$' />
<input type='hidden' name='maop_login' value='$log' />
<input type='hidden' name='maop_remPid' value='ok' />
<input type='hidden' name='maop_service' value='check' />
<select name='maop_remAddrIp'>
MENU
		foreach (@urlAllowed){ # Begin foreach (@urlAllowed)
			$_=~s!__COMA__!,!g;
			print <<MENU;
<option>$_</option>
MENU
		} # End foreach (@urlAllowed)
		print <<MENU;
</select>
<input type='submit' value='Supprimer cette adresse IP / Remove this IP adress' />
<input type='hidden' name='maop_ssection' value='adminGroup' />
</form>
MENU
} # End sub ipAddressRemoved


=head1 sub showsStats(...)

Shows counter of number of visitors.

=head2 PARAMETER(S)

=over 4

=over 4

None.

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

None.

=back

=back

=head2 ERRROR RETURNED

=over 4

=over 4

None.

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

- I<Last modification:> Aug 15 2008

- I<Created on:> Aug 15 2008

=back

=back

=cut

sub showsStats{ # Begin showsStats
	if("$authorized" eq "ok"){ # Begin if("$authorized" eq "ok")
		print '<!-- Start of StatCounter Code -->' . "\n";
		print '<script  language=\"javascript\" type="text/javascript">' . "\n";
		print 'var sc_project=3923109;' . "\n";
		print 'var invisible=0;' . "\n";
		print 'var sc_partition=47;' . "\n";
		print 'var sc_click_stat=1;' . "\n";
		print 'var sc_security="955cdad8";' . "\n";
		print 'var sc_text=2;' . "\n";
		print '</script>' . "\n\n";
		#print '<br /><font color="DarkBlue">Thanks to</font> / Merci &agrave;: <a href="http://www.statcounter.com/">statcounter.com</a> ' . "\n";
		#print '<script type="text/javascript" src="http://www.statcounter.com/counter/counter.js">document.write("Thanks to http://my2.statcounter.com");</script>' . "\n";
		#print '<noscript><div class="statcounter">' . "\n";
		#print 'HITS <a href="http://www.statcounter.com/free_web_stats.html" target="_blank">' . "\n";
		#print '\n<img class="statcounter" src="http://c.statcounter.com/3923109/0/955cdad8/0/" alt="web statistics" /></a>' . "\n";
		#print '</div></noscript>' . "\n";
		#print '<!-- End of StatCounter Code -->' . "\n";
	} # End if("$authorized" eq "ok")
} # End sub showsStats

=head1 sub set_history(...)

Creates a log file.

=head2 PARAMETER(S)

=over 4

=over 4

$u: url
$d: formated date
$p: page number
$f: file to store
$l: geoloc coordinated added

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

None.

=back

=back

=head2 ERRROR RETURNED

=over 4

=over 4

None.

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

- I<Last modification:> Dec 24 2014 optimized sub routine

- I<Last modification:> Dec 23 2014 add extra tests to record trip rec ok if in rage otherwise no (hdf history directory file; path to store data)

- I<Last modification:> May 10 2014 add extra parameter (hdf history directory file; path to store data)

- I<Last modification:> Jan 18 2014 put the trip name in history

- I<Last modification:> Feb 02 2012 geoloc added

- I<Last modification:> Aug 16 2008

- I<Created on:> Aug 14 2008

=back

=back

=cut

sub set_history{ # Begin set_history
	my ($u,$d,$p,$f,$l,$hdf)=@_; # ip|url,date,page,fields to store,history directory file

	#print "<br>----------->>($u,<br>$d,<br>$p,<br>$f,<br>$l,<br>$hdf<br>)<br>\n";

#	print ">>>>>>>>>>>>>>>>>>>>>>>>>>> <u>$dt3</u><$dtb not passed\n";
	io::MyUtilities::setUrlFile("$u#$d#$p#$l","$f",$hdf); 
	return;
} # End sub set_history

=head1 sub accessAdminPicture(...)

Acces to pictures menu admin Granted to public or not Granted to pulic. That's the menu where IP addresses can  be admin (Groups & URLs). The field is Administrer album/Administrate Album.

=head2 PARAMETER(S)

=over 4

=over 4

None

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

None.

=back

=back

=head2 ERRROR RETURNED

=over 4

=over 4

None.

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

- I<Last modification:> Jul 20 2009. Tag admin granted added. allow administration on this machine.

- I<Created on:> Jul 20 2009

=back

=back

=cut

sub accessAdminPicture{ # Begin accessAdminPicture
	print <<MENU
<br />Administrer album/Administrate Album:
<select name="maop_grantAdministration">
	<option selected>Public non autorise/Public not granted</option>
	<option>Administration autorisee/Administration granted</option>
</select>
MENU
} # End accessAdminPicture

=head1 sub accessToPicture(...)

Pictures access to public or not Granted to pulic. This belongs to the menu Administrer des photos/Administration of pictures.

=head2 PARAMETER(S)

=over 4

=over 4

None

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

None.

=back

=back

=head2 ERRROR RETURNED

=over 4

=over 4

None.

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

- I<Last modification: v1.6.13.9> Jul 17 2012. From DB or table print data recorded from user.

- I<Last modification:> Sept 26 2009. Formalize html script.

- I<Last modification:> Jul 20 2009. Tag admin granted added. allow administration on this machine.

- I<Last modification:> Jul 04 2009

- I<Created on:> Jul 04 2009

=back

=back

=cut

sub accessToPicture{ # Begin accessToPicture
	my $grantPicture=($grant=~m!ko!) ? "Public not granted" 
		: (($grant=~m!adm!) ? "Admin granted" : "Public granted") ;
	
	#print "<br>Access to picture: $grant-------$grantPicture<br>$tag------<br>";

	return "How to view a picture:" .
		$doc->popup_menu(
				 -name=>'maop_grantPicture',
				 -values=>[
						'Public granted',
						'Public not granted',
						'Admin granted'
					  ],
				 -defaults=>[
						"$grantPicture"
					    ]
			       ) ; 
} # End accessToPicture

=head1 sub look_if_page_authorized(...)

Looks if a given page is authorized to looked.

=head2 PARAMETER(S)

=over 4

=over 4

$pgnu: page number

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

0 ok otherwise <0.

=back

=back

=head2 ERRROR RETURNED

=over 4

=over 4

None.

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

- I<Last modification:> Jul 05 2009

- I<Created on:> Jul 04 2009

=back

=back

=cut

sub look_if_page_authorized { # Begin look_if_page_authorized
	my ($pgnu)=@_; # page number
	my ($allow,$authorized)=io::MySec::urlsAllowed;
	if($authorized=~m/ok/){ return 0; }
	open( R, "$file_conf_to_save" ) or error_raised("File $file_conf_to_save does not exists");
	my @f = <R>;
	close(R) or error_raised("File $file_conf_to_save does not exists");
	#print "<br />==============<br />";
	foreach my $i (@f){ # Begin foreach my $i (@f)
		my @z=split(/\|\|/,${i});
		# case page asked exist
		if(${i}=~m/^${pgnu}\|\|/){ # Begin if(${i}=~m/^${pgnu}-/)
			if($z[12]=~m/ok/){ # Begin if($z[12]=~m/ok/)
				return 0; 
			} # End if($z[12]=~m/ok/)
		} # End if(${i}=~m/^${pgnu}-/)
	} # End foreach my $i (@f)
	return -1 ; # everything is ok
} # End sub look_if_page_authorized

=head1 sub get_first_page_authorized(...)

Gets first page authorized according to rigths granted.

=head2 PARAMETER(S)

=over 4

=over 4

$pgnu: page number

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

First page authorized.

=back

=back

=head2 ERRROR RETURNED

=over 4

=over 4

None.

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

- I<Last modification:> Jul 04 2009

- I<Created on:> Jul 04 2009

=back

=back

=cut

sub get_first_page_authorized { # Begin look_if_page_authorized
	my ($pgnu)=@_; # page number
	my ($allow,$authorized)=io::MySec::urlsAllowed;
	if($authorized=~m/ok/){ return ${pgnu}; }
	open( R, "$file_conf_to_save" ) or error_raised("File $file_conf_to_save does not exists");
	my @f = <R>;
	close(R) or error_raised("File $file_conf_to_save does not exists");
	foreach my $i (@f){ # Begin foreach my $i (@f)
		#print "00000000000)$i<br />\n";
		my @z=split(/\|\|/,${i}); # splits fields
		# case page asked exist
		if($z[12]=~m/ok/){ # Begin if($z[12]=~m/ok/)
			return $z[0];
		} # End if($z[12]=~m/ok/)
	} # End foreach my $i (@f)
	return 0 ; # everything is ok
} # End sub look_if_page_authorized

=head1 sub firstChoicetMenuadmin(...)

First menu to admin.

=head2 PARAMETER(S)

=over 4

=over 4

None

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

First page authorized.

=back

=back

=head2 ERRROR RETURNED

=over 4

=over 4

None.

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

- I<Last modification:> Sep 03 2009 switch recPid value from ok to none value.

- I<Last modification:> Jul 28 2009

- I<Created on:> Jul 04 2009

=back

=back

=cut

sub firstChoicetMenuadmin{ # Begin firstChoicetMenuadmin
	my $login=uri_unescape($doc->param("maop_login")) ; # Gets login
	my $password=uri_unescape($doc->param("maop_password")) ; # Gets login
	print &menu_page_title( "<br /><br />MENU PRINCIPAL<br /><font color='blue'>MAIN MENU</font>" . $doc->br );
	print <<MENU;
<br />
<br />
<br />
<form action='${main_prog}?maop_service=auth&maop_maop_upld=ok' method='post' name="maop_adminMenu" enctype='multipart/form-data'>
<input type='hidden' name='maop_prev_id' value='$$' />
<input type='hidden' name='maop_login' value='logi n' />
<input type='hidden' name='maop_password' value='passwor d' />
<input type='hidden' name='maop_recPid' value='ok' />
<input type='hidden' name='maop_service' value='check' />
<input type='hidden' name='maop_ssection' value='adminPict' />
<input type='submit' value="Administration des photos/Administration of pictures" />
<br />
</form>
<form id="fAdmin" action='${main_prog}?maop_service=auth&maop_maop_upld=ok' method='post' name="maop_adminMenu" enctype='multipart/form-data'>
MENU
	print "<input type='hidden' name='maop_myLocalTZ' value='".uri_escape(DateTime::TimeZone->new( name => 'local' )->name())."'>\n";
	print <<MENU;
<input type='hidden' name='maop_prev_id' value='$$' />
<input type='hidden' name='maop_login' value='logi n' />
<input type='hidden' name='maop_password' value='passwor d' />
<input type='hidden' name='maop_recPid' value='' />
<input type='hidden' name='maop_service' value='check' />
<input type='hidden' name='maop_ssection' value='adminGroup' />
<input type='submit' value="Groups & URLs/Groups & URLs" onclick="paramEncode('fAdmin')"/>
<br />
</form>
<form action='${main_prog}' method='post' enctype='multipart/form-data'>
<input type='hidden' name='maop_ssection' value='' />
<input type='submit' value="Retour vers l'album/Go back to album" />
</form>
<br />
MENU
	# Footer is here because it is printed from here on all pages without modifying other page structures
	#&showsStats;
		print <<MENU;
	<br />
	<br />
	<script>
		print_info("My hello world",
			   "1 hello world<br>"
			   +"2 hello world<br>"
			   +"3 helloworld<br>"
			   +"helloworld<br>"
			   +"helloworld<br>"
			   +"helloworld<br>"
			   +"helloworld<br>"
		   );
	   </script>
	   ->
MENU
	print &add_print_info("<br>1basic test<br>");
		print <<MENU;
		<-
	   <script>
		   add_print_info( "helloworld<br>"
			   +"helloworld<br>"
			   +"helloworld<br>"
			   +"helloworld<br>"
			   +"helloworld<br>"
			   +"helloworld<br>"
			   +"helloworld<br>"
		   );
		add_print_info("<br>---------------------->My hello world<br>");
	   </script>
MENU
	&add_print_info("2222 basic test");
	print io::MyUtilities::footer(
						$doc,
						&io::MyConstantBase::DIRECTORY_DEPOSIT->() . "powered.gif",
						&io::MyConstantBase::DIRECTORY_DEPOSIT->() . "jangada.gif",
						"http://www.perl.org", 
						ALBUM_VERSION ,
						 &io::MyConstantBase::TESTED_WITH_BROWSERS->(),
						 &io::MyConstantBase::HOSTED_BY->(),
						 &io::MyConstantBase::HOSTED_BY_URL->());
	&add_print_info("<br>2basic test");
	print <<MENU;
</div>
<script>
	add_print_info("<br><br><br><br><br><br><br><br>zaeazeazeazeazeazeazeaeazeazea");
</script>
</body>
</html>
MENU
	exit(-1) ;
} # End sub firstChoicetMenuadmin

=head1 sub groupAndStuff(...)

First menu to admin grpous and other that deals with Internet adresses.

=head2 PARAMETER(S)

=over 4

=over 4

None

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

None.

=back

=back

=head2 ERRROR RETURNED

=over 4

=over 4

None.

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

- I<Last modification:> Jul 28 2009

- I<Created on:> Jul 04 2009

=back

=back

=cut

# attention work here to check if address can be recorded
sub groupAndStuff{ # Begin groupAndStuff
	print &menu_page_title( "<br /><br />ADMINISTRATION DES GROUPES/ADRESSES IP<br /><font color='blue'>ADMINISTRATION OF GROUPS/IP ADDRESSES</font>" . $doc->br );
	print <<MENU;
<table border="0">
<tr>
<td>
MENU
	# put infinite loop here and debug with gdb for ie
	# inject data in "wait" see below
	# <p id="wait"></p>
	# <script>
	# 	var x=document.getElementById("wait");
	# 	x.innerHTML="Please wait while loading..."; /* pid  progr */
	# </script>
	# put infinite loop

	&my_wait(&io::MyConstantBase::LOOP->(),5);
	&menu_admin_GoogleMap_ID; # --------------------> we locate where the error is
	&ipAddressGranted;
	print <<MENU;
</td>
</tr>
<tr>
<td> ********************************<br>
MENU

	&ipAddressRemoved;
	print <<MENU;
</td>
</tr>
</table>
MENU
	&menu_leave_admin;
} # End sub groupAndStuff

=head1 sub setGoogleID(...)

Record in $fname the id

=head2 PARAMETER(S)

=over 4

=over 4

$fname: file name where to save google id map

$googleid: $goohleid: that's the google id

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

None.

=back

=back

=head2 ERRROR RETURNED

=over 4

=over 4

None.

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

- I<Last modification:> Apr 8 2016 regexp added $tn=~s/[\ \n\t]*\-trip/\-trip/; now it seems to be ok

- I<Last modification:> Feb 15 2016 now send email in html form.

- I<Last modification:> Dec 24 2014 bug cleared. d1#d1 recorded instread of d1#d2 s.a d1<d2 where dn is a date and 0<=n<=inf n is an integer inf is the infinite

- I<Last modification:> Jan 18 2014 put the trip name

- I<Last modification:> Feb 13 2011

- I<Created on:> Feb 13 2011

=back

=back

=cut

sub setGoogleID{# Begin setGoogleID
	my ($fname,$googleid)=@_;# $fname: file name where to save google id map;$goohleid: that's the google id
	my $method = $ENV{'REQUEST_METHOD'} ;
	#if($googlid=~m/[\n\t\ ]*$/){ print "</br></br></br><b>>>>>>>>>>>>>>>$googleid<".length($googleid).">>>>>>>>>>>>>>>>>..there is a match in the trip name</b></br>";}
	#$googlid=~s/[\n\t\ ]*$/\_space/;
	#if($googlid=~m/[\n\t\ ]*$/){ print "</br></br></br><b>test 2>>>>>>>>>>>$googlid<".length($googleid).">>>>>>>>>>>>>>>>>>>>..there is a match in the trip name</b></br>";}
	chomp($method);

#	print "We go in param googoid<br>";
	if($method ne "POST"){ # Begin if($method ne "POST")
		my $param_trip_delete=uri_unescape($doc->param("maop_TRIP_ID_DELETE"));
		chomp($param_trip_delete);
		if($param_trip_delete=~m/^ok$/){ # Begin if($param_trip_delete=~m/^ok$/)
			chdir(&io::MyConstantBase::PATH_GOOGLE_MAP_TRIP->());
			#print "file to delete " . &io::MyConstantBase::PATH_GOOGLE_MAP_TRIP->() . "/" . uri_unescape($doc->param("maop_operationokdelete")) . "-trips <br>";
			unlink(uri_unescape($doc->param("maop_operationokdelete")) . "-trips");
			if( ! -f uri_unescape($doc->param("maop_operationokdelete")) . "-trips"){ # Begin if( ! -f uri_unescape($doc->param("maop_operationokdelete")) . "-trips")
				print "<br><br><br><br>Trip " . uri_unescape($doc->param("maop_operationokdelete")) . " removed<br>";
			} # End if( ! -f uri_unescape($doc->param("maop_operationokdelete")) . "-trips")

			chdir("../..");
		
		} # End if($param_trip_delete=~m/^ok$/)
	} # End if($method ne "POST")

	print "Stge 1<br>";
	chomp($fname);#chomp($googleid);
	print "if($param_trip=~m/^ok$/)\n<br>";
#exit(-1);
	if($param_trip=~m/^ok$/){ # Begin if($param_trip=~m/^ok$/)
		#my $tn=&io::MyConstantBase::PATH_GOOGLE_MAP_TRIP->().uri_escape($googleid)."-".&io::MyConstantBase::TRIP_NAME->(); # Trip name
		my $tn=&io::MyConstantBase::PATH_GOOGLE_MAP_TRIP->().$googleid."-".&io::MyConstantBase::TRIP_NAME->(); # Trip name
		$tn=~s/[\ \n\t]*\-trip/\-trip/;
		print "Stge 2 [$googleid]".length($googleid)."<br>";

		if(length($googleid)!=0){ # Begin if(length($googleid)!=0)
			print '<div id="myDemo">';
			print "trip name [$tn] does not exist<br>" if ( ! -f "$tn" );
			print "trip name [$tn] does exist<br>" if ( -f "$tn" );
			print "</div>";
			if( ! -f "$tn" ){ # Begin if( ! -f "$tn" )
				my $bdaytime=uri_unescape($doc->param("maop_bdaytime"));
				my $edaytime=uri_unescape($doc->param("maop_edaytime"));
				my $ltzn_b=uri_unescape($doc->param('maop_ltzn_b'));
				my $ltzn_e=uri_unescape($doc->param('maop_ltzn_e'));

				print "record in $tn<br>";
				if(length($bdaytime)!=0){ # Begin if(length($bdaytime)!=0)
					if(length($edaytime)!=0){ # Begin if(length($edaytime)!=0)
						#print $bdaytime . "#" . $edaytime.'<br>';
						# We create the file that contains data related to trip s.a name, bdate,edate of trip
						print "</br>where we store data [$tn]</br>";
						#print "B4 Storing++++++>".getcwd()."<-----<br>\n"; 
						#print "B----------------><u>${bdaytime}#${edaytime}#${ltzn_b}#${ltzn_e}</u><br>";
						
						$tn=&do_untaint($tn);
						open(W,">","$tn")||die("Error: [$tn] $!");
						print W "${bdaytime}#${edaytime}#${ltzn_b}#${ltzn_e}";
						close(W);
						#print "E----------------><u>${bdaytime}#${edaytime}#${ltzn_b}#${ltzn_e}</u><br>";
						# ---------------------------------------------------
						# format received yyyy-mm-ddThh:mm for params received in maop_bdaytime, maop_edaytime
						my ($bdp,$bhp)=split(/T/,uri_unescape($doc->param('maop_bdaytime')));# Begin date trip param,begin hour trip param
						# prune out info from $bdp and $bhp
						my ($bdy,$bdm,$bdd)=split(/\-/,$bdp);# Begin day year, begin day month, begin day day
						my ($bhh,$bhm)=split(/\:/,$bhp);# Begin hour hour,begin hour minute
						my ($edy,$edm,$edd)=split(/\-/,$bdp);# End day year, end day month, end day day
						my ($ehh,$ehm)=split(/\:/,$bhp);# End hour hour,end hour minute
						#print "begin 1 datetime<br>";
						my $dtb= DateTime->new( year       => $bdy,
									month      => $bdm,
									day        => $bdd,
									hour       => $bhh,
									minute     => $bhm,
									second     => 0,
								); # creates object date time for begining of the trip
								#print "end 1 datetime<br>";
								#print "begin 2 datetime<br>";
						my $dte= DateTime->new( year       => $edy,
									month      => $edm,
									day        => $edd,
									hour       => $ehh,
									minute     => $ehm,
									second     => 0,
								); # creates object date time for end of the trip
								#print "end 2 datetime<br>";
						# ---------------------------------------------------
						#print "A-<br>";
						my $loc_maop_ltzn_b=uri_unescape($doc->param('maop_ltzn_b'));
						#print "B-<br>";
						my $tzbt=DateTime::TimeZone->new( name => $loc_maop_ltzn_b ); # Time zone begining of the trip
						#print "C-<br>";
						my $loc_maop_ltzn_e=uri_unescape($doc->param('maop_ltzn_e'));
						my $tzet=DateTime::TimeZone->new( name => $loc_maop_ltzn_e ); # Time zone end of the trip
						#print "D-<br>";
						my $to = uri_unescape($doc->param("maop_email"));
						#print "E-<br>";
						my $from = 'Bot from MAOP<shark.b@laposte.net>';
						#print "F-<br>";
						my $maop_url_loc = uri_unescape($doc->param('maop_url')); $maop_url_loc=~s/[\n\t\ ]*$//; # watch out there is a variable that already contains that value it is $mgidt in another word we shave all characters that are at the end of the memory taken from parameter
						my $maop_url_loc2 = uri_unescape($doc->param('maop_url')); $maop_url_loc2=~s/[\n\t\ ]*$//; # watch out there is a variable that already contains that value it is $mgidt in another word we shave all characters that are at the end of the memory taken from parameter
						#print "G-<br>";
						my $subject = "Trip / Voyage:" . uri_unescape($doc->param('maop_googid')); 
						my $loc=&io::MyConstantBase::PROTO_USED->().&io::MyConstantBase::LOCAL_HOSTED_BY_URL->().&io::MyConstantBase::WEB_ACCOUNT->() ."cgi-bin/maop.cgi\?maop_googid=". uri_unescape($doc->param('maop_googid'));
						my $dist=&io::MyConstantBase::PROTO_USED->().&io::MyConstantBase::DISTANT_HOSTED_BY_URL->().&io::MyConstantBase::WEB_ACCOUNT->()."cgi-bin/maop.cgi\?maop_googid=". uri_unescape($doc->param('maop_googid'));
						my $loc_map=&io::MyConstantBase::PROTO_USED->().&io::MyConstantBase::LOCAL_HOSTED_BY_URL->().&io::MyConstantBase::WEB_ACCOUNT->() ."cgi-bin/maop.cgi\?maop_googid=". uri_unescape($doc->param('maop_googid')).'&maop_gmv='.&io::MyConstantBase::MAP_VER_IN_USE->().'&maop_prog='.&io::MyConstantBase::MAP_PROG->();
						my $dist_map=&io::MyConstantBase::PROTO_USED->().&io::MyConstantBase::DISTANT_HOSTED_BY_URL->().&io::MyConstantBase::WEB_ACCOUNT->()."cgi-bin/maop.cgi\?maop_googid=". uri_unescape($doc->param('maop_googid')).'&maop_gmv='.&io::MyConstantBase::MAP_VER_IN_USE->().'&maop_prog='.&io::MyConstantBase::MAP_PROG->();

						my $message = "\n".
							"<b><u>Begining of the trip and Time Zone/<i>Debut du voyage et decallage horaire</i>:</u></b>\n".
							"<ul>".
								 "<li>".uri_unescape($doc->param('maop_bdaytime')) . " " . $tzbt->name . " " . $tzbt->offset_for_local_datetime( $dtb ) . "s"."</li>".
							"</ul>\n".
							"<b><u>End of the trip and Time Zone/<i>Fin du voyage et decalage horaire</i>:</u></b>".
							"<ul>".
								"<li>".uri_unescape($doc->param('maop_edaytime')). " " . $tzet->name . " " . $tzet->offset_for_local_datetime( $dte ) . "s"."</li>".
							"</ul>\n".
							"<b><u>Pinpoint the map /<i>Mettre un point lors du voyage</i>:</u></b>\n".
							"<ul>".
								"<li><span style='background-color:red'><a href='".$loc."'>Trip / Voyage</a></span> (LAN)</li>".
								"<li><span style='background-color:green'><a href='".$dist."'>Trip / Voyage</a></span> (WAN)</li>".
							"</ul>\n".
							"<b><u>Watch the trip on the map/<i>Regarder le voyage sur une carte</i>:</u></b>\n".
							"<ul>".
								"<li><span style='background-color:red'><a href='".$loc_map. "'>Trip / Voyage</a></span> (LAN)</li>".
								"<li><span style='background-color:green'><a href='".$dist_map. "'>Trip / Voyage</a></span> (WAN)</li>".
							"</ul>\n".
							"Friendly yours,<br>Bot from MAOP";

						$ENV{PATH}='/bin:/usr/bin:/usr/local/bin';

						$to=&do_untaint($to);
						$from=&do_untaint($from);
						$subject=&do_untaint($subject);

						# ======MAKE ICS FILE======================
						my ($bdt,$btt)=split(/T/, uri_unescape($doc->param('maop_bdaytime'))); # Begining Date Trip , Begining Time Trip (all departure)
						my @dbd=split(/\-/,$bdt); # Prune out Date for departure Begining of the trip
						my @dtd=split(/\:/,$btt); # Prune out Tim for departure Begining of the trip

						# ----------------------------------

						my ($edt,$ett)=split(/T/, uri_unescape($doc->param('maop_edaytime'))); # End Date Trip , End Time Trip (all Arival)
						my @ebd=split(/\-/,$edt); # Prune out Date for departure Begining of the trip
						my @etd=split(/\:/,$ett); # Prune out Tim for departure Begining of the trip

						my $calendar = Data::ICal->new();

						my $vtodo = Data::ICal::Entry::Event->new();
						$vtodo->add_properties(
									summary => "$subject",
									description => "$message",
									dtstart => Date::ICal->new ( day => $dbd[2],
												       month => $dbd[1],
												       year => $dbd[0],
												       hour => $dtd[0],
												       min => $dtd[1],
												       sec => 00
												)->ical,
									dtend => Date::ICal->new(day => $ebd[2],
												       month => $ebd[1],
												       year => $ebd[0],
												       hour => $etd[0],
												       min => $etd[1],
												       sec => 00
												)->ical,
						);
						$calendar->add_entry($vtodo);
						open(WC,">",&io::MyConstantBase::PATH_FOR_CALENDAR_ICS->())||die("Error iCal: $!");
						print WC $calendar->as_string;
						close(WC)||die("Error iCal: $!");
						# ============================

						#$message=&do_untaint($message);
						open(FILE, ">", &io::MyConstantBase::BODY_MESS_TO_SEND->()) or die("Cannot open ".&io::BODY_MESS_TO_SEND->().": $!");
						print FILE "$message";
						close(FILE);
						my $attachment=&io::MyConstantBase::PATH_FOR_CALENDAR_ICS->();

						my $mypath=&io::MyConstantBase::PATH_TO_SENDMAIL_OPT->();
						$mypath=&do_untaint($mypath);
						open(MAIL,"$mypath") || die("Error: $!");
						# Email Header
						print MAIL "To: $to\n";
						#print MAIL "To: sebastien.dorey\@laposte.net\n";
						print MAIL "From: $from\n";
						print MAIL "Subject: $subject\n";
						print MAIL "Content-Type: multipart/mixed; boundary=frontier\n";
						print MAIL "--frontier\n";
						print MAIL "Content-Type: text/html; charset=us-ascii\n";
						print MAIL "MIME-Version: 1.0\n\n";
						open(FILE, "<",  &io::MyConstantBase::BODY_MESS_TO_SEND->() ) or die("Cannot open ".  &io::MyConstantBase::BODY_MESS_TO_SEND->() .":$!");
						print MAIL <FILE>;
						close(FILE);
						print MAIL "\n\n";
						print MAIL "--frontier\n";
						chomp(my $basename=`basename $attachment`);
						print MAIL "Content-Disposition: attachment; filename=$basename\n";
						print MAIL "Content-Type: text/calendar; name=$attachment\n\n";
						open(FILE, "<", "$attachment") or die "Cannot open $attachment: $!";
						print MAIL <FILE>;
						print MAIL "\n";
						close(FILE);
						close(MAIL) || die("Error: $!");

						print "A mail to $to is being sent...\n<br>";
					} # End if(length($edaytime)!=0)
					else{ # Begin else
						#print "<br><br><BR><i>ERRROR<br>";
						#print "Must set dates<br>";
					} # End else
				} # End if(length($bdaytime)!=0)
				else{ # Begin else
					#print "<br><BR><br><i>ERRROR<br>";
					#print "Must set dates<br>";
				} # End else
			} # End if( ! -f "$tn" )
			else { # Begin else
				#print "<br><BR><br><i>ERRROR<br>";
				#print "Trip $googleid already exist. Cannot create it...<br>";
			} # End else
		} # End if(length($googleid)!=0)
		else{ # Begin else
			#print "<br><BR><br><i>ERRROR<br>";
			#print "Must set a trip name<br>";
		} # End else
	} # End if($param_trip=~m/^ok$/)
	else{ # Begin else
		open(W,">$fname");
		print W "$googleid";
		close(W);
	} # End else
} # End setGoogleID

# -----------------------------------
=head1 sub myrec(...)

Sort of mouchard the is used to debug

=head2 PARAMETER(S)

=over 4

=over 4

$c: message for instance the case

$f: file error created,

$m: message due refering to case

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

None.

=back

=back

=head2 ERRROR RETURNED

=over 4

=over 4

None.

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

- I<Created on:> Feb 13 2011

=back

=back

=cut

sub myrec{ # Begin sub myrec
	my ($c,$f,$m)=@_; # $c: message,$f: file error (html),$m:message
	my $mainp=(split(/[\\\/]/,"$0"))[scalar(split(/[\\\/]/,"$0"))-1]; # gets program name
	my $dt = DateTime->from_epoch( epoch => time() );# Current date format DateTime

	open(W,">>$f")||die("$f error $!");
	print W "<pre>\n";
	print W "<b>******************Begin**************************<br>\n";
	print W "*******************\n$mgidt\n*************************<br>\n";
	print W "********************************************</b><br>\n";
	print W "--------------------\n$mainp\n------------$dt---------------------\n";
	print W "$c:\n$m\n\n";
	print W "<br>current path:".cwd()."\n\n<br>";
	print W "<b>******************End**************************<br>\n";
	print W "</pre><br><br>\n";
	close(W)||die("error close$!");
} # End sub myrec

=head1 sub my_wait

Creates html div to promp a message. To unlock a specific file (see $loop) must be present in the current directory to unlock.
Message refresh every $sec and check if $loop is present in current directory to unlock.

=head2 PARAMETER(S)

=over 4

=over 4

$loop: file that block execution if missing.

$sec: sleep $sec before checking if $loop exists.

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

None.

=back

=back

=head2 ERRROR RETURNED

=over 4

=over 4

None.

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

- I<Created on:> Nov 3 2017

=back

=back

=cut

sub my_wait{ # Begin sub my_wait
	my ($loop,$sec) = @_ ; 
	my $b = time;

	print <<MENU;
	<p id="wait2"></p>
MENU

	while( ! -f "$loop" ){ # Begin while( ! -f "$loop" )
		sleep $sec;
		my $e = time;
		my $r = $e -  $b;
		print <<MENU;
<script  language=\"javascript\" type="text/javascript">
	var x=document.getElementById("wait2");
	x.innerHTML="Please wait while loading since ${r}s ... follow the steps bellow to debug...<br>gdb -p $$<br>touch $loop"; /* pid  progr */
</script>
MENU
	} # End while( ! -f "$loop" )
} # End sub my_wait

=head1 sub loadDataTrips

Set global variables to set the menus to set the trips

=head2 PARAMETER(S)

=over 4

=over 4

no parameters for the time being.

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

None.

=back

=back

=head2 ERRROR RETURNED

=over 4

=over 4

None.

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

- I<Created on:> Nov 10 2017

=back

=back

=cut

sub loadDataTrips{ # Begin sub loadDataTrips
	#print "Content-Type: text/html\n\n";
	#print "<br>Get current path ------>>>>".getcwd()."<<<<<-------<br>\n";
	print "\n".'<script src="../js/CallServer.js"></script>'."\n";
	print '<script src="../js/moment.min.js"></script>'."\n";
	print '<script src="../js/moment-timezone-with-data-2012-2022.min.js"></script>'."\n";
	if ( ($resPing==0) && ($resAuth==0) ){ # Begin if ( ($resPing==0) && ($resAuth==0) ) 
		chdir(&io::MyConstantBase::PATH_GOOGLE_MAP_TRIP->());
		#print "<br>Get current path ------>>>>".getcwd()."<<<<<-------<br>\n";
		opendir(ARD,".") || die(". $!");# open current directory
		my @dr= grep { $_ =~ m/\-trips$/ } readdir(ARD);# parse current directory
		closedir(ARD) || die(". $!");# close directory

		# chdir("../..");
		# the following variables were moved from local to global
		#
		#my $trips="var tripListJSON=[";
		#my $lot="var lot= new Array('--',"; # List of trips
		#my $lotList="<select name='maop_operationokdelete' onChange='listToDelete()'>"; # List of trips
		#my $lotList2="<select name='maop_operationokdelete' onChange='listToList()'>"; # List of trips

	#
	# **************************************************************	
	#
		foreach my $i (sort @dr){ # Begin foreach my $i (@dr)
			#print "<br>*************>$i<br>";
			$lot.="\"$i\",\n";
			open(R,"$i") || die("error open $!");
			my @ftr=<R>; # File trip read
			my ($btd,$etd,$btzn,$etzn)=split(/\#/,$ftr[0]);# Begin trip date,end trip date
			$i=~s/-trips$//;
			chomp($i);chomp($btd);chomp($etd);chomp($btzn); chomp($etzn);
			$trips.="\t\t\t{\"TripName\":\"$i\",\"btd\":\"$btd\",\"etd\":\"$etd\",\"btzn\":\"$btzn\",\"etzn\":\"$etzn\"},\n";
			close(R) || die("error close $!");
			$lotList.="<option>$i</option>";
			$lotList2.="<option>$i</option>";
		} # End foreach my $i (@dr)
		chdir("../..");
	} # End if ( ($resPing==0) && ($resAuth==0) ) 
	$trips=~s/\,\n$//;
	$trips.="];\n\n";
# --------------------------------------------------------- need to check here for the list. It depends 
	$lot=~s/,$/\)\;/; # They array is built of trips
# --------------------------------------------------------- 
	$lotList.="</select>";
	$lotList2.="</select>";
} # End sub loadDataTrips

=head1 sub manageError(...)

This function creates an error report in html when html field filled.

=head2 PARAMETER(S)

=over 4

$header: header

$eEn: message error in English 

$eFr: message error in French

=back

=head2 RETURNED VALUE

=over 4

String formated html 5 with css for an error report (not the same for die...).

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG(S) KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Created on:> Feb 9 2018

=back

=cut

sub manageError{ # Begin sub manageError
	my ($header,$eEn,$eFr)=@_; # header,error English, error French
	return "<h3>$header</h3>\n<div class='customHr'>.</div>\n<p>$eEn<br>$eFr</p>";
} # End sub manageError

=head1 sub my_promptB(...)

A prompt is used between each screen. This prompt is used too for debugging too.

=head2 PARAMETER(S)

=over 4

=over 4

$debug: info to help debugging.

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

Returns HTML structure for the new prompt.

=back

=back

=head2 ERRROR RETURNED

=over 4

=over 4

none.

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

- I<Last modification:>  Apr 24 2018

- I<Created on:> Apr 24 2018

=back

=back

=cut

sub my_promptB{ # Begin sub my_promptB
	my ($debug)=@_;
	my $ln=__LINE__;
	my $sn=(caller(0))[3]; # get subroutine name

	my $c=<<A;
	<!DOCTYPE html>
	<html>
	<body>
	<p id="wait"></p>

	<script  language="javascript"  type="text/javascript">
		var x=document.getElementById("wait");
		x.innerHTML="($sn<$ln>) $debug<br><b>$ENV{SERVER_NAME}</b><br>Error case 2 [lon,lat]=[$lon,$lat] not defined<br>Please wait while loading...";
	window.location="$url";
</script>
</body>
</html>
A
	return $c;
} # End sub my_promptB

=head1 sub my_promptA(...)

A prompt is used between each screen. This prompt is used too for debugging too.

=head2 PARAMETER(S)

=over 4

=over 4

$debug: info to help debugging.

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

Returns HTML structure for the new prompt.

=back

=back

=head2 ERRROR RETURNED

=over 4

=over 4

none.

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

- I<Last modification:>  Apr 24 2018

- I<Created on:> Apr 24 2018

=back

=back

=cut

sub my_promptA{ # Begin sub my_promptA
	my ($debug)=@_;
	#my $ln=__LINE__;
	#my $sn=(caller(0))[3]; # get subroutine name

	chomp($url); chomp($debug); #chomp($info);
	my $c=<<A;
<!DOCTYPE html>
<html>
<body>
<p id="wait"></p>

<script  language="javascript" type="text/javascript">
	var x=document.getElementById("wait");
	/* x.innerHTML="Please wait while loading..."; */
	x.innerHTML="<u>$debug</u><br><p>Error case 1<br>[lon,lat]=[$lon,$lat] we check if not defined<br>Please wait while loading...</p>";
	window.location="$url";
</script>
</body>
</html>
A
	return $c;
} # End sub my_promptA

sub print_info { # Begin sub print_info($title,$mess)
	my ($title,$mess)=@_;
	print <<A;
<script type="text/javascript">
	print_info($title,$mess);
</script>
A
} # End sub print_info($title,$mess)

sub add_print_info { # Begin sub add_print_info($mess)
	my ($mess) = @_;
	print "<script>document.getElementById('myDemo').innerHTML+='$mess';</script>\n";
} # End sub add_print_info($mess)

=head1 AUTHOR

Current maintainer: M. Shark Bay <shark dot b at laposte dot net>

=cut
