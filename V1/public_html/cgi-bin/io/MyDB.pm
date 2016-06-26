package MyDB;

use strict;
use warnings;

# +-------------------------------+
# | MyDB.pm                       |
# | Written on Apr 2 2011         |
# +-------------------------------+

my $VERS       = '0.0';
my $REL        = '1.0';
my $VERSION    = "${VERS}.${REL}";
$VERSION    = eval $VERSION;

use constant SEP => '\|\|';
use constant ERR_FILE_DOES_NOT_EXIST => -2;
use constant ERR_COLUMN => -3;
use constant OK => 0;

my $separatorField="||";# separator between each fields names

=head1 sub new(...)

Creates a new object (constructor).

=head2 PARAMETER(S)

=over 4

=over 4

$mddb:path to data base

$myDBNa: name of the table

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

Returns the address of the new object.

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

- I<Last modification:> Apr 22 2011 documentation done

- I<Created on:> Apr 02 2011

=back

=back

=cut

sub new{ # begin sub new
	my ($class,$mddb,$myDBNa)=@_;# data base path, data base name
	my $this={};

	bless($this,$class);
	$this->{sfi}=$separatorField;# field separator in db
	$this->{ddb}=$mddb . "/" . $myDBNa;# data base path+data base file name
	$this->{ddbn}=$myDBNa;# data base name
	$this->{fna}=[];# field names initialization
	$this->{dta}=[];# data initialization
	$this->{res}=[];# data result initialization
	$this->{resTemp}=[];# data result initialization
	$this->{mqu}="";# that's the query
	return $this;
} # end sub new

=head1 sub DESTROY(...)

Destroys the object (destructor).

=head2 PARAMETER(S)

=over 4

=over 4

None.

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

- I<Last modification:> Apr 22 2011 documentation done

- I<Created on:> Apr 02 2011

=back

=back

=cut

sub DESTROY{ # begin sub DESTROY
	my ($this)=@_;

	$this=undef;
} # end sub DESTROY

=head1 sub exists(...)

Check if data base file exists.

=head2 PARAMETER(S)

=over 4

=over 4

None.

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

0 otherwise a negative value.

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

- I<Last modification:> Apr 22 2011 documentation done

- I<Created on:> Apr 02 2011

=back

=back

=cut

sub exists{ # begin sub exists
	my ($this)=@_;

	return (-f "$this->{ddb}") ? 0 : -1;
} # end sub exists


=head1 sub gfn(...)

Gets file name of DB.

=head2 PARAMETER(S)

=over 4

=over 4

None.

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

Returns the field names of DB as an array.

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

- I<Last modification:> Apr 22 2011 documentation done

- I<Created on:> Apr 02 2011

=back

=back

=cut

sub gfn{ # begin sub gfn
	my ($this)=@_;

	return @{$this->{fna}};# field names
} # end sub gfn

=head1 sub query(...)

That's the query to parse data base.
This is under construction format not specified yet.

=head2 PARAMETER(S)

=over 4

=over 4

$mqu: query.

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

Returns the fields values. First line that match.

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

- I<Last modification:> Apr 22 2011 documentation done

- I<Created on:> Apr 02 2011

=back

=back

=cut


sub query{ # begin sub query
	my ($this,$mqu)=@_;
	my ($f,$v)=();
	my ($op)=" ";

	$this->{mqu}=$mqu;# that's the query
	my @q=split(/ /,$mqu);
	my @left=();
	my @right=();
	my $first=0;
	foreach (@q){
		if($_!~m/(OR|AND)/){
			if($first==0){
				$first++;
				($f,$v)=split(/\=/,$_);
				@left=$this->getLine("$f","$v","$op");
			}else{
				($f,$v)=split(/\=/,$_);
				@right=$this->getLine("$f","$v","$op");
				if("$op" eq "AND"){
					#merge_and(@left,@right);
				}elsif("$op" eq "OR"){
					#merge_or(@left,@right);
				}
			}
		}else{
			# save operator
			$op=$_;
		}
	#	print "--->$_ oo)$f $v\n";
	}
	return $this->{dta};
} # end sub query

=head1 sub getLine(...)

That's the query to parse data base.

Must be a private method.

=head2 PARAMETER(S)

=over 4

=over 4

$fn: field name

$fv: field value

$op: operator of comparison

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

List of lines that match.

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

- I<Last modification:> Apr 22 2011 documentation done

- I<Created on:> Apr 02 2011

=back

=back

=cut

sub getLine{ # begin sub getLine
	my ($this,$fn,$fv,$op)=@_;# field name, field value, operator
	my $c=0;
	my @result=();
	my $found=-1;

	# cleaning
	while(pop(@{$this->{res}})){ 1; }

	# check for the rank in the array with th field name
	foreach (@{$this->{fna}}){
		if("$_" eq "$fn"){ $found++;last; }
		$c++;
	}

	# error if not found
	if($found<0){return ERR_COLUMN;}

	foreach my $line (@{$this->{dta}}){
		my @field=split(/\|\|/,$line);
		if("$field[$c]" eq "$fv"){
			print "pppp)$op(oooo)$fn==$field[$c] eq $fv\n";
			push @{$this->{res}},"$line";
		}
	}
	return @{$this->{res}};
} # end sub getLine


=head1 sub gdbn(...)

Gets the data base name with the path.

=head2 PARAMETER(S)

=over 4

=over 4

None.

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

Data base name with the path.

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

- I<Last modification:> Apr 22 2011 documentation done

- I<Created on:> Apr 02 2011

=back

=back

=cut


