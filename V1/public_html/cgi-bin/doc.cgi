#!/usr/bin/perl


my $directorybasewebsite="/home1/derased/public_html/";
my $dirbas="http://derased.heliohost.org/";

if( ! -d "tmp"){mkdir("tmp");}
#$TempFile::TMPDIRECTORY=getcwd() . "/tmp";

# +-------------------------------+
# | doc.cgi                       |
# | Last update on Dec 12 2011     |
# | Last update on Feb 1 2011     |
# | Last update on Jul 8 2010     |
# | Last update on Jun 6 2009     |
# | Written     on Apr 10 2009    |
# +-------------------------------+

use Cwd;
use CGI;
use CGI::Carp qw(fatalsToBrowser); 
use strict;
use File::Copy;
use File::Path;

#my $one_temp=`pwd`; 
my $one_temp=getcwd();# gets current directory path ; that's the root directory at the begining do not erase
chomp($one_temp);

my $doc=new CGI();

use constant TESTED_WITH_BROWSERS    => 'Google Chrome 9.0.597.102; SeaMonkey'; # That's browsers tested
use constant HOSTED_BY     => 'Helio host ';        # That's the host name
use constant HOSTED_BY_URL => 'http://www.heliohost.org';    # That's the url of host name

my $tmpfile= new CGITempFile(1);
print "Content-Type: text/html\n\n";
print "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n";
print "<html xmlns=\"http://www.w3.org/1999/xhtml\">\n";
print "<head>\n";
print "<title>\n";
print "My term\n";
print "</title>\n";
print "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=iso-8859-15\" />\n";
print $doc->meta({ 
			-name=>"author", 
			-content=>"Sebastien DOREY aka shark bait"
		}) ;


my $fileResc=0;

eval "use io::gut::machine::MyFile";
if ($@){
	eval "use io::gut::machine::MyFileRescue";
	if($@){
		#print "Content-Type: text/html\n\n";
		print "No io::gut::machine::MyFileRescue";
#print "aaaa1333";
		exit (-1);
	}
	$fileResc++;
}

use io::MyUtilities;
use io::MyNav;
use vars qw($VERSION);

my ${vers}="0.2";
my ${rel}="38.42";
my ${VERSION}="${vers}.${rel}";

=head1 NAME

doc.cgi

$VERSION='0.2.32.0'

=head1 ABSTRACT

This file creates sort of terminal over internet with a navigator.

=head2 LIST OF FUNCTIONS

=over 4

=over 4 

askPasswd(...)
gets_base(...)
checks_auth(...)
comp(...)
mkDeposit(...)
destroyContext(...)
ed(...)
graph(...)
is_tainted(...)
lastModif(...)
loadFile(...)
menu_command(...)
prints_res(...)
upload_menu(...)
verify_sec(...)

=back

=back

=head2 HISTORY OF MODIFICATIONS

=over 4

- I<Last modification:v0.1.32.0> Aug 14 2011: getDocVers changed to getsDocVers

- I<Last modification:v0.1.31.2> Feb 22sd 2011: see io::gut::machine::MyFile::my_upload

- I<Last modification:v0.1.31.1> Feb 17 2011: see io::MyUtilies::setUrlFile

- I<Last modification:v0.1.31.0>  Feb 10 2011:  see packages::MySec

- I<Last modification:v0.1.30.0> Feb 1st 2011: seee packages::MyFile.pm.
checks path Cwd lib.

- I<Last modification:v0.1.25.0> Jan 31st 2011: see packages::MyFile.pm.

- I<Last modification:v0.1.23.0> Jan 24 2011: $command added as param

- I<Last modification:v0.1.20.4> Jan 17th 2011: bugs due to bad file descriptor.

- I<Last modification:v0.1.19.0RC> May 5th 2010: tests modifications 
Add new service with $command

- I<Last modification:v0.1.19.0RC> May 3rd 2010: tests modifications

- I<Last modification:v0.1.18.2Bet> May 20th 2009: modifications

- I<Last modification:v0.1.0.0> Apr 25th 2009: creation

=back

=cut

$|=1;
use Cwd;
use constant METHOD => gets_request_method ; 
use constant DIRECTORY_DEPOSIT => io::MyUtilities::finds_directory_where_are_stored_images;
my ${v}=`which diff`;# get path + exec of diff command
chomp(${v});
my $lth="&";$lth.="lt";$lth.=";";
my $gth="&";$gth.="gt";$gth.=";";

my ${deposit}="private"; # gets deposit content from param received
&mkDeposit("${deposit}"); # creates private directory if it does not exist
#print "Content-type: text/html\n\n<br>--->". getcwd() . "<br>-" . `pwd` ."<br>";
my (${mybase},${mycontext}) =&gets_base(getcwd() . "/${deposit}"); # sets or gets info where path is set about base 
#print "Content-type: text/html\n\n<br>--->". getcwd() . "<br>-" . `pwd` ."$deposit,$mybase,$mycontext<br>";
my ${doc}=new CGI();


