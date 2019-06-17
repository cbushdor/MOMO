#!/usr/bin/perl-5.30.0
#-T
# #!/Users/sdo/perl5/perlbrew/perls/perl-5.28.1/bin/perl
##!/usr/bin/perl
use feature ':5.10';

$| = 1;

# ------------------------------------------------------
q##//q#
* Created By : sdo
* File Name : weather.cgi
* Creation Date : Sat Apr 13 23:44:44 2015
* Last Modified : Mon Jun 17 13:20:45 2019
* Email Address : sdo@macbook-pro-de-sdo.home
* Version : 0.0.0.0
* License:
*       Permission is granted to copy, distribute, and/or modify this document under the terms of the Creative Commons Attribution-NonCommercial 3.0 
*       Unported License, which is available at http: //creativecommons.org/licenses/by- nc/3.0/.
* Purpose :
   - Basic tests:
]
#;
#------------------------------------------------------
BEGIN {
        push @INC,"/Users/sdo/Sites/cgi-bin/"; # We add a new path to @INC
        # A bug was solved and that's it was "...but still, the newly generated form has al the values from the previous form...".
	#$doc=$CGI::Q ||= new CGI; # It is using the special internal $CGI::Q object, rather than your 'my $doc' object that's why we do this.
	#$rtrip="blue"; # We don't record trip
}
END {
	#$doc->delete_all(); # We clean all variables and parameters when the script is over
}

use LWP::Simple;
# will do weather forecast
# use module
use CGI;

use XML::Simple;
use Data::Dumper;
#use Try::Tiny;

use io::MySec;
use io::MyNav;

my $mip=io::MyNav::gets_ip_address;
$mip = ($mip !~ m/192.168.1.13/) ? "dorseb.hopto.org" : $mip;
my $doc=$CGI::Q ||= new CGI;

print "Content-Type: text/html\n\n";
print "IP addr: $mip<br>";
my $L = $doc->param("lat");
my $l = $doc->param("lon");
my $dir="./album/tests";
my $file_to_parse="$dir/my_owm_tests_data.$$--$L-$l--". time()  .".xml";

#=begin comment
if(defined $L && defined $l && $L ne '' && $l ne ''){ # Begin if(defined $L && defined $l && $L ne '' && $l ne '')
	my $data = ();
	my $url="http://api.openweathermap.org/data/2.5/find?APPID=0efa8f218924f2f1d194893438218851&lat=$L&lon=$l&cnt=2&mode=xml";

	eval { # Begin try
		my $xml = new XML::Simple;
		#my $url="http://api.openweathermap.org/data/2.5/find?APPID=0efa8f218924f2f1d194893438218851&lat=$L&lon=$l&cnt=2&mode=json";
		my $cordstr="";
		my $wfc=get($url) or die "Error $!<br>";
		#if(defined $wfc) { say "result defined". length $wfc ."<br>"; } else { say "result not defined<br>"; }
		#	say "*********>$url<br>We are recording data under $file_to_parse<br>";
		#say "xxxxxxxxx><pre>$wfc</pre><oooooooooooo";
		open(W,">","$file_to_parse") or die("error $!");
		print W $wfc;
		close(W) or die("error $!");
		print "* Weather info recorded under <i><b>$file_to_parse</i></b><br>";

		if(-f "$file_to_parse"){ # Begin if(-f "$file_to_parse")
			say "* File <i>[<b>$file_to_parse</b>]</i> exists";
			#$data = $xml->XMLin("$file_to_parse") || die "<br>Error: $!<br>";

			#rint "<pre>";
			#rint Dumper($data);
			#rint "</pre>";
		} # End if(-f "$file_to_parse")
		else{ # Begin else
			die "X this file $file_to_parse doesn't exist $!<br>";
		} # End else
		1;
	} or do {
		say "<u>Error status:</u><br>";
		say "* Weather taken from <i><b>$url</i></b><br>";
		say "* Data not available check bellow...";
	}; # End try
} # End if(defined $L && defined $l && $L ne '' && $l ne '')
else { # Begin else 
	my $mwfcm=<<MWFCM;
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">

		<link rel="stylesheet" href="https://unpkg.com/leaflet\@1.5.1/dist/leaflet.css" />
		<script src="https://unpkg.com/leaflet\@1.5.1/dist/leaflet.js"></script>
		<script src="../js/leaflet-1.5.1/leaflet.polylineDecorator.js"></script>
            
		<style type="text/css">
			.info { padding: 6px 8px; font: 14px/16px Arial, Helvetica, sans-serif; background: white; background: rgba(255,255,255,0.8); box-shadow: 0 0 15px rgba(0,0,0,0.2); border-radius: 5px; } .info h4 { margin: 0 0 5px; } 
		</style>

		<title>Maquette regarding printing data on a map</title>
        </head>
        <body>
            <h1>Maquette regarding printing data on a map</h1>
            
            <div id="maCarte" style="height: 200px"></div>
	    <p id="lat"></p>
	    <p id="lon"></p>
	    <p id="demo">Let AJAX change this text.</p>

            <script>
		var x = document.getElementById("demo");
		var marker;

		getLocation();

/** ------------------------------------------------------------------------------- **/

		function getLocation() {
			if (navigator.geolocation) {
				navigator.geolocation.getCurrentPosition(showPosition);
			} else {
				x.innerHTML = "Geolocation is not supported by this browser.";
			}
		}

		function showPosition(position) {
			var maCarte = L.map('maCarte').setView([48.83707500083035, 2.358219085090508], 10);

			L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
											maxZoom: 19,
											attribution: ' <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
										}).addTo(maCarte);
			marker = L.marker([position.coords.latitude,position.coords.longitude] ).addTo(maCarte);

			// control that shows state info on hover
			var info = L.control();

			info.onAdd = function (maCarte) {
				this._div = L.DomUtil.create('div', 'info');
				this.update();
				return this._div;
			};

			info.update = function (props) {
				this._div.innerHTML = "<h4>Basic info</h4><br>"+"Ln:"+position.coords.latitude+"<br>Lt:"+position.coords.longitude;
			};
			info.addTo(maCarte);

			var xhttp = new XMLHttpRequest();
			xhttp.onreadystatechange = function() {
				if (this.readyState == 4 && this.status == 200) {
					document.getElementById("demo").innerHTML = this.responseText;
				}
			};

			var myurl="https://$mip/~sdo/cgi-bin/weather.cgi?lon="+position.coords.longitude+"&lat="+position.coords.latitude;
			xhttp.open("GET", myurl, true);
			xhttp.send();

			x.innerHTML = "Latitude: " + position.coords.latitude + "<br>Longitude: " + position.coords.longitude+"<br>" +
				"https://$mip/~sdo/cgi-bin/weather.cgi?rec=1&lon="+position.coords.longitude+"&lat="+position.coords.latitude;
		}
            </script>
        </body>
    </html>
MWFCM

#print "Content-Type: text/html\n\n";
	print "$mwfcm";
} # End else 

#=end comment

#=cut


