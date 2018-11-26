package io::MySec;
use CGI::Carp qw(fatalsToBrowser); 
use HTTP::BrowserDetect;

# ------------------------------------------------------
q##//q#
* Created By : sdo
* File Name : MySec.pm
* Creation Date : Sun Jul 19 21:11:08 2009
* Last Modified : Mon Nov 26 15:32:34 2018
* Email Address : sdo@macbook-pro-de-sdo.home
* Version : 0.0.0.0
* License:
*       Permission is granted to copy, distribute, and/or modify this document under the terms of the Creative Commons Attribution-NonCommercial 3.0
*       Unported License, which is available at http: //creativecommons.org/licenses/by- nc/3.0/.
* Purpose :
#;
# ------------------------------------------------------

# +-------------------------------+
# | MySec.pm                     |
# | Written on Jul 19 2009        |
# +-------------------------------+

require Exporter;

use Fcntl qw( :DEFAULT :flock);
use Net::Ping;
use LWP::Simple;
use io::MyNav;

my $VERS       = '1.0';
my $REL        = '11.2';
$VERSION    = "${VERS}.${REL}";
$VERSION    = eval $VERSION;
@ISA    = qw( Exporter );
@EXPORT = qw(
		addGroup
		addIP2Group
		checksIPList
		checksRevIpAdd
		doesGroupExistsList
		getsAllIPReceived
		getsCoordinates
		getsFileWithGroups
		getsGroupListFromList
		getsGPSCoordinates
		getsIpAddressFromGroup
		getsDFP
		isIPInGrp
		jcode jdecode
		myget
		store
		urlsAllowed 
	     );

@EXPORT_OK = qw( 
		addGroup
		addIP2Group
		checksIPList
		checksRevIpAdd
		doesGroupExistsList
		getsAllIPReceived
		getsCoordinates
		getsFileWithGroups
		getsGroupListFromList
		getsIpAddressFromGroup
		getsDFP
		isIPInGrp
		jcode jdecode
		myget
		store
		urlsAllowed 
       );


my $GROUP_FILE="groups";

# Written by shark bait ###

=head1 NAME

io::MySec.pm

$VERSION = '1.0.11.2'

=head1 ABSTRACT

This package manages stuff that deals with scuzzy data.

=head2 LIST OF subS

=over 4

addGroup
addIP2Group
checksIPList
checksRevIpAdd
doesGroupExistsList
getsAllIPReceived
getsCoordinates
getsFileWithGroups
getsGroupListFromLis
getsGPSCoordinates
getsIpAddressFromGroup
isIPInGrp
jcode
jdecode
myget
store
urlsAllowed 

=back

=head2 HISTORY OF MODIFICATIONS

=over 4

- I<Last modification: v1.0.11.2>  Aug 19 2011:  see getsGPSCoordinates

- I<Last modification: v1.0.9.12>  Aug 19 2011:  see getsAllIPReceived

- I<Last modification: v1.0.9.0>  Feb 10 2011:  modified getsAllIPReceived

- I<Last modification: v1.0.8.0>  Oct 15 2010: add jcode and jdecode function

- I<Last modification:> Jun 15 2010: add # in front of CONTINENT field

- I<Last modification:> Oct 04 2009: created the functions myget getsCoordinates.

- I<Last modification:> Sept 17 2009: created the function getsAllIPReceived

- I<Last modification:> Sept 08 2009: ping from package Net added.

- I<Last modification:> Sept 09 2009. Functions that checks IP address with ping. Ping is a programm.

- I<Last modification:> Aug 02 2009. Functions that deals with group access.

- I<Last modification:> Jul 22 2009. Variable just vanished. 

- I<Last modification:> Jul 21 2009. What a big day for a new package that deals with seciy issues.

- I<Starting date:> Jul 21 2009

=back

=cut

=head1 sub urlsAllowed(...)

Checks if the user is authorized.

=head2 PARAMETER(S)

=over 4

=over 4

@urlAllowed: urls allowed

