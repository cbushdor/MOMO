#!/usr/bin/perl


print "Content-type: text/html\n\n";
print &print_number("192345");

sub print_number { # Begin sub print_number
  my ($title,$num,$dir) = @_;
  my $str = "<table><tr><td align=right valign=center>$title<td>";

  for ($i = 0; $i < length($num); $i++) { # Begin for ($i = 0; $i < length($num); $i++)
    $str .= "<td valign=bottom><img src=\"$dir".substr($num,$i,1).".gif\">\n";
  } # End for ($i = 0; $i < length($num); $i++)
  $str .= "</table>";
  return $str;
} # End sub print_number
