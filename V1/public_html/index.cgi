#!/usr/local/bin/perl -T
##!/usr/bin/perl5.30.2 -T
##!/usr/bin/perl -T


# ------------------------------------------------------
q##//q#
* Created By : sdo
* File Name : index.cgi
* Creation Date :2012-02-16 00:40:17
* @modify date 2020-11-08 23:40:51
* Email Address : sdo@macbook-pro-de-sdo.home
* Version : 0.0.0.0
* License:
*       Permission is granted to copy, distribute, and/or modify this document under the terms of the Creative Commons Attribution-NonCommercial 3.0
*       Unported License, which is available at http: //creativecommons.org/licenses/by- nc/3.0/.
* Purpose :
#;
# ------------------------------------------------------

use strict;
use warnings;
use CGI qw(:all);
use CGI::Carp qw(fatalsToBrowser);
#use CGI::Pretty qw( :html3 );
use Pod::Simple::HTML;
use POSIX;
use POSIX qw/strftime/;
use MIME::Base64;
use Cwd;
use URI::Escape;
use File::Copy;
use Digest::SHA1  qw(sha1 sha1_hex sha1_base64);
use DateTime;
use Fcntl qw(:flock SEEK_END); # import LOCK_* and SEEK_END constants

# -------------------------------------------------------------------------------
# Do not touch the next line
my $gcd = getcwd; # Gets current dir
# -------------------------------------------------------------------------------

# -------------------------------------------------------------------------------
# ------------- Set directories webhost and local --------------------------------
my $HOME_ROOT = "/Users/sdo/Sites/";# alternative directory for local debug)
my $MY_HOME_DIR = "/Users/sdo/Sites/cgi-bin";# alternative directory for local debug
my $HOME_URL='http://127.0.0.1/~sdo';

if("$HOME_ROOT" eq "$gcd"){
	$HOME_ROOT = "/home1/derased/public_html";
	$MY_HOME_DIR = "/home1/derased/public_html/cgi-bin";
	$HOME_URL='http://derased.heliohost.org';
}

# -------------------------------------------------------------------------------


# -------------------------------------------------------------------------------
# ------------- Setup github repository to pull ---------------------------------
my @lor = (
		'git@github.com:perl6/specs.git',
		'https://github.com/perl6/tablets.git',
		'git@github.com:perl6/course.git'
	);# List Of Repositories
# -------------------------------------------------------------------------------

# -------------------------------------------------------------------------------
# ------------- Set timing and frequency ----------------------------------------
my %freq = (minutes=>2*60);# Frequency of update when last submission date is not over
my %lsa = (year => 2012, month => 8, day => 14);# Date of last submission authorized 
my $lag = "+2";#GMT+2
my $timer_directory_js = 1000*20;
my $timer_directory_mobiles_js = 1000*20; # that's 3 seconds sec*3 1 sec =1000 1 sec =1000ms
# -------------------------------------------------------------------------------

# -------------------------------------------------------------------------------
# ------------- Setup font and size as default ----------------------------------
use constant DEFAULT_FONT => '"Bromine","Coming soon","Helvetica Neue", Arial, Helvetica, sans-serif';#"Courier,Sand, fantasy";
use constant DEFAULT_SIZE => "12px";

use constant SECOND_DEFAULT_FONT => '"Comic Sans MS","Apple Chancery", "Zapf Chancery", cursive ';
use constant SECOND_DEFAULT_SIZE => "12px";
# -------------------------------------------------------------------------------

# -------- MY CODE DO NOT REMOVE THIS LINE ------

$CGI::Pretty::INDENT = "\t";

use constant MY_ERROR => -1;
use constant ERROR_CONNEXION => -2;

my $useragent = " ";
$useragent = $ENV{'HTTP_USER_AGENT'};
if(!defined($useragent)){$useragent = "";}else{chomp($useragent);} # for navigator user agent

$useragent =~ m/(msie)\ *([0-9]+(.[0-9]+)*);/i;
my($nav,$ver) = ($1,$2);
if(!defined($nav)){$nav = "";}else{chomp($nav);} # for navigator name
if(!defined($ver)){$ver = "";}else{chomp($ver);} # for navigator version
my @files = ();# Files from current directory
my @lfiles = ();# Files from current directory
my @direc = ();# directories from current directory
my $pti = ""; # Path To Icon
my $myr = "";# MY Root used for the path when navigating with the browser
my $html = "";
my @stat = ();# gets its content
$0 =~ /(.*\/)*(.+)/;# Gets the script name
my $fnc = $2;# File Name CGI
my $f2pd = 0;# File To Print Default
my $cgi = $CGI::Q || new CGI; # Instanciate a CGI object (old, new methods)
my $igithub = (); # Script stored there to print a prompt to indicated it is or it will be processing with github
my $spo = 0;# back or not back menu
my $jasc = ();

# ----------------------------------------------------------------------------
# ----------------- Begin: gets parameters values ----------------------------
# ----------------------------------------------------------------------------
my $method = $cgi->param("method");
my $bgdaem = $cgi->param("bgdaem");
if(!defined($bgdaem)){$bgdaem = "";}else{chomp($bgdaem);} # for background stuff
my $searchreq = ();
#if($method =~ m/^post$/i){
	$searchreq = $cgi->param("request");
#}
my $finace = $cgi->param("go"); # FIle NAme CodEd
if(!defined($finace)){$finace = "";}else{chomp($finace);}
my $lenm=length($finace);
my $C = $cgi->param("C");# sort directories
if(!defined($C)){$C = "";}else{chomp($C);}
my $O = $cgi->param("O");# sort order 
if(!defined($O)){$O = "";}else{chomp($O);}
my $F = $cgi->param("F");# Format of the listing
if(!defined($F)){$F = "";}else{chomp($F);}
# ----------------------------------------------------------------------------
# ----------------- End: gets parameters values ------------------------------
# ----------------------------------------------------------------------------

if(!-d "$MY_HOME_DIR"){
	mkdir("$MY_HOME_DIR");
}


my $cud = getcwd;# Gets current directory
$cud.= ($cud!~m/\/$/) ? "/" : "";
$myr = ("$cud" eq "$MY_HOME_DIR") ? ".":"..";# MY Root used for the path when navigating with the browser
$cud =~ s/$HOME_ROOT/\~/;# Path to print on the screen/ url built

