#!/usr/bin/perl -T

$|=0;

use warnings;
use strict;

BEGIN {
	push @INC, '/Users/sdo/Sites/cgi-bin/';
	push @INC, '/home1/derased/public_html/cgi-bin/';
}

use LWP::Simple;
use XML::Simple;
use Data::Dumper;

use io::MyNav;
use io::MySec;
use io::MyUtilities;

use CGI;

=head1 NAME

g3ogle.cgi

$VERSION=0.2.1.3

=head1 ABSTRACT

This file creates drawings on google map.

=head2 LIST OF FUNCTIONS

=over 4

=over 4

getsLoLa
getsPath
loadFile
mapGoogle
is_array
is_hash

=back

=back

=head2 HISTORY OF MODIFICATIONS

=over 4

- I<Last modification:v0.2.1.3> Feb 10 2014: mark(s) is/are missing on the map.
getsLoLa(...)


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

- I<Last modification: v1.4.15.15> Sep 24 2010: function getVers() added to package::MyUtilities

- I<Last modification: v1.4.15.1> Jun 15 2010: see package::MySec::myGetsUrl()

- I<Last modification: v1.4.14.5> Mar 04 2010: see albun.cgi main_menu;menu modiffied log book admin menu;package::MyUtilities::setUrlFile()

- I<Last modification: v1.4.14.1> Dec 5 2009: help_menu_with_css, general_css_def

- I<Last modification: v1.4.14.0RC> Oct 29 2009: see  ipAddressGranted.

- I<Last modification: v1.4.13.9> Oct 24 2009: mp4 or dat or flv file format added.

- I<Last modification: v1.4.13.1> Oct 18 2009: SHOW_PICTURES_ADMIN added.

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

my $doc=new CGI;

my $gmv=$doc->param("gmv"); # Gets google map version

print "Content-Type: text/html\n\n";

my $ipAddr=io::MyNav::gets_ip_address;
my $fn=$0; # file name
$fn=~m/([0-9a-zA-Z\-\.]*)$/;
$fn=$1;

my $xml = new XML::Simple;
my ($L,$l)=(48.866699,2.333300); # By default these are the coodinates

if($ipAddr=~m/^127./||$ipAddr=~m/localhost/||!length($ipAddr)){ # begin if($ipAddr=~m/^127./||$ipAddr=~m/localhost/||!length($ipAddr))
	#print "------>$ipAddr<br>";
} # end if($ipAddr=~m/^127./||$ipAddr=~m/localhost/||!length($ipAddr))
else{ # begin else
	($L,$l)=getsGPSCoordinates();
} # end else

my $wfc=get("http://api.wunderground.com/auto/wui/geo/WXCurrentObXML/index.xml?query=$L,$l");

open(W,">wfc_data.$$.xml") or die("error $!");
print W $wfc;
close(W) or die("error $!");
#print "ooooooooo)$wfc(oooooooooooooooo<br>";
my $data = $xml->XMLin("wfc_data.$$.xml");
#print "uuuuu>pasted $data<<<<<<<<<<<<<br>";

my $id=();
my @rr=();
my ($dev, $ino, $mode, $nlink, $uid, $gid, $rdev, $size, $atime, $mtime, $ctime, $blksize, $blocks) = stat "$fn";
if(-f "debug"){ # Begin if(-f "debug")
	$id="AIzaSyDoz8j1983lLAncsYMjXLeemy5ks3DkfM8";
} # end if(-f "debug")
else{ # begin else
	$id=io::MyUtilities::loadFile("private/id.googlemap.v3");	
} # end else

my $mymp=() ;

#print "Content-type: text/html\n\n";

#-------------------------------------------------------------------------

#print "<br>XXXXXXXXXXXXXXXXX<br>";
my %l=&getsLoLa("album","hist"); # Load DB 
#print "<br>------------<br>";
#exit(0);
my $path=&getsPath("album/history","Canada"); # Load file
my $path=&getsPath("album/history","New Zealand"); # Load file

