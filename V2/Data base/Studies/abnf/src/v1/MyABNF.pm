package MyABNF;

require Exporter;
@ISA = qw(Exporter);
@EXPORT = qw(new set_abnf start);

my @fr=(); # Contains the file rules
my $fileabnf=();

sub new { # Begin sub new
	# implement later
} # End sub new

# -------------------------------------------------------
# Opens rule that contains grammar
# -------------------------------------------------------
sub set_abnf{ # Begin sub set_abnf
	($fileabnf)=@_;
	open(F,"<${fileabnf}")||die("Error $!\n");
	@fr=<F>; # Contains the file rules
	close(F)||die("Error $!\n");
} # End sub set_abnf

my $nolif=@fr; #  number of line(s) in the file
# -------------------------------------------------------
# End
# -------------------------------------------------------

# Parser based on rfc5234
my $irndosl=0; # is rule name defined on several lines 0=no 1=yes
# () / * =/ -
#my $cpt=0;

my $id_rn="[\<]{0,1}([a-zA-Z][\-a-zA-Z0-9]{0,})[\>]{0,1}"; # identify rule name
my $id_rn_cont="(<){1,1}([a-zA-Z][\-a-zA-Z0-9]{0,})(>){1,1}"; # identify rule name with container
my $id_rn_wd="([a-zA-Z][\-a-zA-Z0-9]{0,})"; # identify rule name without delimiter

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

my $line_with_spaces_or_tabs_only="^[\t\ ]{0,}\$";

my $line_starts_with_spaces_or_tabs_only="^[\t\ ]{0,}";

my $line_ends_with_spaces_or_tabs_only="[\t\ ]{0,}\$";

my $line_with_comments="\;.{0,}\$";

my $line_rn_tabs_or_spaces_affect="^${id_rn}[\t\ ]{0,}\={1,1}";
use data::Dumper;

my %hr=(); # Contains the definitions of the rules.
my %hrc=(); # Hash rule correspond. Contains the definitions of the rules at a corresponding id.
my %sht=(); # String Hash Table. Contains strings is some string between double cot occurs.
my %osbr=(); # Original hash Square Bracket Rules converted


my $nht=0; # number 4 hash tag
my $lnum=0; # to debug
my $orn=(); # old rule name
my($trn,$trd) = (); # t is for temporary then we declare/backup rule name,rule declaration
my($rn,$rd)=(); # rule name (rn),rule delaration (rd)

