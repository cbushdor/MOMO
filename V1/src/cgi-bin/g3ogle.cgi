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
use Net::Ping;
use Cwd;

use io::MyNav;
use io::MySec;
use io::MyUtilities;

use CGI;


my $ipAddr=io::MyNav::gets_ip_address;

=head1 NAME

g3ogle.cgi

$VERSION=0.2.1.20

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

- I<Last modification:v0.2.1.20> Feb 20 2014: test with ping added for local debug

- I<Last modification:v0.2.1.4> Feb 11 2014: see mapGoogle

- I<Last modification:v0.2.1.3> Feb 10 2014: see getsLoLa(...), getsPath(...)

=back

=cut


my $doc=new CGI;

my $lon=$doc->param("maop_lon");
my $lat=$doc->param("maop_lat");

if(! defined($lat)||length($lat)==0||$lat!~m/^[0-9]{1,}\.[0-9]{1,}$/){ # begin if(!defined($lat)||length($lat)==0||$lat!~m/^[0-9]{1,}\.[0-9]{1,}$/)
	my $url=();
	print "Content-Type: text/html\n\n";
	#print "case 2<br>";exit(1);
	if(! defined($ipAddr)||$ipAddr=~m/^127\.0\.0\.1/i||$ipAddr=~m!localhost!){
		$url="http://localhost/~sdo/cgi-bin/maop.cgi?maop_prog=g3ogle.cgi";
	}else{
		$url="http://derased.heliohost.org/cgi-bin/maop.cgi?maop_prog=g3ogle.cgi";
	}
	my $c=<<A;
<!DOCTYPE html>
<html>
<body>
<p id="wait"></p>

<script>
	var x=document.getElementById("wait");
	x.innerHTML="Please wait while loading...";
	window.location="$url";
</script>
</body>
</html>
A
	print $c;
	exit(0);
} # end if(!defined($lat)||length($lat)==0||$lat!~m/^[0-9]{1,}\.[0-9]{1,}$/)

if(! defined($lon)||length($lon)==0||$lon!~m/^[0-9]{1,}\.[0-9]{1,}$/){ # begin if(!defined($lon)||length($lon)==0||$lon!~m/^[0-9]{1,}\.[0-9]{1,}$/)
	my $url=();
	print "Content-Type: text/html\n\n";
	#print "case 1<br>";exit(1);
	if(! defined($ipAddr)||$ipAddr=~m/^127\.0\.0\.1/i||$ipAddr=~m!localhost!){
		$url="http://localhost/~sdo/cgi-bin/maop.cgi";
	}else{
		$url="http://derased.heliohost.org/cgi-bin/maop.cgi";
	}
	my $c=<<A;
<!DOCTYPE html>
<html>
<body>
<p id="wait"></p>

<script>
	var x=document.getElementById("wait");
	x.innerHTML="Please wait while loading...";
	window.location="$url";
</script>
</body>
</html>
A
	print $c;
	exit(0);
} # end if(!defined($lon)||length($lon)==0||$lon!~m/^[0-9]{1,}\.[0-9]{1,}$/)


my ($gmv,$prt)=split(/\-/,$doc->param("maop_gmv")); # Gets google map version
my ($googid)=$doc->param("maop_googid"); # Gets google map version
chomp($prt);chomp($googid);

print "Content-type: text/html\n\n";
print "i$gmv,$prt, check  test prt length if it is ok. implemented but not tested yet<br>";

if(length($googid)==0 || ! defined($googid) ){ # begin if(length($prt)==0 || ! defined($prt) )
	$prt=1;
} # end if(length($prt)==0 || ! defined($prt) )

if ($ipAddr=~m/127.0.0.1/){
	my $pong = Net::Ping->new( $> ? "tcp" : "icmp" );
	if ($pong->ping("www.heliohost.org")) {
	} else {
		print "No connection!\n";
		exit(-1);
	}
}

my $fn=$0; # file name
$fn=~m/([0-9a-zA-Z\-\.]*)$/;
$fn=$1;

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
my $path=(); # olds data to print on the map
my %l=();

#-------------------------------------------------------------------------

chomp($id) ;

