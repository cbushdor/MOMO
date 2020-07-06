package io::gut::machine::MyFile;

# ------------------------------------------------------
q##//q#
* Created By : sdo
* File Name : MyFile.pm
* Creation Date : Wed Aug 20 22:51:08 2008
* @modify date 2020-07-06 21:41:43
* Email Address : sdo@linux.home
* Version : 1.1.4.4
* Purpose :
#;
# ------------------------------------------------------

use strict;
#use CGI::Carp qw(fatalsToBrowser); 
use CGI::Carp qw(fatalsToBrowser); 
use File::Basename;
use Cwd;
use io::MyConstantBase;

my $file_to_upload=();

use constant GET_FILE_UPLOADED => sub { $file_to_upload ; } ;    # where file has to be stored: that's the "to"

my $tmp=getcwd();chomp($tmp);# gets current directory path
$CGITempFile::TMPDIRECTORY="$tmp/" . &io::MyConstantBase::PATH_TMP_DIR_MAOP->() ; # this is where all temporary uploaded file whill go
#exit(0);
if( ! -d "$CGITempFile::TMPDIRECTORY"){ die "$CGITempFile::TMPDIRECTORY $!";}# if there's an error


require Exporter;

my $VERSION    = '1.1.4.4';
$VERSION    = eval $VERSION;
my @ISA    = qw( Exporter );
my @EXPORT = qw(
		error_raised
		my_upload
		reformat
	     );

my @EXPORT_OK = qw( 
		error_raised
		my_upload 
		reformat
	       );

# Written by shark bait ###

	       #use constant ROOT_DESPOSIT           => "../"; # To store information

#use constant io::MyConstantBase::AMOUNT_OF_INFO_TO_READ->()  => ( 5 * 2096 ); # That's the amount bite read each time src files read (slot)

use Fcntl qw( :DEFAULT :flock);

$CGI::DISABLE_UPLOADS = &io::MyConstantBase::OK->();
$CGI::POST_MAX        = &io::MyConstantBase::MAXIMUM_SIZE_FILE->();

# We define a boolean value OK = 0
#use constant OK  => 0;
#use constant NOK => !(OK);

# Define values to set up upload image files
use constant MAXIMUM_FILE_OPENED                          => 100;

=head1 NAME

packages::MyFile.pm

$VERSION    = '1.1.4.0'

=head1 ABSTRACT

This package manages file transactions: upload.

=head2 LIST OF FUNCTIONS

=over 4

error_raised 
my_upload 
reformat 
return_average_file 
size_dir 
title_average_formating 

=back

=head2 HISTORY OF MODIFICATIONS

=over 4

- I<Last modification:1.1.4.1> Feb 22sd 2011: see my_upload

- I<Last modification:1.1.4.0> Jan 31st 2011: $CGITempFile::TMPDIRECTORY added. 

- I<Last modification:1.1.2.0> Nov 22sd 2010: There is better managent of errors

- I<Last modification:1.1.0.0> May 24th 2009

- I<Last modification:> May 13th 2009

- I<Last modification:> Aug 20th 2008

- I<Last modification:> Jun 10th 2008

- I<Last modification:> Jan 27th 2006

- I<Last modification:> Mar 03rd 2005

- I<Starting date:> Nov 10th 2004

=back

=cut


=head1 sub reformat(...)

This function reformats path when it comes from Internet Explorer.

=head2 PARAMETER(S)

=over 4

$path: that's the path to file

=back

=head2 RETURNED VALUE

=over 4

Path reformated.

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

- I<Last modification:> Aug 22sd 2006

- I<Last modification:> Jul 18 2006

- I<Created on:> Jul 17 2006

=back

=cut