my ${prompt}=${doc}->param("prompt"); # gets prompt content from param received
chomp(${prompt}); # removes final character

my ${myfile}=${doc}->param("myfile"); # gets the file name from param received
chomp(${myfile}); # removes final character
my $ext=(split(/\./,${myfile}))[scalar(split(/\./,${myfile}))-1]; # gets extesion if it exists

my ${granted}=${doc}->param("granted"); # gets granted variable content from param received
chomp(${granted}); # removes final character

my ${editor}=${doc}->param("editor"); # gets editor variable content from param received
chomp(${editor}); # removes final character

my ${command}=${doc}->param("command"); # gets command variable content from command line
chomp(${command}); # removes final character

if($command eq "verDoc"){ # Only version is asked
	#print "Content-Type: text/html\n\n";
	print io::MyUtilities::getsDocVers("doc.cgi","$VERSION");
	#print "aaaa3";
	exit(0); # Exit that's it
}elsif($command eq "versioning"){ # Begin Only version is asked
	#print "Content-Type: text/html\n\n";
	print "$VERSION";
	#print "aaaa4";
	exit(0);# Exit that's it
}# End only version is asked

my ${upload_req}=${doc}->param("upload_req"); # gets command variable content upload
chomp(${upload_req}); # removes final character

my ${recarea}=${doc}->param("recarea"); # gets command variable content upload
chomp(${recarea}); # removes final character

#print "Content-type: text/html\n\n";
#my $c=`perl -v`;
#my @k=split(/\n/,$c);
#foreach my $kkk (@k){
#	print "$k[1]<br>";
#}
#print "--++++++++$mybase<br>";
my $myurlp=gets_full_url($mycontext);

if(${recarea}=~m/ok/){ # begin if(${recarea}=~m/ok/)
	my ${myed}=${doc}->param("myed"); # gets command variable content upload
#	print "wwwwwwwwwwwwwwwwwwwwwwww<br>";exit(0);
	open(W,">${mycontext}/${myfile}") or die("open $!");
	foreach my ${o} (split(/\n/,$myed)){
		chomp(${o});
		${o}=~s/\r$//;
		${o}=~s/\-\>\;/\-\>/g;
		${o}=~s/\;\;/\;/g;
		print W "${o}\n";
	}
	close(W) or die("open $!");
	print "<b><i>${mycontext}/${myfile}</i> success fully saved</b><br>";
	${granted}="ok";
} # begin if(${recarea}=~m/ok/)

#print "Content-Type: text/html\n\n";
# WATCHOUT this test it does not look in the private directory from ${mybase} path
# sanitary tests upon command line (from command variable received)
if(${command}=~m/^\ {0,}edit\ {1,}([^\ \t\n\c\r\0]+)$/i){${editor}="ok";${myfile}=$1;}
#if(${command}=~m/\ {0,1}rm\ {1,}/i){${granted}="ko";}
#if(${command}=~m/^\ {0,1}download\ {1,}([^\ \t\n\c\r\0]+)/i){my $f=$1;chomp($f);print "file to download:<a href=\"$f\">$f</a><br>";}
#if(${command}=~m/^\ {0,}download\ {1,}([^\ \t\n\c\r\0\\]+)$/i){my $f=$1;chomp($f); my $dbas="$mycontext/"; chomp($dbas); $dbas=~s/$directorybasewebsite/$dirbas/g; print "<br>file to download:<a href=\"$dbas/$f\">$f</a><br>";}

