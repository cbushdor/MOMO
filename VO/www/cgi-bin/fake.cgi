#!/usr/bin/perl -w

# +-----------------------------+
# | Dorey Sebastien             |
# | index.cgi                   |
# | Written on August 29th 2005 |
# | Written on Sept 6th 2005    |
# +-----------------------------+

$file_log = "loguser";

my @black_list = ("194.199.4","0.0.0.0");

my $remhost = $ENV{REMOTE_HOST} || $ENV{REMOTE_ADDR};

print "Content-type: text/html\n\n";

print "momo";
print  "=====\n".&not_permitted($remhost)."\n_______\n";
