#!/usr/bin/perl

use strict;
use warnings;

use CGI;

use io::MyNav;

my $doc=new CGI();
my $url=();
my $ip=io::MyNav::gets_ip_address;

my $mparam=();# my parameter passed

foreach my $p ($doc->param){
	if($p=~m/^maop\_/){
		if($p!~m!maop_lon!&&$p!~m!maop_lat!&&$p!~m!maop_prog!){
			$mparam.="&$p=".$doc->param($p);
		}
	}
}
my $prog=(length($doc->param("maop_prog"))==0) ? "album.cgi" : $doc->param("maop_prog");

if(! defined($ip)||$ip=~m/^127\.0\.0\.1/i||$ip=~m!localhost!){ # begin if(! defined($ip)||$ip=~m/^127\.0\.0\.1/i||$ip=~m!localhost!)
	$url="http://localhost/~sdo/cgi-bin/$prog";
} # end if(! defined($ip)||$ip=~m/^127\.0\.0\.1/i||$ip=~m!localhost!)
else{ # begin  else
	$url="http://derased.heliohost.org/cgi-bin/$prog";
} # end else

my $myform=<<FORM;
<!DOCTYPE html>
<html>
<body>
<p id="wait"></p>

<script>
var x=document.getElementById("wait");
x.innerHTML="Please wait while loading...$url<br>------->$mparam";
getLocation();

function getLocation() { // begin function getLocation()
    if (navigator.geolocation) { // begin if (navigator.geolocation)
        navigator.geolocation.watchPosition(showPosition,showError);
    } // end if (navigator.geolocation)
    else { // begin else
        x.innerHTML = "Geolocation is not supported by this browser.";
    } // end else
} // end function getLocation()

function showError(error){ // begin function showError(error)
    switch(error.code) { // begin switch(error.code)
        case error.PERMISSION_DENIED:
            x.innerHTML = "User denied the request for Geolocation."
            break;
        case error.POSITION_UNAVAILABLE:
            x.innerHTML = "Location information is unavailable."
            break;
        case error.TIMEOUT:
            x.innerHTML = "The request to get user location timed out."
            break;
        case error.UNKNOWN_ERROR:
            x.innerHTML = "An unknown error occurred."
            break;
    } // end switch(error.code)
} // end function showError(error)

function showPosition(position) { // begin function showPosition(position)
    var lon=position.coords.longitude;
    var lat=position.coords.latitude;
    window.location="$url?maop_lon="+lon+"&maop_lat="+lat+"$mparam";
} // end function showPosition(position)
</script>
</body>
</html>
FORM

print "Content-type: text/html\n\n";
print $myform;