sub start{ # Begin start 
	try { # Begin try
		# -----------------------------------------------------------------
		foreach my $l (@fr){ # Begin foreach my $l (@fr)
			chomp($l); # We remove crlf at the end of the current line
			$lnum++; # We increment the number of line
			$l=~s/${line_with_spaces_or_tabs_only}//; # we clean the line
			$l=~s/${line_with_comments}//; # We remove comments
			$l=~s/${line_starts_with_spaces_or_tabs_only}//; # We clean invisible character(s) at the begining of the line
			$l=~s/${line_ends_with_spaces_or_tabs_only}//; # We clean invisible character(s) at the end of the line
			#print "\n\noooooooooooooooooooooooooooo\n";	
			if(length($l)>0){ # Begin if(length($l)>0)
				#-----------------------------------------------
				if(0){
					print "1\n";
					&pht(%hrc); #  Hash Rule Correspond: Contains the definitions of the rules at a corresponding id.
					print "2\n";
					&pht(%hr); # Contains the definitions of the rules.
					print "3\n";
					&pht(%sht); # String Hash Table. Contains strings is some string between double cot occurs.
					print "4\n";
					&pht(%osbr); # Original hash Square Bracket Rules converted 
				}
				#-----------------------------------------------

				if($l=~m/${line_rn_tabs_or_spaces_affect}/){
					# Begin if($l=~m/${line_rn_tabs_or_spaces_affect}/)
					# that's the case we have a rule name on current line
					$irndosl=0; # This line defines a rule name the value is 0=no
					$l =~ m/([^=]+)=(.+)/; # We old patterns in  $1 for rn and $2 for rd
					($rn,$rd)=&new_tupple($1,$2); # rule name,rule delaration affectation
				} # End if($l=~m/${line_rn_tabs_or_spaces_affect}/)
				elsif($l=~m/^[\t\ ]{0,}$/){ # Begin elsif($l=~m/^[\t\ ]{0,}$/)
					$irndosl=1; # This defines a rule name that is defined on several lines value is 1
			#		($rn,$rd)=&new_tupple(undef,undef); # rules not definede
					# We leave empty $rn and, $rd
				} # End elsif($l=~m/^[\t\ ]{0,}$/)
				else{ # Begin else
					$irndosl=1; # is rule name defined on several lines case yes=1 (that's an hypothesis because case create a rn and, line not empty are covered)
					$l=~m/([^=]+)/;
					($rn,$rd)=&new_tupple($rn,$1); # rule delaration affectation rn not declared that's multiple line rule declaration we keep previous value
				} # End else

				# We check the rn format
				if(defined($rn)){ # Begin if(defined($rn))
					if(!$irndosl){ # Begin if(!$irndosl)
						$rn=~s/^[\t\ ]{0,}//g;# We remove invisible chararter(s) at the begining of the string
						$rn=~s/[\t\ ]{0,}$//g;# We remove invisible chararter(s) at the end of the string

						# -----------------------------------------------
						# Begin we check if the format is well defined 
						# if not we raise an error
						# -----------------------------------------------
						if($rn !~ m/^${id_rn}$/){ # Begin if($rn !~ m/^${id_rn}$/)
							die "${fileabnf}: error at line $lnum the rule name $rn format not accepted.\n";
							#exit(-1);
						} # End if($rn !~ m/^${id_rn}$/)

						# -----------------------------------------------
						# End we check if the format is well defined 
						# if not we raise an error
						# -----------------------------------------------

						# -----------------------------------------------
						# Begin work on rule name
						# -----------------------------------------------
						$rn=~s/[\ \t]{1,}//g; # We remove consecutive invisible character(s) from $rn (we repeat it each time pattern exists)
						# we check if the rule delimiters <> are present
						if($rn!~m/^${id_rn_cont}$/){ # Begin if($rn!~m/^${id_rn_cont}$/)
							my $orn=$rn; # We save in new local memory the old version before modification
							$rn="<$rn>"; # We format the rule name wih square brackets
						} # End if($rn!~m/^${id_rn_cont}$/) 

						# We check if it is not already present/defined in the hash
						if(!exists($osbr{"$rn"})){ # Begin if(!defined($osbr{"$rn"}))
							$osbr{"$rn"}=undef; # We create the reference in the hash but body is not yet defined
						} # End if(!defined($osbr{"$rn"}))

						# -----------------------------------------------
						# End work on rule name
						# -----------------------------------------------
					} # End if(!$irndosl)
				} # End if(defined($rn))

				# We check the rd format
				if(defined($rd)){ # Begin if(defined($rd))
					# -------------------------------------------------------
					# Begin work on rule definition
					# -------------------------------------------------------

					# ------------ Begin case rd with case sensitives --------
					$rd=~s/[\ ](\%[is]\"[^\"]{1,}\")/store("$1")/eg; #  Case space (not included on purpose) then sensitive or insensitive then the string between double cot

					$rd=~s/^(\%[is]\"[^\"]{1,}\")/store("$1")/eg; # Line starts with case sensitive or insensitive then the string between double cot

					$rd=~s/(\"\%[is]\"\ {1,}\"[^\"]{1,}\")/store("$1")/eg; #  Line has a case sensitive or insensitive between a double cot followed by at least one space and, then the string between double cot

					$rd=~s/^(\"[^\"]{1,}\")/store("$1")/eg; # Line starts with a string between double cot

					$rd=~s/\ (\"[^\"]{1,}\")/store("$1")/eg; # Line has a string between double cot

					$rd=~s/[\ \t]{1,}/\ /g; # We remove consecutive invisible character(s) from $rn (we repeat it each time pattern exists)

					# ------------ End case rd with case sensitives ----------

					$rd=~s/(${id_rn_cont}) # We declare rn with delimiters <...>
					      /store_rn("$1")/xeg; # We have a string which represent in $1 a rule name (rn be already defined or not) 

					$rd=~s/[\ \/](${id_rn_wd})[\ \/] # We declare rn without delimiter <...> hence each characters can become a delimiter s.a space slash 
					      /store_rn("$1")/xeg; # We have a string which represent in $1 a rule name (rn be already defined or not) 

					$rd=~s/^(${id_rn_wd})[\/\ ]
					      /store_rn("$1")/xeg; # We have a string which represent in $1 a rule name (rn be already defined or not) 

					$rd=~s/[\/\ ](${id_rn_wd})$
					      /store_rn("$1")/xeg; # We have a string which represent in $1 a rule name (rn be already defined or not) 

					$rd=~s/^(${id_rn_wd})$
					      /store_rn("$1")/xeg; # We have a string which represent in $1 a rule name (rn be already defined or not) 

					$rd=~s/[\ \t]{1,}/ /g; # We remove consecutive invisible character from $rd and replace them with one space (we repeat it each time this pattern exists)
					$rd=~s/\>\</\> \</g; # We put space between ><
					$rd=~s/[\t\ ]+/\ /g; # We remove consecutive spaces to one space between each rules
					# -------------------------------------------------------------------
					# End work on rule definition
					# -------------------------------------------------------------------
					#print "\n++++++++++++++++++++++++++++++\n";
					my $ch_err=""; # Checks error if there is an error while parsing
					foreach (split(/\ +/,$rd)){ # Begin foreach (split(/\ +/,$rd))
						if(length($_)>0){ # Begin if(length($_)>0)
							#print "We analyze($l): $_    " . $sht{"$_"}."\n";

							if($_=~m/\_\={2,2}[a-zA-Z]+\={2,2}\_/){ # Begin if($_=~m/\_\={2,2}[a-zA-Z]+\={2,2}\_/)
								if(!defined($sht{"$_"})){
									$ch_err="$_";
									last;
								}
							} # End if($_=~m/\_\={2,2}[a-zA-Z]+\={2,2}\_/)
							elsif($_=~m/${id_rn_cont}/){ # Begin elsif($_=~m/${id_rn_cont}/)
							} # End elsif($_=~m/${id_rn_cont}/)
							elsif($_=~m/\//){ # Begin elsif($_=~m/\//)
							} # End elsif($_=~m/\//)
							else{ # Begin else
								$ch_err="$_";
								last;
							} # End else
						} # End if(length($_)>0)
					} # End foreach (split(/\ +/,$rd))
					if(length("$ch_err")>0){ # Begin if(length("$ch_err")>0)
						die("${fileabnf}: error at line $lnum $ch_err not well defined.\n");
					} # End if(length("$ch_err")>0)
					#print "\n================================\n";
				} # End if(defined($rd))

			# -------------------rn,rd are formated---------------------------------------------------------------------

				# With the rule name (rn) we check if it owns a reference in the hash if not we create one
				if(!defined($hrc{"$rn"})){ # Begin if(!defined($hrc{"$rn"})) we check if $coi exist
					my $coi=sprintf("%.${nolif}d_$lnum+",$nht++).$rn; # We create a reference with the rn

					$hrc{$rn}=$coi; # We affect to the hash reference with rn the corresponding reference
					$hr{$hrc{$rn}}=$rd; # We affect the rule definition
				} # End if(!defined($hrc{"$rn"}))
				else{ # Begin else
					# Case rule name already exists but its definition not created yet
					if($irndosl){ # Begin
						$hr{$hrc{$rn}}.= " $rd "; # We affect by concatenation the rule definition
					} # End
					else{ # Begin else
						# case it is defined as a rn on multipple lines to treat
						die "${fileabnf}: error at line $lnum $rn already defined.\n";
						#exit(-1);
					} # End else
					$rd=~s/[\t\ ]+/\ /g; # We remove consecutive spaces to one space between each rules
				} # End else

				# end left of =

				if(1){ # Begin stubb 1
					1;
				} # End stubb 1
				else{ # Begin stubb 2
					# Begin once formated we split rd with space character to analyze each field
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
											$m="<$m>"; # we format the rule that is not defined
											$osbr{"$m"}=" "; # We create reference in the hash
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
					# End case if line is not empty
				} # end stubb 2
			} # Begin if(length($l)>0)
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
			my ($n,$tg)=split(/\+/,$l);# n: name of the rule,$tg: definition of the rule

			if($tg!~ m/\<\_\=\=[a-zA-Z]{1,}\=\=\_\>/){ # Begin if($tg!~ m/\<\_\=\=[a-zA-Z]{1,}\=\=\_\>/)
				if($tg !~ m/^${id_rn}$/){ # Begin if($rn !~ m/^${id_rn}$/)
					$l=~m/^.*\_([0-9]+)\+/;
					die "${fileabnf}: error at line $1 the rule name $tg format not accepted.\n";
					#exit(-1);
				} # End if($rn !~ m/^${id_rn}$/)
			} # End if($tg!~ m/\<\_\=\=[a-zA-Z]{1,}\=\=\_\>/)

			if(length($hr{$l})==0&&$tg!~m/\_\=\=[a-zA-Z]+\=\=\_/){ # Begin if(length($hr{$l})==0&&$tg!~m/\_\=\=[a-zA-Z]+\=\=\_/)
				$l=~m/^.*\_([0-9]+)\+/;
				if(defined($osbr{$tg})){$tg=~s/[\<\>]//g;}
				die "${fileabnf}: error at line $1 $tg not defined\n";
				#exit(-1);
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

		&checks_rn;

		die "Ok, it is over\n";
	} # End try
	catch { # Begin catch
		/rule\ name.*format not accepted/ and print "$@";
		/already defined/ and print "$@";
		/Rule name.*not defined/ and print "$@";
		/not well defined/ and print "$@";
		/Ok, it is over/ and print "";
	}; # End catch
} # End start 

=head1 sub prt_store(...)

Prints the string stored in rule $tg

=head2 PARAMETER(S)

=over 4

=over 4

$v: that's the string encoded it can contain spaces. A string is defined between two ".

$tg: definition of the rule

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

Returns the content of the value.

=back

=back

=head2 ERRROR RETURNED

=over 4

=over 4

None.

=back

=back

=head2 BUG(S) KNOWN

=over 4

=over 4

None.

=back

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

=over 4

- I<Last modification:> May 13 2016

- I<Created on:> May 13 2016

=back

=back

=cut

sub prt_store{ # Begin sub prt_store
	my ($v,$tg)=@_;
	if(defined($osbr{$tg})){$tg=~s/[\<\>]//g;}
	print "\t\tString stored in rule $tg:$v-->$sht{$v}\n";
	return $sht{$v};
} # End sub prt_store

=head1 sub store_rn(...)

Store rule name used in rule definition.

=head2 PARAMETER(S)

=over 4

=over 4

$lrn: local rule name

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

Must be defined...

=back

=back

=head2 ERRROR RETURNED

=over 4

=over 4

None.

=back

=back

=head2 BUG(S) KNOWN

=over 4

=over 4

None.

=back

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

=over 4

- I<Last modification:> Dec 18 2016

- I<Created on:> May 13 2016

=back

=back

=cut

sub store_rn{ # Begin sub store_rn
	my ($lrn)= lc $1;

	$lrn=($lrn!~m/^${id_rn_wd}$/) ? "$lrn" : "<${lrn}>";
	#print "This is what we want $lrn\n";

	# We check if it is not defined if it is not we create it without defining it
	if(!defined($osbr{"$lrn"})){ # Begin if(!defined($osbr{"$lrn"}))
		$osbr{"$lrn"}=undef; # We create the reference in the hash but body is not yet defined
	} # End if(!defined($osbr{"$lrn"}))
	return " $lrn ";
} # End sub store_rn


=head1 sub store(...)

Encodes and stores the string that contains space in a hash if it exists. (need to be more prcised)

=head2 PARAMETER(S)

=over 4

=over 4

$s: string to encode

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

The string encoded.

=back

=back

=head2 ERRROR RETURNED

=over 4

=over 4

None.

=back

=back

=head2 BUG(S) KNOWN

=over 4

=over 4

None.

=back

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

=over 4

- I<Last modification:> Dec 18 2016

- I<Created on:> May 13 2016

=back

=back

=cut

sub store{ # Begin sub store
	my ($s)=@_;
	my @chars = ("A".."Z", "a".."z");
	my $string;
	my $minimum=(${nolif} > 8) ? 8 : ${nolif} ;
	my $maximum=(${nolif} < 8) ? 8 : ${nolif} ;
	my $x = $minimum + int(rand($maximum - $minimum));
	my $hi="";
	do{ # Begin do{} while(defined($sht{"$hi"}));
		$string .= $chars[rand @chars] for 1..${x};
		$hi=" _==${string}==_ ";
	}while(defined($sht{"$hi"})); # End do{} while(defined($sht{"$hi"}));

	my $ohi=$hi; # Problem for one case we need to copy and work on the copy
	$ohi=~s/^\ *//g; # Remove leading space(s)
	$ohi=~s/\ *$//g; # Remove ending space(s)
	$sht{"$ohi"}=$s;
	return $hi;
} # End sub store

=head1 sub new_tupple(...)

Creates a tupple.

=head2 PARAMETER(S)

=over 4

=over 4

@_: list of parameters

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

Tupple ($rn,$rd)

=back

=back

=head2 ERRROR RETURNED

=over 4

=over 4

None.

=back

=back

=head2 BUG(S) KNOWN

=over 4

=over 4

None.

=back

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

=over 4

- I<Last modification:> Jan 06 2017 lc $rn

- I<Last modification:> Dec 23 2016

- I<Created on:> Dec 23 2016

=back

=back

=cut

sub new_tupple{ # Begin sub new_tupple
	my($rn,$rd)=@_; # rule name (rn),rule delaration (rd)

	return (lc $rn,$rd);
} # End sub new_tupple

=head1 sub pht(...)

Prints hash table.

=head2 PARAMETER(S)

=over 4

=over 4

@_: list of parameters here hash 

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

None.

=back

=back

=head2 ERRROR RETURNED

=over 4

=over 4

None.

=back

=back

=head2 BUG(S) KNOWN

=over 4

=over 4

None.

=back

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

=over 4

- I<Last modification:> Dec 24 2016

- I<Created on:> Dec 24 2016

=back

=back

=cut


sub pht{ # Begin sub pht
	my %h=@_;
	print "key($_): value($h{$_})\n" for (keys %h);
} # End sub pht

=head1 sub checks_rn

Checks if rules exists and, are defined.

=head2 PARAMETER(S)

=over 4

=over 4

None.

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

Returns void value.

=back

=back

=head2 ERRROR RETURNED

=over 4

=over 4

Exit -1 if not rule's name exist but not defined.

=back

=back

=head2 BUG(S) KNOWN

=over 4

=over 4

None.

=back

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

=over 4

- I<Last modification:> Dec 29 2016

- I<Created on:> Dec 29 2016

=back

=back

=cut

sub checks_rn{ # Begin sub checks_rn
	for(keys %osbr){ # Begin for(keys %osbr)
		if(!defined($hrc{$_})){ # Begin if(!defined($hrc{$_}))
			die "${fileabnf}: Error rule name $_ is not defined\n";
			#exit(-1);
		} # End if(!defined($hrc{$_}))
	} # End for(keys %osbr)
	return;
} # End sub checks_rn

=head1 sub try

Within try we can raise errors with die,.... and can be catched with sub catch

=head2 PARAMETER(S)

=over 4

=over 4

The prototype.

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

None.

=back

=back

=head2 ERRROR RETURNED

=over 4

=over 4

None.

=back

=back

=head2 BUG(S) KNOWN

=over 4

=over 4

None.

=back

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

=over 4

- I<Last modification:> Jan 02sd 2017

- I<Created on:> Jan 02sd 2017

=back

=back

=cut

sub try (&@) { # Begin sub try (&@)
	my($try,$catch) = @_;
	eval { &$try };
	if ($@) { # Begin if ($@)
		local $_ = $@;
		&$catch;
	} # End if ($@)
} # End sub try (&@)

=head1 sub catch

Ctach signal from sub try 

=head2 PARAMETER(S)

=over 4

=over 4

Prototype.

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

None.

=back

=back

=head2 ERRROR RETURNED

=over 4

=over 4

None.

=back

=back

=head2 BUG(S) KNOWN

=over 4

=over 4

None.

=back

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

=over 4

- I<Last modification:> Jan 02sd 2017

- I<Created on:> Jan 02sd 2017

=back

=back

=cut

sub catch (&) { # Begin sub catch (&)
	$_[0] 
} # End sub catch (&)

#try {
	#die "phooey";
#} catch {
#/phooey/ and print "unphooey\n";
#};
1;