if(${command}=~m/^\ {0,}download\ {1,}([^\ \t\n\c\r\0\\]+)$/i){my $f=$1;chomp($f); my $dbas="$mycontext/"; chomp($dbas); $dbas=~s/$directorybasewebsite//g; print "<br>file to download:<a href=\"$dbas/$f\">$f</a><br>";}

if(${command}=~m/^\ {0,}purge\ *$/i){ # begin if(${command}=~m/^\ {0,}purge\ *$/i)
	#print "rmdir $one_temp/.trash<br>";
	rmtree("$one_temp/.trash") or die("$!<br>");
} # end  if(${command}=~m/^\ {0,}purge\ *$/i)
if(${command}=~m/^\ {0,}trash\ {1,}([^\ \t\n\c\r\0]+)$/i){ # begin if(${command}=~m/^\ {0,}trash\ {1,}([^\ \t\n\c\r\0]+)/i)
	if(!-d "$one_temp/.trash"){ # begin if(!-d "$one_temp/.trash")
		mkdir("$one_temp/.trash");
	} # end if(!-d "$one_temp/.trash")

	my @lfile=glob("$1");
	foreach(@lfile){ # begin foreach(@lfile)
		if(-f "$_"){ # begin if(-f "$_")
			move("$_","$one_temp/.trash/") || die("$1 or $one_temp/.trash/ $!");
		} # end if(-f "$_")
	} # end foreach(@lfile)
} # end if(${command}=~m/^\ {0,}trash\ {1,}([^\ \t\n\c\r\0]+)/i)
if(${command}=~m/^\ {0,}help\ {1}(.+)/i){
	my @q=();
	my $ag=$1;
	chomp($ag);
	if($ag=~m/list/i){ # begin if($1=~m/$\ *list\ *^/i)
		my $d=getcwd();
		my $fh=();

		chdir("$one_temp/pod");
		opendir(RD,".");
		@q=("<b><u>Builtins</u></b>");
		while($fh=readdir(RD)){ # begin while($fh=readdir(RD))
			if($fh!~m/^\.{1,2}$/){ # begin if($fh!~m/^\.{1,2}$/)
				$fh=~s/\.pod//i;
				@q=(@q,"<br>$fh");
			} # end if($fh!~m/^\.{1,2}$/)
		} # end while($fh=readdir(RD))
		close(RD);
		chdir($d);
	} # end if($1=~m/$\ *list\ *^/i)
	else{ # begin else
		#print "$1 wwwwwwwwwwwwwwwwwww";
		open(D,"${one_temp}/pod/$1.pod");
		@q=<D>;
		close(D);
	} # end else
	#my $o=`cat ${tmp}/pod/$1.pod`;
	print <<MYCSS;
<div class="postcard_help">
<pre>
MYCSS
	for(@q){print "$_";}
	print <<MYCSS;
</pre>
</div>
MYCSS
if(${command}=~m/^\ *bye\ */i){${granted}="ko";}
if(${command}=~m/^\ *quit\ *$/i){${granted}="ko";}
if(${command}=~m/\ {0,}mpan\ {1}(.+)/i){my $o="perl -M$1 -e 1 >\&${mycontext}/__IIII_$$"; print `$o; cat ${mycontext}//__IIII_$$; rm ${mycontext}//__IIII_$$; `;}
	}
my $kk=();
my $jjj=sets_url("$mycontext");# Returns url with user name  and path.
if(${command}=~m/\ {0,}print\ {1,}([a-z0-9-_]+\.(gif|jpg|jpeg))/i){${kk}="<img src=\"$myurlp/$1\" alt='' />";${granted}="ok";}

if(${upload_req}=~m/^ok$/i){ # begin if(${command}=~m/^\ *upl\ {1,}(.+)/i)
	${granted}="ok";
	# operation of uploading file
	unlink("a");
	print "c0";
	if($fileResc==0){# begin if($fileResc==0)
		open(W,">a");
		print W "c1";
		close(W);
		io::gut::machine::MyFile::my_upload(${doc},${myfile},"${mycontext}","","${ext}"); # upload file within current directory
	}# end if($fileResc==0)
	else{# begin else
		io::gut::machine::MyFileRescue::my_upload(${doc},${myfile},"${mycontext}","","${ext}"); # upload file within current directory		
	}# end else
	$command=();
} # end if(${command}=~m/^\ *upl\ {1,}(.+)/i)
#print "=========++++=====<br>";
if(${command}=~m/^\ *dwl\ *([^\n\t\ ]*)$/i){${granted}="ok";print "<a href=\"file:///${mycontext}/$1\">$1</a>\n"; }
#print "gfhfhfghfghfghfsssss<br>";
print <<FORM;
<style type="text/css">
<!--
div.postcard_help{
//text-align: center;
-moz-transform: rotate(5deg);
-webkit-transform: rotate(5deg);
-o-transform: rotate(5deg);
filter: alpha(opacity = 30);
left: 500px;
opacity: .50;
position: absolute;
z-index: 22;
}
#graph1 { 
position: absolute ;
opacity: .78;
background-color: #black;
top: 40; 
right: 25; 
color: yellow;
width: 400px;
height: 600px;
border: 1px solid red;
z-index: 20;
}
#inner_graph1 { 
margin-left: 10px;
margin-right: 10px;
}
#contents { 
margin: 250px; 
border: 3px solid black; 
background-color: #353135;
}
#comline { 
margin: 50px; 
border: 0px solid white; 
}
#menu_com {
position: relative ;
top: 10; 
}
#result {
border: 1px dash navy;
margin-left: 10px;
background-color: darkslategray;
z-index: 10;
}
#innerResult {
margin-left: 10px;
margin-right: 10px;
color: white;
}
i#pp {
color: red;
}
u#pr {
position: absolute;	
z-index: -100;
font-weight: bold;
font-size: 1em; 
color: black;
margin-top: 10px;
margin-left: -10px;
}
u#po {
position: absolute;	
z-index: -90;
font-weight: bold;
font-size: 3em; 
color: red;
margin-top: -20px;
margin-left: -10px;
}
u#pp {
position: absolute;	
z-index: -95;
font-weight: italic;
font-size: 3em; 
color: green;
margin-top: -15px;
margin-left: -10px;
}
a {
text-decoration: none;
color:  grey;
}
a:visited{
color: red;
}
a:hover {
color: green;
}
u#pe {
position: absolute;	
z-index: -100;
font-weight: bold;
font-size: 3em; 
color: darkorange;
margin-top: 10px;
margin-left: 10px;
}
-->
</style>
FORM
print "\n</head>\n";
print "<body>\n";
print '<img src="../img/1302559859.png" width="50px" alt="" />';

