#!/usr/bin/perl

use threads;

print "Content-type: text/html\n\n";

$Param3 = "toto";
$thr = threads->new(\&sub1, "Param 1", "Param 2", $Param3);
#$thr = threads->new(\&sub1, @ListeDeParametres);
#$thr = threads->new(\&sub1, qw(Param1 Param2 Param3));

sub sub1 {
my @Parametres = @_;
print "Dans le thread\n";
print "Reçu les paramètres >", join("<>", @Parametres), "<\n";
}
