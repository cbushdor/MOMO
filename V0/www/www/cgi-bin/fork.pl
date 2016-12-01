#!/usr/bin/perl -wT

if (!defined($child_pid = fork())) {
	die "Cannott fork $!";
}elsif ($child_pid) { 
	print "I am the Parent\n";
} else  {
	print "I am the Child\n";
}
