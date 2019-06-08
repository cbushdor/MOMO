#!/opt/local/bin/perl5.12.3 -T
##!/usr/bin/perl -T

my $MY_HOME_DIR="/srv/disk4/585431/www/dorey.agilityhoster.com/pod";
my $ALT_MY_HOME_DIR="/Users/sdo/Sites/cgi-bin";# alternative directory(ie for local debug)

# -------- MY CODE DO NOT REMOVE THIS LINE ------

my $fnc=(split(/\//,$0))[scalar(split(/\//,$0))-1];# File Name CGI

if(!-d "$MY_HOME_DIR"){
	$MY_HOME_DIR=$ALT_MY_HOME_DIR;
}

use strict;
use warnings;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use Pod::Simple::HTML;
use POSIX;
use POSIX qw/strftime/;
use MIME::Base64;

my $cgi=new CGI;
$cgi->default_dtd('html');
my $hp2p=<<S;
	th {border-bottom: thin solid black;}
	table {border-collapse: collapse;}
	td.cico {
		padding-left: 5px;
		padding-right: 5px;
	}
	td.cnam {
		padding-right: 5px;
	}
	td.lamo {padding-left: 5px;}
	td.csize {padding-left: 5px;}
	div.head{
		background-color:#00CCFF;
		-moz-border-radius:30px;
		-webkit-border-radius: 30px;

box-shadow:10px 10px 20px #000;
-webkit-box-shadow:10px 10px 20px #000;
-moz-box-shadow: 10px 10px 20px #000;

		padding: 5px 5px;
		border-color: black;
	}
S

print $cgi->header('text/html'),
	$cgi->start_html(
			-title=>'Répertoires',
			-style=>{ -code=>"$hp2p" },
			);

my $mhead=();# js, css, ...
my $mbody=();

my $cont=$cgi->param("go");# we get context must be a file name coded
chomp($cont);
my $C=$cgi->param("C");# sort directories
chomp($cont);
my $O=$cgi->param("O");# order of sort
chomp($cont);
if(length($cont)>0){$cont=decode_base64($cont);}# if var content contains a string we decode it

if(length($cont)==0){# if var content contains a string
	my $fti=""; # File Type Image
	my $f2pd=0;#File To Print Default
	my $p2p=();# page to print
	opendir REP, "." or die "Impossible to open directory"; # we open current directory
	my @direc=();
	my @files = readdir REP;# gets its content
	closedir REP;#close it
	splice(@files,0,2);
	if("$C" eq "N" && "$O" eq "A"){@files=sort @files;}
	elsif("$C" eq "N" && "$O" eq "D"){@files=reverse sort @files;}
	elsif("$C" eq "M" && "$O" eq "A"){@files=sort by_size @files;}
	elsif("$C" eq "M" && "$O" eq "D"){@files=reverse sort by_size @files;}
	elsif("$C" eq "S" && "$O" eq "A"){@files=sort by_date @files;}
	elsif("$C" eq "S" && "$O" eq "D"){@files=reverse sort by_date @files;}
	@files=(".","..",@files);
	$p2p=$cgi->Tr(
				$cgi->th({-valign=>"top",-align=>"middle"},[""]),
				$cgi->th({-valign=>"top",-align=>"middle"},[$cgi->a({-href=>"$fnc?C=N&".(("$O" eq "A") ? "O=D":"O=A")
				},"Name")]),
				$cgi->th({-valign=>"top",-align=>"middle"},[$cgi->a({-href=>"$fnc?C=M&".(("$O" eq "A") ? "O=D" : "O=A")},"Last modified")]),
				$cgi->th({-valign=>"top",-align=>"middle"},[$cgi->a({-href=>"$fnc?C=S&".(("$O" eq "A")  ? "O=D"  : "O=A")},"Size")]),
				$cgi->th({-valign=>"top",-align=>"middle"},[$cgi->a({-href=>"$fnc?C=N&".(("$O" eq "A") ? "O=D":"O=A")},"Description")]),
			);
	foreach my $out (@files){# we get ieach element of the directory
		if($out!~m/^$fnc$/){
			# ------------------------------------------------------
			# begin we associate aspecific image with the file
			if ($out=~m/^\.\.$/){$fti=$cgi->img({-src=>"/icons/back.gif"});}# its a parent directory
			elsif(-d "$out"){$fti=$cgi->img({-src=>"/icons/folder.gif"});}# its a folder
			elsif(-f "$out"){$fti=$cgi->img({-src=>"/icons/text.gif"});}# its a file
			# end we associate a specific image with the file
			# ------------------------------------------------------

			# we encode the file name
			my $eb64=encode_base64("$out");
			# treat each element but not current directory
			if($out!~m!^.$!){
				my $fd=POSIX::open("$out",&POSIX::O_RDONLY) or die("uuuuuu error $!");# we open the file
				my @stat=fstat($fd);# gets its content
				POSIX::close($fd) or die("vvvvvvvvvvvvvvvvvvv error $!");# close it
				if("$out" ne ".."){
					if(-d "$out"){
						&putLink($out);
					}
				}
				if($out!~m/\.pod$/i){# it is not a pod file
					$p2p.=$cgi->Tr(
							$cgi->td({-valign=>"top",-align=>"left",-class=>"cico"},"$fti").
							$cgi->td({-valign=>"top",-align=>"left",-class=>"cnam"},
								$cgi->a({-href=>(($out=~m/^\.\.$/) ? "../index.cgi?C=$C&O=$O" : ((-d "$out") ? "$out?C=$C&O=$O":"$out"))}	,(($out=~m/^\.\.$/) ? "Parent Directory":((-d "$out") ? "$out/" : "$out")))).
							$cgi->td({-valign=>"top",-align=>"right"-class=>"clamo"},(($out=~m/^\.\.$/) ? "" : strftime('%d-%b-%Y %H:%M',localtime($stat[9])))).
							$cgi->td({-valign=>"top",-align=>"right",-class=>"csize"},((-d $out) ? "-" : $stat[7])).
							$cgi->td({-valign=>"top",-align=>"right"})
						 );

				}else{# if it is a pod file
					$p2p.=$cgi->Tr(
							$cgi->td({-valign=>"top",-align=>"left",-class=>"cico"},"$fti").
							$cgi->td({-valign=>"top",-align=>"left",-class=>"cnam"},
								$cgi->a({-href=>"'$fnc?go=$eb64&C=$C&O=$O'"},(($out=~m/^\.\.$/) ? "Parent Directory":((-d "$out") ? "$out/" : "$out")))).
							$cgi->td({-valign=>"top",-align=>"right"-class=>"clamo"},(($out=~m/^\.\.$/) ? "" : strftime('%d-%b-%Y %H:%M',localtime($stat[9])))).
						       $cgi->td({-valign=>"top",-align=>"right",-class=>"csize"},((-d $out) ? "-" : $stat[7])).
						       $cgi->td({-valign=>"top",-align=>"right"})
						 );
				}
			}
			if(length("$cont")==0){
				if($f2pd==0){
					if($out=~m/^readme.pod$/i){# if it is a pod file extension and readme.pod
						$cont="$out";
						$f2pd++;
					}
				}
			}
		}
	}
	#$p2p.="<tr><th>&nbsp;</th><th>&nbsp;</th><th>&nbsp;</th><th>&nbsp;</th><th>&nbsp;</th></tr>\n";
	if($cont=~m/\.pod$/i){ # we print readme.pod file
		my $p = Pod::Simple::HTML->new;
		$p->output_string(\my $html);
		$p->parse_file("$cont");
#print "<body><canvas id=\"canvas\" width=\"1000\" height=\"1000\">";
#print "non supporte";
#print "</canvas></body>";
		print "\n<body class='pod'>\n"."<center><table><tr><td><div style=\"border-color:black black; border-width:5; border-style:solid\" class=\"head\">". $cgi->table($p2p) . "</div></td></tr></table></center>$html";
	}else{
		print "\n<body class='pod'>\n"."<center><table><tr><td><div style=\"border-color:black black; border-width:5; border-style:solid\" class=\"head\">". $cgi->table($p2p)."</div></td></tr></table></center>";
	}
}else{
	if($cont=~m/\.pod$/i){ # we print readme.pod file
		#print `/usr/bin/perl -MPod::Simple::HTML -e Pod::Simple::HTML::go "$cont"`;
		my $p = Pod::Simple::HTML->new;
		$p->output_string(\my $html);
		$p->parse_file("$cont");
		print "$html";
	}else{
		open(R,"$cont") or die("error $!");
		my @aa=<R>;
		close(R) or die("error $!");
		foreach (@aa){
			print "$_";
		}
	}
}

sub putLink{
	my($dir)=@_;# directory to check
	unless ($fnc =~ m#^([\w.-]+)$#){# $1 is untainted
		die "variable '$fnc' has invalid characters.\n";
	}
	$fnc = $1; 
	unless ($dir =~ m#^([\w.-]+)$#){# $1 is untainted
		die "variable '$dir' has invalid characters.\n";
	}
	$dir=$1; 
	my $dlm=(); #Date of Last Modification
	my $fd=POSIX::open("$MY_HOME_DIR/$fnc",&POSIX::O_RDONLY) or die("xxxxx error $MY_HOME_DIR/$fnc $!");
	my @stat=fstat($fd);# gets its content
	$dlm=$stat[7];# Date last modification
	POSIX::close($fd) or die("xxxxxxxxxx  error $!");
	if( ! -f "$dir/$fnc"){# Checks if it is a file
		my $retval=link("$MY_HOME_DIR/$fnc","$dir/$fnc");
	}else{
		my $buf=();
		my $fd=POSIX::open("$dir/$fnc",&POSIX::O_RDONLY) or die("error $!");
		my @stat=fstat($fd);# gets its content
		my $res=POSIX::read($fd,$buf,$stat[7]);
		POSIX::close($fd) or die("error $!");

		if($buf=~m/\r{0,1}\n# -------- MY CODE DO NOT REMOVE THIS LINE ------\r{0,1}\n/){
			print "if(\"$MY_HOME_DIR/$fnc\" ne \"$MY_HOME_DIR/$dir/$fnc\")<br>";
			if("$MY_HOME_DIR/$fnc" ne "$MY_HOME_DIR/$dir/$fnc"){
				unlink("$dir/$fnc") or die("error $dir/$fnc $!");
				my $retval=link "$MY_HOME_DIR/$fnc","$dir/$fnc";
			}
		}
	}
}

sub by_date { return (stat($a))[9] <=> (stat($b))[9] }
sub by_size { return (stat($a))[7] <=> (stat($b))[7] }
