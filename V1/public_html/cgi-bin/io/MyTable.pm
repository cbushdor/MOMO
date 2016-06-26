package MyTable;
use strict;
use warnings;

# +-------------------------------+
# | MyTable.pm                       |
# | Written on Apr 2 2011         |
# +-------------------------------+

my $VERS       = '0.0';
my $REL        = '1.0';
my $VERSION    = "${VERS}.${REL}";
$VERSION    = eval $VERSION;

=head1 NAME

io::MyTable.pm

$VERSION=0.0.1.0

=head1 ABSTRACT

This module works with my Data Base. Prints contents of it in a friendly way.
It is highly flexifle.

=head2 LIST OF FUNCTIONS

=over 4

=over 4

new
print
put

=back

=back

=head2 HISTORY OF MODIFICATIONS

=over 4

- I<Last modification: v0.0.1.0> Jun 09 2011: documentation.

- I<Last modification: v0.0.0.0> Feb 10 2011: beginingChecks function where modif were done.

=back

=cut

=head1 sub new(...)

Constructor.

=head2 PARAMETER(S)

=over 4

=over 4

$sep: separator
@fln: fields names

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

Returns reference of new object.

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

- I<Last modification:> Feb 11 2011

- I<Created on:> Feb 11 2011

=back

=back

=cut


sub new{ # begin sub new
	my ($class,$sep,@fln)=@_; # ref;separator;fields names
	my $this={};

	bless($this,$class);
	$this->{fna}=[];# field name
	$this->{fva}=[];# field value
	$this->{fsi}=[];# field size
	$this->{sep}=$sep;# field separator
	foreach (@fln){ # begin foreach (@fln)
		chomp($_);
		push @{$this->{fna}},$_;
		push @{$this->{fsi}},length($_);
	} # end foreach (@fln)
	return $this;
} # end sub new


=head1 sub DESTROY(...)

Destructor.

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

- I<Last modification:> Feb 11 2011

- I<Created on:> Feb 11 2011

=back

=back

=cut

sub DESTROY{ # begin sub DESTROY
	my ($this)=@_;

	$this=undef;
} # end sub DESTROY


=head1 sub put(...)

Put data in the object.

=head2 PARAMETER(S)

=over 4

=over 4

$flv:field value

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

- I<Last modification:> Feb 11 2011

- I<Created on:> Feb 11 2011

=back

=back

=cut

sub put{ # begin sub put
	my ($this,$flv)=@_;# pointer,field value
	my $s=();
	my $r=0;

	foreach (split(/$this->{sep}/,$flv)){
		#print $this->{fna}[$r]."=>";
		$s.="$_||";
		if($this->{fsi}[$r]<=length($_)){
	#		print $this->{fsi}[$r]."=".length($_);
	#		print "--->";
			$this->{fsi}[$r]=length($_);
		}
#		print $this->{fsi}[$r]."=".length($_)."\n";
		$r++;
	}
	push @{$this->{fva}},$s;
} # end sub put 


=head1 sub print(...)

Prints a table all values.

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

- I<Last modification:> Jun 08 2011: update with comments, documenting.

- I<Last modification:> Feb 11 2011: nothin much than designing the structure of the table with characters.

- I<Created on:> Feb 11 2011

=back

=back

=cut

sub print{
	my ($this)=@_;# pointer,field value
	my $r=();
	my $s=();
	my $max=0;
	my $j=();

	$r=0;
	print "|";
	foreach (@{$this->{fna}}){
		my $o=$this->{fsi}[$r];
		$j.="$o ";
		foreach(1..$o){ $s.="-"; }
		$s.="+";
		printf("%-${o}s|",$_);
		$r++;
	}
	$max=length($s);
	print "\n";
	printf "+$s";
	print "\n";
	foreach my $l (@{$this->{fva}}){
		$r=0;
		print "|";
		foreach(split(/\|\|/,$l)){
			my $o=$this->{fsi}[$r];
			$j.="$o ";
			$s.="+";
			printf("%-${o}s|",$_);
			$r++;
		}
		print "\n";
	}
}

=head1 AUTHOR

Current maintainer: M. Shark Bay <shark dot b at laposte dot net>

=cut
1;
