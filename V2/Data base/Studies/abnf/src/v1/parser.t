#!/Users/sdo/perl5/perlbrew/build/perl-5.8.8/perl

use strict;
use Warnings;

use Test::More tests => 6;

my @subs=qw(set_abnf start);
#my @file_abnf=qw(rules.abnf);


use_ok('MyABNF',@subs);
can_ok(__PACKAGE__,'set_abnf');
can_ok(__PACKAGE__,'start');

TODO:
{
	local $TODO = 'new commant not yet implemented. continuum not yet harnessed';
	ok(my $current = MyABNF->new('rules.abnf'));
	ok(my $future = MyABNF->new('rules2.abnf'));

	cmp_ok(length($current), '<' , length($future),
		'ensuring that we have added text by some day...');
}
