#!/usr/bin/perl5.30.2  -T

# ------------------------------------------------------
q##//q#
* Created By : sdo
* File Name : maop.cgi
* Creation Date : Wed Aug 19 15:51:08 2015
* @modify date 2020-06-10 02:40:40
* Email Address : sdo@linux.home
* License:
*       Permission is granted to copy, distribute, and/or modify this document under the terms of the Creative Commons Attribution-NonCommercial 3.0
*       Unported License, which is available at http: //creativecommons.org/licenses/by- nc/3.0/.
* Version : 1.0.12.542
* Purpose : 
#;
# ------------------------------------------------------

use CGI;
use strict;
use warnings;
use Sys::Hostname;
use Socket;

my $doc;
BEGIN {
	push @INC,"/Users/sdo/Sites/cgi-bin/"; # We add a new path to @INC
	push @INC,"/home/sdo/public_html/cgi-bin/"; # We add a new path to @INC
	# A bug was solved and that's it was "...but still, the newly generated form has al the values from the previous form...".
	$|=1;
	$doc=$CGI::Q ||= new CGI; # It is using the special internal $CGI::Q object, rather than your 'my $doc' object that's why we do this.
	print "Content-Type: text/html ; charset=UTF-8 \n\n";
}
END {
	$doc->delete_all(); # We clean all variables and parameters when the script is over
}

use POSIX qw(strftime);
use io::MyNav;
use DateTime;
use DateTime::Format::Strptime;
use Cwd;
#use Encode;
use URI;
use URI::Escape;
use io::MyConstantBase;
use io::gut::machine::MyFile;

my $VERSION="1.0.12.542";

my $now_string = time(); # strftime "%m %d %H:%M:%S UTC %Y", gmtime;

my $extra_param=""; my $maop_upld=$doc->param("maop_upld")||"";
if(uri_unescape($maop_upld) eq "ok"){
	if($doc->param("maop_file_name_img")){
		my $timsec=localtime;
		#print "<br><br><br><br><br><br><br><br><br><br>----------------->$timsec<br>";
		$timsec=~s/[\ \/\:]/\_/g;
		my $pim=$doc->param("maop_file_name_img");
		$extra_param="maop_file_name_img=";
		$extra_param .= uri_escape("${timsec}$$" . $pim);
		my $final2 = io::gut::machine::MyFile::my_upload($doc, $pim, &io::MyConstantBase::DIRECTORY_DEPOSIT->(), "${timsec}$$",&io::MyConstantBase::ALLOWED_FILE_FORMAT_TYPE->());
		#print "UUUUUUUUUUUUUUUUUUUUUUU>".$final2."<br>";
		$extra_param .= "\&maop_final=$final2";
	}
}

my $ip=io::MyNav::gets_ip_address;
my $ipAddr=io::MyNav::gets_ip_address;
my $logfile="album/hist/log-$ipAddr-$$";
#my $logfile="album/hist/log-$ipAddr-$$";
my $mparam=();# my parameter passed

print "v$VERSION\n<br>";

my $leng=scalar $doc->param;

my $la=$doc->param("maop_lat");
my $lo=$doc->param("maop_lon");

#print "<br><br><br><br><br><br>";
foreach my $p ($doc->param){ # begin foreach my $p ($doc->param)
	#	print "$0  $p: ". $doc->param($p)." <br>";
	if($p=~m/^maop\_/){ # begin if($p=~m/^maop\_/)
		if($p!~m/^maop_lon$/&&
		   $p!~m/^maop_lat$/&&
		   $p!~m/^maop_prog$/&&
		   $p!~m/^maop_date$/&&
		   $p!~m/^maop_file_name_img$/&&
		   $p!~m/^maop_log$/){ # begin if($p!~m!maop_lon!&&$p!~m!maop_lat!&&$p!~m!maop_prog!&&$p!~m!maop_log!)
			my $pram=$doc->param($p);

			if($mparam!~m/[\?\&]$p\=/){
				if (length($pram)>0) { # Begin if (length($pram)>0)
					$mparam.="\&$p=".uri_escape($pram);
				} # End if (length($pram)>0)
			}
		}  # end if($p!~m!maop_lon!&&$p!~m!maop_lat!&&$p!~m!maop_prog!&&$p!~m!maop_log!)
		elsif ($p!~m/^maop_lat$/){ # begin elsif ($p!~m/^maop_lat$/)
		} # end elsif ($p!~m/^maop_lat$/)
		elsif($p!~m/^maop_lon$/){ # begin elsif($p!~m/^maop_lon$/)
		} # end elsif($p!~m/^maop_lon$/)
		else{ # Begin else
		} # End else
	} # end if($p=~m/^maop\_/)
} # end foreach my $p ($doc->param)
$mparam.="&$extra_param";
#print "<br>oooooooo>$mparam<br>";

my $maop_prog=$doc->param("maop_prog")||"";
my $prog=(length($maop_prog)==0) ? "album.cgi" : $maop_prog;

# we build the url
my $url= 'http';
if ("$ENV{HTTPS}" eq "on") { # Begin if ("$ENV{HTTPS}" eq "on")
	$url .= "s";
} # End if ("$ENV{HTTPS}" eq "on")

