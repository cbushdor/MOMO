#!/usr/bin/perl

use warnings;
use strict;
use io::MyUtilities;
my $idgoog=();

if(-f "debug"){ # Begin if(-f "debug")
	$idgoog="ABQIAAAA14j0lCov2bd1GrJ5ANl5IRTD9FXmJRh4UX7FdKnW6k9bqHlslhTnoSdkW9cwNdIa0zOXKE3zzNBZVQ";
} # end if(-f "debug")
else{ # begin else
	$idgoog=io::MyUtilities::loadFile("private/id.googlemap");	
} # end else

print "Content-type: text/html\n\n";
	print <<R;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
	<head>
		<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
		<title>Google Maps</title>
	</head>
R
	print io::MyUtilities::googHead("$idgoog");	
