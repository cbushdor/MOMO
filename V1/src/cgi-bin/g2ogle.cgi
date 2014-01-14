#!/usr/bin/perl

$|=0;
use warnings;
#use strict;


use LWP::Simple;
use XML::Simple;
use Data::Dumper;

use io::MySec;
use io::MyNav;
use io::MyUtilities;

my $ipAddr=io::MyNav::gets_ip_address;
my $fn=$0; # file name
$fn=~m/([0-9a-zA-Z\-\.]*)$/;
$fn=$1;

my $xml = new XML::Simple;
my ($L,$l)=(48.866699,2.333300);
if($ipAddr=~m/^127./||$ipAddr=~m/loclost/){
}
else{
	($L,$l)=getsGPSCoordinates();
}
my $wfc=get("http://api.wunderground.com/auto/wui/geo/WXCurrentObXML/index.xml?query=$L,$l");
open(W,">wfc_data.$$.xml") or die("error $!");
print W $wfc;
close(W) or die("error $!");
my $data = $xml->XMLin("wfc_data.$$.xml");

my $id=();
my @rr=();
my ($dev, $ino, $mode, $nlink, $uid, $gid, $rdev, $size, $atime, $mtime, $ctime, $blksize, $blocks) = stat "$fn";

if(-f "debug"){ # Begin if(-f "debug")
	$id="ABQIAAAA14j0lCov2bd1GrJ5ANl5IRTD9FXmJRh4UX7FdKnW6k9bqHlslhTnoSdkW9cwNdIa0zOXKE3zzNBZVQ";
} # end if(-f "debug")
else{ # begin else
	$id=io::MyUtilities::loadFile("private/id.googlemap.v2");	
} # end else

my $mymp=() ;

print "Content-type: text/html\n\n";
print "<pre>";
#print Dumper($data);
print "</pre>";
#print "----uuuuu)$_:$data->{pressure_in}  $r<br>";
#print "----uuuuu)$_:$data->{dewpoint_string}  $r<br>";
#foreach my $oo (%{$data}){
		#if(is_hash($data->{$oo})){
			#my %mmm=%{$data->{$oo}};
			#foreach my $ii (%mmm){
				#if(is_hash($mmm->{$ii})){
					#my %mmmm=%{$mmm->{$ii}};
					#foreach my $iii (%mmmm){
						##print "$oo --$ii---->this is hash ($iii): $mmmm->{$iii}<br> ";
					#}
				##}else{
					##print "$oo ------>this is hash $ii: $mmm->{$ii}<br> ";
				##}
			##}
		##}else{
			##print "----uuuuu)$oo:". $data->{$oo} . "<br>";
			### print "----uuuuu)$_:$data->{display_location}->{latitude}  $r<br>";
		##}
##}

&sortAndStore("history","album");
my %l=&getsLoLa("album/history"); # Load file
my $path=&getsPath("album/history","Canada"); # Load file
my $path=&getsPath("album/history","New Zealand"); # Load file

#chomp($id) ;
&mapGoogle("$id");