if(${prompt}!~m/auth/ && length(${myfile})==0 && ${granted}!~m/ok/){ # begin if(${prompt}!~m/auth/ && length(${myfile})==0 && ${granted}!~m/ok/)
	my $l=getcwd();chomp($l);# gets current directory path
	my $pa="${mybase}/${deposit}";
	if(-f "$pa/context.base"){unlink("$pa/context.base");}# remove file context.base
	if(-f "$pa/context"){unlink("$pa/context");}# remove file context
	open(W,">$pa/context.base") or die("open error [$pa/context.base] $!");
	print W $l; # save context
	close(W) or die("close $!");
	open(W,">$pa/context") or die("open error $!");
	print W $l; # save context
	close(W) or die("close $!");
	print <<FORM;
<div id="contents">
<form action="doc.cgi" method="post" enctype="multipart/form-data">
<input type="password" name="prompt" size="24" style="color: #353135;background-color: #353135 ; border: 0px;margin: 50px;" />
<input type="submit" />
</form>
</div>
FORM
	&lastModif();
#print "aaaa1";
	exit 0;
} # end if(${prompt}!~m/auth/ && length(${myfile})==0 && ${granted}!~m/ok/)
&checks_auth("${mybase}/${deposit}",${myfile},${doc});
&menu_command(${myfile},${granted},$command);

=head1 FUNCTION sub checks_auth

Prints a menu acording to action.

=head2 PARAMETER(S)

=over 4

=over 4

$deposit: depos

$myfile: that's the file to check

$doc: object

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

=head2 STATUS

=over 4

=over 4

- In use

=back

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

=over 4

- I<Last modification:> Apr 25 2009

- I<Created on:> Apr 25 2009

=back

=back

=cut

sub checks_auth{ # begin sub checks_auth
	my (${deposit},${myfile},${doc})=@_; # deposit: depos;myfile: file to check;doc: object
	my $t=length(${myfile}); #gets file length

	if(${t}!=0 ){ # begin if(${t}!=0 )
#print "------>$deposit<br>";exit(0);
		if(-f "${deposit}/ref.jpg"){ # begin if(-f "${deposit}/${myfile}")
			if(${myfile}=~m/\.jp[e]{0,1}g$/i){ # begin if(${myfile}=~m/.jp[e]{0,1}g$/i)
				#print "_1_check_auth(${deposit},${myfile},${doc})<br />";
				if($fileResc==0){ # begin if($fileResc==0)
					io::gut::machine::MyFile::my_upload(${doc},${myfile},"${deposit}","nouv","jpeg|jpg|JPEG|JPG");
				} # end if($fileResc==0)
				else{ # begin else
					io::gut::machine::MyFileRescue::my_upload(${doc},${myfile},"${deposit}","nouv","jpeg|jpg|JPEG|JPG");
				} # end else
			} # end if(${myfile}=~m/.jp[e]{0,1}g$/i)
		} # end if(-f "${deposit}/${myfile}")
		else { # begin else
#print "ooooooooooo<br>";exit(0);
			if(${myfile}=~m/\.jp[e]{0,1}g$/i){ # begin if(${myfile}=~m/.jp[e]{0,1}g$/i)
				#my $w=`/bin/pwd`;
				my $w=getcwd();chomp($w);# gets current directory path
				#print "_2_check_auth(${deposit},${myfile},${doc})<br>";
				if($fileResc==0){# Begin if($fileResc==0)
					io::gut::machine::MyFile::my_upload(${doc},${myfile},"${deposit}","orig","jpeg|jpg|JPEG|JPG");
				}# end if($fileResc==0)
				else{# begin else
					io::gut::machine::MyFileRescue::my_upload(${doc},${myfile},"${deposit}","nouv","jpeg|jpg|JPEG|JPG");
				}# end else
				rename("${deposit}/orig${myfile}","${deposit}/ref.jpg");
				#print "popopipipipi<br>";exit(0);
				if(-f "$deposit/context"){unlink("$deposit/context");}
				open(W,">${deposit}/context") or die("open $!");
				print W $w;
				close(W) or die("close $!");
			} # end if(${myfile}=~m/.jp[e]{0,1}g$/i)
		} # end else
	} # end if(${t}!=0 )
} # end sub checks_auth

