#!/usr/bin/perl -wT

# +-------------------------------+
# | Dorey Sebastien               |
# | index.cgi                     |
# | Written on August 29th 2005   |
# | Last update on Sept 26th 2005 |
# +-------------------------------+

BEGIN {
    @INC = (@INC,"/usr/home/users/dorey_s/www/cgi-bin");
}

use Time::Local;
use packages::Common;
use packages::MyTime;
use CGI;

my $cgi = new CGI();
my $sid = create_short_id;
my $log_file = "loguser";
my $dir      = "../logbook";
my $log_index= "$dir/index_log.txt";
my $log_f    = "$dir/one_log.$sid.txt";
my $id_session= $cgi->param("id_session");
my $id_index = create_short_id;
my $next_page = $cgi->param("next_page");
my $menu_name = $cgi->param("menu_name");

chomp($next_page);
chomp($id_index);
chomp($id_session);

print "Content-type: text/html\n\n";

$id_session =  $dir . "/one_log." . $id_session . ".txt";
insert_info_when_index_already_created( $id_session , $menu_name);
&print_local($next_page,$id_session);

sub print_local {
    my ($page,$id) = @_;
    my ($dir,$file) =  split(/\//,$page);

    chdir($dir);
    print_file($file,$id);
}

