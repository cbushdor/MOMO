#!/usr/bin/perl

my $directory_for_images = "../images/";

use IO;
use constant IMAGE_NAME => "";

&starts_bar_in_progress_in_the_page;
&shows_progress_bar;


=head1 FUNCTION starts_bar_in_progress_in_the_page

This function starts in a new window the bar that creates the process in progress.

=head2 PARAMETER(S)


=over 4


None.

=back

=head2 RETURNED VALUE

=over 4

None.

=back

=head2 ERROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Mar 02 2006

- I<Last modification:> Feb 04 2005

- I<Created on:> Feb 03 2005

=back

    -------------------------------------------------------

=cut

sub starts_bar_in_progress_in_the_page { # Begin sub starts_bar_in_progress_in_the_page
    print "Content-type: text/html\n\n";
    print " <meta http-equiv=refresh content=1>\n";
    print " <body bgcolor='#18296b' text='yellow'>\n";
}  # End sub starts_bar_in_progress_in_the_page


=head1 FUNCTION sub incr

Gets the counter and then increment it and then store it in a file.

=head2 PARAMETER(S)


=over 4


None.

=back

=head2 RETURNED VALUE

=over 4

None

=back

=head2 ERROR RETURNED

=over 4

None

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Mar 02 2006

- I<Last modification:> May 04 2005

- I<Created on:> Feb 03 2005

=back

    -------------------------------------------------------

=cut

# get counter and then increment it and then store it
sub incr { # Begin sub incr
    if (-f "album/dec") { # Begin if (-f "album/dec")
	open(R,"album/dec");
	foreach (<R>) { # Begin foreach (<R>)
	    chomp($_);
	    $r = $_;
	}  # End foreach (<R>)
	close(R);
	$r++;
	open(W,">album/dec");
	print W $r;
	close(W);
    }  # End if (-f "album/dec")
    else { # Begin else 
	$r = 0;
	open(W,">album/dec");
	print W "0";
	close(W);
    }  # End else 
}  # End sub incr


=head1 FUNCTION sub gets_dec

Gets increm from file

=head2 PARAMETER(S)


=over 4


None.

=back

=head2 RETURNED VALUE

=over 4

None

=back

=head2 ERROR RETURNED

=over 4

None

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Mar 04 2006

- I<Last modification:> May 04 2005

- I<Created on:> Feb 03 2005

=back

    -------------------------------------------------------

=cut

sub gets_dec { # Begin sub gets_dec
    my $file_content = ();

    open(R,"album/dec");
    foreach (<R>) { # Begin foreach (<R>)
	chomp($_);
	$file_content = $_;
    } # End foreach (<R>)
    close(R);
    return $file_content;
}  # End sub gets_dec

=head1 FUNCTION sub shows_progress_bar

Starts the progress bar

=head2 PARAMETER(S)


=over 4


None.

=back

=head2 RETURNED VALUE

=over 4

None

=back

=head2 ERROR RETURNED

=over 4

None

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Mar 03 2006

- I<Last modification:> May 04 2005

- I<Created on:> Feb 03 2005

=back

    -------------------------------------------------------

=cut

sub shows_progress_bar { # Begin sub shows_progress_bar
    my $bar_prog = ();
    my $l = &gets_dec;
    chomp($l);
    my @num = split(/\:/,$l);

    $bar_prog = &adds_new_bar($num[1],"${directory_for_images}/" .IMAGE_NAME);
    if ($l =~ /End/) { #   Begin if ($l =~ /END/i)
	#                 Case when upload is over. Removes upload window information.
	print "Download is over bye :). Bye !!!\n<br>\n";
#	unlink("album/dec");
        sleep(3);
        &prints_bar_2();
    } # End if ($l =~ /END/i)
    elsif ($l !~ /percent/i) { #  Begin  elsif ($l =~ /\./i)
 	#                   Case when image already downloaded.
        print "Image already downloaded. Bye !!!\n<br>\n";
#        print "Please wait\n<br>$l\n";
#	unlink("album/dec");
        sleep(3);
#        &prints_bar_2();
    }  # End  elsif ($l =~ /\./i)
    else { # Begin else
	#    Case when file is being downloaded.
 	&prints_bar_1("${l}${bar_prog}");
	print $bar_prog;
    } # End else
}  # End sub shows_progress_bar


=head1 FUNCTION sub prints_bar_1

Prints the bar in progress on the screen

=head2 PARAMETER(S)


=over 4


$bar: prints information related to information downloaded.

=back

=head2 RETURNED VALUE

=over 4

None

=back

=head2 ERROR RETURNED

=over 4

None

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Mar 02 2006

- I<Last modification:> May 04 2005

- I<Created on:> Feb 03 2005

=back

    -------------------------------------------------------

=cut

sub prints_bar_1 { # Begin sub prints_bar_1
    my $bar = $_[0];

    print "$bar\n";
} # End sub prints_bar_1


=head1 FUNCTION sub prints_bar_2

Prints the bar progress on screen and remove window once finished.

=head2 PARAMETER(S)


=over 4


None.

=back

=head2 RETURNED VALUE

=over 4

None

=back

=head2 ERROR RETURNED

=over 4

None

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Mar 02 2006

- I<Last modification:> May 04 2005

- I<Created on:> Feb 03 2005

=back

    -------------------------------------------------------

=cut

sub prints_bar_2 { # Begin sub prints_bar_2
    print "<script language='javascript'>\nwindow.close();\n</script>\n";
}  # End sub prints_bar_2

=head1 FUNCTION sub adds_new_bar

Adds a new plot in bar progress menu

=head2 PARAMETER(S)


=over 4


$bar_num: that's statistics that have to be printed related to file information downloaded.

$rep_img_bar: that's the image that prints process in progress.

=back

=head2 RETURNED VALUE

=over 4

New string with image in it to print progress bar.

=back

=head2 ERROR RETURNED

=over 4

None

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Mar 02 2006

- I<Last modification:> May 04 2005

- I<Created on:> Feb 03 2005

=back

    -------------------------------------------------------

=cut

sub adds_new_bar { # Begin sub adds_new_bar 
    my ($bar_num, $rep_img_bar) = @_;
    chomp($bar_num);
    my $bar = ();
    my $i =0;	
    $bar_num =~ s/\ +//g;
    $bar_num = ((split(/\./,$bar_num))[0]);

#    $bar_num = (split(/\./,($bar_num/10)))[0];
    while ($i < $bar_num) { #  Begin while ($i < $bar_num)
	#                     We rebuild bar info each time.
	$i++;
	$bar .= "<img src='$rep_img_bar.jpg'>";
    }  # End while ($i < $bar_num)
    chomp($bar);	
    return $bar;
}  # End sub adds_new_bar