foreach(split(/\//,$cud)){ # calculates number of directories to cross in order to get to root
	$pti .= "../";
}

# --------------------------------------------
# Begin Section only used for debugging
if(-f "$HOME_ROOT/.foo"){
	$pti =~ s!^../!!;
}
# End Section only used for debugging
# --------------------------------------------

if("$F" eq "0"){
	if(length($bgdaem)==0){ 
		&cartouch;# Board DIRectoryLIStingDETail
		print &cBVaiV($nav,$ver);
		print $cgi->div({-id=>"listing"},"...");
		print $cgi->div({-id=>"podFileContent"},"");
		print $cgi->end_html;
	}
	else{ print "Content-type: text/html\n\n";}
	&manage_repo;
	&lcd;# Load current directory before doing stuff
	&corps0;
	#system("/usr/bin/touch coco0.0");
}elsif("$F" eq "1"){
	if(length($bgdaem)==0){ 
		&cartouch(SECOND_DEFAULT_FONT,SECOND_DEFAULT_SIZE);# Board DIRectoryLIStingDETail
		print &cBVaiV($nav,$ver);
		print $cgi->div({-id=>"listing"},"");
		print $cgi->div({-id=>"podFileContent"},"");
		print $cgi->end_html;
	}
	else{ print "Content-type: text/html\n\n";}
	&manage_repo;
	&lcd;# Load current directory before doing stuff
	&corps2;
	#system("/usr/bin/touch coco0.1");
}elsif("$F" eq "2"){
	if(length($bgdaem)==0){ 
		&cartouch;
		print &cBVaiV($nav,$ver);
		print $cgi->div({-id=>"listing"},"");
		print $cgi->div({-id=>"podFileContent"},"");
		print $cgi->end_html;
	}
	else{ print "Content-type: text/html\n\n";}
	&manage_repo;
	&lcd;# Load current directory before doing stuff
	&corps2;
	#system("/usr/bin/touch coco0.2");
}else{
	if(length($bgdaem)==0){ 
		&cartouch;
		print &cBVaiV($nav,$ver);
		print $cgi->div({-id=>"listing"},"");
		print $cgi->div({-id=>"podFileContent"},"");
		print $cgi->end_html;
	}
	else{ print "Content-type: text/html\n\n";}
	&manage_repo;
	&lcd;# Load current directory before doing stuff
	if("$bgdaem" eq "1"){ 
		&corps2;
		#system("rm coco*;/usr/bin/touch coco0.3");
	}
	#system("/usr/bin/touch coco0.3");
}


# Lists current directory
sub lcd{
	opendir REP,"."  or die("Impossible to open directory $!");# we open current directory 
	foreach(readdir REP ){# gets its content
		if(-f "$_"){@lfiles = (@lfiles,$_);} # @lfiles is a global variable
		else{@direc = (@direc,$_);} # @direc is a global variable
		@files=(@files,$_); # @files is a global variable
	}
	closedir REP  or die("Error $!");# close 
	splice(@files,0,2); # @files is a global variable
	splice(@direc,0,2); # @direc is a global variable
}

# Creates a cartouche at the top of the page
sub cartouch{# Board DIRectoryLIStingDETail
	my ($font,$size) = @_;
	my $fd = POSIX::open(".",&POSIX::O_RDONLY) or die("Error $!");# we open the file
	@stat = POSIX::fstat($fd);# gets its content
	POSIX::close($fd) or die("Error $!");# close it

	if(length((defined($font))?"$font":"") == 0){$font = DEFAULT_FONT;}
	if(length((defined($size))?"$size":"") == 0){$size = DEFAULT_SIZE;}
	my $hp2p = <<S;
		body{
			font-family: $font;
			font-size: $size;
		}
		#info{
			position: absolute; 
			background-color: #808080;
			width: 550px;
			top: 100px; 
			right: 30px; 
			border-width: 1px 1px 1px 1px;
			border-style: solid solid;
			border-color: black black;
			padding: 0 10px;
			padding-left: 20px;
			padding-right: 10px;
			opacity: 0.9;
			filter: alpha(opacity=90); /* For IE8 and earlier */
			z-index: 3;
		}
		div.indexPath{
			position: absolute; 
			top: 45px; 
			left: 25px; 
			z-index: 2;
		}
		div.mypicla{
			position: absolute; 
			top: 100px; 
			left: 30px; 
			z-index: 2;
		}
		div.mypicua{
			text-align: center; 
			top: 100px; 
			left: 50%;
			z-index: 2;
		}
		div.mypicra{
			position: absolute; 
			top: 100px; 
			right: 30px; 
			z-index: 2;
		}
		div.cartouch{
			height: 70px;
			background-color: #41436D;
			-moz-border-radius: 20px;
			-webkit-border-radius: 20px;
			-khtml-border-radius: 20px;
			border-radius: 20px;
			behavior: url(border-radius.htc);
			border-radius: 20px;
			color: white;
			padding-left: 20px;
			padding-right: 10px;
			box-shadow: 3px 3px 4px #000;
			z-index: 1;
		}
		td.cico {
			padding-left: 5px;
			padding-right: 5px;
		}
		td.cnam {
			padding-right: 5px;
		}
		td.lamo {
			padding-left: 5px;
		}
		td.csize {
			padding-left: 5px;
		}
		a:link {
			text-decoration: none;
			color: gray;
		} 
		a:hover { 
			text-decoration: none;
			color: gray;
			font-weight: bold; 
		}
		a:visited { 
			text-decoration: none;
			color: gray;
		} 
S
	if($nav!~m/msie/i){
		$hp2p .= <<S;
		div.msearch{
			position: absolute; 
			top: 10px;
			right: 10px;
		}
		div.searchcase{
			position: absolute; 
			right: 30px;
		}
		#infos{
			-moz-border-radius: 20px;
			-webkit-border-radius: 20px;
			-khtml-border-radius: 20px;
			border-radius: 20px;
			position: absolute; 
			background-color: #808080;
			//height: 550px;
			width: 550px;
			top: 200px; 
			right: 200px; 
			padding: 0 10px;
			padding-left: 20px;
			padding-right: 10px;
			opacity: 0.9;
			filter: alpha(opacity=90); /* For IE8 and earlier */
			z-index: 3;
		}
S
		$jasc=<<R;
	function remov(){
		document.getElementById("infos").innerHTML="";
	}

	function submitForm(url,field) {
		var xhr;

		field.innerHTML="<div class='msearch'><form><input type='image' src='/icons/close.gif' onclick='remov();'></form></div><br>";
		try {  xhr = new ActiveXObject('Msxml2.XMLHTTP');   }
		catch (e) {
			try {   xhr = new ActiveXObject('Microsoft.XMLHTTP'); }// IE5,IE6
			catch (e2) {
				try {  xhr = new XMLHttpRequest();  }// IE7+, Firefox, Chrome, Safari, and Opera
				catch (e3) {  xhr = false;   }
			}
		}

		xhr.onreadystatechange = function(){
			if(xhr.readyState  == 4)
			{
				if(xhr.status  == 200)
					field.innerHTML+= xhr.responseText;
				else
					field.innerHTML+="Error code " + xhr.status;
			}
		};

		try{
			xhr.open( "GET", url,  true);
			xhr.send(null);
		} catch (e) {
			alert("Browser not supported");
		}
	}

	function submitForm2(url,field) {
		var xhr;

		try { xhr = new ActiveXObject('Msxml2.XMLHTTP');   }
		catch (e) {
			try { xhr = new ActiveXObject('Microsoft.XMLHTTP'); }// IE5,IE6
			catch (e2) {
				try { xhr = new XMLHttpRequest();  }// IE7+, Firefox, Chrome, Safari, and Opera
				catch (e3) { xhr = false;   }
			}
		}

		xhr.onreadystatechange = function(){
			if(xhr.readyState  == 4){
				if(xhr.status  == 200){
					document.getElementById("listing").innerHTML=xhr.responseText;
				}
				else{
					document.getElementById("listing").innerHTML="Error code " + xhr.status;
				}
			}
		};

		try{
			//document.write("script 2 "+url);
			xhr.open( "GET", url,  true);
			xhr.send(null);
		} catch (e) {
			alert("Browser not supported");
		}
	}

	/*
	function orderRequest(value){
		submitForm("/cgi-bin/machine.cgi?p="+value,document.getElementById('infos'));
	}
	*/
	var t;
	function refreshCurDir(){
			var xhr;

			clearTimeout(t);

			try { xhr = new ActiveXObject('Msxml2.XMLHTTP'); }
			catch (e) {
				try { xhr = new ActiveXObject('Microsoft.XMLHTTP'); }// IE5,IE6
				catch (e2) {
					try { xhr = new XMLHttpRequest();  }// IE7+, Firefox, Chrome, Safari, and Opera
					catch (e3) { xhr = false;   }
				}
			}

			xhr.onreadystatechange = function(){
				if(xhr.readyState  == 4){
					if(xhr.status  == 200){
						document.getElementById("listing").innerHTML=xhr.responseText;
					}
					else{
						document.getElementById("listing").innerHTML="Error code " + xhr.status;
					}
				}
			};

			try{
				xhr.open( "GET", "$fnc?F=$F&C=$C&O=$O&bgdaem=1",  true);
				xhr.send(null);
			} catch (e) {
				alert("Browser not supported");
			}

			if(mobile.detect()){
				t=setTimeout('refreshCurDir()',$timer_directory_mobiles_js);// wowo
				/*
				if($timer_directory_mobiles_js==1000){
					$timer_directory_mobiles_js*=2;
					alert("mobile detected $timer_directory_mobiles_js");
				}
				*/
			}else{
				//alert("mobile detected $timer_directory_mobiles_js");
				t=setTimeout('refreshCurDir()',$timer_directory_js);
			}
		}

		var mobile = function(){
			return {
				detect:function(){
					var uagent = navigator.userAgent.toLowerCase(); 
					var list = this.mobiles;
					var ismobile = false;
					for(var d=0;d<list.length;d+=1){
						if(uagent.indexOf(list[d])!=-1){
							ismobile = true;
						}
					}
					return ismobile;
				},
				mobiles:[
					"midp","240x320","blackberry","netfront","nokia","panasonic",
					"portalmmm","sharp","sie-","sonyericsson","symbian",
					"windows ce","benq","mda","mot-","opera mini",
					"philips","pocket pc","sagem","samsung","sda",
					"sgh-","vodafone","xda","palm","iphone",
					"ipod","android"
				]
			};
		}();

		refreshCurDir();
R

	}

	my $ial = 1; # is a leaf

	# <link rel="shortcut icon" href="">
	# <meta charset="utf-8" />
	# <meta name="viewport" content="width=device-width,initial-scale=1.0" />
	# <meta http-equiv="X-UA-Compatible" content="ie=edge" />

	print $cgi->header(-type => 'text/html', 
		-charset => 'utf-8') ;

	if($nav!~m/msie/i){
		print $cgi->start_html(
					-head=> [ 
						$cgi->Link({ -href=>"", -rel=>"shortcut icon", }),
		$cgi->meta( {
			       	-charset => 'utf-8'
			}),
		$cgi->meta( {
				-name => 'viewport' ,
				-content => "width=device-width,initial-scale=1.0"
			}),
		$cgi->meta( {
				-http_equiv => "X-UA-Compatible",
				-content => 'text/html'
			}),
					],
					-title => 'Documentation',
					-meta => {
						'Event' => 'Direcory',
						'Keywords' => 'documentation pod,perl',
						'Description' => 'Perl 6 Tutorial...',
						},
					-style => {-code => "$hp2p"},
					-script => {-code => "$jasc"}
					);
	}else{
		print $cgi->start_html(
					-head=> [ 
						$cgi->Link({ -href=>"", -rel=>"shortcut icon", }),
		$cgi->meta( {
			       	-charset => 'utf-8'
			}),
		$cgi->meta( {
				-name => 'viewport' ,
				-content => "width=device-width,initial-scale=1.0"
			}),
		$cgi->meta( {
				-http_equiv => "X-UA-Compatible",
				-content => 'text/html'
			}),
					],
					-title => 'Documentation',
					-meta => {
						'Event' => '',
						'Keywords' => 'documentation pod,perl',
						'Description' => '...'
						},
	-head=> [ 
		$cgi->Link({
				-href=>"",
				-rel=>"shortcut icon", 
			}),
		$cgi->meta( {
			       	-charset => 'utf-8'
			}),
		$cgi->meta( {
				-name => 'viewport' ,
				-content => "width=device-width,initial-scale=1.0"
			}),
		],
					-style => {-code => "$hp2p"}
					);
	}

	my $dlm = ();#Date of Last Modification
	$fd = POSIX::open("$fnc",&POSIX::O_RDONLY) or die("Error $MY_HOME_DIR/$fnc $!");
	@stat = POSIX::fstat($fd);# gets its content
	$dlm = $stat[7];# Date last modification
	POSIX::close($fd) or die("Error $!");
	#----------------------------
	print $cgi->div({-class => "cartouch"},
				($useragent!~m!msie!i)
				?
					$cgi->h2($cgi->span({-style => "position: relative;float: top;top: 1px;"},"Directory listing")).
					$cgi->h2($cgi->span({-style => "position: relative;float: top;left: 300px;bottom: 30px"},"...")) .
					$cgi->h3($cgi->span({-style => "position: relative;float: top;left: 300px;bottom: 45px"},"Current: ".strftime('%d-%b-%Y %H:%M',gmtime))).
					$cgi->h3($cgi->span({-style => "position: relative;float: left;left: 5px;bottom: 60px;"},"Index ".$cgi->i("$cud")))
				:
					$cgi->span({-style => "position: relative;float:right;top: 5px;"},$cgi->img({-width=>"50",-alt=> "",-src => $HOME_URL . '/icons/logo_mongueurs.png'})).
					$cgi->h2($cgi->span({-style => "position: relative;float: top;top: 1px;"},"Documentation POD")).
					$cgi->h2($cgi->span({-style => "position: relative;float: top;left: 290px;bottom:20px"},"...")) .
					$cgi->h3($cgi->span({-style => "position: relative;float: top;left: 290px;bottom:35px"},"vendredi 29, samedi 30 juin 2012 à Strasbourg, France")).
					$cgi->h3($cgi->span({-style => "position: relative;float: top;left:5px;bottom: 55px;"},"Index ".$cgi->i("$cud"))) 
			) .
			#(($nav=~m/msie/i) ? " ":
			#$cgi->div({-class=>"searchcase"},
				#$cgi->start_form({
						#-method=>"post",
						#-name=>"searchengine",
						#-action=>"$fnc?F=$F&go=$finace&C=$C&O=$O&bgdaem=1"
					    #}).
						#"Search/Chercher ".
							#$cgi->input({-type=>"text",-name=>"request"}).
							#$cgi->input({-type=>"button",-value=>"Soumettre/Submit",
							#-submit=>"orderRequest(this.form.request.value);",
							#-onclick=>"orderRequest(this.form.request.value);"
							#}).
				#"<!-- begin hello world -->". 
				#$cgi->endform())) .
				"<!-- end hello world-->".
				$cgi->div({-id=>"infos"},"").
				$cgi->br();
}

