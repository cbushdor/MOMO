#!/usr/bin/perl -w

use CGI;

my $t = new CGI;

my $toti = $t->param("url"); # "E:\images\terminator.jpg";



my $tti = &replace($toti);

print "Content-type: text/html\n\n";
print $tti . "<br>";


sub replace {
  my ($toto) = @_;

  $toto =~ s/\\/\//g;
  $toto =~ s/^[a-zA-Z]\://g;
  return $toto;
}