=back

=back

=head2 RETURNED VALUE

=over 4

=over 4

Returns string Insert pictures or nothing.

($locallow,$agree)=link and ok if it is ok.
ok is a string as "ok".

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

- I<Last modification:> Dec 13 2011. gets_gps_coordinates added

- I<Last modification:> Jul 21 2009. Moved from album.cgi to MySec.pm package.

- I<Last modification:> Jul 20 2009. Allow administration to certain ip addresses.

- I<Last modification:> Jun 29 2009

- I<Last modification:> May 03 2008

- I<Last modification:> Apr 27 2008

- I<Created on:> Apr 20 2008

=back

=back

=cut

sub urlsAllowed { # Begin sub urlsAllowed
	my @urlAllowed=split(/\,/, io::MyUtilities::getUrlFromFile);
	my $ipaddr=io::MyNav::gets_ip_address ; # get IP address in order to print the right stuff on the screen 
	my $locallow="<!--time for a rest -->"; 
	my $agree="ko" ; 

	foreach my $urlAls (@urlAllowed){ # Begin foreach my $urlAl (@urlAllowed)
		my $urlAl=(split(/\|\|/,$urlAls))[0]; # gets url
		my $adm=(split(/\|\|/,$urlAls))[2]; # gets rights
#print "urlsAllowed-------->$urlAl eq $ipaddr<<<<<<<<<br>";
		if("$urlAl" eq "$ipaddr") { # Begin if("$urlAl" eq "$ipaddr")
			if($adm=~/Administration granted/){
				$locallow= "<a href=\"album.cgi?service=auth\"><font color=blue>Insert pictures</font> / Insérez photos</a><!-- $ipaddr -->";
			}
			$agree="ok";
		} # End if("$urlAl" eq "$ipaddr")
	} # End foreach my $urlAl (@urlAllowed)
	return ($locallow,$agree);
} # End sub urlsAllowed


=head1 sub getsFileWithGroups(...)

Loads the file that contains groups.

=head2 PARAMETER(S)

=over 4 

None.

=back

=head2 RETURNED VALUE

=over 4

Returns content of the given file name in an array.

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

- I<Modified on:> Aug 02 2009

- I<Created on:> jul 29 2009

=back

=cut

sub getsFileWithGroups{ # Begin sub getsFileWithGroups
	my @grpl=(); # group list

	open(FILE,"$GROUP_FILE") || die("Error $GROUP_FILE $!");
	@grpl=<FILE>;
	close(FILE) || die("Error $GROUP_FILE $!");
	return @grpl;
} # End sub getsFileWithGroups

=head1 sub getsGroupListFromList(...)

Builds group list from file stored in array.

=head2 PARAMETER(S)

=over 4 

@grpl: file (contains group list+ip address list associated) stored in an array.

=back

=head2 RETURNED VALUE

=over 4

Returns the list of all the groups in an array.

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

- I<Modified on:> Aug 02 2009

- I<Created on:> Aug 01 2009

=back

=cut

sub getsGroupListFromList{ # Begin sub getsGroupListFromList
	my (@grpl)=@_; # group list
	my @lgrpl=(); # group final list

	foreach (@grpl){ # Begin foreach (@grpl)
		@lgrpl=(@grpl,(split(/\|\|/,$_))[0]);
	} # End foreach (@grpl)
	return @lgrpl;
} # End sub getsGroupListFromList


=head1 sub getsIpAddressFromGroup(...)

Gets the list of ip addresses associated with the given group name.

=head2 PARAMETER(S)

=over 4 

${grn}: group name.
@grpl: file (contains group list+ip address list) stored in an array.

=back

=head2 RETURNED VALUE

=over 4

Returns ip list associated to group name. If none then returns an empty list.

=back

=head2 ERRROR RETURNED

=over 4

Empty list.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Modified on:> Aug 02 2009

- I<Created on:> Aug 02 2009

=back

=cut