# Option to print inde
sub corps0{
	my $corps = ();
	my $ues = ();# Uri EScape

	if(length($finace)>0){$finace = uri_unescape("$finace");} # Transform file name encoded with escaped character to decoded 
	if(length($finace) == 0){ # Case no name provided
		@files = ("..",@files); # is a global variable that contains files from the current directory
		if(length($finace)>0){$finace = uri_unescape("$finace");}
		foreach my $out (@files){
			chomp($out);
			if("$out" ne ".."){#
				if(-d "$out"){
					$out=~s/\ +/\_$$\_\_MY\_SPACE\_$$\_\_/g;
					unless ($out =~ m#^([\w.-]+)$#){# $1 is untainted
						die("Variable '$out' has invalid characters $!.\n");
					}
					$out=$1;
					$out=~s/\_$$\_\_MY\_SPACE\_$$\_\_/\ /g;
					&putLink($out);# copy index.cgi to subdir 1 level
				}
			}
			$ues = uri_escape("$out");# Uri EScape
			if("$myr" eq ".." || "$out" ne ".."){# case we are not in the homedir
				$corps .= $cgi->li( $cgi->a({-href => ((-d "$out") ? "$out/$fnc?F=$F" : (($out!~/.pod$/) ? "$ues?F=$F" : "$fnc?F=$F&go=$ues&bgdaem=1"))},(($out =~ m/^\.\.$/) ? "Parent Directory":((-d "$out") ? "$out/" : "$out"))));
			}else{
				$corps .= $cgi->li( $cgi->a({-href => ((-d "$out") ? (("$out" eq "..") ? "":"$out/$fnc?F=$F&go=$ues&C=$C&O=$O&bgdaem=1") : "?F=$F&go=$ues&bgdaem=1")},(($out =~ m/^\.\.$/) ? "Parent Directory":((-d "$out") ? "$out/" : "$out"))));
			}
			if(length("$finace") == 0){
				if($f2pd == 0){
					if($out =~ m/^readme.pod$/i){# if it is a pod file extension and readme.pod
						$finace = "$out";
						$f2pd++;
					}
				}
			}
		}
		if($finace =~ m/\.pod$/i){ # we print readme.pod file
			my $p = Pod::Simple::HTML->new;
			$p->output_string(\$html);
			$p->parse_file("$finace");
			#$spo++;# 
		}
		my $body0=$cgi->center($cgi->table({-summary => "Listings of file in current directory"},$cgi->Tr($cgi->td({-align => "left",-valign => "top"},$cgi->ul($corps)))) 
			#.  $cgi->img({-width => "50", -alt => "",-src =>$HOME_URL .  '/icons/_logo.png'})
		);  # onion image added
		print "$body0";
		&myenc("$html",$spo);
	}else{ # Case name provided
		#system("touch popo");
		if($finace =~ m/\.pod$/i){# we print readme.pod file
			my $p = Pod::Simple::HTML->new;
			$p->output_string(\$html); # We attach memory $html to $p object
			$p->parse_file("$finace"); # Store the content of the pod file in the object $p
			$spo++;# 
		}else{# this is not a pod file
			open(R,"$finace") or die("Error $!");
			my @aa = <R>;
			close(R) or die("Error $!");
			$spo++;# 
			foreach (@aa){
				print "$_";
			}
			$html=" ";# fake html page
		}
	}
	&myenc("$html",$spo);
}