sub reformat { # Begin sub reformat
	my ($path) = @_;

	chomp($path);
	my $toto = $path;
	if ($path =~ m/^[a-zA-Z0-9]+\:(.+)/) { # Begin if ($path =~ m/^[a-zA-Z0-9]+\:(.+)/)
		$path = $1;
	} # End if ($path =~ m/^[a-zA-Z0-9]+\:(.+)/)
	$path =~ s/\ //g;
	$path =~ s/\\/\//g;
	$path =~ s/^[a-zA-Z]\://g;

	return $path;
} # End sub reformat

=head1 sub my_upload(...)

This function allows upload.

=head2 PARAMETER(S)

=over 4

$doc: that's new CGI object.

$file_from: that's the file to upload.

$directory_deposit: that's where the file needs to be stored.

$suffix_for_image_file: that can be used to give to initial file a suffix s.a date, url, ip address...

$file_format: jpeg|jpg|gif can be written like this. Don't forget to put the pipe to give different file choices.

=back

=head2 RETURNED VALUE

=over 4

0 ok otherwise -1

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

- I<Last modification:> Feb 22sd 2011 management error of file received corrected

- I<Last modification:> Nov 22sd 2010 better managent of errors

- I<Last modification:> May 13th 2009

- I<Last modification:> Aug 20th 2008

- I<Last modification:> Jun 10th 2008

- I<Last modification:> Aug 22sd 2006

- I<Last modification:> Mar 04 2006

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back

=cut

