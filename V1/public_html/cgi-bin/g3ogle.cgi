#!/usr/bin/perl5.30.2  -T

# ------------------------------------------------------
q##//q#
* Created By : sdo
* File Name : g3ogle.cgi
* Creation Date : Sat Jul 26 12:35:15 2014
* @modify date 2020-06-04 22:18:50
* Email Address : sdo@linux.home
* Version : 0.2.1..500
* License:
*       Permission is granted to copy, distribute, and/or modify this document under the terms of the Creative Commons Attribution-NonCommercial 3.0
*       Unported License, which is available at http: //creativecommons.org/licenses/by- nc/3.0/.
* Purpose :
#;
# ------------------------------------------------------

use CGI;

$|=0;

my $doc;
BEGIN {
	push @INC,"/Users/sdo/Sites/cgi-bin/"; # We add a new path to @INC
	push @INC,"/home/sdo/public_html/cgi-bin/"; # We add a new path to @INC
	# A bug was solved and that's it was "...but still, the newly generated form has al the values from the previous form...".
	$doc=$CGI::Q ||= new CGI; # It is using the special internal $CGI::Q object, rather than your 'my $doc' object that's why we do this.
}
END {
	$doc->delete_all(); # We clean all variables and parameters when the script is over
}

use warnings;
use strict;

use DateTime;
use DateTime::Format::Strptime;
use DateTime::TimeZone;
use POSIX;

use LWP::Simple;
use XML::Simple;
use Data::Dumper;
use Net::Ping;
use Cwd;

use io::MyConstantBase;
use io::MyNav;
use io::MySec;
use io::MyUtilities;

use URI::Escape;
use Encode qw(from_to);

our $mip=io::MyNav::gets_ip_address; # We retreive IP address it can be Public or Private IP

print "Content-Type: text/html\n\n";

#my $ipAddr=io::MyNav::gets_ip_address;
my $VERSION="0.2.1.578";

=head1 NAME

g3ogle.cgi

$VERSION="0.2.1.578"

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
infoCenter

=back

=back

=head2 HISTORY OF MODIFICATIONS

=over 4

- I<Last modification:v0.2.1.500> Jan 30 2019 This is perl 5, version 24, subversion 3 (v5.24.3) built for darwin-thread-multi-2level to This is perl 5, version 28, subversion 1 (v5.28.1) built for darwin-2level (with 1 registered patch, see perl -V for more detail).

