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

- I<Last modification:v0.2.1.3> Feb 11 2014: see mapGoogle

- I<Last modification:v0.2.1.3> Feb 10 2014: see getsLoLa(...), getsPath(...)

=back

=cut

my $doc=new CGI;

my ($gmv,$prt)=split(/\-/,$doc->param("gmv")); # Gets google map version

#$prt= (! defined($prt)) ? "0";

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
my $path=(); # olds data to prin on the map
my %l=();

#-------------------------------------------------------------------------

$path.=&getsPath("album/history","Canada"); # Load file
$path.=&getsPath("album/history","New Zealand"); # Load file

# Checks options for map rinting with Markers
if(defined($prt)){ # Begin if(definied($prt))
	# Prints all markers
	if($prt==1){ # Begin if($prt==1)
		%l=&getsLoLa("album","hist"); # Load DB 
	} # End if($prt==1)
} # End if(definied($prt))

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
	grep { $_ ne '.' and $_ ne '..' and $_ !~ m/pl$/i and $_ !~ m/cgi$/i} readdir(ARD);

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

- Last modification: Feb 10 2014
	grep { $_ ne '.' and $_ ne '..' and $_ !~ m/pl$/i and $_ !~ m/cgi$/i} readdir(ARD);

- Last modification: Jan 14 2014

- Created on: Feb 13 2011

=back

=back

=cut

sub getsPath{# begin getsPath
	my ($file,$field)=@_; # File name to analyze
	my $llL=();# list of Longitude and latitude taken from a given file
	$llL="\t\t\t\t//Begin polyline code \n";
	$llL.="\t\t\t\tvar polyline = [\n";

	#open(R,"$file"); # Load given file
	#my $r=<R>;
	#close(R);
	chdir("album");chdir("hist");# we go in album/hist
	my $r=();# store content of each file
	opendir(ARD,".") || die(". $!");# open current directory
	my @dr= grep { $_ ne '.' and $_ ne '..' and $_ !~ m/pl$/i and $_ !~ m/cgi$/i} readdir(ARD);# parse current directory
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
				@zz=(@zz,"$dte@ new google.maps.LatLng($l,$L),\n");
				#$llL.="new google.maps.LatLng($l,$L),\n";
			}# end if(!("$ll" eq "$l" && "$LL" eq "$L"))
			$ll=$l;$LL=$L;
#print "	
		}# end if($q[7]=~m/$field/i)
	} # end for my $p (@a)
	my @qq=sort(@zz);
	foreach(@qq){ # begin foreach(@qq)
		my($ed,$ea)=split(/\@/,$_);
		chomp($_);
		$llL.="\t\t\t\t\t$ea";
	} # end foreach(@qq)
	$llL=~s/,\n$//;
	$llL.="  ];\n"; #", \"#ff0044\", 5); \nmap.addOverlay(polyline);\n //End polyline code";
	$llL.=<<POLY;

				var flightPath = new google.maps.Polyline({
					path: polyline,
					geodesic: true,
					strokeColor: '#FF0000',
					strokeOpacity: 1.0,
					strokeWeight: 2
					});

				flightPath.setMap(map);
				// End polylines codes

POLY
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

- Last modification: Feb 11 2014
Modified the script to make it more readable

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

	$cart="\t\t\t\tvar points=[";
	# we add markers on the map
	my $gls=scalar(@aa);# geoloction size
	for my $i (@aa){ # Begin for my $i (@aa)
		$cvbn++;# increase of 1 each time pass here
		if(length($i)>0){ # Begin if(length($i)>0)
			my ($v,$u)=split(/\@/,$i); # split date and geoloc coord
			$cart.="new google.maps.LatLng($u)";
			# Tests for the comma at the end of the list
			if($gls!=1){ # Begin if($gls!=1)
				$cart.=",";
			} # End if($gls!=1)
			$gls--;
		} # End if(length($i)>0)
	} # End for my $i (@aa)
	$cart.="\n\t\t\t\t\t];\n";
	$cart.="\t\t\t\tfor(var i=0;i<points.length;i++){\n";
	$cart.="\t\t\t\t\tvar marker = createMarker(points[i],'text');\n";
	$cart.="\t\t\t\t\tmarker.setMap(map);\n";
	$cart.="\t\t\t\t}\n";
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
$path;
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
