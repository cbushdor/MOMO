#!/Users/sdo/perl5/perlbrew/build/perl-5.8.8/perl

use strict;
use Warnings;

my %ht4r=&parse("test_base.rules");# Hash table for rules

foreach(sort keys %ht4r){
	print "$_ : $ht4r{$_}\n";
}

sub parse{ # Begin sub parse
	my(@rul)=@_;
	my %rules=();

	open(RR, "<$rul[0]")||die("Error $!");
	my @fgr=<RR>;# already defined base grammar rules
	close(RR)||die("Error $!");
	# Open file to read

	#open(RR, "<grammar.rules")||die("Error $!");
	#my @fgr=<RR>;# store content of file file grammar rules
	#close(RR)||die("Error $!");

	my @bgr=();
	@fgr=(@fgr,@bgr);
	my $cru="";# current rules
	my $crt="";# current rules tempo
	my $cpt=0;
	my $siz='%0'.@fgr.'d'; # Get the ize of an array
	my $lin=1; # line number

	my $nfg="";# new file for grammar

	# Copy data from one file to another.
	foreach my $line (@fgr){ # Begin foreach my $line (@fgr)
		# Add space before and after '

		# We identify a string or a character
		if($line=~m/^[\t\ ]*\|/){ # Begin if($line=~m/^[\t\ ]*\|/)
			# Separator after 0 or more space(s) or tab(s) at begin the line
			chomp($nfg);
			chomp($crt);
			$line=~s/^[\t\ ]*//;# We remove thee trailers characters
			$crt.=" [$lin] $line"; # We concatenate the content of the previous line with the new line number and its content
		} # End if($line=~m/^[\t\ ]*\|/)
		elsif($line=~m/^[\t\ ]*\#.*$/){ # Begin elsif($line=~m/^[\t\ ]*\#.*$/)
			# Commented line (start with #)
		} # End elsif($line=~m/^[\t\ ]*\#.*$/)
		elsif($line=~m/^[\t\ ]*\n/){ # Begin elsif($line=~m/^[\t\ ]*\n/)
			# Empty line only new line character found after 0 or more space(s) or tab(s) at begin the line
		} # End elsif($line=~m/^[\t\ ]*\n/)
		elsif($line=~m/^[\t\ ]*(\<([A-Z](\_{0,1}[A-Z0-9]+)*)\>)/){ # Begin elsif($line=~m/^[\t\ ]*(\<([A-Z](\_{0,1}[A-Z0-9]+)*)\>)/)
			# rules used after 0 or more space(s) or tab(s) at begin the line
			$line=~s/^[\t\ ]*//;
			chomp($nfg);
			chomp($crt);
			$crt.=" [$lin] $line";
		} # End elsif($line=~m/^[\t\ ]*(\<([A-Z](\_{0,1}[A-Z0-9]+)*)\>)/)
		elsif($line=~m/^[\t\ ]*([A-Z](\_{0,1}[A-Z0-9]+)*)[\t\ ]*\:\:\=/){ # Begin elsif($line=~m/^[\t\ ]*([A-Z](\_{0,1}[A-Z0-9]+)*)[\t\ ]*\:\:\=/)
			if(length($crt)>0){ # Begin if(length($crt)>0)
				$crt=~s/\>\ *\</\>\ \</g;
				$crt=~s/\ *\|\ */\ \|\ /g;
				chomp($crt);
				my $result = sprintf("${siz}", $cpt++);
				$crt=" [$lin] ".$crt;
				my $kex=0;# Check if key exists
				foreach my $lk (keys %rules){ 
					if($lk=~m/[0-9]+\-$cru$/){
						if(length($rules{$lk})>0){
							print "Error $cru rule was already defined.\n";
							exit(-1);
						}
					}
				}
				$rules{"$result-$cru"}=$crt;
			} # End if(length($crt)>0)
			$cru=$1;
			$line=~s/^[\t\ ]*//;
			$line=~s/\ *\:\:\=\ *(.*)$/\:\:\=/g;
			my $r=$1;
			# We need to manage spaces betweeb "...." which is a string
			if($r=~m/^(")(.*)(")$/){ # Begin if($r=~m/^(")(.*)(")$/)
				my $p1=$1; my $p2=$2; my $p3=$3;

				$p2=~s/(.)/sprintf("%x",ord($1))/eg;

				#printf("oooooooooo>$p2\n");
				$r="$p1 $p2 $p3";# We add a space between the " 
				$p2=~s/([a-fA-F0-9][a-fA-F0-9])/chr(hex($1))/eg;
				#printf("oooooooooo>$p2\n");
			} # End# if($r=~m/^(")(.*)(")$/)
			elsif($r=~m/^(')(.*)(')$/){ # Begin if($r=~m/^(")(.*)(")$/)
				my $p1=$1; my $p2=$2; my $p3=$3;

				if(length($p2)!=1){
					print "Error with declaration of character. Size must be 1\n";
					exit(-1);
				}
				$p2=~s/(.)/sprintf("%x",ord($1))/eg;

				#printf("oooooooooo>$p2\n");
				$r="$p1 $p2 $p3";# We add a space between the " 
				$p2=~s/([a-fA-F0-9][a-fA-F0-9])/chr(hex($1))/eg;
				#printf("oooooooooo>$p2\n");
			} # End# if($r=~m/^(")(.*)(")$/)
			$crt="[$lin] $r";
		} # End elsif($line=~m/^[\t\ ]*([A-Z](\_{0,1}[A-Z0-9]+)*)[\t\ ]*\:\:\=/)
		else{ # Begin else
				chomp($line);
				print "Error line $lin: $line\nVerify the definition of the rule format.";
				exit(-1);
		} # End else
		$lin++;
	} # End foreach my $line (@fgr)

	if(length($crt)>0){ # Begin if(length($crt)>0)
		$crt=~s/\>\ *\</\>\</g;
		$crt=~s/\ *\|\ */\|/g;
		chomp($crt);
		my $result = sprintf("${siz}", $cpt++);
		$crt=$crt;
		my $kex=0;# Check if key exists
		foreach my $lk (keys %rules){ 
			if($lk=~m/[0-9]+\-$cru$/){
				if(length($rules{$lk})>0){
					print "Error $cru rule was already defined.\n";
					exit(-1);
				}
			}
		}
		$rules{"$result-$cru"}=$crt;
	} # End if(length($crt)>0)

	# -------------------------------------
	# * We are on definition of the rules *
	# -------------------------------------

	my $ncih=0; # next character is hexadecimal

	# Vertical (that's left side)
	foreach my $lm (sort keys %rules){ # Begin foreach my $lm (keys %rules)
		my %tmpr=%rules;
		$crt=0;

		print "OOOOOOOOOOOOOO>$lm\n";
		# Horizontal (right side value that's the core definition of the rules aka the bodys)
		foreach my $la (split(/\ +/,$rules{$lm})){ # Begin foreach my $la (split(/\ +/,$rules{$lm}))
			#print ">>>>>>>>>$la ".length($la)."\n";
			if(length($la)>0){ # Begin if(length($la)>0)
				if($la=~m/<[^\<\>+\>]/){ # Begin if($la=~m/<[^\<\>+\>]/)
					if($la!~m/\<([A-Z](\_{0,1}[A-Z0-9]+)*)\>/){ # Begin if($la!~m/\<([A-Z](\_{0,1}[A-Z0-9]+)*)\>/)
						print "Error line $cpt: '$la' cannot be defined as a rule\n";
						exit(-1);
					} # End if($la!~m/\<([A-Z](\_{0,1}[A-Z0-9]+)*)\>/)
					else{ # Begin else
						$la=~s/[\<\>]//g;
						$crt++;
					} # End else
				} # End if($la=~m/<[^\<\>+\>]/)
				else{
					print "--------$rules{$lm}------------>$la\n";
					if($la!~/["']/){
						if($rules{$lm}=~m/^\ *(\[[0-9]+\]\ *){1,2}$la\ /){
							$rules{$lm}=~s/^\ *(\[[0-9]+\]\ *){1,2}//;
							print "Error line $cpt: $la which is part of $rules{$lm} this is not a terminal rule\n";
							exit(-1);
						}
					}
					# We define a terminal rule
					if($la=~m/^[\ \t]*[a-zA-Z]([-_]{0,1}[a-zA-Z0-9]{1,})*$/){
					}
					elsif($la=~m/^["']$/){
						# We have a character or a string
						$ncih=($ncih==0)?1:0;
					}
					elsif($ncih==1){
						# We know that we have a string or a character encoded in hexadecimal
					}
					elsif($la=~m/^\[[0-9]+\]/){
						# case line number used for error location
					}
					else{
						print "Error line $cpt: $la this is not a terminal rule\n";
						exit(-1);
					}
				}
				if($la=~m/\'/){ # Begin if($la=~m/\'/)
					# case character
				}# End if($la=~m/\'/)
				elsif($la=~m/\[([1-9][0-9]*)\]/){ # Begin elsif($la=~m/\[([1-9][0-9]*)\]/)
					$cpt=$1;# current line number
				} # End elsif($la=~m/\[([1-9][0-9]*)\]/)
				elsif($crt){ # Begin elsif($crt)
					$cru=0;
					foreach my $lo (keys %tmpr){ # Begin foreach my $lo (keys %tmpr)
						if($lo=~m/\-$la$/){ # Begin if($lo=~m/\-$la$/)
							$cru++;
							last;
						} # End if($lo=~m/\-$la$/)
					} # End foreach my $lo (keys %tmpr)
					if(!$cru){ # Begin if(!$cru)
						print "Error line $cpt: $la not defined\n";
						exit(-1);
					} # End if(!$cru)
				} # End elsif($crt)
			} # End if(length($la)>0)
		} # End foreach my $la (split(/\ +/,$rules{$lm}))
	} # End foreach my $lm (keys %rules)
	return %rules;
} # End sub parse
