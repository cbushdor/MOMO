#!/usr/bin/perl

use strict;
use MIME::Base64;
use CGI;
use POSIX;
use POSIX qw/strftime/;
use strict;
use File::Find ();

my $mwd=getcwd;

print "Content-Type: text/html\n\n";
print "--->$mcwd<br>";

my $fnc=(split(/\//,$0))[scalar(split(/\//,$0))-1];# File Name CGI
my $obj=new CGI;

my $cont=$obj->param("go");# we get context must be a file name coded
chomp($cont);
if(length($cont)>0){$cont=decode_base64($cont);}# if var content contains a string we decode it

#if(-f "conf"){} else{}


if(length($cont)==0){# if var content contains a string
	opendir REP, "." or die "Impossible to open directory"; # we open current directory
	my @files = readdir REP;# gets its content
	closedir REP;#close it

	my $fti=""; # File Type Image
	my $f2pd=0;#File To Print Default
	my $p2p=();# page to print
	$p2p="<style type=\"text/css\">\nth {border-bottom: thin solid black ; }\ntable { border-collapse:collapse; }\n</style>";
	$p2p.="<table>\n";
	$p2p.="<tr><th valign=top align=middle></th><th valign=top align=middle>Name</th><th valign=top align=middle>Last modified</th><th valign=top align=middle >&nbsp;Size</th><th>Description</th></tr>\n";
	foreach my $out (@files){# we get ieach element of the directory
		# ------------------------------------------------------
		# begin we associate an image
		if ($out=~m/^\.\.$/){$fti="<img src=\"/icons/back.gif\" />";}# its a parent directory
		elsif(-d "$out"){$fti="<img src=\"/icons/folder.gif\" />";}# its a folder
		elsif(-f "$out"){$fti="<img src=\"/icons/text.gif\" />";}# its a file
		# end we associate an image
		# ------------------------------------------------------

		# we encode the file name
		my $eb64=encode_base64("$out");
		# treat each element but not current directory
		if($out!~m!^.$!){
			my $fd = POSIX::open( "$out", &POSIX::O_RDONLY );# we open the file
			my @stat=fstat($fd);# gets its content
			POSIX::close($fd);# close it
			if($out!~m/\.pod$/i){# if it is a pod file
				$p2p.="<tr><td valign=top align=left>$fti</td><td valign=top align=left><a href='$out'>".
			(($out=~m/^\.\.$/) ? "Parent Directory" : $out)
			."</a></td><td valign=top align=right>". 
				(($out=~m/^\.\.$/) ? "" : strftime('%d-%b-%Y %H:%M',localtime($stat[9]))) .
				 "</td><td valign=top align=right>&nbsp;".
				 (($out=~m/^\.\.$/) ? "-" : $stat[7]) 
				 ." </td><td></td></tr>\n";
			}else{# if it is not a pod file
				$p2p.="<tr><td valign=top align=left>$fti</td><td valign=top align=left><a href='$fnc?go=$eb64'>".
				(($out=~m/^\.\.$/) ? "Parent Directory" : $out)
			."</a></td><td valign=top align=right>". 
				(($out=~m/^\.\.$/) ? "" : strftime('%d-%b-%Y %H:%M',localtime($stat[9]))) .
				 "</td><td valign=top align=right>&nbsp;".
				 (($out=~m/^\.\.$/) ? "-" : $stat[7]) 
				 ." </td><td></td></tr>\n";
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
	$p2p.="<tr><th>&nbsp;</th><th>&nbsp;</th><th>&nbsp;</th><th>&nbsp;</th><th>&nbsp;</th></tr>\n";
	$p2p.="</table>\n";
	print "$p2p";
	if($cont=~m/\.pod$/i){ # we print readme.pod file
		print `/usr/bin/perl -MPod::Simple::HTML -e Pod::Simple::HTML::go "$cont"`;
	}
}else{
	if($cont=~m/\.pod$/i){ # we print readme.pod file
		print `/usr/bin/perl -MPod::Simple::HTML -e Pod::Simple::HTML::go "$cont"`;
	}else{
		#print "--->". $cont . "<br>";
		open(R,"$cont") or die("error $!");
		my @aa=<R>;
		close(R) or die("error $!");
		foreach (@aa){
			print "$_";
		}
	}
}
 
# creates dynamic links
foreach (&myrecdir){
	if( "$_" ne "."){
		if( -f "$_/$fnc"){ unlink "$_/$fnc"; }
	}
	if( ! -f "$_/$fnc"){
		my $retval=link $fnc,"$_/$fnc";
		if( $retval == 1 ){
		}else{
			print"Error in creating link $!<br>\n";
		}
	}
}

sub myrecdir{
	my @dirs=();

	eval 'exec /usr/bin/perl -S $0 ${1+"$@"}'
		if 0; #$running_under_some_shell


	# Set the variable $File::Find::dont_use_nlink if you're using AFS,
	# since AFS cheats.

	# for the convenience of &wanted calls, including -eval statements:
	use vars qw/*name *dir *prune/;
	*name   = *File::Find::name;
	*dir    = *File::Find::dir;
	*prune  = *File::Find::prune;

	sub wanted;



	# Traverse desired filesystems
	File::Find::find({wanted => \&wanted}, '.');
	return @dirs;

	sub wanted {
		my ($dev,$ino,$mode,$nlink,$uid,$gid);

		(($dev,$ino,$mode,$nlink,$uid,$gid) = lstat($_)) &&
		-d _ &&
		(@dirs=(@dirs,$name));
	}
}
