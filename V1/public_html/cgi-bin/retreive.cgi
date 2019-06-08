#!/usr/bin/perl 
#-T

use lib '/Users/sdo/Sites/cgi-bin/';
use lib '/home1/derased/public_html/cgi-bin/';
#push @INC, '/Users/sdo/Sites/cgi-bin/';
#push @INC, '/home1/derased/public_html/cgi-bin/';

use strict;
use warnings;
use LWP::Simple;
use XML::LibXML;
use io::MyTime;
use XML::Simple;
use Data::Dumper;
use io::MyNav;
use CGI;

my $mdoc=new CGI;

use constant ALBUM_INFO_DIRECTORY  	=> "album/"; # that's where album info are stored
use constant ALBUM_INFO_HIST_DIRECTORY 	=> ALBUM_INFO_DIRECTORY . "hist/";

my $ipAddr=io::MyNav::gets_ip_address;
my %geoloc=&pruneOutOfTheNodeGeoLoc("$ipAddr");
my $me="IP Address Labs (Product: Pro)";
my %u=&getsMethodFromHash($me,%geoloc);

print "Content-type: text/html\n\n";
print "$ipAddr ----->" . &getsFromMethodData("IP Address",%u)."\n";
print "<pre>";
print  &storeData("$ipAddr",$me);
print "</pre>";

sub storeData{
	my ($ip,$me)=@_;# IP address,method used to get data
	#uy %geoloc=&pruneOutOfTheNodeGeoLoc($ip);
	#my %u=&getsMethodFromHash($me,%geoloc);
	my ($L,$l)=();# Latitude Longitude
	my $doc=XML::LibXML::Document->new('1.0', 'utf-8');
	my $root=$doc->createElement("ip");
	my $u=localtime;$u=~s/\ //g;
	$root->setAttribute('IPAd'=> "$ip");
	$root->setAttribute('Method'=> "$me");
	my $fwea=ALBUM_INFO_HIST_DIRECTORY. &getsFromMethodData("Country",%u) . "-$ip-"."wfc_data.$u.xml";

	{
		my $tag = $doc->createElement("Date");
		$tag->appendTextNode(io::MyTime::gets_formated_date); 
		$root->appendChild($tag);
	}

	{
		my $tag = $doc->createElement("ContinentName");
		$tag->appendTextNode(&getsFromMethodData("Continent",%u));
		$root->appendChild($tag);
	}

	{
		my $tag = $doc->createElement("ContinentName");
		$tag->appendTextNode(&getsFromMethodData("Country",%u));
		$root->appendChild($tag);
	}

	{
		my $tag = $doc->createElement("RegionName");
		$tag->appendTextNode(&getsFromMethodData("Region",%u));
		$root->appendChild($tag);
	}

	{
		my $tag = $doc->createElement("CityName");
		$tag->appendTextNode(&getsFromMethodData("City",%u));
		$root->appendChild($tag);
	}

	{
		my $tag = $doc->createElement("Latitude");
		$tag->appendTextNode($L=&getsFromMethodData("Latitude",%u));
		$root->appendChild($tag);
	}

	{
		my $tag = $doc->createElement("Longitude");
		$tag->appendTextNode($l=&getsFromMethodData("Longitude",%u));
		$root->appendChild($tag);
	}

	{
		my $tag = $doc->createElement("Provider");
		$tag->appendTextNode(&getsFromMethodData("ISP",%u));
		$root->appendChild($tag);
	}

	{
		my $tag = $doc->createElement("TripName");
		$tag->appendTextNode($mdoc->param("TRIP"));
		$root->appendChild($tag);
	}

	{
		my $wfc=get("http://api.wunderground.com/auto/wui/geo/WXCurrentObXML/index.xml?query=$L,$l");
		open(W,">$fwea") or die("$fwea\nerror $!");
		print W $wfc;
		close(W) or die("error $!");

		#my $tag = $doc->createElement("Weather");
		#$tag->appendTextNode("$fwea");
		#$root->appendChild($tag);
	}


	my $xml = new XML::Simple;
	$doc->setDocumentElement($root);
	open(W,">".ALBUM_INFO_HIST_DIRECTORY.&getsFromMethodData("Country",%u)."-". "$ip.xml") or die("error $!\n");
	print W $doc->toString(1);
	close(W) or die("error $!\n");
	my $data = $xml->XMLin(ALBUM_INFO_HIST_DIRECTORY.&getsFromMethodData("Country",%u)."-". "$ip.xml");
	print Dumper($data);
	print $doc->toString(1);
}

