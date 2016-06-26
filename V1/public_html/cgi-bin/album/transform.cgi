#!/usr/bin/perl
# transform character upper to lower
my @o=();

&cpy("conf.file","conf.file.tt");

print "Content-Type: text/html\n\n";

foreach (@o){
	chomp($_);
	print "---->$_<br>";
	$_=~s/\|TOP\|/\|top\|/gi;
	$_=~s/\|bottom\|/\|bottom\|/gi;
	$_=~s/\|left\|/\|left\|/gi;
	$_=~s/\|right\|/\|right\|/gi;
	$_=~s/\|center\|/\|center\|/gi;
	$_=~s/\|middle\|/\|middle\|/gi;
	print "---->$_<br>";
}


open(W,">conf.file");
foreach (@o){
	print W "$_\n";
}
close(W);

sub cpy{
	my ($s,$d)=@_;
	open(R,"$s");
	@o=<R>;
	close(R);
	
	open(W,">$d");
	foreach (@o){
		print W "$_";
	}
	close(W);
}
