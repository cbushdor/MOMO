#!/usr/bin/perl

use strict; 
use warnings; 
use Time::HiRes qw(usleep ualarm gettimeofday tv_interval);
use io::MyTable;
my $file="FF";

if(-f "$file"){ # begin if(-f "$file")
	unlink($file);
} # end if(-f "$file")

my @res=();
my ($s,$m0,$m1)=();

# ---------------------------------------------
$m0=[gettimeofday];
@res=calc("(3+9)"); # string to analyze
check(12,@res,tv_interval($m0,[gettimeofday]));
# ---------------------------------------------

# ---------------------------------------------
$m0=[gettimeofday];
@res=calc("1-3*9-2"); # string to analyze
check(-28,@res,tv_interval($m0,[gettimeofday]));
# ---------------------------------------------

# ---------------------------------------------
$m0=[gettimeofday];
@res=calc("1+3*9-2"); # string to analyze
check(26,@res,tv_interval($m0,[gettimeofday]));
# ---------------------------------------------

# ---------------------------------------------
$m0=[gettimeofday];
@res=calc("1-3*9+2"); # string to analyze
check(-24,@res,tv_interval($m0,[gettimeofday]));
# ---------------------------------------------

# ---------------------------------------------
$m0 = [gettimeofday];
@res=calc("(1-3)*(9+2)"); # string to analyze
check(-23,@res,tv_interval($m0,[gettimeofday]));
# ---------------------------------------------

# ---------------------------------------------
$m0 = [gettimeofday];
@res=calc("(1-3)*(9+2)-1"); # string to analyze
#($s,$m1)=gettimeofday();
check(-22,@res,tv_interval($m0,[gettimeofday]));
# ---------------------------------------------

open(R,"FF");
my @fln=<R>;
close(R);
my $ta=MyTable->new( "\\|\\|",(
		"Result","Expected result","Returned result","Expression","length of the string","time"
));
foreach(@fln){
chomp($_);
$ta->put($_);
}
$ta->print;