chomp($id) ;
&mapGoogle("$id","$gmv");

=head1 sub getsLoLa(...)

=head2 SYNOPSIS

=over 4

=over 4

Loads file where are stored Longitude and Latitude.

=back

=back

=head2 PARAMETER(S)

=over 4

=over 4

$dp: directory parent. This is the base directory where are stored Data Base

$ds: directory son. This is where the directory from $dp are stored Data Base

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

Returns a list.

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

- Last modification: Feb 10 2014: mark(s) is/are missing on the map.

- Last modification: Jan 14 2014

- Created on: Feb 13 2011

=back

=back

=cut

sub getsLoLa{# begin getsLoLa
	my ($dp,$ds)=@_; # (dp: directory parent,ds: directory son) where are stored DB

	my %llL=();# list of Longitude and latitude taken from a given file
	
	chdir("$dp");chdir("$ds");# we go in $dp/$ds. Now it's current diectory
	my $r=();# store content of each file
	opendir(ARD,".") || die(". $!");# open current directory
	my @dr= grep { $_ ne '.' and $_ ne '..' and $_ !~ m/pl$/i and $_ !~ m/cgi$/i} readdir(ARD);# parse current directory
	closedir(ARD) || die(". $!");# close directory

	# @dr contains all files and directories from current dir except . and ..
	foreach my $ee (@dr){ # begin foreach (@dr) ; parse each file name from current directory
		if(length("$ee")>0){# begin if(length("$ee")>0)
			open(RO,"$ee") || die("$ee $!");$r.=<RO>;chomp($r);close(RO)||die("$ee $!");# store data from files in $r variable
			#if($r=~m/perl/){
				#print "#############)$ee<br>";
			#}
		}# end if(length("$ee")>0)
	} # end foreach (@dr)
	chdir("..");chdir(".."); # come back to original dir configuration
	my @a=split(/\,/,$r);# split in an array
	for my $p (@a){# begin for my $p (@a)
		chomp($p);#remove cariage return if one found
		my @q=split(/\#/,$p); # split each lines as a column
		if(scalar(@q)>10){# begin if(scalar(@q)>10)
			my $dtes=$q[1]; # Gets login date
			my $l=$q[11]; # Gets Latitude
			my $L=$q[12]; # Gets Longitude
			$l=~s/LATITUDE\://; # Remove comment for the column name
			$L=~s/LONGITUDE\://; # Remove comment for the column name
			if(length("$l")){# begin if(length($l))
				if(length("$L")){# begin if(length($L))
		#print "\n<br>ooo(". scalar(@q) . ")oooo) {$dtes arobase $l,$L}(ooooooooooooooo>";
		#if(scalar(@q)>14){# begin if(scalar(@q)>14)
			#print "---->$p";
		#}# end if(scalar(@q)>14)
		#print "<br>";
					#print "\n<br>$dtes @ $l,$L stop here<br>";
					$llL{"$dtes @ $l,$L"}.="<br>$dtes <!-- $q[7]-->";
					#print "\n<br>$dtes @ $l,$L stop here<br>";
					$dtes=~s/(Mon|Tues|Wed|Thu|Fri|Sat|Sun)//g;
					if($dtes=~m/(Jan)/){$dtes=~s/$1/01/;}
					if($dtes=~m/(Feb)/){$dtes=~s/$1/02/;}
					if($dtes=~m/(Mar)/){$dtes=~s/$1/03/;}
					if($dtes=~m/(Apr)/){$dtes=~s/$1/04/;}
					if($dtes=~m/(May)/){$dtes=~s/$1/05/;}
					if($dtes=~m/(Jun)/){$dtes=~s/$1/06/;}
					if($dtes=~m/(Jul)/){$dtes=~s/$1/07/;}
					if($dtes=~m/(Aug)/){$dtes=~s/$1/08/;}
					if($dtes=~m/(Sep)/){$dtes=~s/$1/09/;}
					if($dtes=~m/(Oct)/){$dtes=~s/$1/10/;}
					if($dtes=~m/(Nov)/){$dtes=~s/$1/11/;}
					if($dtes=~m/(Dec)/){$dtes=~s/$1/12/;}
					@rr=(@rr,"$dtes\@$l,$L");
				}# end if(length($L))
			}# end if(length($l))
		} # end if(scalar(@q))
		#else { # begin else
			#print "-------> " . scalar(@q) . " <<<<<<------$p<br>\n";
		#} # end else
	}# end for my $p (@a)
	return %llL; # Returns hash
} # end getsLoLa


=head1 sub getsPath(...)

=head2 SYNOPSIS

=over 4

=over 4

Loads file where are stored longitude and latitude.

=back

=back

=head2 PARAMETER(S)

=over 4

=over 4

$file: File name to analyze

$field: must be (for current version) the country name

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

Returns a $path (to complete).

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

- Last modification: Jan 14 2014

- Created on: Feb 13 2011

=back

=back

=cut

sub getsPath{# begin getsPath
	my ($file,$field)=@_; # File name to analyze
	my $llL=();# list of Longitude and latitude taken from a given file
	$llL="//Begin polyline code \n";
	$llL.="var polyline = new GPolyline([\n";

	#open(R,"$file"); # Load given file
	#my $r=<R>;
	#close(R);
	chdir("album");chdir("hist");# we go in album/hist
	my $r=();# store content of each file
	opendir(ARD,".") || die(". $!");# open current directory
	my @dr= grep { $_ ne '.' and $_ ne '..' } readdir(ARD);# parse current directory
	closedir(ARD) || die(". $!");# close directory
	foreach my $ee (@dr){ # begin foreach (@dr) ; parse each file name from current directory
		if(length("$ee")>0){# begin if(length("$ee")>0)
			open(R,"$ee") || die("$ee $!");$r.=<R>;chomp($r);close(R)||die("$ee $!");# store data from files in $r variable
		}# end if(length("$ee")>0)
	} # end foreach (@dr)
	chdir("..");chdir(".."); # come back to original dir configuration
	
	my @a=split(/\,/,$r);
	my $l=();my $L=();my $ll=();my $LL=();
	my @zz=();
	for my $p (@a){ # begin for my $p (@a)
		chomp($p);
		my @q=split(/\#/,$p); # split each lines as a column
		# we check country name below
		if($q[7]=~m/$field/i){# begin if($q[7]=~m/$field/i)
			my $dte=$q[1]; # Gets login date
			my $l=$q[11]; # Gets Latitude
			my $L=$q[12]; # Gets Longitude
			$l=~s/LATITUDE://; # Remove coment
			$L=~s/LONGITUDE://; # Remove coment
			#print ">>>>>>>>>>>>>>>$l $L\n";
			# we remove same coordnitates that next to each ohers (line before)
			if(!("$ll" eq "$l" && "$LL" eq "$L")){ # begin if(!("$ll" eq "$l" && "$LL" eq "$L"))
				my $jj=$dte;
				$dte=~s/(Mon|Tues|Wed|Thu|Fri|Sat|Sun)//g;
				if($dte=~m/(Jan)/){$dte=~s/$1/01/;}
				if($dte=~m/(Feb)/){$dte=~s/$1/02/;}
				if($dte=~m/(Mar)/){$dte=~s/$1/03/;}
				if($dte=~m/(Apr)/){$dte=~s/$1/04/;}
				if($dte=~m/(May)/){$dte=~s/$1/05/;}
				if($dte=~m/(Jun)/){$dte=~s/$1/06/;}
				if($dte=~m/(Jul)/){$dte=~s/$1/07/;}
				if($dte=~m/(Aug)/){$dte=~s/$1/08/;}
				if($dte=~m/(Sep)/){$dte=~s/$1/09/;}
				if($dte=~m/(Oct)/){$dte=~s/$1/10/;}
				if($dte=~m/(Nov)/){$dte=~s/$1/11/;}
				if($dte=~m/(Dec)/){$dte=~s/$1/12/;}
				#print "$jj $dte<br>";
				#print "blobloblobloblo>$dte@ new GLatLng($l,$L),\n";
				@zz=(@zz,"$dte@ new GLatLng($l,$L),\n");
				#$llL.="new GLatLng($l,$L),\n";
			}# end if(!("$ll" eq "$l" && "$LL" eq "$L"))
			$ll=$l;$LL=$L;
#print "	
		}# end if($q[7]=~m/$field/i)
	} # end for my $p (@a)
	my @qq=sort(@zz);
	foreach(@qq){ # begin foreach(@qq)
		my($ed,$ea)=split(/\@/,$_);
		chomp($_);
		$llL.="/* $_ */$ea";
	} # end foreach(@qq)
	$llL=~s/,\n$//;
	$llL.="  ], \"#ff0044\", 5); \nmap.addOverlay(polyline);\n //End polyline code";
	return $llL; # Returns list
}# end getsPath


=head1 sub loadFile(...)

=head2 SYNOPSIS

=over 4

=over 4

Load a file

=back

=back

=head2 PARAMETER(S)

=over 4

=over 4

$fn: File name

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

Returns the contents of the file name loaded.

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

- Last modification: Feb 06 2014
added documentation.

- Last modification: Jan 14 2014

- Created on: Feb 13 2011

=back

=back

=cut

sub loadFile{# begin loadFile
	my ($fn)=@_; # File name

	open(R,"$fn");
	my @r=<R>;# fle content
	close(R);
	return join("",@r);
}# end loadFile


=head1 sub mapGoogle(...)

=head2 SYNOPSIS

=over 4

=over 4

Draw basic map acording to db recorded

=back

=back

=head2 PARAMETER(S)

=over 4

=over 4

$idgoog: Google id for one page.

$gmv: Google map version.

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

Returns nothing (Checks if environmental variable are modified).

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

- Last modification: Feb 06 2014
googheader modified. by default sensor is set to false can't be modified for 
the moment.

- Created on: Feb 13 2011

=back

=back

=cut

sub mapGoogle{# begin mapGoogle
	my ($idgoog,$gmv)=@_ ; # Google id for one page; google map version
	chomp($idgoog); # Remove CR at end of string
	my $cart=();
	my @aa=sort(@rr);
	my $vbn=@aa;
	my $cvbn=0;# counter

	# we add markers on the map
	for my $i (@aa){ # Begin for my $i (@aa)
		#print "xxxxxxxxx>$i<<<<<<\n<br>\n";
		$cvbn++;# increase of 1 each time pass here
		if(length($i)>0){ # Begin if(length($i)>0)
			my ($v,$u)=split(/\@/,$i); # split date and geoloc coord
			#print "oooo)$i oooooo $v|$u<br>\n";
			# we build the map

			# -------------------------------------
			$cart.="/* A---$i $cvbn / $vbn  ------------------------------------------------ */\n";
			$cart.="var point = new google.maps.LatLng($u);\n";
			$cart.="var marker = createMarker(point,'text');\n";
			$cart.="marker.setMap(map);\n";
			$cart.="/* B---$i $cvbn / $vbn  ------------------------------------------------ */\n\n";
			# -------------------------------------
		} # End if(length($i)>0)
	} # End for my $i (@aa)
	$cart.="/* C--------------------------------------------------- */\n\n";
	print <<R;
<!DOCTYPE html">
<html>
	<head>
		<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
		<title>Google Maps</title>
R
	#print "inside:\n<br>--->$idgoog\n<br>----->$gmv";	
	print <<R;
		<style type="text/css">
			<!--
				html { height: 100% }
				body { height: 100%; margin: 0; padding: 0 }
				#map { height: 100% }

				a.mailaddr { color: #008000;text-decoration: none; }
				a.mailaddr:visited { color: #008000;text-decoration: none; }
			-->
		</style>

		<script language="JavaScript" 
			  src="http://www.geoplugin.net/javascript.gp" type="text/javascript">
		</script>

R
	print io::MyUtilities::googHead("$idgoog","$gmv");	
	print <<R;

		<script type="text/javascript">
			//<![CDATA[
			var map;
			var marker;
			var la=geoplugin_latitude();
			var lo=geoplugin_longitude();
			var position= new google.maps.LatLng(la,lo);

			function initialize(){ // Begin function initialize()
				var mapOptions = {
					center: position,
					zoom: 8
				};
				map=new google.maps.Map(document.getElementById("map"),mapOptions);

				marker=createMarker(position,"text");
				marker.setMap(map);
				$cart;
			} // End function initialize()


			// To add the marker to the map, call setMap();
			function createMarker(point,text) { // Begin function createMarker(point,html)
				var lmarker = new google.maps.Marker({
						position: point,
						map: map,
						title: text
					});
					return lmarker;
			} // End function createMarker(point,html)

			google.maps.event.addDomListener(window, 'load', initialize);



				/*
					map.addControl(new GLargeMapControl());
					map.addControl(new GMapTypeControl());
				*/

				// Display the map, with some controls and set the initial location 
				/*
				var point = new new google.maps.LatLng(la,lo);
				var marker = createMarker(point,'lo la from geoplugin');
				map.addOverlay(marker);
				*/
				// -------------------------------------------------------------

				// -------------------------------------------------------------
				// -------------------------------------------------------------

				/*
					display_location:$data->{display_location}->{longitude}<br>
					display_location:$data->{display_location}->{latitude}<br>
					observation_location:$data->{observation_location}->{longitude}<br>
					observation_location:$data->{observation_location}->{latitude}<br>
				*/

				// -------------------------------------------------------------
				/*
				var cIcon = new GIcon();
				cIcon.image = "http://nhw.pl/images/cross.png";
				cIcon.iconSize = new GSize(16,16);
				cIcon.iconAnchor = new GPoint(8,9);
				var point = new GLatLng($data->{observation_location}->{latitude},$data->{observation_location}->{longitude});
				var marker = createMarker(point,'lo la from api.wunderground.com');
				map.addOverlay(marker);
				*/
				// -------------------------------------------------------------
	$path;
			//]]>
		</script>
	</head>
<body>
	<div id="map"/>
	$fn proto: 0.3.$mtime <a href="mailto:shark.baits\@laposte.net" class="mailaddr">shark bait</a>
</body>

</html>
R
} # end mapGoogle


=head1 sub is_array(...)

=head2 SYNOPSIS

=over 4

=over 4

1 if equal.

=back

=back

=head2 PARAMETER(S)

=over 4

=over 4

$re: variable to check its type.

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

1 if it is equal.

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

- Last modification: Feb 06 2014

- Created on: Feb 13 2011

=back

=back

=cut

sub is_array{ # begin sub is_array
	my ($re)=@_; # $re: variable to check its type.
	return ref($re) eq 'ARRAY';
} # end sub is_array


=head1 sub is_hash(...)

=head2 SYNOPSIS

=over 4

=over 4

1 if equal.

=back

=back

=head2 PARAMETER(S)

=over 4

=over 4

$re: variable to check its type.

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

1 if it is equal.

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

- Last modification: Feb 06 2014

- Created on: Feb 13 2011

=back

=back

=cut

sub is_hash{ # begin sub is_hash
	my ($re)=@_; #$re: variable to check its type.
	return ref($re) eq 'HASH';
} # end sub is_hash
