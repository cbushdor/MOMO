#!/Users/sdo/perl5/perlbrew/build/perl-5.8.8/perl
#-d
#-T

use strict;
use Warnings;

use MyABNF;

&MyABNF::set_abnf("rules.abnf");
&MyABNF::start();