=head1 FUNCTION menu_command

Ask for image as  password. Checks file for authentication if is there. If not write as ref.jpg. If there write as <ext>file for comparison later on.

=head2 PARAMETER(S)

=over 4

=over 4

${deposit}: depos

${myfile}: file to check

${doc}: doc: object

$command: that's the command line

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

=head2 STATUS

=over 4

=over 4

- In use

=back

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

=over 4

- I<Last modification:> May 22 2009

- I<Created on:> Apr 25 2009

=back

=back

=cut

sub menu_command{ # begin sub menu_command
	my (${myfile},${granted},$command)=@_;
	my $pwsd=getcwd();chomp($pwsd);# gets current directory path
	print "\n<div id=\"menu_com\">\n";
	if((&comp("nouv${myfile}")==0 || "${granted}" eq "ok") && (gets_request_method()=~m/POST/i)){ # begin if((&comp("nouv${myfile}")==0 || "${granted}" eq "ok") && (METHOD =~ m/POST/i))
		if($command=~m/^\ *upl\ */) { # begin if($command=~m/^\ *upl\ */)
			&upload_menu(${mycontext});
		} # end if($command=~m/^\ *upl\ */)
		else { # begin else
			print <<FORM;
<form action="doc.cgi" method="post" enctype="multipart/form-data">
<input type=text name="command" size=120>
<input type=hidden name="granted" value="ok">
</form>
FORM
			&prints_res($command,"${mybase}",${doc});
		} # end else
	} # end if((&comp("nouv${myfile}")==0 || "${granted}" eq "ok") && (METHOD =~ m/POST/i))
	else { # begin else
		my $pp=getcwd();chomp($pp);# gets current directory path
		open(W,">private/base.dir") or die("private/base.dir $!");# save current path
		print W $pp;
		close(W) or die("close $!");
		print <<FORM;
<center> <img width="200px"  src="../img/sorry.jpg" alt='' border="1" /> </center>
<div id="contents">
FORM
		&askPasswd();
		print <<FORM;
</div>
FORM
	} # end else
	# footer
	print "</div>\n";
	&lastModif();
} # end sub menu_command


=head1 FUNCTION sub deposit

Creates a deposit directory in . directory. It creates too a temporary directory tmp in . directory.

=head2 PARAMETER(S)

=over 4

=over 4

${d}: directory for deposit

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

=head2 STATUS

=over 4

=over 4

- In use

=back

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

=over 4

- I<Last modification:> Apr 25 2009

- I<Created on:> Apr 25 2009

=back

=back

=cut

sub mkDeposit{ # begin sub mkDeposit
	my ($d)=@_;
	if( !-d "$d" ){ # begin if( !-d "$d" )
		mkdir("$d");
	} # end if( !-d "$d" )
	if( !-d "tmp" ){ # Begin if( ! -d "tmp" )
		mkdir("tmp");
	} # End if( ! -d "tmp" )
} # end sub mkDeposit


=head1 FUNCTION sub loadFile()

Loads a file.

=head2 PARAMETER(S)

=over 4

=over 4

${myfile}: file to load.

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

File content as an array or -1 if there is an error.

=back

=back

=head2 ERRROR RETURNED

=over 4

=over 4

-1

=back

=back

=head2 BUG(S) KNOWN

=over 4

=over 4

None.

=back

=back

=head2 STATUS

=over 4

=over 4

- In use

=back

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

=over 4

- I<Last modification:> Apr 25 2009

- I<Created on:> Apr 25 2009

=back

=back

=cut

sub loadFile(){ # begin sub loadFile()
	my (${myfile})=@_;

	if( -f "${myfile}"){ # begin if( -f "${myfile}")
#		print "ttutyuutyjhnnbvnvbnvbpupupupupupupu<br />";exit(0);
		open(RS,"${myfile}") or die("open $!");
		my @rs=<RS>;
		close(RS) or die("close $!");
		return @rs;
	} # end if( -f "${myfile}")
	return -1;
} # end sub loadFile()


=head1 FUNCTION sub comp()

Does comparison between two files.

=head2 PARAMETER(S)

=over 4

=over 4

${myfile}: file to check

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

0 if ok otherwise -1.

=back

=back

=head2 ERRROR RETURNED

=over 4

=over 4

-1

=back

=back

=head2 BUG(S) KNOWN

=over 4

=over 4

None.

=back

=back

=head2 STATUS

=over 4

=over 4

