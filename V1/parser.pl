#!/Users/sdo/perl5/perlbrew/build/perl-5.8.8/perl 
#-d
#-T

#use strict;
#use Warnings;

# Parser based on rfc5234

# () / * =/ -
#my $cpt=0;

my $id_rn="(<){0,1}([a-zA-Z][\-a-zA-Z0-9]{0,})(>){0,1}"; # identify rule name

my $oper_concat=".";

# Definition of the alphabet
my $bin_digits="[01]{8}";# Alphabet for binary digits
my $dec_digits="(([1][0-9]{2})|([1-9][0-9])|([0-9]))";# Alphabet for decimal digits
my $hex_digits="[0-9A-Fa-f]{2}";# Alphabet for hexadecimal digits

# Definition of the base
my $bin_base='%b';# b: binary
my $hex_base='%x';# h: hexadecimal
my $dec_base='%d';# d: decimal
my $case_sensitive='%s';# s: sensitive cf rfc 7405
my $case_insensitive='%i';# i: insensitive cf rfc 7405


# definition of declaration of 
my $bin_format=<<A;
	${bin_base}${bin_digits}(${oper_concat}${bin_digits}){0,}
A
my $hex_format=<<A;
	${hex_base}${hex_digits}(${oper_concat}${hex_digits}){0,}
A
my $dec_format=<<A;
	${dec_base}${dec_digits}(${oper_concat}${dec_digits}){0,}
A

# -------------------------------------------------------
# Opens rule that contains grammar
# -------------------------------------------------------
open(F,"<rules.abnf")||die("Error $!\n");
my @fr=<F>; # Contains the file rules
close(F)||die("Error $!\n");
my $nolif=@fr; #  number of linesin the file
# -------------------------------------------------------
# End
# -------------------------------------------------------

my %hr=(); # Contains the definitions of the rules.
my %hrc=(); # Contains the definitions of the rules corresponding id.
my %sht=(); # String hash table. Contains strings is some string between double cot occurs.
my %osbr=(); # original hash (squared) bracket) rules converted