sub getsFromMethodData{
	my ($df,%h)=@_;
	return $h{$df};
}

sub getsMethodFromHash{
	my($meth,%refu)=@_;#Method,hash containing all methods
	#chomp($meth);
	foreach my $m (keys %refu){
		my %p=%{$refu{$m}};
		#print length($meth). "  "  . length($m) . " $meth=~m/^$m\$/<br>\n";
		if("$m" eq "${meth}"){
			return %p; 
		}
	}
	#print "no";
}

sub printGeoLoc{
	my(%refu)=@_;
	print '<span style="color:red;">';
	print "===========\n";
	print "</span>";
	foreach my $m (keys %refu){
		my %p=%{$refu{$m}};
		print '<span style="color:blue;">';
		print "ppppppp>";
		print "</span>";
		print "$m\n";
		#my %k=%refu{$m};
		foreach my $o (keys %p){
			print "             x $o : $p{$o}\n";
		}
	}
}

sub pruneOutOfTheNodeGeoLoc{ # begin sub pruneOutOfTheNodeGeoLoc
	my ($ip)=@_;

	$ip=(defined $ip) ? "?query=$ip":"";
	#print "http://www.iplocation.net$ip\n";
	my $content = get("http://www.iplocation.net$ip") or die 'Unable to get page';# gets contents of distant
	my @mcontent=split(/\n/,$content);
	my $mc=join(" ",@mcontent);
	my @geo=(); # 
	my $mt=(); # method
	my $r=();

	$mc=~s/^.*<br \/> <\/form>//g;
	$mc=~s/[\r\n]//g;
	$mc=~s/Registry Information for.*$//;
	@geo=split(/Geolocation data from/,$mc);
	$r=scalar(@geo)-2;

	my %at=();# hash table
	my $ln=0;# line number
	foreach my $i (1..$r){ # begin foreach my $i (1..$r)
		my %data=(); # store data
		my $lll=$geo[$i]; # we take one block that contains data for one method of geolocation
		my @lin=split(/\<\ *tr[^\>\<]*\>/,$lll); # we split the table by lines
		my @an=();
		my @am=();

		# we work on one line of the table
		for my $o (@lin){ # begin for my $o (@lin)
			$o=~s/(\<\/table\>).*//i;
			$o=~s/\<a[^\<\>]*\>//gi;
			$o=~s/\<spacer[^\<\>]*\>//gi;
			$o=~s/\<table[^\<\>]*\>//gi;
			$o=~s/\<\/a\>//gi;
			$o=~s/\<\/div\>//gi;
			my @col=split(/\<\ *td[^\>\<]*\>/,$o);# we split to get columns
			my $param=$1;# save params of the column
			my @ac=(); # array column(s) init

			if($o=~m/Product:/){
				$mt=$o;
				$mt=~s/^\ *//g;
				$mt=~s/\ *$//g;
				#print "uuuuuuuuuuu>$o<\n";
			}
			if($o=~m/^\<td[^\<\>]*\>(.*)\<\/td\>\<td[^\<\>]*\>(.*)\<\/td\>\<td[^\<\>]*\>(.*)\<\/td\>\<td[^\<\>]*\>(.*)\<\/td\>\<td[^\<\>]*\>(.*)\<\/td\>/i){
				#print "xxxxxxxxxxxxxxxxx>$1,$2,$3,$4,$5\n";
				if($ln==0){
					$ln=1;
					@an=($1,$2,$3,$4,$5);
				}else{
					@am=($1,$2,$3,$4,$5);
					for my $i (0..4){
						$data{$an[$i]}=$am[$i];
					}
					$ln="&nbsp;";
					delete $data{$ln};
					$ln=0;
				}
			}
			#if($bl) {$bl=0; $ln++;}# incrrem line number reset 
		} # end for my $o (@lin)
		$at{$mt}=\%data;
		#%data=(); # We init 
		#my %a=%{$at{$mt}}; foreach (keys %a){ print '<span style="color:red;">'; print "ooooo>$_ :"; print "</span>"; print $a{$_}."\n"; }
	} # end foreach my $i (1..$r)
	return %at;
} # end sub pruneOutOfTheNodeGeoLoc

exit 0;