- In use

=back

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

=over 4

- I<Last modification:> Apr 30 2009

- I<Created on:> Apr 25 2009

=back

=back

=cut

sub comp{ # begin sub comp
	my (${myfile})=@_;
	#my $pwwd=`which pwd`;chomp($pwwd);
#	my $pwsd=`$pwwd`;chomp($pwsd);
	my $pwsd=getcwd();chomp($pwsd);# gets current directory path
	chomp($myfile);
	#print "::comp($pwsd/$deposit/$myfile);<br />";
	if(!-f "$pwsd/${deposit}/${myfile}"){ # begin if(-f "${deposit}/${myfile}")
	#	print "***error****<br />";
		return -1;
	} # end if(-f "${deposit}/${myfile}")
	if(!-f "$pwsd/${deposit}/ref.jpg"){ # begin if(-f "$pwsd/${deposit}/$ref.jpg")
	#	print "**----error****<br />";
		return -1;
	} # end if(-f "$pwsd/${deposit}/$ref.jpg")

	my $inf1=(stat("$pwsd/${deposit}/ref.jpg"))[7];
	my $inf2=(stat("$pwsd/${deposit}/${myfile}"))[7];

	# checks size
	if(${inf1}!=${inf2}) { return -1; }

	if(length(${v})==0) { return -1 ; }
	#print "${v} $pwsd/${deposit}/ref.jpg $pwsd/${deposit}/${myfile}<br />";
	my ${r}=`${v} $pwsd/${deposit}/ref.jpg $pwsd/${deposit}/${myfile}`; # loads file 2
	#print "pppppppppp)$r<br />";
	if(length(${r})!=0) { return -1 ; }

	# removes file if it exists
	if(-f "$pwsd/${deposit}/${myfile}"){ # begin if(-f "${deposit}/${myfile}")
		unlink("$pwsd/${deposit}/${myfile}"); # remove file 2
	} # end if(-f "${deposit}/${myfile}")
	else { # begin else
		# not good otherwise
		return -1; 
	} # end else
	#print "iiiiiiiiiii)$r->".length(${r})."<br>";
	return (length(${r})!=0) ? -1 : 0;
} # end sub comp()


=head1 FUNCTION checks_auth()

Ask password.

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

=head2 STATUS

=over 4

=over 4

- In use

=back

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

=over 4

- I<Last modification:> Apr 30 2009

- I<Created on:> Apr 30 2009

=back

=back

=cut

sub askPasswd(){ # begin sub askPasswd()
	print <<FORM;
<form action="doc.cgi" method="post" enctype="multipart/form-data">
<input type=file name="myfile" style="margin:50px;color: #353135;background-color:#353135;">
<input type=submit>
</form>
FORM
} # end sub askPasswd()


=head1 FUNCTION sub upload_menu()

Upload file.

=head2 PARAMETER(S)

=over 4

=over 4

${cd}: current directory.

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

=head2 STATUS

=over 4

=over 4

- In use

=back

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

=over 4

- I<Last modification:> Apr 29 2009

- I<Created on:> Apr 26 2009

=back

=back

=cut

sub upload_menu(){ # begin sub askPasswd()
	my ($cd)=@_; # current directory
	print <<FORM;
<b>>$cd</b><br>
<form action="doc.cgi" method="post" enctype="multipart/form-data">
<input type=file name="myfile" style="margin:50px;color: #353135;background-color:#353135;">
<input type=hidden name="granted" value="ok">
<input type=hidden name="upload_req" value="ok">
<input type=submit>
</form>
FORM
} # end sub askPasswd()


=head1 FUNCTION sub prints_res()

Prints result of the command.

=head2 PARAMETER(S)

=over 4

=over 4

$command: that's the command line.

${deposit}: depos

${doc}: object doc cgi

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

=head2 STATUS

=over 4

=over 4

- In use

=back

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

=over 4

- I<Last modification: v0.1.23.0> Jan 24 2011: $command added as param

- I<Last modification:> May 21 2009

- I<Created on:> Apr 27 2009

=back

=back

=cut