# Option to print index
sub corps2{
	if($lenm>0){$finace = uri_unescape("$finace");
		#open(A,">rrrr.txt");
		#print A "$finace";
		#close(A);
	}
	#else{ print "ooooooooooooo>$lenm,$finace,$$<br>"; }
	if(length($finace) == 0){
		my $fti = "";# File Type Image
		my $p2p = ();# page to print
		if   ("$C" eq "N" && "$O" eq "A"){@files =         sort         @lfiles,@direc;}
		elsif("$C" eq "N" && "$O" eq "D"){@files = reverse sort         @lfiles,@direc;}
		elsif("$C" eq "S" && "$O" eq "A"){@files =         sort @direc; @files=(@files,sort by_size @lfiles); }
		elsif("$C" eq "S" && "$O" eq "D"){my @filesd = reverse sort @direc; my @filesf = reverse sort by_size @lfiles; @files=(@filesf,@filesd); }
		elsif("$C" eq "M" && "$O" eq "A"){@files =         sort by_date @lfiles,@direc;}
		elsif("$C" eq "M" && "$O" eq "D"){@files = reverse sort by_date @lfiles,@direc;}
		elsif("$C" eq "D" && "$O" eq "A"){@files =         sort by_date @lfiles,@direc;}
		elsif("$C" eq "D" && "$O" eq "D"){@files = reverse sort by_date @lfiles,@direc;}
		@files = (".","..",@files);
		$p2p = $cgi->Tr(
					$cgi->th({-valign => "top",-align => "center"},[""]),
					$cgi->th({-valign => "top",-align => "center"},[$cgi->a({-href => "$fnc?F=$F&C=N&".(("$O" eq "A") ? "O=D":"O=A")
					},"Name")]),
					$cgi->th({-valign => "top",-align => "center"},[$cgi->a({-href => "$fnc?F=$F&C=M&".(("$O" eq "A") ? "O=D" : "O=A")},"Last modified")]),
					$cgi->th({-valign => "top",-align => "center"},[$cgi->a({-href => "$fnc?F=$F&C=S&".(("$O" eq "A")  ? "O=D"  : "O=A")},"Size")]),
					$cgi->th({-valign => "top",-align => "center"},[$cgi->a({-href => "$fnc?F=$F&C=D&".(("$O" eq "A") ? "O=D":"O=A")},"Description")]),
				);
		$p2p .= $cgi->Tr($cgi->td({-valign => "top",-align => "center",-colspan => "5"},$cgi->hr()));
		foreach my $out (@files){# we get each element of the current directory
			chomp($out);

			# ------------------------------------------------------
			# begin we associate aspecific image with the file
			if ($out =~ m/^\.\.$/){$fti = $cgi->img({-alt => "", -src => '/icons/back.gif'});}# its a parent directory
			elsif(-d "$out"){$fti = $cgi->img({-alt => "",-src => '/icons/folder.gif'});}# its a folder
			elsif(-f "$out"){$fti = $cgi->img({-alt => "",-src => '/icons/text.gif'});}# its a file
			# end we associate a specific image with the file
			# ------------------------------------------------------

			# we encode the file name
			my $ues = uri_escape("$out");# Uri EScape
			# treat each element but not current directory
			if($out!~m!^\.$!){
				#print "ooooooooo)$out<br>";
				my $fd = POSIX::open("$out",&POSIX::O_RDONLY) or die("$gcd .... $out--> Error $!");# we open the file
				@stat = POSIX::fstat($fd);# gets its content
				POSIX::close($fd) or die("Error $!");# close it
				if("$out" ne ".."){
					if(-d "$out"){
						$out=~s/\ +/\_$$\_\_MY\_SPACE\_$$\_\_/g;
						unless ($out =~ m#^([\w.-]+)$#){# $1 is untainted
							die("Variable '$out' has invalid characters $!.\n");
						}
						$out=$1;
						$out=~s/\_$$\_\_MY\_SPACE\_$$\_\_/\ /g;
						&putLink($out);# copy index.cgi to subdir 1 level
					}
				}
				if($out!~m/\.pod$/i){# it is not a pod file
					$p2p .= $cgi->Tr(
							$cgi->td({-valign => "top",-align => "left",-class => "cico"},"$fti").
							$cgi->td({-valign => "top",-align => "left",-class => "cnam"},
								$cgi->a({-href => (($out =~ m/^\.\.$/) ? "$myr/$fnc?F=$F&C=$C&O=$O" : ((-d "$out") ? "$out?F=$F&C=$C&O=$O":"$out"))}	,(($out =~ m/^\.\.$/) ? "Parent Directory":((-d "$out") ? "$out/" : "$out")))).
							$cgi->td({-valign => "top",-align => "right",-class => "clamo"},(($out =~ m/^\.\.$/) ? "" : strftime('%d-%b-%Y %H:%M',&calLocalTime($stat[9],$lag)))).
							$cgi->td({-valign => "top",-align => "right",-class => "csize"},((-d $out) ? "-" : $stat[7])).
							$cgi->td({-valign => "top",-align => "right"})
						 );
				}else{# if it is a pod file
					$p2p .= $cgi->Tr(
							$cgi->td({-valign => "top",-align => "left",-class => "cico"},"$fti").
							$cgi->td({-valign => "top",-align => "left",-class => "cnam"},
								$cgi->a({-href => "$fnc?F=$F&go=$ues&C=$C&O=$O&bgdaem=1"},(($out =~ m/^\.\.$/) ? "Parent Directory":((-d "$out") ? "$out/" : "$out")))).
							$cgi->td({-valign => "top",-align => "right",-class => "clamo"},(($out =~ m/^\.\.$/) ? "" : strftime('%d-%b-%Y %H:%M',&calLocalTime($stat[9],$lag)))).
							$cgi->td({-valign => "top",-align => "right",-class => "csize"},((-d $out) ? "-" : $stat[7])).
							$cgi->td({-valign => "top",-align => "right"})
						 );
				}
			}
			if(length("$finace") == 0){
				if($f2pd ==0){
					if($out =~ m/^readme.pod$/i){# if it is a pod file extension and readme.pod
						$finace = "$out";
						$f2pd++;
					}
				}
			}
		}
		$p2p .= $cgi->Tr( $cgi->td({-valign => "top",-align => "center",-colspan => "5"},$cgi->hr()
					# . $cgi->img({-width => "50", -alt => "",-src => $HOME_URL . '/icons/_logo.png'})
				));
		if($finace =~ m/\.pod$/i){ # we print readme.pod file
			my $p = Pod::Simple::HTML->new;
			$p->output_string(\$html);
			$p->parse_file("$finace");
			#$spo++;
		}
		my $body2=$cgi->center($cgi->table({-summary => "Listings of file in current directory"},$p2p)). "\n$html"; # PID(Ajax):$$ $html";
		print "$body2";
#		&myenc("$html",$spo);
		#print $cgi->b("+++---------------oooooooooooo-----<br>");
	}else{
		#system("/usr/bin/touch popo2.0.0");
		if($finace =~ m/\.pod$/i){# we print readme.pod file
			my $p = Pod::Simple::HTML->new;
			$p->output_string(\$html);
			$p->parse_file("$finace");
			$spo++;
		}else{
			open(R,"$finace") or die("Error $!");
			my @aa = <R>;
			close(R) or die("Error $!");
			foreach (@aa){
				print "$_";
			}
			$html=" ";# fake html page
			$spo++;
		}
		&myenc("$html",$spo);
	}
}