sub getsIpAddressFromGroup{ # Begin sub getsIpAddressFromGroup
	my (${grn},@grpl)=@_; # Group name, group list
	my ${gr}=(); 

	foreach (@grpl){ # Begin foreach (@grpl)
		if($_=~m/^${grn}\|\|/){ # Begin if($_=~m/^${grn}\|\|/)
			${gr}=$_;
			${gr}=~s/^${grn}\|\|//;
			return ${gr}; # list
		} # End if($_=~m/^${grn}\|\|/)
	} # End foreach (@grpl)
	return ${gr}; # nothin
} # End sub getsIpAddressFromGroup

=head1 sub doesGroupExistsList(...)

Checks if group name exists from the array.

=head2 PARAMETER(S)

=over 4 

${grn}: Group name
@grpl: file (contains group list+ip address list associated) stored in an array.

=back

=head2 RETURNED VALUE

=over 4

0 if exists otherwise -1.

=back

=head2 ERRROR RETURNED

=over 4

Empty list.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Modified on:> Aug 02 2009

- I<Created on:> Aug 02 2009

=back

=cut

sub doesGroupExistsList{ # Begin sub doesGroupExists
	my (${grn},@grpl)=@_; # Group name, group list

	foreach (@grpl){ # Begin foreach (@grpl)
		if($_=~m/^${grn}\|\|/){ # Begin if($_=~m/^${grn}\|\|/)
			return 0;
		} # End if($_=~m/^${grn}\|\|/)
	} # End foreach (@grpl)
	return -1;
} # End sub doesGroupExists

=head1 isIPInGrp

Checks if ip address belongs to group.

=head2 PARAMETER(S)

=over 4 

${name}: group name
${ip}: ip address
@grp: fle loaded in array

=back

=head2 RETURNED VALUE

=over 4

0 if exists otherwise -1.

=back

=head2 ERRROR RETURNED

=over 4

Empty list.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Modified on:> Aug 02 2009

- I<Created on:> Aug 02 2009

=back

=cut

sub isIPInGrp{ # Begin sub checksFileGrp
	my (${name},${ip},@grp)=@_; # group name; ip address;fle loaded in array

	foreach (@grp){ # Begin foreach (@grp)
		if($_=~m/${name}\|\|/){ # Begin if($_=~m/${name}\|\|/)
			if(!&checksIPList(${ip},$_)){ # Begin if(!&checksIPList(${ip},$_))
				return 0;
			} # End if(!&checksIPList(${ip},$_))
		} # End if($_=~m/${name}\|\|/)
	} # End foreach (@grp)
	return -1;
} # End sub checksFileGrp


=head1 checksIPList

Checks if IP is in the given list.

=head2 PARAMETER(S)

=over 4 

${ip}: ip address.
@group: fle loaded in array.

=back

=head2 RETURNED VALUE

=over 4

0 if exists otherwise -1.

=back

=head2 ERRROR RETURNED

=over 4

Empty list.

=back

=head2 BUG KNOWN

=over 4

None.

=back

=head2 HISTORY OF CREATION/MODIFICATION

=over 4

- I<Modified on:> Aug 02 2009

- I<Created on:> Aug 02 2009

=back

=cut

sub checksIPList{ # Begin sub checksIPList
	my (${ip},${group})=@_ ; # ip address; group

	foreach (split(/\|\|/,${group})) { # Begin foreach my $i in (split(/\|\|/,${group}))
		if($_=~m/^${ip}$/){ # Begin if($i=~m/^${ip}$/)
			return 0;
		} # End if($i=~m/^${ip}$/)
	} # End foreach my $i in (split(/\|\|/,${group}))
	return -1;
} # End sub checksIPList


=head1 addGroup

Add a group.

=head2 PARAMETER(S)

=over 4 

${nogta}: Name of the group to add.
@grpl: file (contains group list+ip address list associated) stored in an array.

=back

=head2 RETURNED VALUE

=over 4

New list with new group if it does not already did.

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

- I<Modified on:> Aug 02 2009