$url .= "://"; # We build url
#print "<br><u>A server name:</u>$ENV{SERVER_NAME}<br><u>server port:</u>$ENV{SERVER_PORT}<br><u>server request uri:</u>$ENV{REQUEST_URI}<br>";
if ("$ENV{SERVER_PORT}" ne "80") { # Begin if ("$ENV{SERVER_PORT}" ne "80") 
#	print "<br><u>A url before:</u>$url<br>";
	$url .= $ENV{SERVER_NAME}.":".$ENV{SERVER_PORT}.$ENV{REQUEST_URI};
	$url=~s/maop\.cgi/$prog/; # we put the destination for URL
	#print "<br>UNDER CONSTRUCTION> $url<br>";
	#$url.=$mparam;
	#print "<br>UNDER CONSTRUCTION> $url<br>";
#	print "<br><u>A url after:</u>$url<br><u>prog:</u>$prog<br>";
} # End if ("$ENV{SERVER_PORT}" ne "80")
else { # Begin else
#	print "<br><u>B url before:</u>$url<br>";
	$url .= $ENV{SERVER_NAME}.$ENV{REQUEST_URI};
	$url=~s/maop\.cgi.*/$prog/;
#	print "<br><u>B url after:</u>$url<br>";
} # End else
#print "<br><u>C server name:</u>$ENV{SERVER_NAME}<br><u>server port:</u>$ENV{SERVER_PORT}<br><u>server request uri:</u>$ENV{REQUEST_URI}<br>";
$url=~s/(\/)[^\/]+$/$1/;
$url.=$prog;
#exit(-1);

# =====================================================================================
# =====================================================================================
# =====================================================================================

if( -f "$logfile"){ # begin if( -f "$logfile")
	#unlink("$logfile");
	#&myrec("Case logfile format maop ","../error.html","-f $logfile");
} # end if( -f "$logfile")

$logfile=&do_untaint($logfile);

open(FD,">","${logfile}") or die("$logfile error $!");
print FD " ";
close(FD) or die("$logfile error $!");
$logfile=~s/\//\_/g;

# =====================================================================================
# =====================================================================================
# =====================================================================================

my $myform=<<FORM;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<body>
pouet poet<br>
<p id="wait"></p>

<script>
var mycounter=0;
var x=document.getElementById("wait");
x.innerHTML="1- Attendre svp pendant le chargement...<br><i>Please wait while loading...</i>";
// + "$url?maop_lon="+lon+"&maop_lat="+lat+"$mparam&maop_date=$now_string&maop_log=$logfile";
getLocation();

function getLocation() { // begin function getLocation()
    if (navigator.geolocation) { // begin if (navigator.geolocation)
    //	var options = { maximumAge: 600000, timeout: 1000000 }; 
        navigator.geolocation.watchPosition(showPosition,showError);
    } // end if (navigator.geolocation)
    else { // begin else
        x.innerHTML = "Geolocation is not supported by this browser.";
    } // end else
} // end function getLocation()

function showError(error){ // begin function showError(error)
    switch(error.code) { // begin switch(error.code)
        case error.PERMISSION_DENIED:
            x.innerHTML = "User denied the request for Geolocation.";
            break;
        case error.POSITION_UNAVAILABLE:
            x.innerHTML = "Location information is unavailable.";
            break;
        case error.TIMEOUT:
            x.innerHTML = "The request to get user location timed out.";
            break;
        case error.UNKNOWN_ERROR:
            x.innerHTML = "An unknown error occurred.";
            break;
    } // end switch(error.code)
} // end function showError(error)

function showPosition(position) { // begin function showPosition(position)
    var x=document.getElementById("wait");
    var lon=position.coords.longitude;
    var lat=position.coords.latitude;

    x.innerHTML += "<br>counter:"+mycounter+"<br>"; 
    /*
    mycounter++:
    if(counter>5){
	    #x.innerHTML = "too much calculus<br>";
	    exit(0);
    }
    */
	    

    lon=encodeURIComponent(lon);
    lat=encodeURIComponent(lat);
    var myURL="$url?maop_lon="+lon+"&maop_lat="+lat+"&$mparam&maop_date=$now_string&maop_log=$logfile";
    x.innerHTML += "<br>Seeking longitude: "+lon+"<br>Seeking latitude: "+lat+"<br><b><u>$url</u></b>";
    //var myURL="$url?maop_lon="+lon;
    //myURL+="&maop_lat="+lat;
    //myURL+="&$mparam&maop_date=$now_string&maop_log=$logfile";
    window.location="$url?maop_log=$logfile&maop_lon="+lon+"&maop_lat="+lat+"&$mparam&&maop_date=${now_string}";
} // end function showPosition(position)
</script>
</body>
</html>
FORM

#&myrec("Case 1 ","../error.html","logfile: $logfile");

sub myrec{ # Begin sub myrec
	my ($c,$f,$m)=@_;# $c:case name ; $f: logifile where to store stuff; $m:that's the message
	my $dt = DateTime->from_epoch( epoch => time() );# Current date format DateTime
	my $mainp=(split(/[\\\/]/,"$0"))[scalar(split(/[\\\/]/,"$0"))-1]; # gets program name

	open(W,">>$f")||die("error $!");
	print W "<pre>\n";
	print W "--------------------\n$mainp\n------------$dt---------------------\n";
	print W "$c:\n$m\n\n";
	print W "</pre><br><br>\n";
	close(W)||die("error close$!");
} # End sub myrec

print $myform;
