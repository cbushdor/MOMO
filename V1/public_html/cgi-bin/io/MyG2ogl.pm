package io::MyG2ogl;
use CGI::Carp qw(fatalsToBrowser); 

# +-------------------------------+
# | MySec.pm                      |
# | Written on Jul 19 2009        |
# +-------------------------------+

require Exporter;

use Fcntl qw( :DEFAULT :flock);
use Net::Ping;
use LWP::Simple;

my $VERS       = '0.0';
my $REL        = '0.1';
$VERSION    = "${VERS}.${REL}";
$VERSION    = eval $VERSION;
@ISA    = qw( Exporter );
@EXPORT = qw(
	mapGoogle
	     );

@EXPORT_OK = qw( 
	mapGoogle
       );


my $GROUP_FILE="groups";

# Written by shark bait ###

=head1 NAME

packages::MyG2ogl.pm

$VERSION = '0.0.0.1'

=head1 ABSTRACT

This package manages stuff that deals Google maps.

=head2 LIST OF FUNCTIONS

=over 4

mapGoogle

=back

=head2 HISTORY OF MODIFICATIONS

=over 4

- I<Last modification:> Mar 22 2010. What a big day for a new package that deals with google issues.

- I<Last modification:> Mar 21 2010. What a big day for a new package that deals with google issues.

- I<Starting date:> Mar 21 2010 prototypes were written but this is the real starting date.

=back

=cut

# -----------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------

=head1 FUNCTION mapGoogle

Draws basic map according to data base.

=head2 PARAMETER(S)

=over 4

=over 4

$idgoog: Google id for one page

$perm : allow to print information according to given grants.

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

Returns script that manage the map with flags.

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

- I<Last modification:> Mar 21 2010 perm arg addes to function.

- I<Created on:> Mar 21 2010

=back

=back

=cut

sub mapGoogle{
	my ($idgoog,$perm)=@_ ; # Google id for one page

	chomp($idgoog); # Remove CR at end of string
	my $cart=();
	for my $i (keys %l){
		$cart.="// ---------------------------------------------------\n";
		$cart.="			var point = new GLatLng($i);\n";
		if($perm==0){ # perm granted print info about logs
			$cart.="			var marker = createMarker(point,'<i>Logs</i>$l{$i}')\n";
		}else{
			$cart.="			var marker = createMarker(point,'Thanks for the visit/Merci pour la visite')\n";
		}
		$cart.="			map.addOverlay(marker);\n";
		$cart.="// ---------------------------------------------------\n\n";
	}
	print <<R;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
	<head>
		<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
		<title>Google Maps</title>
		<script src="http://maps.google.com/maps?file=api&amp;v=2&amp;sensor=false&amp;key=${id}" type="text/javascript"></script>
	</head>
<body onunload="GUnload()">

	<div id="map" style="width: 550px; height: 450px"></div>

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
			var map = new GMap2(document.getElementById("map"));
			map.addControl(new GLargeMapControl());
			map.addControl(new GMapTypeControl());
			map.setCenter(new GLatLng(43.91892,-78.89231),8);

			// Display the map, with some controls and set the initial location 
			var point = new GLatLng(43.91892,-78.89231);
			var marker = createMarker(point,'Some stuff to display in the<br>Second Info Window')
			map.addOverlay(marker);
			// -------------------------------------------------------------
$cart
		} // display a warning if the browser was not compatible
		else {
			alert("Sorry, the Google Maps API is not compatible with this browser");
		}

		//]]>
	</script>
	proto: 0.1<br>shark bait
	</body>

</html>
R
}

=head1 FUNCTION loadFile

Loads a file.

=head2 PARAMETER(S)

=over 4

=over 4

$fn: file name.

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

Returns file content.

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

- I<Last modification:> Mar 22 2010 nothin much for now on.

- I<Created on:> Mar 22 2010

=back

=back

=cut

sub loadFile{
	my ($fn)=@_; # File name
	

	open(R,"$fn");
	my @r=<R>;# fle content
	close(R);
	return join("",@r);
}

=head1 FUNCTION getsLoLa

Loads file where are stored logitude and latitude 

=head2 PARAMETER(S)

=over 4

=over 4

$file: file name to analyze.

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

Returns list.

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

- I<Last modification:> Mar 22 2010 nothin much for now on.

- I<Created on:> Mar 22 2010

=back

=back

=cut


sub getsLoLa{
	my ($file)=@_; # File name to analyze
	my %llL=();# list of Longitude and latitude taken from a given file

	open(R,"$file"); # Load given file
	my $r=<R>;
	close(R);

	my @a=split(/\,/,$r);
	for my $p (@a){
		chomp($p);
		my @q=split(/#/,$p); # split each lines as a column
		my $dte=$q[1]; # Gets login date
		my $l=$q[9]; # Gets Latitude
		my $L=$q[10]; # Gets Longitude
		$l=~s/LATITUDE://; # Remove coment
		$L=~s/LONGITUDE://; # Remove coment
		if(length($l)){
			if(length($L)){
				$llL{"$l,$L"}.="<br>$dte";
			}
		}
	}
	return %llL; # Returns list
}

1;

=head1 AUTHOR

Current maintainer: sebush, <sebush@laposte.net>

=cut