- I<Created on:> Aug 02 2009

=back

=cut

sub addGroup{ # Begin sub addGroup
	my(${nogta},@grpl)=@_ ; # Name of the group to add; Group list

	if(&doesGroupExistsList(${nogta},@grpl)<0){ # Begin if(&doesGroupExistsList(${nogta},@grpl)<0)
		@grpl=(@grpl,"${nogta}||"); # Grop added
	} # End if(&doesGroupExistsList(${nogta},@grpl)<0)
	return @grpl;
} # End sub addGroup

=head1 sub store(...)

Store new list

=head2 PARAMETER(S)

=over 4 

@f: content of the new file to store.

=back

=head2 RETURNED VALUE

=over 4

none

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

- I<Modified on:> Aug 02 2009

- I<Created on:> jul 29 2009

=back

=cut

sub store{ # Begin sub store
	my (@f)=@_; # file to store
	open(FILE,">$GROUP_FILE") || die("Error $GROUP_FILE $!");
	foreach (@f){ # Begin foreach (@f)
		chomp($_);
		print FILE "$_\n";
	} # End foreach (@f)
	close(FILE) || die("Error $GROUP_FILE $!");
} # End sub store

=head1 addIP2Group

Adds a group.

=head2 PARAMETER(S)

=over 4 

${ip}: IP address to a given group.
${nogta}: Name of the group to add.
@grpl: file (contains group list+ip address list associated) stored in an array.

=back

=head2 RETURNED VALUE

=over 4

New list with new IP in group if group exists and IP not already in.

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

- I<Modified on:> Aug 02 2009

- I<Created on:> Aug 02 2009

=back

=cut

sub addIP2Group{ # Begin sub addIP2Group
	my(${ip},${nogta},@grpl)=@_ ; # IP to add to a given group; Name of the group; Group list

	foreach (@grpl){ # Begin foreach (@grpl)
		if($_=~m/^${nogta}\|\|/){ # Begin if($_=~m/^${nogta}\|\|/)
			if(&checksIPList(${ip},$_)<0){ # Begin if(&checksIPList(${ip},$_)<0)
				chomp($_);
				$_.="${ip}||\n"; # IP added to group
			} # End if(&checksIPList(${ip},$_)<0)
		} # End if($_=~m/^${nogta}\|\|/)
	} # End foreach (@grpl)
	return @grpl;
} # End sub addIP2Group

=head1 sub checksRevIpAdd(...)

Checks if ip address if correct

=head2 PARAMETER(S)

=over 4 

@{host}: list of ip address received. 

=back

=head2 RETURNED VALUE

=over 4

0 if ok otherwise -1.

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

- I<Modified on:> Sept 08 2009: ping from package Net added.

- I<Modified on:> Sept 07 2009

- I<Created on:> Sept 07 2009

=back

=cut

sub checksRevIpAdd{ # Begin sub checksRevIpAdd
	my (@host)=@_;# list of ip address(es)
	my $op = Net::Ping->new();

	#print "<br>".scalar @host ;
	foreach (@host){ # Begin foreach (split(/\n/,$des))
		#print "<br>\nMySec====>$_<br>".  $op->ping($_) ."<br>";
		if ($op->ping($_)){ # if ip is ok returns 0
			$op->close();
			#print "<br>ok\n";
			return (0,$_);
		}
	} # End foreach (split(/\n/,$des))
	$op->close();
	#print "<br>not ok\n";
	return (-1,0);
} # End sub checksRevIpAdd


=head1 sub getsAllIPReceived(...)

Gets all ip received from ifconfig.

=head2 PARAMETER(S)

=over 4 

None.

=back

=head2 RETURNED VALUE

=over 4

List of ip gotten from commad ifconfig for the time being.
None if there is an eror.

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

- I<Modified on:> Aug 19 2011: tests enhance for ifconfig

- I<Modified on:> Sept 17 2009: gets ip addresses

- I<Created on:> Sept 17 2009

=back

