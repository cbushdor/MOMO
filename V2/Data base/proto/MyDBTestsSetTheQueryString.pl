#!/usr/bin/perl

my $a=<<AA;
hello world;
AA


print $a . "\n";
&f($a);

sub f{
	my ($a)=@_;
	print $a . "\n";
}