sub sortAndStore{# begin
	my ($file,$dn)=@_;#$file: file modify;$dn:directory name wher to find file
#	print "$file\n";
	if(-f "$dn/$file"){ # begin if(-f "$dn/$file")
#	  print "zzz\n";
	  	open(R,"$dn/$file"); # Load given file
		my $r=<R>;
		close(R);
		my @a=split(/\,/,$r);
		if( ! -d "$dn/hist"){ # begin if( ! -d "$dn/hist")
			mkdir("$dn/hist");
		} # end if( ! -d "$dn/hist")
		for my $p (@a){# begin for my $p (@a)
			chomp($p);
			my @q=split(/\#/,$p); # split each lines as a column
			my $ipa=$q[0]; # Gets  ip address
			my $cna=$q[7]; # Gets  country name
			$cna=~s/COUNTRY NAME://;
			$cna=~s/\ /_/g;
			if(length($cna)>0){ # begin if(length($cna)>0)
#				print ">>$dn/hist/$cna.$ipa<<<<\n";
				open(W,">>$dn/hist/$cna.$ipa") or die("$dn/hist/$cna $!");
				print W "$p,";
				close(W) or die("$dn/hist/$cna $!");
			} # end if(length($cna)>0)
		} # end 
		open(W,">$dn/$file.old") or die("$dn/$file.old $!");
		print W $r;
		close(W);
		unlink("$dn/$file");
	} # end if(-f "$dn/$file")
} # end 

# load file where are stored longitude and latitude 
sub getsLoLa{# begin getsLoLa
	my ($file)=@_; # File name to analyze
	# $file unused any more checks if it is ok to be removed

	my %llL=();# list of Longitude and latitude taken from a given file
	
	chdir("album");chdir("hist");# we go in album/hist
	my $r=();# store content of each file
	opendir(ARD,".") || die(". $!");# open current directory
	my @dr= grep { $_ ne '.' and $_ ne '..' } readdir(ARD);# parse current directory
	closedir(ARD) || die(". $!");# close directory
	foreach my $ee (@dr){ # begin foreach (@dr) ; parse each file name from current directory
		if(length("$ee")>0){# begin if(length("$ee")>0)
			open(RO,"$ee") || die("$ee $!");$r.=<RO>;chomp($r);close(RO)||die("$ee $!");# store data from files in $r variable
		}# end if(length("$ee")>0)
	} # end foreach (@dr)
	chdir("..");chdir(".."); # come back to original dir configuration
	#print $r;
	#exit(0);
	my @a=split(/\,/,$r);# split in an array
	for my $p (@a){# begin for my $p (@a)
		chomp($p);#remove cariage return if one found
		my @q=split(/\#/,$p); # split each lines as a column
		if(scalar(@q)==14){
		#foreach(@q){ print "\n\nooooiiii)$_\n"; }
		#exit(0);
		#print "#########>".@q." @q\n";
		my $dte=$q[1]; # Gets login date
		my $l=$q[11]; # Gets Latitude
		my $L=$q[12]; # Gets Longitude
		#print "uuuuuuuuuuuuu>$l $L<oooooooo\n";
		#exit(0);
		$l=~s/LATITUDE\://; # Remove comment for the column name
		$L=~s/LONGITUDE\://; # Remove comment for the column name
		if(length("$l")){# begin if(length($l))
		#	print "uuuuuuuuuuuuu>$l $L<oooooooo\n";
			#exit(0);
			if(length("$L")){# begin if(length($L))
				$llL{"$dte@$l,$L"}.="<br>$dte <!-- $q[7]-->";
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
				@rr=(@rr,"$dte\@$l,$L");
				#print "ooooooooooooooooooooooooooooooooooooooooooooo\n";
				#print "ooooooooooo $dte\@$l,$L ooooooooooooo\n";
				#print "ooooooooooooooooooooooooooooooooooooooooooooo\n";
				#exit(0);
			}# end if(length($L))
		}# end if(length($l))
		}# end if(scalar(@q))
	}# end for my $p (@a)
	return %llL; # Returns list
} # end getsLoLa

# loads file where are stored longitude and latitude 
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

# load a file
sub loadFile{# begin loadFile
	my ($fn)=@_; # File name

	open(R,"$fn");
	my @r=<R>;# fle content
	close(R);
	return join("",@r);
}# end loadFile

# Draw basic map acording to db recorded
sub mapGoogle{# begin mapGoogle
	my ($idgoog)=@_ ; # Google id for one page
	chomp($idgoog); # Remove CR at end of string
	my $cart=();
	#foreach(@rr){ print "----->$_\n"; }
	my @aa=sort(@rr);
	#for my $i (keys %l){
	my $vbn=@aa;
	my $cvbn=0;
	for my $i (@aa){
		#print "xxxxxxxxx>$i<<<<<<\n";
		$cvbn++;
		if(length($i)>0){
			my ($v,$u)=split(/\@/,$i);
			#print "oooo)$i oooooo $v,$u\n";
			$cart.="/* A---$i $cvbn / $vbn  ------------------------------------------------ */\n";
			$cart.="			var point = new GLatLng($u);\n";
			$cart.="			var marker = createMarker(point,'');\n";
			$cart.="			map.addOverlay(marker);\n";
			$cart.="/* B---$i $cvbn / $vbn  ------------------------------------------------ */\n\n";
		}
	}
	$cart.="/* C--------------------------------------------------- */\n\n";
	print <<R;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
	<head>
		<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
		<title>Google Maps</title>
R
	print io::MyUtilities::googHead("$idgoog");	
	print <<R;
	<style type="text/css">
		<!--
			a.mailaddr { color: #008000;text-decoration: none; }
			a.mailaddr:visited { color: #008000;text-decoration: none; }
		-->
	</style>
	</head>
<body onunload="GUnload()">

	<div id="map" style="width: 950px; height: 450px"></div>
	<script language="JavaScript" src="http://www.geoplugin.net/javascript.gp" type="text/javascript"></script>

	<script type="text/javascript">
		//<![CDATA[
		function createMarker(point,html) {
			var marker = new GMarker(point);
			GEvent.addListener(marker, "click", function() {
					marker.openInfoWindowHtml(html);
					});
			return marker;
		}

		if (GBrowserIsCompatible()) { 
			var la=geoplugin_latitude();
			var lo=geoplugin_longitude();
			var map = new GMap2(document.getElementById("map"));

			document.write("la:"+la+"   lo:"+lo+"<br>@ $ipAddr <br>");
			map.addControl(new GLargeMapControl());
			map.addControl(new GMapTypeControl());
			//map.setCenter(new GLatLng(43.91892,-78.89231),8);
			map.setCenter(new GLatLng(la,lo),8);

			// Display the map, with some controls and set the initial location 
			var point = new GLatLng(la,lo);
			var marker = createMarker(point,'lo la from geoplugin');
			map.addOverlay(marker);
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
			var cIcon = new GIcon();
			cIcon.image = "http://nhw.pl/images/cross.png";
			cIcon.iconSize = new GSize(16,16);
			cIcon.iconAnchor = new GPoint(8,9);
			var point = new GLatLng($data->{observation_location}->{latitude},$data->{observation_location}->{longitude});
			var marker = createMarker(point,'lo la from api.wunderground.com');
			map.addOverlay(marker);
			// -------------------------------------------------------------
$cart;
$path;
		} // display a warning if the browser was not compatible
		else {
			alert("Sorry, the Google Maps API is not compatible with this browser");
		}

		//]]>
	</script>
	$fn proto: 0.3.$mtime <a href="mailto:shark.baits\@laposte.net" class="mailaddr">shark bait</a>
</body>

</html>
R
}# end mapGoogle

sub is_array{
	my ($re)=@_;
	return ref($re) eq 'ARRAY';
}

sub is_hash{
	my ($re)=@_;
	return ref($re) eq 'HASH';
}