sub gdbn{ # begin sub gdbn
	my ($this)=@_;

	return $this->{ddb};# get data base name
} # end sub gdbn

=head1 sub gdbb(...)

Gets dir where data base stored

=head2 PARAMETER(S)

=over 4

=over 4

None.

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

Gets dir where data base stored

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

- I<Last modification:> Apr 22 2011 documentation done

- I<Created on:> Apr 02 2011

=back

=back

=cut

sub gddb{ # begin sub gddb
	my ($this)=@_;

	return $this->{ddb};# gets dir where data base stored
} # end sub gddb

=head1 sub load(...)

Loads data base.

=head2 PARAMETER(S)

=over 4

=over 4

None.

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

- I<Last modification:> Apr 22 2011 documentation done

- I<Created on:> Apr 02 2011

=back

=back

=cut

sub load { # begin sub load
	my ($this)=@_;
	my @fcl=();# file content loaded
	my $r=0;

	if(!-f "$this->{ddb}"){ return ERR_FILE_DOES_NOT_EXIST;}

	open(R,"$this->{ddb}") || die("$this->{ddb} $!");
	@fcl=<R>;
	close(R) || die("$this->{ddb} $!");
	foreach (split(/\|\|/,$fcl[0])){ # begin foreach (split(/\|\|/,$fcl[0]))
		push @{$this->{fna}},"$_";
	} # end foreach (split(/\|\|/,$fcl[0]))
	foreach(@fcl){ # begin foreach(@fcl)
		if($r>0){ # begin if($r>0)
			push @{$this->{dta}},"$_";
		} # end if($r>0)
		else{ # begin else
			$r++;
		} # end else
	} # end foreach(@fcl)
} # end sub load


=head1 sub toString(...)

Gets all data base as a string.

=head2 PARAMETER(S)

=over 4

=over 4

None.

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

String.

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

- I<Last modification:> Apr 22 2011 documentation done

- I<Created on:> Apr 02 2011

=back

=back

=cut

sub toString{ # begin sub toString
	my ($this)=@_;
	my $s=();

	foreach (@{$this->{fna}}){ # begin foreach (@{$this->{fna}})
		$s.="$_$this->{sfi}";
	} # end foreach (@{$this->{fna}})
	$s=~s/\|\|$//;
	foreach (@{$this->{dta}}){ # begin foreach (@{$this->{dta}})
		$s.="$_";
	} # end foreach (@{$this->{dta}})
	return $s;
} # end sub toString

=head1 sub ccn(...)

Creates column names

=head2 PARAMETER(S)

=over 4

=over 4

None.

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

Returns OK

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

- I<Last modification:> Apr 22 2011 documentation done

- I<Created on:> Apr 02 2011

=back

=back

=cut

sub ccn{ # begin sub ccn
	my ($this,@fv)=@_;

	if(scalar @fv==0){ return ERR_COLUMN ; }
	foreach (@fv){ # begin foreach (@fv)
		push @{$this->{fna}},"\U$_";
	} # end foreach (@fv)
	#push @{$this->{lines}},@{$this->{fna}};
	return OK;
} # end sub ccn

=head1 sub cfv(...)

Creates field value
Private method ?

=head2 PARAMETER(S)

=over 4

=over 4

$fna: field name

$fva: field value associated to column name

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

Gets dir where data base stored

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

- I<Last modification:> Apr 22 2011 documentation done

- I<Created on:> Apr 02 2011

=back

=back

=cut

sub cfv{ # begin sub cfv
	my ($this,$fna,$fva)=@_;# field name, field value associated to column name

	push @{$this->{fna}},[$fva];
	return OK;
} # end sub cfv


=head1 sub commit(...)

Commit to data base.

=head2 PARAMETER(S)

=over 4

=over 4

@param: verify what is param

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

OK: everything were stored well.

ERR_FILE_DOES_NOT_EXIST;

=back

=back

=head2 ERRROR RETURNED

=over 4

=over 4

ERR_FILE_DOES_NOT_EXIST;

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

- I<Last modification:> Apr 22 2011 documentation done

- I<Created on:> Apr 02 2011

=back

=back

=cut

sub commit{ # begin sub commit
	my ($this,@param)=@_;# verify what is param
	my $s=();
	
	if(scalar @param==0){ # begin if(scalar @param==0)
		if(!-f "$this->{ddb}"){ # begin if(!-f "$this->{ddb}")
			my $rank=0;
			open(W,">$this->{ddb}") || die("$this->{ddb} error $!");
			open(WF,">$this->{ddb}Data.pm") || die("$this->{ddb}Data.pm error $!");
			print WF "package $this->{ddbn}Data;\n";
			print WF "\n";
			foreach (@{$this->{fna}}){ # begin foreach (@{$this->{fna}})
				print WF "use constant FIELD_$_ => $rank;\n";
				$rank++;
				$s.="$_$this->{sfi}";
			} # end foreach (@{$this->{fna}})
			$s=~s/\|\|$//;
			print W "$s\n";
			close(W) || die("$this->{ddb} error $!");
			close(WF) || die("$this->{ddb}Data.pm error $!");
		} # end if(!-f "$this->{ddb}")
		else{ # begin else
			return ERR_FILE_DOES_NOT_EXIST;
		} # end else
	} # end if(scalar @param==0)
	return OK;
} # end sub commit

sub printQuery{ # begin sub printQuery
	my ($this,$mqu)=@_;

	if(length($this->{mqu})>0){ # begin if(length($this->{mqu})>0)
		print "$this->{mqu}";# that's the query
	} # end if(length($this->{mqu})>0)
}# end sub printQuery

1;