=cut

sub getsAllIPReceived{ # Begin sub getsAllIPReceived
	my @z=();# contains ip list
	my $ifconf=();# path to ifconfig
	my $des=();# will contain the result of ifconfig command execution
	my $PATH="$ENV{'PATH'}:/sbin";

	$ifconf=`export PATH="$PATH";which ifconfig`;# That's where the file ifconfig is
	chomp($ifconf);
	return @z if (!-f "$ifconf");
	$des=`$ifconf`;# contains the result of ifconfig command execution
	if(-f "album/debug_album_DO_NOT_REMOVE"){ # begin if(-f "album/debug_album_DO_NOT_REMOVE")
		print "<br>oooo)$ENV{'PATH'} after modif $PATH to $ifconf<br>$des<br>";
	} # end if(-f "album/debug_album_DO_NOT_REMOVE")

	return @z if (length($des)<=0);# case command does not exist
	foreach (split(/\n/,$des)){ # Begin foreach (split(/\n/,$des))
		if($_=~m/inet/){ # Begin if($_=~m/inet/)
			my $os=`uname -s`; chomp($os);# os name
			my ($a,$b)=();# used to fragment ifconfig lines

			# according to os version there is ifconfig version too
			if($os=~m/(darwin||linux)/i){ # begin if($os=~m/darwin/i)
				$b=(split(/\:/,$_))[1];
				$a=(split(/ Bca/,$b))[0];# contains ip list
			} # end if($os=~m/darwin/i)
			else{ # begin else
				$a=(split(/\ /,$_))[1];# contains ip list
			} # end else
			@z=(@z,$a); # collect all ip addresses
			if(-f "album/debug_album_DO_NOT_REMOVE"){ # begin if(-f "album/debug_album_DO_NOT_REMOVE")
				print "test($os)----[IP]--->$a<br>\n";
			} # end if(-f "album/debug_album_DO_NOT_REMOVE")
		} # End if($_=~m/inet/)
	} # End foreach (split(/\n/,$des))
	return @z;
} # End sub getsAllIPReceived

=head1 sub myget(...)

Gets html result page from ip request.

=head2 PARAMETER(S)

=over 4 

IP address.

=back

=head2 RETURNED VALUE

=over 4

Gets page wth coordinate of ip (html page).

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

- I<Modified on:> Oct 04 2009

- I<Created on:> Oct 04 2009

=back

=cut

sub myget{ # Begin sub myget
	my ($ip)=@_;
	my $url = "http://maxwell-media.com/domain-city-country-geo-location-region/custom-ip-info-and-ip-lookup/ip_info.php?ip=${ip}&x=0&y=0";
	return get ${url};
} # End sub myget

=head1 sub getsCoordinates(...)

Gets coordinates result from ip request.

=head2 PARAMETER(S)

=over 4 

$ip: ip address

=back

=head2 RETURNED VALUE

=over 4

coordinates as an associative array.

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

- I<Modified on:> Oct 04 2009

- I<Created on:> Oct 04 2009

=back

=cut

sub getsCoordinates{ # Begin sub getsCoordinates
	my ($ip)=@_;
	my @content=split(/\n/,&myget($ip));
	my $line=();

	foreach my $k (@content){ # Begin foreach my $k (split(/\n/,$content))
		chomp($k);
		if($k=~m/td_var/i){ # Begin if($k=~m!td_var!i)
			$k=~s/(<[^<>]*>){1,}//g;
			$line.="$k";
		} # End if($k=~!td_var!i)
		elsif($k=~m/td_val/i){ # Begin elsif($k=~m!td_val!i)
			$k=~s/(<[^<>]*>){1,}//g;
			if(length($k)!=0){ # Begin if(length($k)!=0)
				$line.=":$k\n";
			} # End if(length($k)!=0)
			else { # Begin else 
				$line.=":NA\n";#NA: not available
			} # End else 
		} # End elsif($k=~m!td_val!i)
	} # End foreach my $k (split(/\n/,$content))
	$line=~s!CONTINENT!\#CONTINENT!g;
	return $line;
} # End sub getsCoordinates


