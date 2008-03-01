#!/usr/bin/perl

# +-------------------------------+
# | Dorey Sebastien               |
# | index.cgi                     |
# | Written on August 29th 2005   |
# | Last update on Oct 12sd 2005  |
# +-------------------------------+

BEGIN {
    @INC = (@INC,
	    "/usr/local/home/users/dorey_s/www/cgi-bin"
	    );
}

use Time::Local;
use Fcntl qw(:DEFAULT :flock);
use packages::Common;
use packages::Paranoiac;
use packages::MyDataBaseTools;

my $id_index = create_short_id;
my $log_file = "loguser";
my $dir      = "../logbook";
my $log_index= "$dir/index_log.txt";
my $log_f    = "$dir/one_log.$id_index.txt";
my $block    = "blocking_system";

#while (!-f "toto.brk") {
#    1;
#}

chomp($id_index);
print "Content-type: text/html\n\n";

if (!defined($child_pid = fork())) { # Begin if (!defined($child_pid = fork()))
    die "Cannot fork $!";
}  # End if (!defined($child_pid = fork()))
elsif ($child_pid) { # Begin elsif ($child_pid)
    if ( !&is_current_website_not_permitted ) { # Begin if ( !&is_current_website_not_permitted )
	insert_info_logfile("That's the first page","$log_file","$id_index");
	print_file("index_final.html",$id_index);
#	print "$id_index";
    } # End if (!&is_current_website_not_permitted )
    else { # Begin if (&is_current_website_not_permitted )
	print "not permitted<br><br>";
	print "<center><img src=\"image/farside.gif\"></center>\n";
    } # End if (&is_current_website_not_permitted )
} # End elsif ($child_pid)
else { # Begin else
    if (!-d "$dir") { # Begin if (!-d "$dir")
	mkdir("$dir");
    }  # End if (!-d "$dir")
    starts_daemon("$log_f","$log_index");
    send_mail('dorey_s@kwan.com','dorey_s@kwan.com',"Web report consulting of $id_index access",'as to be the list of what is consulted');
}  # End else

# Check the black list
sub is_current_website_not_permitted {
    my $current_web_site = &return_website_address_format_according_to_permission;
    
    open(READ_FILE_LOG,"$log_file") or die("$log_file not found\n");
    foreach my $i (<READ_FILE_LOG>) { # Begin foreach my $i (<READ_FILE_LOG>)
	chomp($i);
	my @line_access = split(/\*/,$i);
	if ($line_access[1] =~ m/$current_web_site/) { # Begin 	if ($line_access[1] =~ m/$current_web_site/)
	    if ($line_access[4] eq "nok") { # Begin if ($line_access[4] eq "nok") {
		close(READ_FILE_LOG);
		return (1); # ok not permitted 
	    }  # End if ($line_access[4] eq "nok") {
	    elsif ($line_access[4] eq "nallok") { # Begin  elsif ($line_access[4] eq "nallok") {
		close(READ_FILE_LOG);
		return (1); # ok not permitted 
	    }  # End elsif ($line_access[4] eq "nallok") {
	}  # End if ($line_access[1] =~ m/$current_web_site/)
    }  # End foreach my $i (<READ_FILE_LOG>)
    close(READ_FILE_LOG);
    # ok can log on website
    return (0);
}

# Return the format of current url to check
sub return_website_address_format_according_to_permission {
    my $current_web_site = $ENV{REMOTE_HOST} || $ENV{REMOTE_ADDR};
    
    open(READ_FILE_LOG,"$log_file") or die("$log_file not found\n");
    foreach my $i (<READ_FILE_LOG>) {
	chomp($i);

	if ($i =~ m/^$current_web_site$/) {
	    my $grant = (split(/\*/,$i))[4];

	    if ($grant eq "nallok") {
		close(READ_FILE_LOG);
		my @new_url = split(/\./,$current_web_site);
		return ("$new_url[0].$new_url[1].$new_url[2]"); # ok not permitted 
	    }
	}
    }
    close(READ_FILE_LOG);
    # ok can log on website
    return ($current_web_site);
}
