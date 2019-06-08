#!/usr/bin/perl

use strict;
use warnings;


print "Content-type: text/html\n\n";
print "<pre>";
opendir(my $dd,".") or die("Problem: $!");
while(my $p=readdir $dd ){ # begin while(readdir($dd))
	#chomp($_);
	&my_print($p);
	#&transform("$p");
} # end while(readdir($dd))
closedir($dd) or die("Problem: $!");
print "</pre>";

sub transform{ # begin sub transform
	my ($n)=@_;

	rename("$n","${n}_");
	# Load a file
	open(R,"${n}_") or die("Problem $!");
	my @f=<R>; 
	close(R) or die("Problem $!");
	open(W,">${n}-") or die("Problem $!");
	foreach(@f){ # begin foreach(@f)
		#print $_ . "\n";
		foreach(split(/\,/,$_)){
		# begin foreach(split(/\,/,$_))
			print W "$_\n";
		}
		# end foreach(split(/\,/,$_))
	} # end foreach(@f)
	close(W) or die("Problem $!");
} # end sub transform

sub my_print{ # begin sub my_print
	my ($n)=@_;
	my ($addr,$date,$alb,$dt,$domain,$co,$cc,$cn,$rc,$rn,$cty,$lat,$lon,$pro)=();

	$~="LOCALIZE";
	# Load a file
	open(R,"${n}") or die("Problem $!");
	my @f=<R>; 
	close(R) or die("Problem $!");
	foreach(@f){ # begin foreach(@f)
		#print $_ . "\n";
		foreach(split(/\,/,$_)){ # begin foreach(split(/\,/,$_))
			($addr,$date,$alb,$dt,$domain,$co,$cc,$cn,$rc,$rn,$cty,$lat,$lon,$pro)=split(/\#/,$_);
			write;
		}
		# end foreach(split(/\,/,$_))
	} # end foreach(@f)

	format LOCALIZE =
+-------------------------------------------------------------------------+ 
| @<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< |
$date
| @<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< |
$addr
| @<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<                 |
$co
| @<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<                 |
$cc
| @<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<                 |
$cn
| @<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<                 |
$rn
| @<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<                 |
$domain 
| @<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<                 |
$cty 
| @>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> |
$lat 
| @>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> |
$lon 
+-------------------------------------------------------------------------+ 
.

} # end sub my_print