sub prints_res{ # begin sub prints_res
	my ($command,$deposit,$doc)=@_;
	#my ${command}=${doc}->param("command"); # gets command variable content from command line
	#chomp(${command}); # removes final character
	if("${editor}" ne "ok"){ # begin if("${editor}" ne "ok")
		# next versions try to remove this with lines which and get something tat do similar stuff but as to be platform independent
		my ${myecho}=`which echo`;chomp(${myecho});
		my ${mycat}=`which cat`;chomp(${mycat});
		my ${mypwd}=`which pwd`;chomp(${mypwd});# usefull for getting command with its path
		#my ${mypwd}=getcwd();chomp(${mypwd});# gets current directory path
		my @z=();
		my @w=();

		if( -f "${deposit}/private/context"){ # begin if( -f "${deposit}/private/context")
#			print "cacacacacacacacacacaca<br>${deposit}/private/context<br>";
			open(R,"${deposit}/private/context") or die("error ${deposit}/private/context $!");
			@z=<R>;
			close(R) or die("close $!");
			chomp($z[0]);chomp($command);chomp($mypwd);
#			print "---X-->$z[0]<br>$command<br>";
			if(length($command)>0){ # begin if(length($command)>0)
#				print "jolo<br>";
				my ${r}=`cd $z[0];${command};${mypwd}`;
				@w=split(/\n/,${r});
				if(scalar(@w)){ # begin if(scalar(@w))
					chomp($w[(scalar(@w)-1)]); # removes last info line last character
#					print "sssssssss".$w[(scalar(@w)-1)]."<<<<<<br>";
					open(W,">${deposit}/private/context") or die("open ${deposit}/private/context error $!");
					print W $w[(scalar(@w)-1)]; # save context
					close(W) or die("close ${deposit}/private/context $!");
					delete $w[scalar(@w)-1];
				} # end if(scalar(@w))
			} # end if(length($command)>0)
		} # end if( -f "${deposit}/private/context")

		print <<DEB;
<b><i>${mycontext}</i>>${command}</b><br>
DEB
		my $k=();
		foreach my ${o} (@w){ # begin foreach my ${o} (@w)
			${o}=~s/\</$lth/g;
			${o}=~s/\>/$gth/g;
			${k}.="${o}<br>\n";
		} # end foreach my ${o} (@w)

		# ${k}.="</font><br>\n";

		print <<DEB;
<div id="result">
<div id="innerResult">
${k}
</div>
</div>
DEB
	} # end if("${editor}" ne "ok")
	else { # begin else
		&ed(${myfile}); # prints a menu kinda html
	} # end else
} # end sub prints_res


=head1 FUNCTION sub ed()

Editor.

=head2 PARAMETER(S)

=over 4

=over 4

${myfile}: file to edit.

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

=head2 STATUS

=over 4

=over 4

- In use

=back

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

=over 4

- I<Last modification:> May 19 2009

- I<Created on:> May 2 2009

=back

=back

=cut

sub ed(){ # begin sub ed()
	my (${myfile})=@_;
	my @content=&loadFile("${mycontext}/${myfile}");
	my $source=();
	for my $i (@content){ # begin for my $i (@content)
		${source}.=$i;
	} # end for my $i (@content)
${source}=~s/\</$lth/g;
${source}=~s/\>/$gth/g;
		chomp(${source});
	print <<DEB;
<form name="editor" method="post" action="doc.cgi">
<i>File name:</i><input type="text" name="myfile" value="${myfile}"><br>
<input type="hidden" name="recarea" value="ok">
<textarea name="myed" cols="120" rows="25">${source}</textarea><br>
<input type=submit value=Save>
</form>
<form name="editor" action="doc.cgi">
<input type=submit value=Cancel>
<input type="hidden" name="myfile" value="${myfile}">
<input type=hidden name="granted" value="ok">
</form>
DEB
} # end sub ed()


=head1 FUNCTION sub lastModif()

Prints file last modification.

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

=head2 STATUS

=over 4

=over 4

- In use

=back

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

=over 4

- I<Last modification:> Apr 25 2009

- I<Created on:> Apr 25 2009

=back

=back

=cut

sub lastModif(){ # begin sub lastModif()
	print "<hr width='55%' align='left' />\n\n";
	print "<br /><br />" . io::MyUtilities::footer($doc, 
						 DIRECTORY_DEPOSIT . "powered.gif",
						 DIRECTORY_DEPOSIT . "jangada.gif",
						 "http://www.perl.org",
						 ${VERSION},
						 TESTED_WITH_BROWSERS,
						 HOSTED_BY,
						 HOSTED_BY_URL);
#	print io::MyUtilities::footer(${doc}, DIRECTORY_DEPOSIT . "powered.gif",DIRECTORY_DEPOSIT . "jangada.gif","http://www.perl.org", ${VERSION},"IE ; Mozilla 1.8b ; Rev. 5-17-07 Safari ; Google Chrome 1.0.154.65","");
	print "\n</div></body>\n</html>\n";
} # end sub lastModif()


=head1 FUNCTION sub is_tainted()

Checks if variable is tainted.

=head2 PARAMETER(S)

=over 4

=over 4

None.

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

True or false.

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

=head2 STATUS

=over 4

=over 4

- In use

=back

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

=over 4

- I<Last modification:> Apr 25 2009

- I<Created on:> Apr 25 2009

=back

=back

=cut

