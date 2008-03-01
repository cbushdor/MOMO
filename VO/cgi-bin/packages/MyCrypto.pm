package packages::MyCrypto;

# +-------------------------------+
# | Dorey Sebastien               |
# | MyCrypt.pm                    |
# | Written     on Oct 13rd 2005  |
# | Last update on Nov  3rd 2005  |
# +-------------------------------+
  
require Exporter;

$VERSION    = '1.0';
$VERSION    = eval $VERSION;
@ISA    = qw( Exporter );
@EXPORT = qw( 
	      create_keys
	      jarriquez_423_encrypt       jarriquez_423_decrypt
	      jarriquez_givenKey_encrypt  jarriquez_givenKey_decrypt
	      );
@EXPORT_OK = qw( );

use packages::MyTime;

# Variables that are used by all functions
my @defined_alphabet             = &init_new_alphabet(32,126);
my @forbidden_characters         = ("'",'"',"&","^","?","=",'~');
my $size_of_new_defined_alphabet = @defined_alphabet;

# Create a serie of keys in order 
sub create_keys {
    return (&transform_date_to_key(get_digital_date_format));
}

# Crypt with an already formated key that is 423
# Jarriquez is the guy in the novel 'La Jangada' of Jules Vernes who discover
# this code (for sure)
sub jarriquez_423_encrypt {
    my ($sentence) = @_;
    my @key = (4,2,3);
    my $key_l = @key;
    my $encrypted_sentence = ();
    my $l = 0;
    my $i = 0;

    $sentence =~ s/[\ \*]//g;
    chomp($sentence);
    while ($l != length($sentence)) { # Begin  while ($l != length($sentence))
	my $p = substr($sentence,$l,1);
	my $value = (ord($p) + $key[$i]);

	$encrypted_sentence .= chr($value % 128);
	$i++;
	$i = $i % $key_l;
	$l++;
    } # End while ($l != length($sentence))
    return $encrypted_sentence;
}

# Crypt with a given key
sub jarriquez_givenKey_encrypt {
    my ($sentence,@key) = @_;
    my $key_l = @key;
    my $encrypted_sentence = ();
    my $length_sentence = 0;
    my $i = 0;

    chomp($sentence);
    while ($length_sentence != length($sentence)) { # Begin  while ($length_sentence != length($sentence))
	my $p = substr($sentence,$length_sentence,1);
	my $rank = &get_rank_within_new_alphabet($p,@defined_alphabet);
	my $my_ord = ($rank + $key[$i]) % $size_of_new_defined_alphabet;

	$encrypted_sentence .=  &prohibited_characters($defined_alphabet[$my_ord],@forbidden_characters);
	$i++;
	$i = $i % (($key_l == 0) ? 2 : $key_l);
	$length_sentence++;
    } # End while ($length_sentence != length($sentence))
#    $encrypted_sentence =~ s/\"/\\\"/g;
    return $encrypted_sentence;
}

# While prohibitted characters are given a new character is given instead
sub prohibited_characters {
    my ($current_char,@list_prohibitted_char) = @_;
    my @begin = @list_prohibitted_char;
    my $rank = (create_keys)[0];

    foreach (@list_prohibitted_char) { # Begin  foreach (@list_prohibitted_char)
	if (ord($current_char) == ord($_)) { # Begin if (ord($current_char) == ord($_))
	    my $char_rank = (ord($current_char)+$rank) % $size_of_new_defined_alphabet; # we use modulus in order to stay in alphabet

	    $current_char = chr($char_rank);
	    @list_prohibitted_char = @begin;
	}  # End if (ord($current_char) == ord($_))
    } # End  foreach (@list_prohibitted_char)
    return $current_char;
}

# Crypt with a given key
sub jarriquez_givenKey_decrypt {
    my ($sentence,@key) = @_;
    my $key_l = @key;
    my $decrypted_sentence = ();
    my $length_sentence = 0;
    my $i = 0;

    chomp($sentence);
    while ($length_sentence != length($sentence)) { # Begin  while ($length_sentence != length($sentence))
	my $p = substr($sentence,$length_sentence,1);
	my $rank = &get_rank_within_new_alphabet($p,@defined_alphabet);
	my $my_ord = ($rank - $key[$i]) % $size_of_new_defined_alphabet;

	$decrypted_sentence .=  $defined_alphabet[$my_ord];
	$i++;
	$i = $i % $key_l;
	$length_sentence++;
    } # End while ($length_sentence != length($sentence))

    return $decrypted_sentence;
}

# Get rank from a given char within new alphabet
sub get_rank_within_new_alphabet {
    my ($char,@alphabet) = @_;
    my $rank = 0;

    foreach (@alphabet) { # Begin foreach (@alphabet)
	if ("$char" eq "$_") { # Begin if ("$char" eq "$_")
#	    print "$char eq $_ : $rank\n";
	    return $rank;
	}  # End if ("$char" eq "$_")
	$rank++;
    } # End foreach (@alphabet)
}

# Init my alphabet
sub init_new_alphabet {
    my ($begin,$end) = @_;
    my @new_alphabet = ();
    my $forbidden_char = ord('*');

    foreach ($begin..$end) { # Begin  foreach ($begin..$end)
	if ($_ != $forbidden_char) { # Begin if ($new_char != '*')
	    @new_alphabet = (@new_alphabet,chr($_));
	} # End if ($new_char != '*')
    }  # End  foreach ($begin..$end)
    return @new_alphabet;   
}

# Decrypt with an already given key that is 423
sub jarriquez_423_decrypt {
    my ($sentence) = @_;
    my @key = (4,2,3);
    my $key_l = @key;
    my $encrypted_sentence = ();
    my $length_sentence = 0;
    my $i = 0;

    chomp($sentence);
    while ($length_sentence != length($sentence)) { # Begin while ($length_sentence != length($sentence))
	my $p = substr($sentence,$length_sentence,1);
	$encrypted_sentence .= (chr(ord($p) - $key[$i]) % $key_l);
	$i++;
	$i = $i % $key_l;
	$length_sentence++;
    } # End while ($length_sentence != length($sentence))
    return $encrypted_sentence;
}

# We transform a given date to an array  to create keys to crypt data
sub transform_date_to_key {
    my ($given_date) = @_;
    chomp($given_date);
    my ($date,$time) = split(/\ /,$given_date);
    my @my_date = split(/\//,$date);
    my @new_date = ($my_date[0],$my_date[1],substr($my_date[2],0,2) * substr($my_date[2],2,2));

    @last = (@new_date,split(/\:/,$time));
    foreach (@last) { # Begin foreach (@last)
	if ($_ == 0) { # Begin if ($_ == 0)
	    $_++;
	}  # End if ($_ == 0)
    } # End foreach (@last)
    return (@last);
}

1;