- I<Last modification:v0.2.1.154> Aug 30 2015: removed test below
			if(!("$ll" eq "$l" && "$LL" eq "$L")){ # Begin if(!("$ll" eq "$l" && "$LL" eq "$L"))

- I<Last modification:v0.2.1.55> Jan 31 2015: added test below
		$lat!~m/^[\-\+]{0,1}[0-9]{1,}\.[0-9]{1,}$/

- I<Last modification:v0.2.1.50> Jan 31 2015: see infoCenter

- I<Last modification:v0.2.1.34> Jan 06 2014: see infoCenter

- I<Last modification:v0.2.1.20> Feb 20 2014: test with ping added for local debug

- I<Last modification:v0.2.1.4> Feb 11 2014: see mapGoogle

- I<Last modification:v0.2.1.3> Feb 10 2014: see getsLoLa(...), getsPath(...)

=back

=cut


{
	open(REC,">>../rec.html")||die("err: $!");
	my $tft=gmtime(); #time for test
	print REC "<br>BEGIN < $0 > $tft<br>";
	foreach my $p ($doc->param){ # Begin foreach my $p ($doc->param)
		print REC ">>>>>>>$p --->".$doc->param($p)."<br>";
	} # End foreach my $p ($doc->param)
	print REC "<br>END < $0 > $tft<br>";
	close(REC)||die("Error:$!");
}

my $lstlog=30*2; # That's seconds
my $lon=$doc->param("maop_lon");# We retreive longitude from param
my $lat=$doc->param("maop_lat");# We retreive latitude from param
my $logfile= $doc->param("maop_log"); # We retreive last logfile  to help to calculate if file is older than $lstlog in seconds from param
$logfile=~s/\_/\//g; # We retreive the path
my $ui=time - (stat "$logfile")[9]; # We calculte the lag
my $statlastlogfile =($ui > $lstlog); # We check if log file is older than $lstlog seconds
my $ilws=0; # Is local website variable used for tests (local website,distant website)

if($statlastlogfile){ # Begin if($statlastlogfile)
	my $mparam=();
	print "Content-Type: text/html\n\n";
	print "<h1>Under construction</h1><br>$ui > $lstlog<br>";
	#exit(-1);

	foreach my $p ($doc->param){ # Begin foreach my $p ($doc->param)
		#		print ">>>>>>>$p --->".$doc->param($p)."<br>";
		if($p=~m/^maop\_/){ # Begin if($p=~m/^maop\_/)
			if($p!~m/^maop_lon$/&&
				$p!~m/^maop_lat$/&&
				$p!~m/^maop_prog$/&&
				$p!~m/^maop_log$/){ # Begin if($p!~m!maop_lon!&&$p!~m!maop_lat!&&$p!~m!maop_prog!&&$p!~m!maop_log!)
				$mparam.='&'."$p=".$doc->param($p);
			}  # End if($p!~m!maop_lon!&&$p!~m!maop_lat!&&$p!~m!maop_prog!&&$p!~m!maop_log!)
			elsif ($p!~m/^maop_lat$/){ # Begin elsif ($p!~m/^maop_lat$/)
				#&myrec("Case logfile format maop ","../error.html","****** $la" );
			} # End elsif ($p!~m/^maop_lat$/)
			elsif($p!~m/^maop_lon$/){ # Begin elsif($p!~m/^maop_lon$/)
				#&myrec("Case logfile format maop ","../error.html","****** $lo" );
			} # End elsif($p!~m/^maop_lon$/)
		} # End if($p=~m/^maop\_/)
	} # End foreach my $p ($doc->param)
	my $url=();
	#	if(-e "$logfile") { print "file  $logfile exists<br>";}
	#	else { print "file  $logfile does not exists<br>";}
	if( -e "$logfile"){ # Begin if( -e "$logfile")
		my ($foo) = ($logfile =~ /^(.*)$/g);
		unlink("$foo");
	} # End if( -e "$logfile")
	chdir("album");chdir("hist");
	my @lflb=split(/\//,$logfile);
	my $lfl=$lflb[scalar(@lflb)-1];
	$lfl=~/^(.*)$/g;$lfl=$1;
	#	print "<br><h2>this is the log file to use $lfl</h2>";
	#	print "<h1><br>- ". getcwd() ."</h1><br>";
	open(W,">$lfl") || die("Error with $lfl $!");
	print W " ";
	close(W) || die("Error with $lfl $!");

	#	if(-e "$lfl") {print "<h3>------------>$lfl exist</h3><br>" ;}
	#	else { print "$lfl does not exist<br>";}

	chdir("..");chdir("..");
	$logfile=~s/\//\_/g;
	#my $locres=&io::MyConstantBase::LOCAL_HOSTED_BY_URL->();
	if(&io::MyNav::is_local_network_address){ # Begin if(&io::MyNav::is_local_network_address)
		#$url="http://localhost/~sdo/cgi-bin/maop.cgi?maop_prog=g3ogle.cgi";
		my $param_trip=uri_unescape($doc->param("maop_googid"));
		$url= "https://".&io::MyConstantBase::LOCAL_HOSTED_BY_URL->(). "/~sdo/cgi-bin/maop.cgi?maop_prog=g3ogle.cgi\&maop_log=$logfile$mparam\&maop_googid=$param_trip";
		$ilws=0; # is local website 0=yes (for local wesite tests)
	} # End if(&io::MyNav::is_local_network_address)
	else{ # Begin else
		$ilws=1; # is local website 1=no (for distant wesite tests)
		#$url="https://dorey.effers.com/~sdo/cgi-bin/maop.cgi?maop_prog=g3ogle.cgi\&maop_log=$logfile$mparam";
		$url= "https://".&io::MyConstantBase::DISTANT_HOSTED_BY_URL->(). "/~sdo/cgi-bin/maop.cgi?maop_prog=g3ogle.cgi\&maop_log=$logfile$mparam";
	} # End else
	print "ooooooooo>$url<br>";
	exit(-1);
	#	print "case 2-------($statlastlogfile)=======$logfile<br>";exit(1);
	#my $c=<<A;
	print <<A;
<!DOCTYPE html>
<html>
<body>
case 34
<p id="wait"></p>

<script>
	var x=document.getElementById("wait");
	x.innerHTML="3- Please wait while loading...<br>$url<br>current ip: $mip<br>";
	window.location="$url";
</script>
</body>
</html>
A
#print $c;
	exit(0);
} # End if($statlastlogfile)
print "Content-Type: text/html\n\n";
print "<br>We stop here";

if(! defined($lat)||length($lat)==0||$lat!~m/^[\-\+]{0,1}[0-9]{1,}\.[0-9]{1,}$/){ # Begin if(!defined($lat)||length($lat)==0||$lat!~m/^[\-\+]{0,1}[0-9]{1,}\.[0-9]{1,}$/)
	my $url=();
	print "Content-Type: text/html\n\n";
	print "case 2 latitude not defined or don't exist '$lat'<br>";exit(1);
	#if(! defined($mip)||$mip=~m/^127\.0\.0\.1/i||$mip=~m!localhost!||$mip=~m!&io::MyConstantBase::LOCAL_HOSTED_BY_URL->()!){ # Begin if(! defined($mip)||$mip=~m/^127\.0\.0\.1/i||$mip=~m!localhost!||$mip=~m!&io::MyConstantBase::LOCAL_HOSTED_BY_URL->()!)
	if(&io::MyNav::is_local_network_address){ # Begin if(&io::MyNav::is_local_network_address)
		my $param_trip=uri_unescape($doc->param("maop_googid"));
		$url= "https://".&io::MyConstantBase::LOCAL_HOSTED_BY_URL->(). "/~sdo/cgi-bin/maop.cgi?maop_prog=g3ogle.cgi\&maop_googid=$param_trip";
		#$url="http://localhost/~sdo/cgi-bin/maop.cgi?maop_prog=g3ogle.cgi";
		#}# End if(! defined($mip)||$mip=~m/^127\.0\.0\.1/i||$mip=~m!localhost!||$mip=~m!&io::MyConstantBase::LOCAL_HOSTED_BY_URL->()!)
	} # End if(&io::MyNav::is_local_network_address)
	else{
		#$url="http://derased.heliohost.org/cgi-bin/maop.cgi?maop_prog=g3ogle.cgi";
		#$url="https://dorey.effers.com/~sdo/cgi-bin/maop.cgi?maop_prog=g3ogle.cgi";
		$url= "https://".&io::MyConstantBase::DISTANT_HOSTED_BY_URL->(). "/~sdo/cgi-bin/maop.cgi?maop_prog=g3ogle.cgi";
	}
	print "<br>carlamentrant<br>url:$url<br>";
	exit(-1);
	#my $c=<<A;
	print <<A;
<!DOCTYPE html>
<html>
<body>
<p id="wait"></p>

<script>
	var x=document.getElementById("wait");
	x.innerHTML="1- Please wait while loading...";
	window.location="$url";
</script>
</body>
</html>
A
	#print $c;
	exit(0);
} # End if(!defined($lat)||length($lat)==0||$lat!~m/^[\-\+]{0,1}[0-9]{1,}\.[0-9]{1,}$/)

if(! defined($lon)||length($lon)==0||$lon!~m/^[\-\+]{0,1}[0-9]{1,}\.[0-9]{1,}$/){ # Begin if(!defined($lon)||length($lon)==0||$lon!~m/^[\-\+]{0,1}[0-9]{1,}\.[0-9]{1,}$/)
	my $url=();
	print "Content-Type: text/html\n\n";
	print "case 1 longitude not defined or don't exist '$lon'<br>";exit(1);
	#if(! defined($mip)||$mip=~m/^127\.0\.0\.1/i||$mip=~m!localhost!||$mip=~m!&io::MyConstantBase::LOCAL_HOSTED_BY_URL->()!){ # Begin if(! defined($mip)||$mip=~m/^127\.0\.0\.1/i||$mip=~m!localhost!||$mip=~m!&io::MyConstantBase::LOCAL_HOSTED_BY_URL->()!)
	if(&io::MyNav::is_local_network_address){ # Begin if(&io::MyNav::is_local_network_address)
		$url="http://localhost/~sdo/cgi-bin/maop.cgi";
		my $param_trip=uri_unescape($doc->param("maop_googid"));
		$url= "https://".&io::MyConstantBase::LOCAL_HOSTED_BY_URL->(). "/~sdo/cgi-bin/maop.cgi?maop_googid=$param_trip";
		$ilws=0; # is local website 0=yes (for local wesite tests)
		#}# End if(! defined($mip)||$mip=~m/^127\.0\.0\.1/i||$mip=~m!localhost!||$mip=~m!&io::MyConstantBase::LOCAL_HOSTED_BY_URL->()!)
	} # End if(&io::MyNav::is_local_network_address)
	else{
		#$url="http://derased.heliohost.org/cgi-bin/maop.cgi";
		#$url="https://dorey.effers.com/~sdo/cgi-bin/maop.cgi";
		$url= "https://".&io::MyConstantBase::DISTANT_HOSTED_BY_URL->(). "/~sdo/cgi-bin/maop.cgi";
		$ilws=1; # is local website 1=no (for distant wesite tests)
	}
	#my $c=<<A;
	print "KARL>>>>>>>>>>>>>>>>>>>>>$url<br>";
	exit(-1);
	print <<A;
<!DOCTYPE html>
<html>
<body>
case 2
<p id="wait"></p>

<script>
	var x=document.getElementById("wait");
	x.innerHTML="2- Please wait while loading...";
	window.location="$url";
</script>
</body>
</html>
A
#print $c;
	exit(0);
} # End if(!defined($lon)||length($lon)==0||$lon!~m/^[\-\+]{0,1}[0-9]{1,}\.[0-9]{1,}$/)

print "<br>We reached end of sanitary tests <br>lon:$lon;<br>lat:$lat<br>";
#exit(0);
my ($gmv,$prt)=split(/\-/,$doc->param("maop_gmv")); # Gets google map version, googlemap option: 0,1,2
my ($googid)=$doc->param("maop_googid"); # Gets google map version
chomp($prt);chomp($googid);

print "Content-type: text/html\n\n";

#print "A - i$gmv,$prt, check  test prt length if it is ok. implemented but not tested yet<br>";
if(length($googid)==0 || ! defined($googid) ){ # Begin if(length($prt)==0 || ! defined($prt) )
	$prt=1;
} # End if(length($prt)==0 || ! defined($prt) )

my $fn=$0; # file name
$fn=~m/([0-9a-zA-Z\-\.]*)$/;
$fn=$1;

my $id=();
my ($dev, $ino, $mode, $nlink, $uid, $gid, $rdev, $size, $atime, $mtime, $ctime, $blksize, $blocks) = stat "$fn";

if(-f "debug"){ # Begin if(-f "debug")
	$id="AIzaSyDoz8j1983lLAncsYMjXLeemy5ks3DkfM8";
} # End if(-f "debug")
else{ # Begin else
	$id=io::MyUtilities::loadFile("private/id.googlemap.v3");	
} # End else

my $mymp=() ;
my $path=(); # olds data to print on the map
my %l=();
my @rr=();

#-------------------------------------------------------------------------

chomp($id) ;

# Checks options for map rinting with Markers
#if(defined($prt)){ # Begin if(definied($prt))
# Prints where you are
if($prt==0){ # Begin if($prt==0)
	$path.=&getsPath("album/hist","$googid"); # Load file
	&mapGoogle("$id","$gmv");
} # End if($prt==0)
# Prints all markers
if($prt==1){ # Begin if($prt==1)
	$path.=&getsLoLa("album","hist"); # Load DB 
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

sub getsLoLa{ # Begin getsLoLa
	my ($dp,$ds)=@_; # (dp: directory parent,ds: directory son) where are stored DB

	my $llL=();# list of Longitude and latitude taken from a given file

	chdir("$dp");chdir("$ds");# we go in $dp/$ds. Now it's current diectory
	my $r=();# store content of each file
	opendir(ARD,".") || die(". $!");# open current directory
	my @dr= grep { $_ ne '.' and $_ ne '..' and $_ !~ m/pl$/i and $_ !~ m/cgi$/i and $_=~m!^maop-!} readdir(ARD);# parse current directory
	closedir(ARD) || die(". $!");# close directory

	# @dr contains all files and directories from current dir except . and ..
	foreach my $ee (@dr){ # Begin foreach (@dr) ; parse each file name from current directory
		if(length("$ee")>0){ # Begin if(length("$ee")>0)
			open(RO,"$ee") || die("$ee $!");$r.=<RO>;chomp($r);close(RO)||die("$ee $!");# store data from files in $r variable
		} # End if(length("$ee")>0)
	} # End foreach (@dr)
	chdir("..");chdir(".."); # come back to original dir configuration
	my @a=split(/\,/,$r);# split in an array
	for my $p (@a){ # Begin for my $p (@a)
		chomp($p);#remove cariage return if one found
		my @q=split(/\#/,$p); # split each lines as a column
		if(scalar(@q)>3){ # Begin if(scalar(@q)>3)
			my $dtes=$q[7]; # Gets login date
			my $l=$q[4]; # Gets Latitude
			my $L=$q[3]; # Gets Longitude
			if(length("$l")){ # Begin if(length($l))
				if(length("$L")){ # Begin if(length($L))
					@rr=(@rr,"$dtes\@$l,$L");
				} # End if(length($L))
			} # End if(length($l))
		} # End if(scalar(@q)>3)
	} # End for my $p (@a)
	return $llL; # Returns list
} # End getsLoLa


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

sub getsPath{ # Begin getsPath
	my ($file,$field)=@_; # File name to analyze
	my $llL=();# list of Longitude and latitude taken from a given file

	chomp($file);
	foreach my $ld (split(/\//,$file)){ # Begin foreach (split(/\//,$file))
		chdir("$ld");
	} # End foreach (split(/\//,$file))
	my $r=();# store content of each file
	opendir(ARD,".") || die(". $!");# open current directory
	my @dr= grep { $_ ne '.' and $_ ne '..' and $_ !~ m/pl$/i and $_ !~ m/cgi$/i and $_=~m/^maop\-/} readdir(ARD);# parse current directory
	closedir(ARD) || die(". $!");# close directory
	foreach my $ee (@dr){ # Begin foreach (@dr) ; parse each file name from cuon directory
		if(length("$ee")>0){ # Begin if(length("$ee")>0)
			open(R,"$ee") || die("$ee $!");$r.=<R>;chomp($r);close(R)||die("$ee $!");# store data from files in $r variable
		} # End if(length("$ee")>0)
	} # End foreach (@dr)
	chdir("..");chdir(".."); # come back to original dir configuration

	my @a=split(/\,/,$r);
	my $l=();my $L=();my $ll=();my $LL=();
	my @zz=(); # path stored
	my $prev=();
	my $newArrows=();
	my @infoWC=();
	for my $p (@a){ # Begin for my $p (@a)
		chomp($p);
		my @q=split(/\#/,$p); # split each lines as a column
		# we check country name below
		if($q[5]=~m/$field/i){ # Begin if($q[7]=~m/$field/i)
			#print "oooooooooooooooo)$q[14] ------------ ";
			#		print ")))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))$q[7]<br>";
			my $dte=$q[7]; # Gets login date
			my $l=$q[4]; # Gets Latitude
			my $L=$q[3]; # Gets Longitude
			@infoWC=(@infoWC,&infoCenter("$q[6]"));# Info Weather Center
			# we remove same coordnitates that next to each ohers (line before)
			#if(!("$ll" eq "$l" && "$LL" eq "$L")){ # Begin if(!("$ll" eq "$l" && "$LL" eq "$L"))
			# checks here if we can mix array with weather forecast
			# trig with vi a.s /new google.maps.LatLng
			#print "------------------------------------------------------->$dte<br>";
			@zz=(@zz,"$dte@ new google.maps.LatLng($l,$L),\n");
			#} # End if(!("$ll" eq "$l" && "$LL" eq "$L"))
			$ll=$l;$LL=$L;
			#print "	
		} # End if($q[7]=~m/$field/i)
	} # End for my $p (@a)
	my @qq=sort(@zz);
	my $markersTrip=();

	#print "size of the array ". scalar(@qq) . "<<<<<<<<<<<<<<<<br>";
	my $max=scalar(@qq);
	my $cur=1;
	#use constant &io::MyConstantBase::PATH_GOOGLE_MAP_TRIP->() 	=> "album/trips/";
	#use constant &io::MyConstantBase::TRIP_NAME->()           	=> "trips"; # Album trips
	my $mgidt=$doc->param("maop_googid"); #my google id  trip
	chomp($mgidt);

	my $tn=&io::MyConstantBase::PATH_GOOGLE_MAP_TRIP->().$mgidt ."-".&io::MyConstantBase::TRIP_NAME->(); # Trip name

	if ( ! -f "$tn"){ # Begin if ( ! -f "$tn")
		print "Content-type: text/html\n\n";
		print <<R;
			<p1>
			File not exists $mgidt;
			</p1>
			<br><b><u>We are checking all variables values passed as param:</b></u><br>
R
		exit(-1);
	} # End if ( ! -f "$tn")
	open(RTN,"$tn") or die ("$tn error $!");my @rtn=<RTN>;close(RTN) or die("$tn close error"); # RTN: read trip name file (contains begin and end of trip)
	#open(W,">____test.txt");print W "$logfile °°°°°° $rtn[0]\n";close(W);
	chomp($rtn[0]);my ($brtn,$ertn)=split(/\#/,$rtn[0]);
	my $anal = DateTime::Format::Strptime->new( pattern => '%Y-%m-%dT%H:%M' ); # Analyzer
	my $dtb = $anal->parse_datetime( $brtn );
	$logfile=~s/\//\_/g;

	#print "Content-Type: text/html\n\n";
	foreach(@qq){ # Begin foreach(@qq)
		my($ed,$ea)=split(/\@/,$_);
		chomp($_);
		#print "$_<br>\n";
		chomp($ea);
		$ea=~s/,$//;
		if($cur<$max){ # Begin if($cur<$max)
			if ($cur>1){ # Begin if ($cur>1)
				#open(W,">>____test.txt");print W "cur($cur)<max($max) ---  dte($dte)<dt3($dt3)=".($dte<$dt3)."\n";close(W);
				#	{ # Begin if($dte<$dt3)
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
								// displays marker position
								infowindow.setContent( "$infoWC[$cur]" );
								infowindow.open( this.getMap(), this);
							}); 
				// --------------------------------
			// --------------------------------
TRIP_MARKERS
				#} # End if($dte<$dt3)
			} # End if ($cur>1)
			else { # Begin else
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
				// displays marker position
				    infowindow.setContent( "$cur==1 ---->$ea" );
				    infowindow.open( this.getMap(), this);
				  }); 
				// --------------------------------
			// --------------------------------
TRIP_MARKERS
			} # End else
		} # End if($cur<$max)
		else{
			my $anal2 = DateTime::Format::Strptime->new( pattern => '%Y-%m-%dT%H:%M' ); # Analyzer
			my $dte = $anal2->parse_datetime( $ertn );
			my $dt3 = DateTime->from_epoch( epoch => time() );# Current date format DateTime

			if($dte<$dt3)
			{
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
				// displays marker position
				    infowindow.setContent( "$cur==1 ---->$ea" );
				    infowindow.open( this.getMap(), this);
				  }); 
				// --------------------------------
			// --------------------------------
TRIP_MARKERS
			}
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
	} # End foreach(@qq)
	#exit(-1);
	$llL.=<<POLY;
				// Begin polylines codes

				$markersTrip

				// End polylines codes

					$newArrows
POLY
	return $llL; # Returns list
} # End getsPath


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

sub loadFile{ # Begin loadFile
	my ($fn)=@_; # File name

	open(R,"$fn");
	my @r=<R>;# fle content
	close(R);
	return join("",@r);
} # End loadFile


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

sub mapGoogle{ # Begin mapGoogle
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
	$cart.="\t\t\t\t\tmarkers.push(marker);\n";
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
	print io::MyUtilities::googHead("$idgoog","$gmv",$ilws);	
	my $colo="CCCC00";
	my $leng=<<A;
				EtapeDebut: {
					name: "Début d'étape/Begining of stage",
					icon: 'https://chart.googleapis.com/chart?chst=d_map_pin_icon&chld=flag|003300'
				},
				EtapeTerminée: {
					name: 'Etape terminée/Stage is over',
					icon: 'https://chart.googleapis.com/chart?chst=d_map_pin_icon&chld=flag|00FF00'
				},
				EtapeEnCour: {
					name: 'Etape en cour/Stage processing',
					icon: 'https://chart.googleapis.com/chart?chst=d_map_pin_icon&chld=flag|FF0000'
				},
				wyrrn: {
					name: 'Vous etes ici/You are here',
					icon: "https://chart.googleapis.com/chart?chst=d_map_xpin_letter&chld=pin|W|CCCC00"
				}
A
	#print "Content-type text/html\n\n"; print "ooooooooooooooooooooooooooooooo>$gmv<------<br>";
	if($prt!~0){
		$colo="0033CC";
		$leng=<<A;
				ywt: {
					name: 'Vous etiez là/You were there',
					icon: "https://chart.googleapis.com/chart?chst=d_map_xpin_letter&chld=pin|W|0033CC"
				},
				wyrrn: {
					name: 'You are here',
					icon: "https://chart.googleapis.com/chart?chst=d_map_xpin_letter&chld=pin|W|CCCC00"
				}
A
	}
	#my $lanal = DateTime::Format::Strptime->new( pattern => '%Y-%m-%dT%H:%M' ); # Analyzer
	#$lanal->pattern('%z');
	my $mldate= strftime '%Y-%m-%dT%H:%M %z', localtime;

	#my $mldtz=$lanal->offset_for_datetime;
	my $param_trip=uri_unescape($doc->param("maop_googid"));
	#my $ldtb = $lanal->parse_datetime( $brtn );
	print <<R;
		<script type="text/javascript" src="../js/markerclusterer.js"></script>
		<script type="text/javascript">
			//<![CDATA[
			var map;
			var mc;// MarkerClusterer
			var mcOptions = {gridSize: 50, maxZoom: 15};// MarkerCluster Options
			var markers = [];
			var marker;
			var la=$lat; //geoplugin_latitude();
			var lo=$lon; //geoplugin_longitude();
			var position= new google.maps.LatLng(la,lo);

			var icons = {
				$leng
			};

			function initialize(){ // Begin function initialize()
				var mapOptions = {
					center: position,
					zoom: 15,
					zoomControl: true,
					mapTypeId: google.maps.MapTypeId.TERRAIN
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
				var div = document.createElement('div');
				div.innerHTML = "<i>v$VERSION</i>";
				legend.appendChild(div);

				map=new google.maps.Map(document.getElementById("map"),mapOptions);
				map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(legend);

				$cart;
				$path;
				mc=new MarkerClusterer(map,markers,mcOptions);
				marker=createMarkerWhereYouAre(position,"text");
				marker.setMap(map);
			} // End function initialize()

			// To add the marker to the map, call setMap();
			function createMarker(point,text) { // Begin function createMarker(point,html)
				var lmarker = new google.maps.Marker({
						position: point,
						map: map,
						icon: "https://chart.googleapis.com/chart?chst=d_map_xpin_letter&chld=pin|W|$colo",
						title: text
					});
					return lmarker;
			} // End function createMarker(point,html)

			function createMarkerWhereYouAre(point,text) { // Begin function createMarker(point,html)
				var lmarker = new google.maps.Marker({
						position: point,
						map: map,
						icon: "https://chart.googleapis.com/chart?chst=d_map_xpin_letter&chld=pin|W|CCCC00",
						 zIndex: google.maps.Marker.MAX_ZINDEX + 1,
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
	<div id="legend"><center><h2>$param_trip</h2></center><br>On $mldate<br><h3>Legend</h3></div>
	<!--
	$fn proto: 0.3.$mtime <a href="mailto:shark.baits\@laposte.net" class="mailaddr">shark bait</a>
	-->
</body>

</html>
R
} # End mapGoogle


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

sub is_array{ # Begin sub is_array
	my ($re)=@_; # $re: variable to check its type.
	return ref($re) eq 'ARRAY';
} # End sub is_array


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

sub is_hash{ # Begin sub is_hash
	my ($re)=@_; #$re: variable to check its type.
	return ref($re) eq 'HASH';
} # End sub is_hash


=head1 sub infoCenter(...)

=head2 SYNOPSIS

=over 4

=over 4

Return a string that contains data from weather center  website.

=back

=back

=head2 PARAMETER(S)

=over 4

=over 4

$nwc: file name that contains weather center data

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

That's a formated string.

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

- Last modification: Jan 08 2014

- Created on: Jan 02 2014

=back

=back

=cut

sub infoCenter{ # Begin sub infoCenter
	my ($nwc)=@_; # Name weather center
	if(-e "$nwc"){ # Begin if(-e "$nwc")
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
	} # End if(-e "$nwc")
	else{ # Begin else
		return   
		"<div id='content'>"
		."<ul>"
		."<li>- No data available</li></ul>"
		."</div>"
		;
	} # End else
} # End sub infoCenter

print "v$VERSION\n<br>";
