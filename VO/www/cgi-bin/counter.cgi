#!/usr/bin/perl 


BEGIN {
    @INC = (@INC,"/usr/local/home/users/dorey_s/www/cgi-bin");
    @INC = (@INC,"/usr/local/home/users/dorey_s/www/cgi-bin/packages");
}

 
$my_args = $ARGV[0];
$home = ();
 
if ($my_args ne "") {
    $home = $ENV{'HOME'};
} 
 
chomp($home); 
# $home = ();
 
local $max_log_user = 5000;
 
#require "${home}/www/cgi-bin/packages/conf.file"; 
#require "${home}/www/cgi-bin/packages/counter.pl";
 
require "cgi-bin/packages/conf.file"; 
require "cgi-bin/packages/counter.pl"; 
require "cgi-bin/packages/graphMonthly.pl";
  
&parse_form; 
$remhost = $ENV{REMOTE_HOST} || $ENV{REMOTE_ADDR};
 
if ($my_args eq "") {
    $service = $input{"service"};
    $material = $input{"material"};
    $goto = $input{"goto"};
    $year_param = $input{"year"};
    $month_param = $input{"month"};
    $goto = "$goto";
#$year_param = 2004;
#$month_param = 02;
    
#$service = "show";
    
#$service = "statM";
    
} else {
    
    $service = "show";
    
    &insert_info2;
    
}
 
#$service = "material";
 
#$service = "list";
 
 
 
open(RW,">toto"); 
print RW "--->$goto"; 
close(RW); 
 
$ly = &lastYearStored("$file_stat",$ye);
 
if ($ye > $ly || !-f "$file_stat" || -z "$file_stat") {
    print "Content-type: text/html\n\n";
    print "we create a new calendar $ye $ly\n";
    &CreateCounter("$file_stat",$ye,$ly);
}
 
if ($service eq "show") { 
    &callGnuplot($root,$temporary_files,$home);
    &start_stat("$file_stat","$stat_script_monthly");
    &changeRights("$temporary_files");
} elsif ($service eq "statM") { # show stat for a given month
    print "Content-type: text/html\n\n";
    print "Created by Sebastien Dorey";
    &listMonth($file_stat,$year_param,$month_param,$ye,$mo);
} elsif ($service eq "statY") { # show stat for a given year
    open(R,"monthly.html");
    @lst = <R>;
    close(R);
    for $l (@lst) {
	$l =~ s/\_\&img\&\_/\ /g;
    }
    print "Content-type: text/html\n\n";
    &backGrounds;
    print "@lst";
} elsif ($service eq "list") { # that's the menu
    open(HH,">>loguser");
    $mydate = `date`;
    chomp($mydate);
    print HH "Menu choosen stat menuTAGLogged on $mydate by user with address $remhost\n"; 
    close(HH);
    print "Content-type: text/html\n\n";
    &printList("$temporary_files",$ye,$mo);
} elsif ($service eq "material") {
    &insert_info($remhost);
    &remove("$file_stat","$file_stat",$max_year_base,$ly,$home);
    &incremMonth($ye,$mo,"$file_stat");
    &incremMonthMaterial($ye,$mo,"$file_stat",$material);
    &banner("Patientez svp... / Wait please ...",$goto);
} else {
    &insert_info($remhost);
    &remove("$file_stat","$file_stat",$max_year_base,$ly);
    &incremMonth($ye,$mo,"$file_stat");
    &banner("Patientez svp... / Wait please ...",$goto);
}



sub backGrounds {
    
    print "";
    
    print "Who loged \n";
    
    return 0;
}

sub banner {
    local ($mess,$goto); 
    
    $mess = $_[0];
    $goto = $_[1];    
    print "Location:http://wcube.epita.fr/~dorey_s/$goto\n\n";
    return 0;
}



sub insert_info {
    my $rem_host = $_[0];
    my @l = ();
    my $max = 3;
    my $lnum = 0;
        
    open(HH_R,"loguser");
    @list_lng = HH_R; 
    close(HH_R);
        
    &shrink(@list_lng);
        
    if ($rem_host !~ m/^194.199.4/) {
	open(HH,">>loguser");	
	$mydate = `date`;	
	chomp($mydate);	
#	use Sys::Hostname;
	
#	my $address = sprintf('%s@%s', scalar getpwuid($<), hostname);
	
	print HH "Menu choosen $subject[$material-1]TAGLogged on $mydate by user with address $rem_host TAG$address\n";
	close(HH);
    }
}

sub insert_info2 {
    my @l = ();
    my $max = 3;
    my $lnum = 0;
    
    open(HH_R,"loguser");
    @list_lng = HH_R; 
    close(HH_R);

    &shrink(@list_lng);

    open(HH,">>loguser");
    $mydate = `date`;
    chomp($mydate);
    print HH " Last check on $mydate \n"; 
    close(HH);
}



# The aim of this function is cut line from the file 
# and still ave the same number of line number
sub shrink {
    my @line_file_array = @_; 
    
    $length = @line_file_array;
    if ($length > $max_log_user) { 
	my %g = &cutArray(@line_file_array) ;
	
	open(WW,"loguser");
	foreach $l (keys %g) {
	    chomp($l);
	    print WW "$g{$l}\n";
	}
	close(WW);
    } else {
# nothin' is done because there's max_log_use > 
    }
    
}

# this function set associative array from an array
sub cutArray {
    my @line_array = @_;
    my $p = 0;

    foreach my $n (@line_array) {
	if ($p != 0) {
	    $h{$p} = $line_array[$p]; 
	}
	$p++; 
    } 
    return %h;
    
}

 
