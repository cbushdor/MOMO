#!/usr/bin/perl

use strict;
use warnings;
use POSIX qw(strftime);
use io::MyNav;

#my $now_string = strftime "%a %b %e %H:%M:%S %Y", localtime;
# or for GMT formatted appropriately for your locale:
my $now_string = strftime "%m %d %H:%M:%S UTC %Y", gmtime;

#print "Content-Type: text/html\n\n";
#print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@>$now_string<<<<<<<<<<<<<<<<<<<<<<<";

#exit(1);
#my $dt3 = DateTime->from_epoch( epoch => time() );# Current date format DateTime

use CGI;

use io::MyNav;

my $doc=new CGI();
my $url=();
my $ip=io::MyNav::gets_ip_address;

my $mparam=();# my parameter passed

#print "Content-type: text/html\n\n";

foreach my $p ($doc->param){ # begin foreach my $p ($doc->param)
	if($p=~m/^maop\_/){ # begin if($p=~m/^maop\_/)
		if($p!~m!maop_lon!&&$p!~m!maop_lat!&&$p!~m!maop_prog!&&$p!~m!maop_log!){ # begin if($p!~m!maop_lon!&&$p!~m!maop_lat!&&$p!~m!maop_prog!&&$p!~m!maop_log!)
			$mparam.="&$p=".$doc->param($p);
		} # end if($p!~m!maop_lon!&&$p!~m!maop_lat!&&$p!~m!maop_prog!&&$p!~m!maop_log!){ # begin if($p!~m!maop_lon!&&$p!~m!maop_lat!&&$p!~m!maop_prog!&&$p!~m!maop_log!)
	} # end if($p=~m/^maop\_/)
} # end foreach my $p ($doc->param)


my $prog=(length($doc->param("maop_prog"))==0) ? "album.cgi" : $doc->param("maop_prog");

if(! defined($ip)||$ip=~m/^127\.0\.0\.1/i||$ip=~m!localhost!){ # begin if(! defined($ip)||$ip=~m/^127\.0\.0\.1/i||$ip=~m!localhost!)
	$url="http://localhost/~sdo/cgi-bin/$prog";
} # end if(! defined($ip)||$ip=~m/^127\.0\.0\.1/i||$ip=~m!localhost!)
else{ # begin  else
	$url="http://derased.heliohost.org/cgi-bin/$prog";
} # end else

my $ipAddr=io::MyNav::gets_ip_address;
my $logfile="album/hist/log-$ipAddr-$$";

if( -f "$logfile"){ # begin if( -f "$logfile")
	unlink("$logfile");
} # end if( -f "$logfile")
open(FD,">$logfile") or die("$logfile error $!");
print FD " ";
close(FD) or die("$logfile error $!");

$logfile=~s/\//\_/g;
#$logfile=~s/\_/\//g;

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
    window.location="$url?maop_lon="+lon+"&maop_lat="+lat+"$mparam&maop_date=$now_string&maop_log=$logfile";
} // end function showPosition(position)
</script>
</body>
</html>
FORM

print "Content-type: text/html\n\n";
print $myform;
