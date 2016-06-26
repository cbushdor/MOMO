#!/usr/bin/perl -d
#-T

use strict;
use warnings;

my %word_reserved=(SELECT=>"SELECT",FROM=>"FROM",WHERE=>"WHERE");
my %rules=();
my ($rule,$def)=();

open(RSTRDB,"QUERY.str") or die("error $!");
foreach my $i (<RSTRDB>){
	chomp $i;
	$i=~s/\#.*//g;
	if(length($i)>0){
		($rule,$def)=split(/\:\=/,$i);
		if(defined($def)){
			$def=~s/(\<)([^\>\<]+)(\>)/$1DEF\_$2$3/g;
			$def=~s/(\>)\ *(\<)/$1$2/g;
			$rules{$rule}=$def;
		}
	}
}
close(RSTRDB) or die("error $!");

my $u=$rules{DEF_MAIN};
my $base=$u;
if($u=~m/^\</){
	$u=~s/^\<//;
	if($u=~m/\>$/){
		$u=~s/\>$//;
	}else{
		exit -1;
	}
}else{
	exit -1;
}

#my $tag=();
BEG:
	$u=~s/$u/$rules{$u}/g;
	foreach my $v (split(/\ /,$u)){
		#print "$v\n";
		if(defined($word_reserved{$v})){
		}else{
			if($v=~m/\(*\</){
				$v=~s/\({0,}\<//;
				if($v=~m/\>[\+\*]{0,1}\)*\;{0,1}/){
					$v=~s/\>[\+\*]{0,1}\)*\;{0,1}//;
					if(defined($rules{$v})){
						if(length($rules{$v})>0){
							$u=~s/\<$v\>/$rules{$v}/g;
						}else{
							print "Error rule >$rules{$v}< cannot be found\n";
							exit -1;
						}
					}
					#print "------>$u\n";
					goto BEG;
				}else{
				#	print "Error in the token $base\n";
				#	exit -1;
				}
			}else{
				#print "Error in the token $base\n";
				#exit -1;
			}
		}
	}
print "---" . $u . "\n";
foreach my $i (keys %rules){
	print "oooo)$i ------------>$rules{$i}\n";
}