sub calc{ # begin sub calc
	my ($mathExpr)=@_;
	my @opd=(); # Stack for operand
	my @opt=(); # Stack for operator
	my $pbeg=0; # Position at the begining
	my $pend=0; # Position at the end
	my $size=length($mathExpr); # size of string
	my $i=0;
	my $num=();
	my $c=(); # current char
	my $opt1=(); # operand
	my $opt2=(); # operand
	my $opt3=(); # operand
	my $res=(); # reduce
	my $locd1=""; # unshift operator to check precedency # reduce
	my $locd2=""; # unshift operator to check precedency # reduce

	# ------------------------------------------------------------
	# begin sanitary tests

	$mathExpr=~s/[\ ]*//g;# prune out all spaces in expression

	# Checks if expression is all right with characters used
	if($mathExpr!~m/^[()0-9]{1,}([\-\+\*\/]{1,1}[()0-9]{1,})*$/g){ # begin if($mathExpr!~m/^[0-9]{1,}([\-\+\*\/]{1,1}[0-9]{1,})*$/g)
		return ("ERR", "err: $mathExpr",$mathExpr);
	} # end if($mathExpr!~m/^[0-9]{1,}([\-\+\*\/]{1,1}[0-9]{1,})*$/g)

	# checks if some operands are sarting the expression
	if($mathExpr=~m/^[\)\*\/]*/g){ # begin if($mathExpr=~m/^[\)\*\/]*/g)
		return ("ERR","err: $mathExpr",$mathExpr);
	} # end if($mathExpr=~m/^[\)\*\/]*/g)
	if($mathExpr=~m/\(\)/g){ # begin if($mathExpr=~m/\(\)/g)
		return ("ERR","err: $mathExpr",$mathExpr);
	} # end if($mathExpr=~m/\(\)/g)
	# Counting open and close parenthesis
	$num=0;
	while($i<$size){ # begin while($i<$size)
		$c=substr($mathExpr,$i,1); # gets one character
		if($c=~m/\(/){ # begin if($c=~m/\(/)
			$num++;
		} # end if($c=~m/\(/)
		elsif($c=~m/\)/){ # begin elsif($c=~m/\)/)
			$num--;
		} # end elsif($c=~m/\)/)
		$i++;
	} # end while($i<$size)
	if($num>0){
		return ("ERR","err($num): $mathExpr",$mathExpr);
	} # end if($mathExpr!~m/^[\)\*\/]*/g)
	# end sanitary tests
	# ------------------------------------------------------------

	# ------------------------------------------------------------
	$i=0;# initialise counter
	$num="";
	while($i<$size){ # begin while($i<$size)
		$c=substr($mathExpr,$i,1); # gets one character

		# ----------------------------------------------------
		if($c=~m!\+!){ # begin if($c=~m!\+!)
			if(length($num)>0){ # begin if(length($num)>0)
				push @opd,$num; # shift number
			} # end if(length($num)>0)
			if(scalar(@opt)==0){ # begin if(scalar(@opt)==0)
				push @opt,$c; # shift operator
			} # end if(scalar(@opt)==0)
			else{ # begin else
				my $locd=pop @opt; # unshift operator to check precedency
				if($locd=~m!\*!){ # begin if($locd=~m!\*!)
					$opt1=pop @opd; # reduce
					$opt2=pop @opd; # reduce
					$res=$opt1*$opt2; # operation done

					push @opd,$res; # shift operand
					push @opt,$c; # shift operator
				} # end if($locd=~m!\*!)
				elsif($locd=~m!\/!){ # begin elsif($locd=~m!\/!)
					$opt1=pop @opd; # reduce
					$opt2=pop @opd; # reduce
					$res=$opt2/$opt1; # operation done

					push @opd,$res; # shift operand
					push @opt,$c; # shift operator
				} # end elsif($locd=~m!\/!)
				elsif($locd=~m!\+!){ # begin elsif($locd=~m!\+!)
					$opt1=pop @opd; # reduce
					$opt2=pop @opd; # reduce
					$res=$opt1+$opt2; # operation done

					push @opd,$res; # shift operand
					push @opt,$c; # shift operator
				} # end elsif($locd=~m!\+!)
				elsif($locd=~m!\-!){ # begin elsif($locd=~m!\-!)
					$opt1=pop @opd; # reduce
					$opt2=pop @opd; # reduce
					$res=$opt2-$opt1; # operation done

					push @opd,$res; # shift operand
					push @opt,$c; # shift operator
				} # end elsif($locd=~m!\-!)
				elsif($locd=~m!\(!){ # begin if($locd=~m!\(!)
		#			push @opd,$num; # shift operand
					push @opt,$locd; # shift operator
					push @opt,$c; # shift operator
				} # end if($locd=~m!\(!)
			} # end else
			$num="";
		} # end if($c=~m!\+!)
		# ----------------------------------------------------

		# ----------------------------------------------------
		elsif($c=~m!\-!){ # begin elsif($c=~m!\-!)
			if(length($num)>0){ # begin if(length($num)>0)
				push @opd,$num; # shift number
			} # end if(length($num)==0)
			if(scalar(@opt)==0){ # begin if(scalar(@opt)==0)
				push @opt,$c; # shift operator
			} # end if(scalar(@opt)==0)
			else{ # begin else
				my $locd=pop @opt; # unshift operator to check precedency # reduce
				if($locd=~m!\*!){ # begin if($locd=~m!\*!)
					$opt1=pop @opd; # reduce
					$opt2=pop @opd; # reduce
					$res=$opt1*$opt2; # operation done

					push @opd,$res; # shift operand
					push @opt,$c; # shift operator
				} # end if($locd=~m!\*!)
				elsif($locd=~m!\/!){ # begin elsif($locd=~m!\/!)
					$opt1=pop @opd; # reduce
					$opt2=pop @opd; # reduce
					$res=$opt1/$opt2;

					push @opd,$res; # shift operand
					push @opt,$c; # shift operator
				} # end elsif($locd=~m!\/!)
				elsif($locd=~m!\+!){ # begin elsif($locd=~m!\+!)
					$opt1=pop @opd; # reduce
					$opt2=pop @opd; # reduce
					$res=$opt1+$opt2; # operation done

					push @opd,$res; # shift operand
					push @opt,$c; # shift operator
				} # end elsif($locd=~m!\+!)
				elsif($locd=~m!\-!){ # begin elsif($locd=~m!\-!)
					$opt1=pop @opd; # reduce
					$opt2=pop @opd; # reduce
					$res=$opt2-$opt1; # operation done

					push @opd,$res; # shift operand
					push @opt,$c; # shift operator
				} # end elsif($locd=~m!\-!)
				elsif($locd=~m!\(!){ # begin elsif($locd=~m!\(!)
					push @opt,$locd; # shift operator
					push @opt,$c; # shift operator
				} # end elsif($locd=~m!\(!)
			} # end else
			$num="";
		} # end elsif($c=~m!\-!)
		# ----------------------------------------------------

		# ----------------------------------------------------
		elsif($c=~m!\*!){ # begin elsif($c=~m!\*!)
			if(length($num)>0){ # begin if(length($num)>0)
				push @opd,$num; # shift number
			} # end if(length($num)==0)
			if(scalar(@opt)==0){ # begin if(scalar(@opt)==0)
				push @opt,$c; # shift operator
			} # end if(scalar(@opt)==0)
			else{ # begin else
				my $locd=pop @opt; # unshift operator to check precedency # reduce
				if($locd=~m!\*!){ # begin if($locd=~m!\*!)
					$opt1=pop @opd; # reduce
					$opt2=pop @opd; # reduce
					$res=$opt1*$opt2; # operation done

					push @opd,$res; # shift operand
					push @opt,$c; # shift operator
				} # end if($locd=~m!\*!)
				elsif($locd=~m!\/!){ # begin elsif($locd=~m!\/!)
					$opt1=pop @opd; # reduce
					$opt2=pop @opd; # reduce
					$res=$opt2/$opt1; # operation done

					push @opd,$res; # shift operand
					push @opt,$c; # shift operator
				} # end elsif($locd=~m!\/!)
				elsif($locd=~m!\+!){ # begin elsif($locd=~m!\+!)
					push @opt,$locd; # shift previous operator
					push @opt,$c; # shift current operator
				} # end elsif($locd=~m!\+!)
				elsif($locd=~m!\-!){ # begin elsif($locd=~m!\-!)
					push @opt,$locd; # shift previous operator
					push @opt,$c; # shift current operator
				} # end elsif($locd=~m!\-!)
				elsif($locd=~m!\(!){ # begin elsif($locd=~m!\(!)
					push @opt,$locd; # shift operator
					push @opt,$c; # shift operator
				} # end elsif($locd=~m!\(!)
			} # end else
			$num="";
		} # end elsif($c=~m!\*!)
		# ----------------------------------------------------

		# ----------------------------------------------------
		elsif($c=~m!\/!){ # begin elsif($c=~m!\/!)
			if(length($num)>0){ # begin if(length($num)>0)
				push @opd,$num; # shift number
			} # end if(length($num)==0)
			if(scalar(@opt)==0){ # begin if(scalar(@opt)==0)
				push @opt,$c; # shift operator
			} # end if(scalar(@opt)==0)
			else{ # begin else
				my $locd=pop @opt; # unshift operator to check precedency # reduce
				if($locd=~m!\*!){ # begin if($locd=~m!\*!)
					$opt1=pop @opd; # reduce
					$opt2=pop @opd; # reduce
					$res=$opt1*$opt2; # operation done

					push @opd,$res; # shift operand
					push @opt,$c; # shift operator
				} # end if($locd=~m!\*!)
				elsif($locd=~m!\/!){ # begin elsif($locd=~m!\/!)
					$opt1=pop @opd; # reduce
					$opt2=pop @opd; # reduce
					$res=$opt1/$opt2;

					push @opd,$res; # shift operand
					push @opt,$c; # shift operator
				} # end elsif($locd=~m!\/!)
				elsif($locd=~m!\+!){ # begin elsif($locd=~m!\+!)
					push @opt,$locd; # shift previous operator
					push @opt,$c; # shift current operator
				} # end elsif($locd=~m!\+!)
				elsif($locd=~m!\-!){ # begin elsif($locd=~m!\-!)
					push @opt,$locd; # shift previous operator
					push @opt,$c; # shift current operator
				} # end elsif($locd=~m!\-!)
				elsif($locd=~m!\(!){ # begin elsif($locd=~m!\(!)
					push @opt,$locd; # shift operator
					push @opt,$c; # shift operator
				} # end elsif($locd=~m!\(!)
			} # end else
			$num="";
		} # end elsif($c=~m!\/!)
		# ----------------------------------------------------

		# ----------------------------------------------------
		elsif($c=~m!\(!){ # begin elsif($c=~m!\(!)
			if(length($num)>0){ # begin if(length($num)>0)
				push @opd,$num; # shift number
			} # end if(length($num)>0)
			if(scalar(@opt)==0){ # begin if(scalar(@opt)==0)
				push @opt,$c; # shift operator
			} # end if(scalar(@opt)==0)
			else{ # begin else
				push @opt,$c; # shift operator
			} # end else
			$num="";
		} # end elsif($c=~m!\(!)
		# ----------------------------------------------------

		# ----------------------------------------------------
		elsif($c=~m!\)!){ # begin elsif($c=~m!\)!)
			if(length($num)>0){ # begin if(length($num)>0)
				push @opd,$num; # shift number
			} # end if(length($num)>0)
			if(scalar(@opt)==0){ # begin if(scalar(@opt)==0)
				return ("ERR","err: $mathExpr",$mathExpr);
			} # end if(scalar(@opt)==0)
			else{ # begin else
				my $locd=pop @opt; # unshift operator to check precedency # reduce
				# we calculculate till ( is met
				while($locd!~m/\(/){ # begin while($locd!~m/\(/)
					if($locd=~m!\*!){ # begin if($locd=~m!\*!)
						$opt1=pop @opd; # reduce
						$opt2=pop @opd; # reduce
						$res=$opt1*$opt2; # operation done

						push @opd,$res; # shift operand
						#$opt1=pop @opt; # reduce
					} # end if($locd=~m!\*!)
					elsif($locd=~m!\/!){ # begin elsif($locd=~m!\/!)
						$opt1=pop @opd; # reduce
						$opt2=pop @opd; # reduce
						$res=$opt1/$opt2;

						push @opd,$res; # shift operand
					} # end elsif($locd=~m!\/!)
					elsif($locd=~m!\+!){ # begin elsif($locd=~m!\+!)
						$opt1=pop @opd; # reduce
						$opt2=pop @opd; # reduce
						$res=$opt1+$opt2; # operation done

						push @opd,$res; # shift operand
					} # end elsif($locd=~m!\+!)
					elsif($locd=~m!\-!){ # begin elsif($locd=~m!\-!)
						$opt1=pop @opd; # reduce
						$opt2=pop @opd; # reduce
						$res=$opt2-$opt1; # operation done

						push @opd,$res; # shift operand
					} # end elsif($locd=~m!\-!)
					$locd=pop @opt; # unshift operator to check precedency # reduce
				} # end while($locd!~m/\(/)
			} # end else
			$num="";
		} # end elsif($c=~m!\)!)
		# ----------------------------------------------------

		# ----------------------------------------------------
		else{ # begin else
			$num.="$c"; # concatenate string (number)
		} # end else
		# ----------------------------------------------------

		$i++; # go to next character
	} # end while($i<$size)

	if(length($num)!=0){
		push @opd,$num; # shift operand
	}

	my $s=scalar(@opt);
	$locd1="";
	$locd2="";
	# ----------------------------------------------------
	# flush stacks
	$opt1=$opt2="";
	$locd1=$locd2="";
	while(scalar(@opd)||scalar(@opt)){ # begin while(scalar(@opd)||scalar(@opt))
		$opt1=$opt2="";
		$opt1=pop @opd; # reduce
		$opt2=pop @opd; # reduce
		$locd1=pop @opt; # unshift operator to check precedency # reduce
		if($s==2){ # begin if($s==2)
			if($locd1=~m/[\+\-]/){ # begin if($locd1=~m/[\+\-]/)
				if(scalar(@opt)>0){
					$locd2=pop @opt; # unshift operator to check precedency # reduce
					# ----------------------------------------------------
					if($locd2=~m!\+!){ # begin if($locd2=~m!\+!)
						$opt3=pop @opd; # reduce
						$res=$opt3+$opt2;

						push @opd,$res; # shift result
						push @opd,$opt1; # shift result
						push @opt,$locd1; # shift operand
					} # end if($locd2=~m!\+!)
					# ----------------------------------------------------

					# ----------------------------------------------------
					elsif($locd2=~m!\-!){ # begin elsif($locd2=~m!\-!)
						$opt3=pop @opd; # reduce
						$res=$opt3-$opt2;

						push @opd,$res; # shift result
						push @opd,$opt1; # shift result
						push @opt,$locd1; # shift operand
					} # end elsif($locd2=~m!\-!)
					# ----------------------------------------------------
					# restablish context
					$opt1=pop @opd; # reduce
					$opt2=pop @opd; # reduce
					$locd1=pop @opt; # unshift operator to check precedency # reduce
				}
			} # end if($locd1=~m/[\+\-]/)
		} # end if($s==2)
		if(!defined($opt1)){
			return ("ERR","err:",$mathExpr);
		}
		if(!defined($opt2)){
	return ($res,"",$mathExpr);
	#		return ("ERR","err:",$mathExpr);
		}

		# ----------------------------------------------------
		if($locd1=~m!\*!){ # begin if($locd1=~m!\*!)
			$res=$opt1*$opt2;
		} # end if($locd1=~m!\*!)
		# ----------------------------------------------------

		# ----------------------------------------------------
		elsif($locd1=~m!\/!){ # begin elsif($locd1=~m!\/!)
			$res=$opt2/$opt1;
		} # end elsif($locd1=~m!\/!)
		# ----------------------------------------------------

		# ----------------------------------------------------
		elsif($locd1=~m!\+!){ # begin elsif($locd1=~m!\+!)
			$res=$opt1+$opt2;
		} # end elsif($locd1=~m!\+!)
		# ----------------------------------------------------

		# ----------------------------------------------------
		elsif($locd1=~m!\-!){ # begin elsif($locd1=~m!\-!)
			$res=$opt2-$opt1;
		} # end elsif($locd1=~m!\-!)
		# ----------------------------------------------------

		# ----------------------------------------------------
		else{ # begin else
			if(length($opt2)==0){
				$res=$opt1;
			}else{
				$res=$opt2;
			}
		} # end else
		# ----------------------------------------------------
	} # end while(scalar(@opd)||scalar(@opt))
	# ----------------------------------------------------

	if(length($res)==0){
		if(scalar(@opd)>0){
			$res=pop @opd;
		}else{
			return ("ERR","err:",$mathExpr);
		}
	}
	return ($res,"",$mathExpr);
} # end sub calc

sub check{
	my ($res,$rres,$mess,$expr,$t)=@_;#result wanted;result returned;message error if one
	my $s=length($expr);

	open(W,">>FF");
	if("$res" eq "$rres"){ # begin if("$res" eq "$rres")
		print W "OK||$res||$rres||$expr||$s||$t\n";
	} # end if("$res" eq "$rres")
	else{
		print W "BAD||$res||$rres||$expr||$s||$t\n";
	}
	close(W);
}