# Updates file that prints the index if needed
sub putLink{
	my($dir) = @_;# directory to check

	#print ">>>>>>>>>$dir<<<<<br>";
	if( ! -f "$dir/$fnc"){# Checks if it is a file
		#print "case 1 copy($MY_HOME_DIR     /     $fnc,              $dir/$fnc)<br>";
		if(-f "$MY_HOME_DIR/$fnc") {
			copy("$MY_HOME_DIR/$fnc","$dir/$fnc") or die(getcwd() . " error $!");
		}else{
			copy("$fnc","$dir/$fnc") or die(getcwd() . " error $!");
		}
		chmod(0755,"$dir/$fnc");
		#if( -f "$dir/$fnc"){# Checks if it is a file
		#print "----------->ok exists<br>";
		#else{
		#print "----------->not ok exists<br>";
		#}
	}else{
		my ($buf1,$buf2,$buf3) = ();# buffers for signatures
		#print "case 2<br>";
		my $fd = POSIX::open("$fnc",&POSIX::O_RDONLY) or die("Error $!");
		@stat = POSIX::fstat($fd);# gets its content
		my $res1 = POSIX::read($fd,$buf1,$stat[7]);
		POSIX::close($fd) or die("Error $!");
		my $fd2 = POSIX::open("$dir/$fnc",&POSIX::O_RDONLY) or die("Error $!");
		my @stat2 = POSIX::fstat($fd2);# gets its content
		my $res2 = POSIX::read($fd2,$buf2,$stat2[7]);
		POSIX::close($fd2) or die("Error $!");
		my $fd3 = POSIX::open("$dir/$fnc",&POSIX::O_RDONLY) or die("Error $!");
		my @stat3 = POSIX::fstat($fd3);# gets its content
		my $res3 = POSIX::read($fd3,$buf3,$stat3[7]);
		POSIX::close($fd3) or die("Error $!");

		if($stat[9]>$stat2[9]){
			#print "case 2.1<br>";
			if($buf2 =~ m/\r{0,1}\n# -------- MY CODE DO NOT REMOVE THIS LINE ------\r{0,1}\n/){
				#print "case 2.2<br>";
				if(-f "$dir/$fnc") {
					#open(W,">err.txt");
					#print W "case 2.2.1 unlink($dir/$fnc) <br>";
					#close(W);
					unlink("$dir/$fnc") or die("Error $dir/$fnc $!");
				}
				#print "case 2.3 copy($fnc,$dir/$fnc)<br>";
				copy("$fnc","$dir/$fnc");
				chmod(0755,"$dir/$fnc");
				if("$gcd" ne "$MY_HOME_DIR"){
					if($buf3 =~ m/\r{0,1}\n# -------- MY CODE DO NOT REMOVE THIS LINE ------\r{0,1}\n/){
						if("$buf1" ne "$buf3"){
							if(-f "$MY_HOME_DIR/$fnc"){
								#print "case 2.4 unlink($MY_HOME_DIR/$fnc)<br>";
								unlink("$MY_HOME_DIR/$fnc") or die("Error $dir/$fnc $!");
							}
							#print "case 2.5 copy($fnc,$MY_HOME_DIR/$fnc)<br>";
							copy("$fnc","$MY_HOME_DIR/$fnc");
							chmod(0755,"$MY_HOME_DIR/$fnc");
						}
					}
				}
			}
		}
	}
}