sub is_tainted(){ # begin sub is_tainted()
	my $arg=shift;
	my $nada=substr($arg,0,0); # zero length
	local $@; # preserve caller's version
	eval { eval "# $nada"};
	return (length($@)!=0);
} # end sub is_tainted()


=head1 FUNCTION sub verify_sec()

Checks is var received is not weird

=head2 PARAMETER(S)

=over 4

=over 4

@command: command.

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

If variable is tainted then exit(0).

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

=head2 STATUS

=over 4

=over 4

- In use

=back

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

=over 4

- I<Last modification:> Jan 16 2011: print added

- I<Last modification:> Apr 25 2009

- I<Created on:> Apr 25 2009

=back

=back

=cut

sub verify_sec(){ # begin sub verify_sec()
	my ($command)=@_;
#print ""
#	return 0;
	if(&is_tainted (${command})){ # begin if(&is_tainted (${command}))
		#print "case verify sec";
		&askPasswd();
		&lastModif();
#print "aaaa2";
		exit 0;
	} # end if(&is_tainted (${command}))
} # end sub verify_sec()


=head1 FUNCTION sub destroyContext()

Destroy context.

=head2 PARAMETER(S)

=over 4

=over 4

$fil: gets file where context is saved.

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

=head2 STATUS

=over 4

=over 4

- In use

=back

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

=over 4

- I<Last modification:> May 3 2009

- I<Created on:> May 3 2009

=back

=back

=cut

sub destroyContext(){ # begin sub destroyContext()
	my (${fil})=@_; # gets file where context is saved
	if(-f "${fil}"){ # begin if(-f "${fil}")
		return !unlink($fil);
	} # end if(-f "${fil}")
	return -1;
} # end sub destroyContext()


=head1 FUNCTION sub gets_base(...)

Sets or gets path if already recorded.

=head2 PARAMETER(S)

=over 4

=over 4

${dir}: directory.

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

${mybase},${mycontext} which are respectively base directory and context directory.

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

=head2 STATUS

=over 4

=over 4

- In use

=back

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

=over 4

- I<Last modification:> Apr 30 2009

- I<Created on:> Apr 29 2009

=back

=back

=cut

sub gets_base{ # begin sub gets_base
	my (${dir}) = @_; # directory

	if( -f "${dir}/context.base"){ # begin if( -f "${dir}/context.base")
		#print "sdfsdffsdf sdfv dsbsfdb bfdgfdfdgdf<br>";exit(-1);
		#print "Content-type: text/html\n\n sdfsdffsdf sdfv dsbsfdb bfdgfdfdgdf [${dir}/context.base]<br>";
		open(R,"${dir}/context.base") or die("${dir}/context.base $!"); # gets context
		my @k=<R>;	
		close(R) or die("error $!");
		open(R,"${dir}/context") or die("${dir}/context.base $!"); # gets context
		my @l=<R>;	
		close(R) or die("error $!");
		chomp($l[0]);
		#print "return ($k[0],$l[0])<br>";
		return ($k[0],$l[0]) if(-d "$k[0]");
	} # end if( -f "${dir}/context.base")
	my $p=getcwd; chomp(${p});# gets current directory path
	#print "$dir --- 1.1<br>";
	my $k=${p}; chomp(${k});
#		print "$dir --- 1.2<br>";exit(0);
	open(W,">${dir}/context.base") or die("${dir}/context.base $!"); # gets context
	print "$dir --- 1.3<br>";
	print W $k;	
	#print "$dir --- 1.4<br>";
	close(W) or die("error $!");
	#print "$dir --- 1.5<br>";
	#print "dsfsdfsdfsdfsdfsdfsd >2<br>";
	open(W,">${dir}/context") or die("${dir}/context $!"); # gets context
	print W $k;	
	close(W) or die("error $!");
	#print "dsfsdfsdfsdfsdfsdfsd 3<br>";
	return ($k,$k);
} # end sub gets_base


=head1 FUNCTION sub graph()

Prints a graph (svg format).

=head2 PARAMETER(S)

=over 4

=over 4

${myfile}: file to check

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

=head2 STATUS

=over 4

=over 4

- Under construction

=back

=back

=head2 HISTORY OF CREATION/MODIFICATION 

=over 4

=over 4

- I<Last modification:> May 15 2009

- I<Created on:> May 15 2009

=back

=back

=cut

sub graph(){ # begin sub graph()
	my (${myfile})=@_;
	my ${o}=`ls -R ${mycontext}`;

	print <<DEB;
<div id="graph1"> 
<div id="inner_graph1"> 
place pour un graphique
DEB
		for my $k (split(/\n/,${o})){
			print "$k\n";
		}
		print <<DEB;
</div> 
</div> 
DEB
} # end sub graph()

=head1 AUTHOR

Current maintainer: M. Shark Bay <shark dot b at laposte dot net>

=cut
