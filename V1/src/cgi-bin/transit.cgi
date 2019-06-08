#!/usr/bin/perl -T

use strict;
use warnings;

use CGI;

my $doc=new CGI;
my $googid=$doc->param("googid");
my ($gmv,$prt)=split(/\-/,$doc->param("gmv")); # Gets google map version


print "Content-Type: text/html\n\n";

my $form=<<FORM;
<form id="myform" method="post" action="g${gmv}ogle.cgi">
	<input id="googid" type="hidden" value="$googid" /> 
	<input id="gmv" type="hidden" value="$gmv" /> 
</form>

<script type="text/javascript">
	document.getElementById("myform").submit();
</script>
FORM


print $form;