=head1 sub jdecode(...)

Decode message with the signature given. This is the Jangada algorithm.

=head2 PARAMETER(S)

=over 4 

$signature: that's the signature given

$sentence: the sentence to decrypt

=back

=head2 RETURNED VALUE

=over 4

Sentence decrypted.

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

- I<Modified on:> Oct 04 2010

- I<Created on:> Oct 04 2010

=back

=cut

sub jdecode{ # Begin sub jdecode
	my ($signature,$sentence)=@_;# the signatur, the sentence to decrypt
	my @alph=();# alphabet
	my $answer=();# decrypted sentence
	my $se=();# length of the signature
	my $sc=();# size of the alphabet
	my $tal=();# size of the alphabet
	my $j=0;

	$se=length($signature);#calculate the length of the signature
	$sc=length($sentence);# size of the sentence

	# Init alphabet
	# set the alphabet
	for(my $i=1;$i<128;$i++){ # Begin for(my $i=1;$i<128;$i++)
		@alph=(chr($i),@alph);
	} # End for(my $i=1;$i<128;$i++)
	$tal=scalar(@alph);# calculate the size of the alphabet
	my $ok=();

	# go threw the sentence that is crypted
	for(my $i=0;$i<$sc;$i++){# Begin for(my $i=0;$i<$sc;$i++)
		my $k,$l,$v,$u;

		$ok=0;
		$v=substr($sentence,$i,1);
		for($k=0;$k<$tal;$k++){ # Begin for($k=0;$k<$tal;$k++)
			# we get the ank of the letter in the alphabet
			if($alph[$k] eq $v){ # Begin if($alph[$k] eq $v)
				# we get the current letter
				$u=substr($signature,$j,1);
				# Checks get raw for signature
				for($l=0;$l<$tal;$l++){ # Begin for($l=0;$l<$tal;$l++)
					# we get the ank of the letter in the alphabet
					if($alph[$l] eq $u){ # Begin if($alph[$l] eq $u)
#						$res=($k+$l)%$tal;
						if(($k+$l)>$tal){
							 $res=$tal-($k+$l);
						}else{
							$res= ($k+$l);
						}
						#print "--->$alph[$res] $answer\n";
						$ok=1;
						break;
					} # End if($alph[$l] eq $u)
				} # End for($l=0;$l<$tal;$l++)
				break; 
			} # End if($alph[$k] eq $v)
		} # End for($k=0;$k<$tal;$k++)
		# If we get a result
		if($ok==1){ # Begin if($ok==1)
			$answer.=$alph[$res]; # we concatenate the translated letter
		} # End if($ok==1)
		#print "ooooooooo)$answer\n";
		$j++;
		$j%=length($signature)
	}
	return $answer;
} # End sub jdecode


=head1 sub jcode(...)

Code message with the signature given. This is the Jangada algorithm.

=head2 PARAMETER(S)

=over 4 

$signature: that's the signature given

$sentence: the sentence to crypt

=back

=head2 RETURNED VALUE

=over 4

Sentence crypted.

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

- I<Modified on:> Oct 04 2010

- I<Created on:> Oct 04 2010

=back

=cut