# Checks options for map rinting with Markers
#if(defined($prt)){ # Begin if(definied($prt))
	# Prints where you are
	if($prt==0){ # Begin if($prt==0)
		#$path.=&getsPath("album/hist","New Zealand"); # Load file
		#$path.=&getsPath("album/hist","Canada"); # Load file
		#$path.=&getsPath("album/hist","FOURTHTEST"); # Load file
		$path.=&getsPath("album/hist","$googid"); # Load file
		&mapGoogle("$id","$gmv");
	} # End if($prt==0)
	# Prints all markers
	if($prt==1){ # Begin if($prt==1)
		%l=&getsLoLa("album","hist"); # Load DB 
		&mapGoogle("$id","$gmv");
	} # End if($prt==1)
	# marks trips
	if($prt==2){ # Begin if($prt==2)
		$path.=&getsPath("album/hist","Canada"); # Load file
		$path.=&getsPath("album/hist","New Zealand"); # Load file
		$path.=&getsPath("album/hist","THIRDTEST"); # Load file
		&mapGoogle("$id","$gmv");
	} # End if($prt==2)
#} # End if(definied($prt))
#else {
	#&mapGoogle("$id","$gmv");
#}

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

sub getsLoLa{ # begin getsLoLa
	my ($dp,$ds)=@_; # (dp: directory parent,ds: directory son) where are stored DB

	my %llL=();# list of Longitude and latitude taken from a given file
	
	chdir("$dp");chdir("$ds");# we go in $dp/$ds. Now it's current diectory
	my $r=();# store content of each file
	opendir(ARD,".") || die(". $!");# open current directory
	my @dr= grep { $_ ne '.' and $_ ne '..' and $_ !~ m/pl$/i and $_ !~ m/cgi$/i} readdir(ARD);# parse current directory
	closedir(ARD) || die(". $!");# close directory

	# @dr contains all files and directories from current dir except . and ..
	foreach my $ee (@dr){ # begin foreach (@dr) ; parse each file name from current directory
		#print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@)$ee<br>";
		if(length("$ee")>0){ # begin if(length("$ee")>0)
			open(RO,"$ee") || die("$ee $!");$r.=<RO>;chomp($r);close(RO)||die("$ee $!");# store data from files in $r variable
			#if($r=~m/perl/){
				##print "#############)$ee<br>";
			#}
		} # end if(length("$ee")>0)
	} # end foreach (@dr)
	chdir("..");chdir(".."); # come back to original dir configuration
	my @a=split(/\,/,$r);# split in an array
	for my $p (@a){ # begin for my $p (@a)
		chomp($p);#remove cariage return if one found
		my @q=split(/\#/,$p); # split each lines as a column
		if(scalar(@q)>10){ # begin if(scalar(@q)>10)
			my $dtes=$q[1]; # Gets login date
			my $l=$q[11]; # Gets Latitude
			my $L=$q[12]; # Gets Longitude
			$l=~s/LATITUDE\://; # Remove comment for the column name
			$L=~s/LONGITUDE\://; # Remove comment for the column name
			if(length("$l")){ # begin if(length($l))
				if(length("$L")){ # begin if(length($L))
		#print "\n<br>ooo(". scalar(@q) . ")oooo) {$dtes arobase $l,$L}(ooooooooooooooo>";
		#if(scalar(@q)>14){ # begin if(scalar(@q)>14)
			#print "---->$p";
		#} # end if(scalar(@q)>14)
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
				} # end if(length($L))
			} # end if(length($l))
		} # end if(scalar(@q))
		#else { # begin else
			#print "-------> " . scalar(@q) . " <<<<<<------$p<br>\n";
		#} # end else
	} # end for my $p (@a)
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

sub getsPath{ # begin getsPath
	my ($file,$field)=@_; # File name to analyze
	my $llL=();# list of Longitude and latitude taken from a given file

	#$llL="\t\t\t\t// Begin polyline code \n";
	#$llL.="\t\t\t\tvar polyline = [\n";

	chomp($file);
	foreach my $ld (split(/\//,$file)){ # begin foreach (split(/\//,$file))
		chdir("$ld");
		#print "directory: $ld  ---->".getcwd()."<br>\n";
	} # end foreach (split(/\//,$file))
#	chdir("hist");# we go in album/hist
	my $r=();# store content of each file
	opendir(ARD,".") || die(". $!");# open current directory
	my @dr= grep { $_ ne '.' and $_ ne '..' and $_ !~ m/pl$/i and $_ !~ m/cgi$/i and $_=~m/^maop\-/} readdir(ARD);# parse current directory
	closedir(ARD) || die(". $!");# close directory
	foreach my $ee (@dr){ # begin foreach (@dr) ; parse each file name from cuon directory
		if(length("$ee")>0){ # begin if(length("$ee")>0)
			open(R,"$ee") || die("$ee $!");$r.=<R>;chomp($r);close(R)||die("$ee $!");# store data from files in $r variable
		} # end if(length("$ee")>0)
	} # end foreach (@dr)
	chdir("..");chdir(".."); # come back to original dir configuration
	
	my @a=split(/\,/,$r);
	my $l=();my $L=();my $ll=();my $LL=();
	my @zz=(); # path stored
	my $prev=();
	my $newArrows=();
	my @infoWC=();
	for my $p (@a){ # begin for my $p (@a)
		chomp($p);
		my @q=split(/\#/,$p); # split each lines as a column
		# we check country name below
		if($q[5]=~m/$field/i){ # begin if($q[7]=~m/$field/i)
			#print "oooooooooooooooo)$q[14] ------------ ";
			my $dte=$q[7]; # Gets login date
			my $l=$q[4]; # Gets Latitude
			my $L=$q[3]; # Gets Longitude
			@infoWC=(@infoWC,&infoCenter("$q[6]"));# Info Weather Center
			# we remove same coordnitates that next to each ohers (line before)
			if(!("$ll" eq "$l" && "$LL" eq "$L")){ # begin if(!("$ll" eq "$l" && "$LL" eq "$L"))
				# checks here if we can mix array with weather forecast
				# trig with vi a.s /new google.maps.LatLng
				#print "------------------------------------------------------->$dte<br>";
				@zz=(@zz,"$dte@ new google.maps.LatLng($l,$L),\n");
				#$llL.="new google.maps.LatLng($l,$L),\n";
			} # end if(!("$ll" eq "$l" && "$LL" eq "$L"))
			$ll=$l;$LL=$L;
#print "	
		} # end if($q[7]=~m/$field/i)
	} # end for my $p (@a)
	my @qq=sort(@zz);
	my $markersTrip=();

	#print "size of the array ". scalar(@qq) . "<<<<<<<<<<<<<<<<br>";
	my $max=scalar(@qq);
	my $cur=1;
	foreach(@qq){ # begin foreach(@qq)
		my($ed,$ea)=split(/\@/,$_);
		chomp($_);
		chomp($ea);
		$ea=~s/,$//;
		if($cur<$max){ # Begin if($cur<$max)
			if ($cur>1){
				$markersTrip.=<<TRIP_MARKERS;

			// --------------  $ea   ------------------
				var contentString = "$infoWC[$cur]";

				var infowindow = new google.maps.InfoWindow({
						content: contentString
					});

				var marker = new google.maps.Marker({
						position: $ea,
						map: map,
						icon: 'https://chart.googleapis.com/chart?chst=d_map_pin_icon&chld=flag|00FF00'
					});

				// --------------------------------
    
				marker.setMap(map);
				google.maps.event.addListener( marker, 'click', function( data){
								// affichage position du marker
								infowindow.setContent( "$infoWC[$cur]" );
								infowindow.open( this.getMap(), this);
							}); 
				// --------------------------------
			// --------------------------------
TRIP_MARKERS
			}
			else {
				$markersTrip.=<<TRIP_MARKERS;

			// --------------  $ea   ------------------
				var contentString = "$infoWC[$cur]";

				var infowindow = new google.maps.InfoWindow({
						content: contentString
					});

				var marker = new google.maps.Marker({
						position: $ea,
						map: map,
						icon: 'https://chart.googleapis.com/chart?chst=d_map_pin_icon&chld=flag|003300'
					});

				// --------------------------------
    
				marker.setMap(map);
				google.maps.event.addListener( marker, 'click', function( data){
				    // affichage position du marker
				    infowindow.setContent( "$cur==1 ---->$ea" );
				    infowindow.open( this.getMap(), this);
				  }); 
				// --------------------------------
			// --------------------------------
TRIP_MARKERS
			}
		} # end if($cur<$max)
		else{
			$markersTrip.=<<TRIP_MARKERS;

			// --------------------------------
				var marker = new google.maps.Marker({
						position: $ea,
						map: map,
						icon: 'https://chart.googleapis.com/chart?chst=d_map_pin_icon&chld=flag|FF0000'
					});
				marker.setMap(map);
			// --------------------------------
TRIP_MARKERS
		}
		$cur++;
		if(length($prev)!=0){ # Begin if(length($prev)!=0)
			$newArrows.=<<ARROWS;
			var lineSymbol = {
				path: google.maps.SymbolPath.FORWARD_CLOSED_ARROW
			};

			var lineCoordinates = [
				$prev,
				$ea
			];

			var line = new google.maps.Polyline({
				path: lineCoordinates,
				icons: [{
					icon: lineSymbol,
					offset: '50%'
				}],
				map: map
			});
ARROWS
		} # End if(length($prev)!=0)
		$prev="$ea";
	} # end foreach(@qq)
	$llL.=<<POLY;
				// Begin polylines codes

				$markersTrip

				// End polylines codes

					$newArrows
POLY
	return $llL; # Returns list
} # end getsPath


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

sub loadFile{ # begin loadFile
	my ($fn)=@_; # File name

	open(R,"$fn");
	my @r=<R>;# fle content
	close(R);
	return join("",@r);
} # end loadFile


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

sub mapGoogle{ # begin mapGoogle
	my ($idgoog,$gmv)=@_ ; # Google id for one page; google map version
	chomp($idgoog); # Remove CR at end of string
	my $cart=();
	my @aa=sort(@rr);
	my $vbn=@aa;
	my $cvbn=0;# counter

	$cart="\t\t\t\tvar points=[";
	# we add markers on the map
	my $gls=scalar(@aa);# geolocation size
	for my $i (@aa){ # Begin for my $i (@aa)
		$cvbn++;# increase of 1 each time pass here
		if(length($i)>0){ # Begin if(length($i)>0)
			my ($v,$u)=split(/\@/,$i); # split date and geoloc coord
			#// check if we can't make an array of different values at once with weather forcast
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
				#content {
					width: 650px;
				}
				img.infoWin{
					margin-top:1px;
					margin-bottom:1px;
					float: left;
					vertical-align: top;
				}
				ul {
					margin-top:1px;
					margin-bottom:1px;
					float: left;
					list-style: none;
				}
				html { height: 100% }
				body { height: 100%; margin: 0; padding: 0 }
				#map { height: 100% }

				#legend {
					font-family: Arial, sans-serif;
					background: #fff;
					padding: 10px;
					margin: 10px;
					border: 3px solid #000;
				}
				#legend h3 {
					margin-top: 0;
				}
				#legend img {
					vertical-align: middle;
				}
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
			var la=$lat; //geoplugin_latitude();
			var lo=$lon; //geoplugin_longitude();
			var position= new google.maps.LatLng(la,lo);

			var icons = {
				EtapeDebut: {
					name: "Début d'étape/Stage starts",
					icon: 'https://chart.googleapis.com/chart?chst=d_map_pin_icon&chld=flag|003300'
				},
				EtapeTerminée: {
					name: 'Etape terminée/Stage over',
					icon: 'https://chart.googleapis.com/chart?chst=d_map_pin_icon&chld=flag|00FF00'
				},
				EtapeEnCour: {
					name: 'Etape en cour/Start',
					icon: 'https://chart.googleapis.com/chart?chst=d_map_pin_icon&chld=flag|FF0000'
				},
				wyrrn: {
					name: 'You are here',
					icon: "https://chart.googleapis.com/chart?chst=d_map_xpin_letter&chld=pin|W|CCCC00"
				}
			};

			function initialize(){ // Begin function initialize()
				var mapOptions = {
					center: position,
					zoom: 15,
					zoomControl: true
				};

				var legend = document.getElementById('legend');
				for (var key in icons) {
					var type = icons[key];
					var name = type.name;
					var icon = type.icon;
					var div = document.createElement('div');
					div.innerHTML = '<img src="' + icon + '"> ' + name;
					legend.appendChild(div);
				}

				map=new google.maps.Map(document.getElementById("map"),mapOptions);
				map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(legend);

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
						icon: "https://chart.googleapis.com/chart?chst=d_map_xpin_letter&chld=pin|W|CCCC00",
						title: text
					});
					return lmarker;
			} // End function createMarker(point,html)

			google.maps.event.addDomListener(window, 'load', initialize);
			document.getElementById("legend")="https://chart.googleapis.com/chart?chst=d_map_xpin_letter&chld=pin|H|FFFF42";

			//]]>
		</script>
	</head>
<body>
	<div id="map"/>
	<div id="legend"><h3>Legend</h3></div>
	<!--
	$fn proto: 0.3.$mtime <a href="mailto:shark.baits\@laposte.net" class="mailaddr">shark bait</a>
	-->
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


sub infoCenter{
	my ($nwc)=@_; # Name weather center
	my $xml = new XML::Simple;
	my $data = $xml->XMLin("$nwc");

	return   
		"<div id='content'><!-- $data->{credit} -->"
		."<p><img class='infoWin' src='$data->{icons}->{icon_set}->{Default}->{icon_url}'>"
		."<ul><li>$data->{local_time}</li>"
		."<li>$data->{display_location}->{city},$data->{display_location}->{state_name}</li>"
		."<li>$data->{temperature_string}</li></ul>"
		."<ul><li><u>Visibilité/Visibility:</u>$data->{visibility_mi}</li>"
		."<li><u>Vent/Wind:</u>$data->{wind_string}</li>"
		."<li><u>Pression/Pressure:</u>$data->{pressure_string}</li>"
		."<li><u>Lat/Lon:</u>$data->{display_location}->{latitude},$data->{display_location}->{longitude}</li></ul></p>"
		."</div>"
	;
}