# Comparison by date
sub by_date { return(stat("$a"))[9] <=> (stat("$b"))[9] }

# Comparison by size
sub by_size { return(stat($a))[7] <=> (stat($b))[7] }

# Print html page
sub myenc{
	my ($html,$spo) = @_; # html: file to print,name: provided or not
	if(length($html)>0){
		#print "----------->$spo<-----<br>";
		if($spo == 1){
			# At the end of the input with history.go(-1) tag <h1></h1> added
			# otherwith there is an indent not justified on the screen
			# when the pod page does not contain at the begening a title within <h1></h1> tag.
			print  $cgi->input({-type=>"text",-value=>"Previous/Précédent",-onclick=>"history.go(-1)"}) .  $cgi->br(). $cgi->br(). 
			$cgi->table( {-border=>"0",-width=>"100%",-background => $HOME_URL . "/icons/9197733-red-papier-peint-sans-soudure-floral-avec-des-fleurs-roses-et-des-papillons.jpg"},$cgi->Tr($cgi->td({-valign=>"bottom",-align=>"center"},$cgi->h1($cgi->font({-style=>"color: black;"},"$finace"))))
			);
		}
		my $escaped = uri_escape($html); # encode html due to carriage return
		print <<E; 
<script language="JavaScript" type="text/javascript"> 
<!--/* <![CDATA[ */ 
document.write(unescape("$escaped")); // un encode encode due to carriage return 
/* ]]> */--> 
</script> 
E
	}
}