sub my_upload { # Begin sub my_upload
	my ($doc, $file_from, $directory_deposit, $suffix_for_image_file,$file_format) = @_;
	my $file_name_saved_at_server_side  = ();    # file that is used to save uploaded file
	my $bytes_read     = ();    # bytes read from file uploaded
	my $buff           = ();    # buffer used to read image
	my $is_image_file_need_to_be_uploaded = 1;
	my @l_file_scat = ();
	my $ldi=getcwd; # we record current dir

	chomp($file_from);
	$ldi=&do_untaint($ldi);
	$file_from=~m/(\.[a-z0-9]{3})$/i;
	return -1 if ($file_format!~m/$1/i);

	$doc->cgi_error and error_raised( $doc, "Transfert error of file :", $doc->cgi_error );
	chomp($file_from);

	# We check if file has the following format
	# <drive name>:\d1\d1\f1.gif where d[num] is a directory and and f1.gif an image file name
	# then we take only the image file name

	@l_file_scat = split( /\//, &reformat($file_from) );
	if(scalar(@l_file_scat)>0){# begin if(scalar(@l_file_scat)>0)
		$file_name_saved_at_server_side = &reformat($l_file_scat[ scalar(@l_file_scat) - 1 ]);
	}# end if(scalar(@l_file_scat)>0)
	else {# begin else
		$file_name_saved_at_server_side=();		
	}# end else

	# We create a file into a path where to store new image file
	$file_to_upload = $directory_deposit . "/${suffix_for_image_file}${file_name_saved_at_server_side}";
	#chomp($file_to_upload);
	#print "<br>FILE RECORDED: $file_to_upload<br>";

	if ( $file_from !~ m/(${file_format})$/i ) { # Begin if ($file !~ m/^[a-zA-Z][a-zA-Z0-9\-_]*.(jpeg|jpg|gif)$/i)
	#	error_raised( $doc, "File received [$file_from].<br>Character accepted: from <u>a to z</u> and <u>A to Z</u> as first file character. Then several occurrencies from <u>a to z</u> and <u>A to Z</u> and <u>0 to 9</u> and <u>- and _</u> can be accepted.<br>\nFormat of image different from gif, jpeg, jpg.");
	}
	#elsif( $file_from !~ m/${socnet}/i){
	
	#print "<br><b>format not accepted</b>"; 
	#return -1; 
	#} # End if ($file !~ m/^[a-zA-Z][a-zA-Z0-9\-_]*.(jpeg|jpg|gif)$/i)
	
	if ( $is_image_file_need_to_be_uploaded == 1 ) { # Begin  if ($is_image_file_need_to_be_uploaded == 1 )
		my $load=0;
		${file_to_upload}=&do_untaint(${file_to_upload});
		chomp(${file_to_upload});
		if(${file_to_upload}=~m/\/$/){ print "no download: file name empty<br>";return -1;}
		open(FW,">${file_to_upload}" ) || die("Error ${file_to_upload}");
		my $seg_file_read = 0;
		while ( $bytes_read = read( $file_from, $buff, io::MyConstantBase::AMOUNT_OF_INFO_TO_READ->() ) ) { # Begin while ($bytes_read=read($file_from,$buff,io::MyConstantBase::AMOUNT_OF_INFO_TO_READ->())
			$seg_file_read += $bytes_read;
			binmode FW;
			print FW $buff;
		} # End while ($bytes_read=read($file_from,$buff,io::MyConstantBase::AMOUNT_OF_INFO_TO_READ->())
		close(FW) || die("Error: $!");
		chmod( 0755, "$file_to_upload" );
	} # End  if ($is_image_file_need-to_be_uploaded == 1 )
	return 0;
} # End sub my_upload

=head1 sub error_raised(...)

This function generates an error message when a problem occurs.

=head2 PARAMETER(S)

=over 4

$doc: that's an implementation of the object CGI (new CGI to be precised).

$explaination: explaination of the error.

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

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back

=cut

sub error_raised { # Begin sub error_raised
	my ($explaination,$doc) = @_;
	#print $doc->header("text/html"),

	#    $doc->start_html("Error"),
	#  $doc->h1("Error"),
	#  $doc->p(
	#    "Your deposit was not successul because of the following error: "),
	#  $doc->p( $doc->i($explaination) ),
	#  $doc->p("<a href=\"JavaScript:history.back()\">go back</a>"),

	#    $doc->end_html;
	exit;
} # End sub error_raised


=head1 sub size_dir(...)

This function calculates the size of directory.

=head2 PARAMETER(S)

=over 4

$dir: directory.

=back

=head2 RETURNED VALUE

=over 4

Returns size of the directory.

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

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back

=cut

sub size_dir { # Begin sub size_dir
	my $dir          = shift;
	my $size_dir_tmp = 0;

	opendir DIR, $dir or die "Impossible to open $dir: $!";
	while ( readdir DIR ) { #  Begin  while (readdir DIR)
		$size_dir_tmp += -s "$dir/$_";
	} # End while (readdir DIR)
	return $size_dir_tmp;
} # End sub size_dir


=head1 sub return_average_file(...)

This function calculates info for upload to be printed.

=head2 PARAMETER(S)

=over 4

$file_size: That's the file size.

$info_read_from_begining: Info to print.

$size_read: That's the size read from the begining.

=back

=head2 RETURNED VALUE

=over 4

Returns string to print.

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

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back

=cut

sub return_average_file { # Begin sub return_average_file
	my ( $file_size, $info_read_from_begining, $size_read ) = @_;
	my $percent_read = sprintf "%.2f", ( ( 100 * $info_read_from_begining ) / $file_size ) . '%';

	return (
		&title_average_formating( "Percent read", $percent_read . '%' )
		. &title_average_formating( "Info read", $size_read . " Byte(s)" )
		. &title_average_formating(
		"File size read",
		$info_read_from_begining
		. " Byte(s) over a total of $file_size Byte(s)"
		),
		$percent_read
	);
} # End sub return_average_file


=head1 sub title_average_formating(...)

This function center the title of the main page.

=head2 PARAMETER(S)

=over 4

$title1: that's the title.

$title2: other info abour title.

=back

=head2 RETURNED VALUE

=over 4

Returns the title formated with the two titles concatenated.

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

- I<Last modification:> Nov 10 2004

- I<Created on:> Nov 10 2004

=back

=cut

sub title_average_formating { # Begin sub title_average_formating
	return "<u>$_[0]:</u> $_[1]<br>";
} # End sub title_average_formating

1;
