$VERSION    = '1.0';
$VERSION    = eval $VERSION;
@ISA    = qw( Exporter );
@EXPORT = qw( 
	     finds_directory_where_are_stored_images
	     checks_file_dependencies
	     looks_for_images_used
	    );

use constant ROOT_DEPOSIT => "../"; # To store information

=head1 FUNCTION  finds_directory_where_are_stored_images

We create a variable that stores image path for the constant DIRECTORY_DEPOSIT

=head2 PARAMETER(S)

=over 4

=over 4

None.

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

Returns directory path.

=back

=back

=head2 ERRROR RETURNED

=over 4

=over 4

-1 when no directory found for image that are already stored.

=back

=back

=head2 BUG KNOWN

=over 4

=over 4

None.

=back

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

=over 4

- I<Last modification:> Jan 04 2006

- I<Created on:> Jan 04 2006

=back

=back

=cut

sub finds_directory_where_are_stored_images {  # Begin sub finds_directory_where_are_stored_images
    my $directory_where_are_stored_imagess = ROOT_DESPOSIT;

    if ( -d "../img/" ) {             # Begin if (-d "../img/")
        return ROOT_DEPOSIT . "img/";
    }    # End if (-d "../img/")
    elsif ( -d "../image/" ) {    # Begin elsif (-d "../image")
        return ROOT_DEPOSIT . "image/";
    }    # End elsif (-d "../image")
    elsif ( -d "../images/" ) {    # Begin elsif (-d "../images")
        return ROOT_DEPOSIT . "images/";
    }    # End elsif (-d "../images")
    elsif ( -d "../Image/" ) {    # Begin elsif (-d "../Image")
        return ROOT_DEPOSIT . "image/";
    }    # End elsif (-d "../Image")
    elsif ( -d "../IMAGE/" ) {    # Begin elsif (-d "../IMAGE")
        return ROOT_DEPOSIT . "IMAGE/";
    }    # End elsif (-d "../IMAGE")
    elsif ( -d "../IMAGES" ) {    # Begin elsif (-d "../IMAGES")
        return ROOT_DEPOSIT . "IMAGES/";
    }    # End elsif (-d "../IMAGES")
    elsif ( -d "../Image" ) {    # Begin elsif (-d "../Image")
        return ROOT_DEPOSIT . "Image/";
    }    # End elsif (-d "../Image")
    elsif ( -d "../Images" ) {    # Begin elsif (-d "../Images")
        return ROOT_DEPOSIT . "Images/";
    }    # End elsif (-d "../Images")
    else {    # Begin else
           # That's the case where no directory was found under the above names.
         # Case where directory does not exist. we create a directory where all images will be stored.
         # &error_raised("can't find a directory to store images");

        mkdir( ROOT_DEPOSIT . "images/", 0755 );
        return ROOT_DEPOSIT . "images/";
    }    # End else
} # End sub finds_directory_where_are_stored_images

=head1 FUNCTION looks_for_images_used

This function check if all necessary images are stored in the path where images are stored.

=head2 PARAMETER(S)

=over 4

$application_name: give an application name

@images_used: that's the image names

=back

=head2 RETURNED VALUE

=over 4

None.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jul 24th 2006

- I<Last modification:> Mar 27 2006

- I<Last modification:> Feb 17 2006

- I<Created on:> Feb 17 2006

=back

=cut

sub looks_for_images_used {    # Begin sub looks_for_images_used
  my ($application_name,@images_used) = @_;

  if ( !-f "${application_name}/image_checked" ) {                         # Begin if (!-f "private/image_checked")
    my $counter = 0;
    print "<center><b>Checks</b>\n";
    print "</center>\n";
    print "<table>\n";
    print
      "	<tr><td align=left><font color=blue><b>Status</b></font><td align=right><font color=blue><b>Image</b></font></tr>\n";
    foreach (@images_used) {    # Begin foreach (@images_used)
      if ( -f "$_" ) {        # Begin if (-f DIRECTORY_DEPOSIT . "$_")
	$counter++;
	print
	  "	<tr><td align=left><b><font color=green>ok</font></b><td align=right>$_</tr>\n";
      }    # End if (-f DIRECTORY_DEPOSIT . "$_")
      else {    # Begin else
	print
	  "<tr><td align=left><font color=red>n'existe pas / does not exist !!!</font><b><td align=right>$_</tr>\n";
      }    # End else
    }    # End foreach (@images_used)
    print "</table>\n";
    if ( ($counter) == scalar(@images_used) ) {    # Begin if (($counter+1) == scalar(@images_used))
	open( W, ">${application_name}/image_checked" )
	  || die("Can't create ${application_name}/image_checked file $!\n");
	print W "";
	close(W);
	print "All images are present in the directory "
	  . DIRECTORY_DEPOSIT
	    . "<br>\n";
      }    # End if (($counter+1) == scalar(@images_used))
    else {    # Begin else
      exit;
    }    # End else
  }    # End if (!-f "$application_name/image_checked")
}    # End sub looks_for_images_used


=head1 FUNCTION checks_file_dependencies

This function check if all necessary images are stored in the path where images are stored.

=head2 PARAMETER(S)

=over 4

$application_name: that's application name

@file_dependencies: file are stored there.

=back

=head2 RETURNED VALUE

=over 4

None.

=back

=head2 ERRROR RETURNED

=over 4

None.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

- I<Last modification:> Jul 25 2006

- I<Created on:> Feb 17 2006

=back

=cut

sub checks_file_dependencies {    # Begin sub checks_file_dependencies
  my ($file,$application,@file_dependencies) = @_;

  if (!-f "$application/$file.ok") { # Begin if (-f "$application/check_file.ok")
    my $error = 0;
    my @files = ();

    open(W,">$application/$file") || die("$application/check_file cannot be created");
    foreach (@file_dependencies) { # Begin foreach (@file_dependencies)
      if (! -f  "$_") { # Begin if (! -f PACKAGE_DIRECTORY . "MyUtilities.pm")
	@files = (@files,$_);
	$error++;
	print W "$_ nok\n";
      }  # End if (! -f PACKAGE_DIRECTORY . "MyUtilities.pm")
      else { # Begin else
	print W "$_ ok\n";
      } # End else
    }# End foreach (@file_dependencies)
    close(W) || die("Cannot close $application/check_file");
    if ($error != 0) { # Begin if ($error != 0)
	print "Content-type: text/html\n\n";
	print "<body bkground=black>\n";
	foreach (@files) { # Begin foreach (@files)
	  print  "$_ not found<br>" ;
	} # End foreach (@files)
	exit;
    } # End if ($error != 0)
    open(W,">$application/$file.ok") || die("$application/check_file.ok cannot be created");
    open(R,"$application/$file") || die("$application/check_file cannot be read");
    foreach (<R>) { # Begin foreach (<R>)
      chomp($_);
      print W "$_\n";
    }  # End foreach (<R>)
    close(R) || die("$application/$file cannot be closed");
    close(W) || die("$application/$file.ok cannot be closed");
    unlink("$application/$file") || die("$application/$file cannot be unlinked");
  } # End if (-f "$application/check_file.ok")
}    # End sub checks_file_dependencies

1;