my $nht=0; # number 4 hash tag
my $lnum=0; # to debug
my $orn=(); # old rule name
foreach my $l (@fr){ # Begin foreach my $l (@fr)
	$lnum++;
	#print "$lnum\n---------------------------------------------------\n";
	$l=~s/\;.{0,}$//;
	if($l=~m/^[\t\ ]{0,}$/){ # Begin if($l=~m/^[\t\ ]{0,}$/)
	} # End if($l=~m/^[\t\ ]{0,}$/)
	else{ # Begin else
		my($trn,$trd) = (); # backup rule name,rule delaration
		# --------------------------------------------------------------------------------------
		# ---------------------------- begin of we are working on current line -----------------
		# --------------------------------------------------------------------------------------

		chomp($l);
		# Must be done two times. First time to check $rn if well formed, second time we know that rule def is well formed we can split wit space 
		if($l =~ m/([^=]+)=(.+)/){ # Begin if($l=~ m/[\t\ ]*=[\t\ ]*/)
			#my($rn,$rd)=split(/[\t\ ]{0,}\=[\t\ ]{0,}/,$l); # rule name,rule delaration
			my($rn,$rd)=($1,$2); # rule name,rule delaration
			($trn,$trd)=($1,$2); # rule name,rule delaration
			$rn=~s/^[\t\ ]{0,}//g;
			$rn=~s/[\t\ ]{0,}$//g;
			if($rn !~ m/^${id_rn}$/){ # Begin if($rn !~ m/^${id_rn}$/)
				print "Line $lnum the rule name $rn format not accepted.\n";
				exit(-1);
			} # End if($rn !~ m/^${id_rn}$/)
		} # End if($l=~ m/[\t\ ]*=[\t\ ]*/)
		#$l=~s/\ {0,}\/[\ ]{0,}/\ \/\ /g;
		#my($rn,$rd)=split(/[\t\ ]*=[\t\ ]*/,$l); # rule name,rule delaration
		my($rn,$rd)=($trn,$trd); # rule name,rule delaration
		if(length($rd)==0){
			if($l!~m/		# does not match to the regular expression
				  ^[\ \t]{0,}	# then line starts with space or tab 0 or +infinite times
				  ${id_rn}	# identify a rule name
				  [\ \t]{0,}\=	# then line starts with space or tab 0 or +infinite times followed by affecttion
				  /x){
				$rd=$rn;
				$rn=$orn; # this line belongs to the same $rule name defined line(s) before
			}
		}
		$rd=~s/((\%[is]{1,1}){0,1}\"[^\"]{0,}\")/store($1)/eg; # We have a string and we added case sensitive and insensitive cases
		$rn=~s/[\ \t]{1,}//g;
		$rd=~s/[\ \t]{1,}/ /g;

		# we check if the rule container <> is present
		if($rn!~m/^\</){ # Begin if($rn!~m/^\</)
			if($rn!~m/\>$/){ # Begin if($rn!~m/\>$/)
				if($rn!~/^\"[^\"]+\"$/){ # Begin if($rn!~/^\"[^\"]+\"$/)
					my $orn=$rn; # We save in new local memory the old version before modification
					$rn="<$rn>"; # We format the rule name wih square brackets
					# We check if it is not defined
					if(!defined($osbr{"$rn"})){ # Begin if(!defined($osbr{"$rn"}))
						$osbr{"$rn"}=" "; # We create the reference in the hash but body is not yet defined
					} # End if(!defined($osbr{"$rn"}))
					else{ # Begin else
						# We check if it is defined but not defined with the body of the rule
						if($osbr{"$rn"} !~ m/^ $/){ # Begin if($osbr{"$rn"} !~ m/^ $/)
							print "Line $lnum error rule $orn already defined\n";
							exit(-1);
						} # End if($osbr{"$rn"} !~ m/^ $/)
					} # End else
				} # End if($rn!~/^\"[^\"]+\"$/)
			} # End if($rn!~m/\>$/)
		} # End if($rn!~m/^\</)
		chomp($rn); # We remove crlf

		# -------------------------
		#     Begin Formating 
		# -------------------------
		$rd=~s/\>\</\> \</g; # We put space between ><
		$rd=~s/\ +/\ /g; # We remove consecutive spaces to one space between each rules
		# -------------------------
		#     End Formating 
		# -------------------------

		if(!defined($hrc{$rn})){ # Begin if(!defined($hrc{$rn}))
			if($rn!~/^\"[^\"]+\"$/){ # Begin if($rn!~/^\"[^\"]+\"$/)
				my $coi=sprintf("%.${nolif}d_$lnum+",$nht++).$rn;	
				#print ">>>>>>>>>>>>>>>>>>>>>$coi<<<<\n";
				$hrc{$rn}=$coi;
				$hr{$hrc{$rn}}=$rd;
			} # End if($rn!~/^\"[^\"]+\"$/)
		} # End if(!defined($hrc{$rn}))
		else{ # Begin else
			#if(length($hrc{$rn})==0){
				$hr{$hrc{$rn}}.=$rd;
			#}
		} # End else

		# end left of =

		# begin of right of =
		# From current line we add rules even if not defined yet
		foreach my $mm (split(/\ +/,$rd)){ # Begin foreach my $mm (split(/\ +/,$rd))
			my @fields=split(/[\ \t\n]{0,}\\[\ \t\n]{0,}/,$mm);
			foreach my $m(@fields){ # Begin foreach my $m(@fields)
				# match id of rule name well formed
				if($m=~m/($id_rn)/i){ # Begin if($m=~m/($id_rn)/i) 
					#print ")))))))))))))))))))))))))))))))))))))))))))))))))$m  id_rn well formed\n";
					# We check if rule exists already
					if($m!~m/^\<[^\<\>]+\>$/){ # Begin if($m!~m/^\<[^\<\>]+\>$/)
						if($m!~m/^"
							|
							(
								 (
									${bin_base} 				# That's the base for binary
									${bin_digits} 				# That's the number binary format 
									(
										${oper_concat}${bin_digits}	# That's the operatio of concatenation
									){0,}
								  )
								| (
									${hex_base} 				# That's the base for hexadecimal
									${hex_digits}				# That's the number hexadecimal format 
									(
										${oper_concat}${hex_digits}	# That's the operatio of concatenation
									){0,}
								   )
								|(
									${dec_base} 				# That's the base for decimal
									${dec_digits}				# That's the number decimal format 
									(
										${oper_concat}${dec_digits}	# That's the operatio of concatenation
									){0,}
								   )
							)
							/x
						   ){ # Begin Complex regular expression
								$m="<$m>";
								$osbr{"$m"}=" ";;
							} # End Complex regular expression
					} # End if($m!~m/^\<[^\<\>]+\>$/)
					if(!defined($hrc{$m})){ # Begin if(!defined($hrc{$m}))
						if($m!~m/^"
							|
							(
								 (
									${bin_base} 				# That's the base for binary
									${bin_digits} 				# That's the number binary format 
									(
										${oper_concat}${bin_digits}	# That's the operatio of concatenation
									){0,}
								  )
								| (
									${hex_base} 				# That's the base for hexadecimal
									${hex_digits}				# That's the number hexadecimal format 
									(
										${oper_concat}${hex_digits}	# That's the operatio of concatenation
									){0,}
								   )
								|(
									${dec_base} 				# That's the base for decimal
									${dec_digits}				# That's the number decimal format 
									(
										${oper_concat}${dec_digits}	# That's the operatio of concatenation
									){0,}
								   )
							)
							/x
						   ){ # Begin complex regexp
								my $coi=sprintf("%.${nolif}d_$lnum+",$nht++).$m;	

								$hrc{$m}=$coi;
								$hr{$hrc{$m}}="";	
						} # End complex regexp
					} # End if(!defined($hrc{$m}))
				} # End if($m=~m/($id_rn)/i) 
			} # End foreach my $m(@fields)
		} # End foreach my $mm (split(/\ +/,$rd))
		# end of right of =
		# --------------------------------------------------------------------------------------
		# ---------------------------- end of we are working on current line -------------------
		# --------------------------------------------------------------------------------------
		$orn=$rn;
	} # End else
} # End foreach my $l (@fr)

print "\n---------------------------------------------------------------------\n";
print "---------------------------------------------------------------------\n\n";

foreach my $l (sort keys %hrc){ # Begin foreach my $l (sort keys %hrc)
	print "$l ------ $hrc{$l}\n";
} # End foreach my $l (sort keys %hrc)

print "\n---------------------------------------------------------------------\n";
print "---------------------------------------------------------------------\n\n";
#print "\n==============================\n";

foreach my $l (sort keys %hr){ # Begin foreach my $l (sort keys %hr)
	my ($n,$tg)=split(/\+/,$l);

		if($tg!~ m/\<\_\=\=[a-zA-Z]{1,}\=\=\_\>/){
			if($tg !~ m/^${id_rn}$/){ # Begin if($rn !~ m/^${id_rn}$/)
				$l=~m/^.*\_([0-9]+)\+/;
				print "Line $1 the rule name $tg format not accepted.\n";
				exit(-1);
			} # End if($rn !~ m/^${id_rn}$/)
		}

	if(length($hr{$l})==0&&$tg!~m/\_\=\=[a-zA-Z]+\=\=\_/){ # Begin if(length($hr{$l})==0&&$tg!~m/\_\=\=[a-zA-Z]+\=\=\_/)
		$l=~m/^.*\_([0-9]+)\+/;
		if(defined($osbr{$tg})){$tg=~s/[\<\>]//g;}
		print "Line $1 $tg not defined\n";
		exit(-1);
	} # End  # Begin if(length($hr{$l})==0&&$tg!~m/\_\=\=[a-zA-Z]+\=\=\_/)
	else{ # Begin else
		if(defined($osbr{$tg})){$tg=~s/[\<\>]//g;}
		if($hr{$l}=~m/\_\=\=[A-Za-z]+\=\=\_/){ # Begin if($hr{$l}=~m/\_\=\=[a-zA-Z]+\=\=\_/)
			print "$tg------->$hr{$l}\n";
			print "\tWithin definition of rule $tg matches at least a string...\n";
			$hr{$l}=~s/(\_\=\=[a-zA-Z]+\=\=\_)/prt_store($1,$tg)/eg;
			print "$tg------->$hr{$l} (original formated)\n\n" if(length($hr{$l})>0);
		} # End if($hr{$l}=~m/\_\=\=[a-zA-Z]+\=\=\_/)
		else{
			print "$tg------->$hr{$l}\n\n" if(length($hr{$l})>0);
		} # End else
	} # End else
} # End foreach my $l (sort keys %hr)

print "Ok, it is over\n";

sub prt_store{ # Begin sub prt_store
	my ($v,$tg)=@_;
	if(defined($osbr{$tg})){$tg=~s/[\<\>]//g;}
	print "\t\tString stored in rule $tg:$v-->$sht{$v}\n";
	return $sht{$v};
} # End sub prt_store

sub store{ # Begin sub store
	my ($s)=@_;
	my @chars = ("A".."Z", "a".."z");
	my $string;
	my $minimum=(${nolif} > 8) ? 8 : ${nolif} ;
	my $maximum=(${nolif} < 8) ? 8 : ${nolif} ;
	my $x = $minimum + int(rand($maximum - $minimum));
	my $hi="";
	do{
		$string .= $chars[rand @chars] for 1..${x};
		$hi="_==${string}==_";
	}while(defined($sht{"$hi"}));

	$sht{"$hi"}=$s;
	return $hi;
} # End sub store
 