# Calculates when to send a pull request with githubs
sub manage_repo{
	my $fd = ();
	my $buf1 = ();
	my $lim_da = DateTime->new(%lsa);# Calculates the date for last submission authorized
	my $dt2 = DateTime->now();# Gets the current date
	my $cal2 = DateTime->compare($lim_da,$dt2);# Calculates if date for submition is still authorized

	if(&checkIfNotRunning==0){ return 0; } # Checks if githubs is running

	# ---------------------------------------------------
	# ----- Begin                                  ------
	# ----- Calculates when to launch pull request ------
	# ---------------------------------------------------
	if(!-f "$MY_HOME_DIR/.sync"){
		if($cal2>=0){# checks the date for last submission authorised
			if(-f "$MY_HOME_DIR/.sync2"){
				unlink("$MY_HOME_DIR/.sync2") or die "Error $!";
			}
			print $cgi->div({-id => "github"},$cgi->div({-id => "info"},$igithub)).
			<<R;
<script type="text/javascript">
		document.getElementById('info').innerHTML='Synchronize data with github/Synchronisation des données avec github...';
</script>
R
			$fd = POSIX::open("$MY_HOME_DIR/.sync2",(&POSIX::O_WRONLY|&POSIX::O_CREAT)) or die("Error $!");
			flock($fd,LOCK_EX);
			POSIX::write($fd,"$$",length("$$"));
			POSIX::close($fd) or die("Error $!");
			$fd = POSIX::open("$MY_HOME_DIR/.sync",&POSIX::O_WRONLY|&POSIX::O_CREAT) or die("Error $MY_HOME_DIR/.sync $!");
			POSIX::write($fd,"$$",length("$$"));
			POSIX::close($fd) or die("Error $!");
			my $loc=getcwd;

			if ($loc =~ /^(.*)$/) {
				$loc=$1;
			}else{
				#die("oooooo> Variable '$loc' has invalid characters $!.\n");
				return MY_ERROR;
			}
			foreach my $ore (@lor){
				if(&git_ping("$ore")!=MY_ERROR){# checks if repository exists
					#chdir("$MY_HOME_DIR");# Save initial conf
					my $lr=(split(/\:/,$ore))[1];
					$lr=~s/(\.git)$//;
					if(!-d "$MY_HOME_DIR/$lr/.git"){# checks if repository is not already cloned
						$igithub .= $cgi->b("Cloning: $ore found on github... ".$cgi->br());
						chdir("$MY_HOME_DIR");# Save initial conf
						&git_clone("$ore","$lr");
						chdir($loc);
					}else{# Pull request on the repository
						$igithub .= $cgi->b("Updating: $ore found on github... ".$cgi->br());
						chdir($lr);
						&git_pull;
						chdir($loc);
					}
				}else{# Prints a message error
					 $igithub .= $cgi->b("Updating: $ore cannot be found on github...".$cgi->br());
				}
			}
			print $cgi->div({-id => "github"},$cgi->div({-id => "info"},$igithub)).
			<<R;
<script type="text/javascript">

	var mobile = function(){
		return {
			detect:function(){
				var uagent = navigator.userAgent.toLowerCase(); 
				var list = this.mobiles;
				var ismobile = false;
				for(var d=0;d<list.length;d+=1){
					if(uagent.indexOf(list[d])!=-1){
						ismobile = true;
					}
				}
				return ismobile;
			},
			mobiles:[
				"midp","240x320","blackberry","netfront","nokia","panasonic",
				"portalmmm","sharp","sie-","sonyericsson","symbian",
				"windows ce","benq","mda","mot-","opera mini",
				"philips","pocket pc","sagem","samsung","sda",
				"sgh-","vodafone","xda","palm","iphone",
				"ipod","android"
			]
		};
		setTimeout(continueExecution,$timer_directory_js);// wow 1

	function continueExecution(){
		document.getElementById('github').innerHTML='';
	}
</script>
R
			if(-f "$MY_HOME_DIR/.sync2"){
				unlink("$MY_HOME_DIR/.sync2") or die "Error $!";
			}
		}
		return 0;
	}
	$fd = POSIX::open("$MY_HOME_DIR/.sync",&POSIX::O_RDONLY) or die("Error $!");
	@stat = POSIX::fstat($fd);# gets its content                
	POSIX::close($fd) or die("Error $!");
	my $dt1 = DateTime->from_epoch(epoch=>$stat[9])->add(%freq);# Adds times for next submission if it is still authorized
	my $cal = DateTime->compare($dt2,$dt1);# Checks last submition
	# ---------------------------------------------------
	# ----- End                                   -------
	# ----- Calculate when to launch pull request -------
	# ---------------------------------------------------

	if($cal2>=0){# checks the date for last submission authorised
		if(&cbu("$MY_HOME_DIR/.sync")!=MY_ERROR){# Can Be Used
			if($cal>=0){# Checks if submition can be done since last update
			print $cgi->div({-id => "github"},$cgi->div({-id => "info"},$igithub)).
			<<R;
<script type="text/javascript">
		document.getElementById('info').innerHTML='Synchronize data with github/Synchronisation des données avec github...';
	</script>
R
				my $loc=getcwd;

				if ($loc =~ /^(.*)$/) {
					$loc=$1;
				}else{
					#die("Variable '$loc' has invalid characters $!.\n");
					return MY_ERROR;
				}

				my $fd = POSIX::open("$MY_HOME_DIR/.sync",&POSIX::O_RDONLY);
				if($fd < 0){return MY_ERROR;}
				my @lstats = POSIX::fstat( $fd );
				my $res0 = POSIX::read($fd,$buf1,$lstats[7]);
				POSIX::close($fd);
				if($buf1 =~ /^(.*)$/){# error with taint otherwise
					$buf1=$1;
				}else{
					return MY_ERROR;
				}
				if(kill(0,$buf1)==0){
					# ---------------------------------------
					# Calculate the pull request or clone
					my $smoke=pipe(PIPE_R, PIPE_W);
					my $pid=fork();
					if($pid==0){ 
					        close PIPE_R;          # <-- the handle you do not need.
						select PIPE_W;
										  
						# ---------------------------------------
						# Update time to sync
						if(-f "$MY_HOME_DIR/.sync2"){
							unlink("$MY_HOME_DIR/.sync2") or die "Error $!";
						}
						$fd = POSIX::open("$MY_HOME_DIR/.sync2",&POSIX::O_WRONLY|&POSIX::O_CREAT) or die("Error $!");
						flock($fd,LOCK_EX);
						POSIX::write($fd,"$$",length("$$"));
						POSIX::close($fd) or die("Error $!");
						if(-f "$MY_HOME_DIR/.sync"){
							unlink("$MY_HOME_DIR/.sync") or die "Error $!";
						}
						$fd = POSIX::open("$MY_HOME_DIR/.sync",&POSIX::O_WRONLY|&POSIX::O_CREAT) or die("Error $!");
						flock($fd,LOCK_EX);
						POSIX::write($fd,"$$",length("$$"));
						POSIX::close($fd) or die("Error $!");
						# ---------------------------------------

						foreach my $ore (@lor){
							if(&git_ping("$ore")!=MY_ERROR){# checks if repository exists
								my $lr=(split(/\:/,$ore))[1];

								$lr=~s/(\.git)$//;
								if(!-d "$MY_HOME_DIR/$lr/.git"){# checks if repository is not already cloned
									chdir("$MY_HOME_DIR");# Save initial conf
									&git_clone("$ore","$lr");
									print PIPE_W "<li> clone $ore</li>";
									chdir($loc);
								}else{# Pull request on the repository
									chdir($lr);
									&git_pull;
									print PIPE_W "<li> pull $ore</li>";
									chdir($loc);
								}
							}else{
								print PIPE_W "<li> error $ore not found</li>";
							}
						}

						if(-f "$MY_HOME_DIR/.sync2"){
							unlink("$MY_HOME_DIR/.sync2") or die("Error $!");
						}
						exit(0);
					}else{
					#	close PIPE_W;   # <- won't be writing to it. 
					#	foreach my $ore (@lor){
					#		my $i = <PIPE_R>;
					#	}
						#print $cgi->div({-id => "github"},$cgi->div({-id => "info"},$cgi->ul($igithub)));
						#print $cgi->div({-id => "info"},$cgi->ul($igithub));
					}
					# ---------------------------------------
				}
				chdir($loc);

				print <<R;
<script type="text/javascript">
	setTimeout(continueExecution,$timer_directory_js); // wow 43
	function continueExecution(){
		document.getElementById('github').innerHTML='';
	}
</script>
R
			}
		}
	}else{
		if(-f "$MY_HOME_DIR/.sync"){
			unlink("$MY_HOME_DIR/.sync");
		}
	}
	return 0;
}

# pull request
sub git_pull{
	$ENV{PATH}="";# error with taint otherwise
	open (FH,"export PATH=/bin:/usr/local/bin/:/usr/bin/;git pull|") or die "Error $!";
	while(<FH>){}
}

# clones a repository
sub git_clone{
	my($dir,$path)=@_;
	$ENV{PATH}="";# error with taint otherwise

	open(FH,"export PATH=/bin:/usr/local/bin/:/usr/bin/;git clone $dir $path|") or die "Error $!";
	while(<FH>){}
}

# checks if repository exists otherwise MY_ERROR is returned.
sub git_ping{
	my($REPO_URL)=@_;
	my $out=0;
	$ENV{PATH}="";# error with taint otherwise

	open(FH,"export PATH=/bin:/usr/local/bin/:/usr/bin/;git ls-remote $REPO_URL|") or die "Error $!";
	while(<FH>){
		$out++;
		if($_=~m/ERROR\:/i){while(<FH>){};return MY_ERROR;}
		elsif($_=~m/ssh_exchange_identification\:/i){while(<FH>){};return ERROR_CONNEXION;}
		elsif($_=~m/ssh\: Could not resolve hostname/i){while(<FH>){};return ERROR_CONNEXION;}
		elsif($_=~m/Operation timed out/i){while(<FH>){};return ERROR_CONNEXION;}
	}
	return MY_ERROR if($out==0);# If not in the loop once then MY_ERROR is returned
	return 0;
}

# Checks if we can access to github 0 if no process is running otherwise MY_ERROR.
sub cbu{# Can be used
	my ($fil) = @_;
	my $buf1 = ();

	if(!-f "$fil"){return MY_ERROR;}# does file exists if no cannnot access to the session
	my $fd = POSIX::open("$fil",&POSIX::O_RDONLY);# we open the file
	if($fd < 0){return MY_ERROR;}# if there is a problem then  MY_ERROR
	my @lstats = POSIX::fstat( $fd );# we get all stats upon file
	my $res0 = POSIX::read($fd,$buf1,$lstats[7]);# we store the content of the file in a memory
	POSIX::close($fd);# wz close the file
	if ($res0 =~ /^(.*)$/) { $res0=$1; }# otherwise there is an error with taint
	else{ return MY_ERROR; }
	if ($buf1 =~ /^(.*)$/) { $buf1=$1; }# otherwise there is an error with taint
	else{ return MY_ERROR; }
	if($res0 !~ m/[0-9]+/){return MY_ERROR;}
	if($res0 < 0){return MY_ERROR;}
	return ( kill(1,$buf1) == 0) ? 0 : MY_ERROR;#checks if there is no process running
}


# Prints a message if github is running
sub checkIfNotRunning{
	if(-f "$MY_HOME_DIR/.sync2"){
		print $cgi->div({-id => "github"},$cgi->div({-id => "info"},"Githubs is running"));
		print <<R;
<script type="text/javascript">
	setTimeout(continueExecution,$timer_directory_js); // wow 5
	function continueExecution(){
		document.getElementById('github').innerHTML='';
	}
</script>
R
		return 0;
	}
	return 1;
}


sub calLocalTime{
	my ($t,$laggmt)=@_;
	my @rt = gmtime($t);# result time
	$rt[2] = $rt[2]+$laggmt;
	return @rt;
}

# checks the Browser and its Version
sub cBVaiV{
	my($nav,$ver)=@_;

	if($nav=~m/msie/i){
		if("$ver" lt "7.0"){
			return $cgi->div({-id => "navinfo"},$cgi->div({-id => "info"},
			"Le navigateur ($nav<7.0) n'est pas totalement compatible...".
			"<br>".
			"The browser ($nav<7.0) not fully compatible..."
			)).
			<<R;
<script type="text/javascript">
	setTimeout(continueExecution,$timer_directory_js);// wow 11
	function continueExecution(){
		document.getElementById('navinfo').innerHTML='';
	}
</script>
R
		}
	}
}

=pod

=head1 SYNOPSIS

Prints the current directory structure.

=head1 VARIABLES

Variables can be set for the web site directory (B<see below> ).

Directories are updated automaticaly (B<see below>).

The frequency of reading github can be setup(B<see below>).

Date and time of last update of the file when listed can be setup according to gmt value.

=over 4

=item Variables name and their synopsis:

=over 4

=item - $HOME_ROOT This is the directory where web site starts.

=item - $MY_HOME_DIR is where all pod files are installed.

=item - $lag is +2 that's UTC/GMT+2 (Paris France, Madrid Spain).

=item - @lor contains a repository list of address from github to pull when it is permitted by %freq and, %lsa (List Of Repositories).

=item - %freq this is the FREquency of update when last submission date is not over.

=item - %lsa is the date of Last Submission Authorized.

=item - DEFAULT_FONT defines the font.

=item - DEFAULT_SIZE defines the size of characters to be printed.

=back

=back

=head1 SEE ALSO

DateTime is used to setup the following associative arrays: %freq, %lsa.

=head1 AUTHOR

Written by dorey.sebastien@laposte.net.

=cut