sub jcode{ # Begin sub jcode
	my ($signature,$sentence)=@_;# the signature, and the sentence
	my $answer=();# crypted sentence
	my @alph=(); # alphabet
	my $j=0;
	my $se=();# length of the signature
	my $sc=();# size of the alphabet
	my $tal=();# size of the alphabet

	# Init alphabet
	# set the alphabet
	for(my $i=1;$i<128;$i++){ # Begin for(my $i=1;$i<128;$i++)
#		if(chr($i) ne '\\'){ # Begin if(chr($i) ne '\\')
			@alph=(chr($i),@alph);
#		} # End if(chr($i) ne '\\')
	} # End for(my $i=1;$i<128;$i++)
	#$i=0;
	#foreach (@alph){
#		print $i . " " . $_ . ",";
#		$i++;
#	}
	$se=length($signature);#calculate the length of the signature
	# gets new length of the sentence after transformation
	$sc=length($sentence);# size of the sentence
	#print "$sc $sentence\n";
	$tal=scalar(@alph);# calculate the size of the alphabet
	# go threw the sentence that is not crypted yet
	for(my $i=0;$i<$sc;$i++){ # Begin for(my $i=0;$i<$sc;$i++)
		my $k,$l,$v,$u;

		# we get the current letter
		$v=substr($sentence,$i,1);
		# we get the ank of the letter in the alphabet
		for($k=0;$k<$tal;$k++){# Begin for(my $i=0;$i<$sc;$i++)
			# We check for the rank of the letter in a given alphabet
			if($alph[$k] eq $v){ # Begin if($alph[$k] eq $v)
				# we get the current letter for the signature
				$u=substr($signature,$j,1);# we get on character from signature
				for($l=0;$l<$tal;$l++){ # Begin for($l=0;$l<$tal;$l++)
					# We check for the rank of the letter in a given alphabet
					if($alph[$l] eq $u){ # Begin if($alph[$l] eq $u)
						#print "----\n";
				#		$res=($k-$l)%$tal;
						$sub=$k-$l;
						if($sub<0){
							 $res=$tal+$sub;
						}else{
							$res=$sub;
						}
#						print "$res $alph[$res],";
						break;
					} # End if($alph[$l] eq $u)
				} # End for($l=0;$l<$tal;$l++)
				break; 
			} # End if($alph[$k] eq $v)
		}# End for(my $i=0;$i<$sc;$i++)
		#print " $res $alph[$res] $v $answer $tal\n";
		$answer.=$alph[$res]; # we concatenate
		$j++;
		$j%=length($signature)
	} # End for(my $i=0;$i<$sc;$i++)
	return $answer;
} # End sub jcode


=head1 sub getsGPSCoordinates(...)

Gets gps coordinates.

=head2 PARAMETER(S)

=over 4 

none.

=back

=head2 RETURNED VALUE

=over 4

That's an array that contains longitude and latitude.

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

- I<Modified on:> Dec 13 2011

- I<Created on:> Dec 13 2011

=back

=cut

sub getsGPSCoordinates{ # begin sub getsGPSCoordinates
	my $ipAddr=io::MyNav::gets_ip_address;
	my @res=split(/\n/,io::MySec::getsCoordinates(${ipAddr}));
	$res[6]=~s/[a-zA-Z]*://g;
	$res[7]=~s/[a-zA-Z]*://g;
	return ($res[6],$res[7]);
} # end sub getsGPSCoordinates


=head1 sub getsDFP (...)

Gets device's finger print.

=head2 PARAMETER(S)

=over 4 

none.

=back

=head2 RETURNED VALUE

=over 4

That's a string that returns the device's finger print.

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

- I<Modified on:> Nov 26 2018

- I<Created on:> Nov 26 2018

=back

=cut

sub getsDFP { # Begin sub getsDFP
	my $ua = HTTP::BrowserDetect->new($ENV{'HTTP_USER_AGENT'});

	return &gets_fp(
		$ua->browser_string,
		$ua->browser,
		$ua->browser_version,
		$ua->browser_properties,
		$ua->browser_beta,
		$ua->os,
		$ua->device,
		$ua->mobile,
		$ua->tablet,
		$ENV{'HTTP_USER_AGENT'});

	sub gets_fp{ # Begin sub gets_fp
		my $finger_print=();

		foreach my $a (@_){ # Begin foreach my $a (@_)
			chomp($a);
			$finger_print.=$a . ",";
		} # End foreach my $a (@_)
		return $finger_print;
	} # End sub gets_fp
} # End sub getsDFP

1;

=head1 AUTHOR

Current maintainer: sebush, <sebush@laposte.net>

=cut
