package io::MyNav;
use CGI::Carp qw(fatalsToBrowser); 


# ------------------------------------------------------
q##//q#
* Created By : sdo
* File Name : MyNav.pm
* Creation Date : Wed Nov 30 22:51:08 2005
* @modify date 2020-06-03 02:18:18
* Email Address : sdo@linux.home
* Version : 0.0.0.0
* License:
*       Permission is granted to copy, distribute, and/or modify this document under the terms of the Creative Commons Attribution-NonCommercial 3.0
*       Unported License, which is available at http: //creativecommons.org/licenses/by- nc/3.0/.
* Purpose :
#;
# ------------------------------------------------------

# +-------------------------------+
# | MyNav.pm                      |
# | Last update on Jul 19 2009    |
# | Written     on Nov 30 2008    |
# +-------------------------------+

require Exporter;

use Fcntl qw( :DEFAULT :flock);
use Sys::Hostname;
use Socket;

my $VERS       = '1.0';
my $REL        = '14.40';
$VERSION    = "${VERS}.${REL}";
$VERSION    = eval $VERSION;
@ISA    = qw( Exporter );
@EXPORT = qw(
	gets_request_method
	gets_remote_user
	gets_server_name
	gets_server_address
	gets_full_url
	gets_server_name
	gets_remhost_address
	gets_ip_address
	gets_user_agent
	gets_navigtor_name
	gets_navigator_machine_info
	gets_navigator_info_I
	gets_user_agent_bp gets_user_agent_e
	gets_server_signature
	gets_all_user_agent_fields
	gets_url_base
	gets_path
	gets_user_name
	sets_url
	gets_user_log
	is_local_network_address
	     );

@EXPORT_OK = qw( 
	gets_request_method
	gets_remote_user
	gets_server_address
	gets_server_name
	gets_server_name
	gets_remhost_address
	gets_full_url
	gets_path
	gets_ip_address
	gets_user_agent
	gets_navigtor_name
	gets_navigator_machine_info
	gets_navigator_info_I
	gets_user_agent_bp gets_user_agent_e
	gets_server_signature
	gets_user_log
	gets_all_user_agent_fields
	gets_url_base
	gets_user_name
	sets_url
	is_local_network_address
	       );

# Written by shark bait ###

=head1 NAME

io::MyNav.pm

$VERSION = '1.0.14.8'

=head1 ABSTRACT

This package manages stuff that deals with data related to navigator

=head2 LIST OF FUNCTIONS

=over 4

gets_all_user_agent_fields
gets_server_name
gets_ip_address 
gets_navigator_info_I 
gets_navigator_machine_info 
gets_navigtor_name 
gets_remhost_address 
gets_remote_user 
gets_request_method
gets_server_address
gets_server_name
gets_server_signature
gets_url_base
gets_user_agent 
gets_user_agent_bp
gets_user_agent_e
gets_user_name
sets_url

=back

=head2 HISTORY OF MODIFICATIONS

=over 4

- I<Last modification:> Jun 03 2020 check sub gets_ip_address

- I<Last modification:> Jul 25 2009. Gets in the field $ENV{'HTTP_X_FORWARDED_FOR'}  last IP address (real one).

- I<Last modification:> Jul 19 2009. Look at fuction gets_ip_address 

- I<Last modification:> May 23rd 2009

- I<Last modification:> Nov 30th 2008

- I<Starting date:> Nov 30th 2008

=back

=cut

=head1 sub gets_user_agent(...)

This function gets data from navigator

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

Sting that deals with navgator.

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

- I<Last modification:> Nov 30 2008

- I<Created on:> Nov 30 2008

=back

=cut

sub gets_user_agent { # begin sub gets_user_agent
	return $ENV{'HTTP_USER_AGENT'};
} # end sub gets_user_agent

=head1 sub gets_navigtor_name(...)

This function gets name + vers of navigator

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

Navigator name, version of navigator.

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

- I<Last modification:> Dec 01 2008

- I<Created on:> Nov 30 2008

=back

=cut

sub gets_navigtor_name { # begin sub getNavNam
	my ($u,$m) = (split(/\(/,
			$ENV{'HTTP_USER_AGENT'}
			));
	return (
		$u
		#(split(/\//,$u))[0],
		#(split(/\//,$u))[1]
		 );
} # end sub getNavNam

=head1 sub gets_navigator_machine_info(...)

This function gets info about navigator

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

Array that is between parenthesis

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

- I<Last modification:> Dec 03 2008

- I<Created on:> Dec 03 2008

=back

=cut

sub gets_navigator_machine_info { # begin sub gets_navigator_machine_info
	my ($u,$m) = (split(/\(/,
			$ENV{'HTTP_USER_AGENT'}
			));
	my ($bepar,$oth)=split(/\)/,$m);
	return (split(/\;/,$bepar));
} # end sub gets_navigator_machine_info

=head1 sub gets_navigator_info_I(...)

This function gets info about navigator info (...) info (...

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

Array that is between parenthesis

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

- I<Last modification:> Dec 17 2008

- I<Created on:> Dec 06 2008

=back

=cut

sub gets_navigator_info_I { # begin sub gets_navigator_info_I
	my ($h,$m) = split(/\)/,$ENV{'HTTP_USER_AGENT'});
	my ($h,$j) = split(/\(/,$m);
	my ($h,$n) = split(/\(/,$j);
	my ($l,$r)=split(/\,/,$h);
	return ($l,$r);
} # end sub gets_navigator_info_I

=head1 sub gets_user_agent_bp(...)

Returns field bp from user agent.

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

Array that is between parenthesis

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

- I<Last modification:> Dec 17 2008

- I<Created on:> Dec 06 2008

=back

=cut

sub gets_user_agent_bp { # begin sub gets_user_agent_bp
	my ($u,$v)=split(/\)/,$ENV{'HTTP_USER_AGENT'});
	my ($k,$l)=split(/\(/,$v);
	return $k;
} # end sub gets_user_agent_bp

=head1 sub gets_user_agent_e(...)

This function gets last field after information after last ) rom UA .

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

Last field after last ) from UA.

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

- I<Last modification:> Dec 17 2008

- I<Created on:> Dec 06 2008

=back

=cut

sub gets_user_agent_e { # begin sub gets_user_agent_e
	my ($u,$v,$w)=split(/\)/,$ENV{'HTTP_USER_AGENT'});
	return $w;
} # end sub gets_user_agent_e

=head1 sub gets_all_user_agent_fields(...)

This function gets info about User agent (navigator info) (...) info (...

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

The string from UA as an array: delimiters are ;  

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

- I<Last modification:> Dec 24 2008

- I<Created on:> Dec 06 2008

=back

=cut

sub gets_all_user_agent_fields { # begin gets_all_user_agent_fields
	return (
		gets_navigtor_name,
		gets_navigator_machine_info,
		gets_user_agent_bp ,
		gets_navigator_info_I,
		gets_user_agent_e);
} # end  gets_all_user_agent_fields

=head1 sub gets_server_signature(...)

This function gets server signature.

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

Returns serveur signature.

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

- I<Last modification:> May 01 2009

- I<Created on:> Jan 30 2009

=back

=cut

sub gets_server_signature{ # begin gets_server_signature
	return $ENV{SERVER_SIGNATURE};
} # end gets_server_signature

=head1 sub gets_server_name(...)

Gets the server name.

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

Returns the server name.

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

- I<Last modification:> Dec 01 2008

- I<Created on:> Nov 30 2008

=back

=cut

sub gets_server_name{ # begin gets_server_name
	return $ENV{SERVER_NAME};
} # end gets_server_name

=head1 sub gets_ip_address(...)

This function that returns ip adress

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

IP address.

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

- I<Modified on:> Jun 03 2020. function reshaped entirely

- I<Modified on:> Jul 25 2009. Gets in the field $ENV{'HTTP_X_FORWARDED_FOR'}  last IP address (real one).

- I<Modified on:> Jul 19 2009. Checks for X-Forwarded-For field.

- I<Modified on:> Nov 30th 2008

- I<Modified on:> Nov 17th 2008

- I<Created on:> Sep 2sd 2006

=back

=cut

sub gets_ip_address { # begin sub gets_ip_address
	my $serv_addr=inet_ntoa((gethostbyname(hostname))[4]);
	my $remote_addr=$ENV{'REMOTE_ADDR'} if defined $ENV{'REMOTE_ADDR'};

	if ( $serv_addr !~ m/^$remote_addr$/) {
		#print "distant<br>";
		#print "1.1 distant address ". $remote_addr  . "<br>";
		#print "1.2 local address ". $serv_addr  . "<br>";
		return $remote_addr;
	} else {
		#print "local<br>";
		#print "2.1 distant address ". $remote_addr  . "<br>";
		#print "2.2 local address ". $serv_addr  . "<br>";
		return $serv_addr;
	}
} # end sub gets_ip_address

=head1 sub gets_remhost_address(...)

This function that returns ip adress

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

Remote host address or IP address.

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

- I<Modified on:> Dec 21 2008

- I<Created on:> Dec 21 2008

=back

=cut

sub gets_remhost_address { # begin sub gets_remhost_address
	return $ENV{REMOTE_HOST} || $ENV{REMOTE_ADDR};
} # end sub gets_remhost_address

=head1 sub gets_server_address(...)

Gets server address.

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

The adress of the server as a string.

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

- I<Modified on:> Dec 21 2008

- I<Created on:> Dec 21 2008

=back

=cut

sub gets_server_address{ # begin sub gets_server_address
	return $ENV{SERVER_ADDR} ; 
} # end sub gets_server_address

=head1 sub gets_remote_user(...)

Gets server address.

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

The adress of the server as a string.

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

- I<Modified on:>  May 21 2009

- I<Modified on:> Dec 21 2008

- I<Created on:> Dec 21 2008

=back

=cut

sub gets_remote_user { # begin sub gets_remote_user
	return $ENV{REMOTE_USER};
} # end sub gets_remote_user

=head1 sub gets_request_method(...)

Gets method.

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

Variable of environment.

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

- I<Modified on:>  May 21 2009

- I<Created on:> May 21 2009

=back

=cut

sub gets_request_method{ # begin sub gets_request_method
	return $ENV{REQUEST_METHOD};
} # end sub gets_request_method


=head1 sub gets_url_base(...)

Returns url.

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

A string with url.

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

- I<Modified on:> May 20 2009

- I<Created on:> May 20 2009

=back

=cut

sub gets_url_base{ # begin sub gets_url_base
	my ${url}=$ENV{SERVER_NAME};
	${url}.="/";
 	${url}.=(split(/\\\//,$ENV{SCRIPT_NAME}))[1];
	#print "---->$url\n<br>";
	return ${url};
} # end sub gets_url_base


=head1 sub gets_user_name(...)

Gets user name

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

Returns the name as a string.

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

- I<Modified on:> May 20 2009

- I<Created on:> May 20 2009

=back

=cut

sub gets_user_name{ # begin sub gets_user_name
	my $o=(split(/\//,$ENV{SCRIPT_NAME}))[1];
	$o=~s/\~//g;
	return $o;
} # end sub gets_user_name

=head1 sub gets_user_log(...)

Gets user log name

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

Returns the log name as a string.

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

- I<Modified on:> Jun 15 2009

- I<Modified on:> May 20 2009

- I<Created on:> May 20 2009

=back

=cut

sub gets_user_log{ # begin sub gets_user_log
	my $o=(split(/\//,$ENV{SCRIPT_NAME}))[1];
	return $o;
} # end sub gets_user_log


=head1 sub gets_path(...)

Returns path as url.

=head2 PARAMETER(S)

=over 4

$cp: context

$un: user name

=back

=head2 RETURNED VALUE

=over 4

Returns url with user name  and path.

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

- I<Modified on:> May 30 2009

- I<Created on:> May 30 2009

=back

=cut

sub gets_path{ # begin sub gets_path
	my ($cp,$un)=@_; # $cp: context ; $un: user name
	$un=~s/\~//g;

	return "$a" ;
} # end sub gets_path


=head1 sub gets_full_url(...)

Returns path as url.

=head2 PARAMETER(S)

=over 4

${mycontext}: Context path.

=back

=head2 RETURNED VALUE

=over 4

Returns url with user name  and path.

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

- I<Modified on:> jun 6 2009

- I<Modified on:> May 30 2009

- I<Created on:> May 30 2009

=back

=cut

sub gets_full_url{ # begin sub gets_full_url
	my (${mycontext})=@_;
	my $o="http://" . 
		&gets_url_base . 
		&gets_user_log . 
		&gets_path(${mycontext},&gets_user_log);
#	print "====>$o<br>";
	return $o;
} # end sub gets_full_url

=head1 sub sets_url(...)

Returns url with user name  and path.

=head2 PARAMETER(S)

=over 4 
Context path.

=back

=head2 RETURNED VALUE

=over 4

Returns url with user name  and path.

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

- I<Modified on:> May 20 2009

- I<Created on:> May 20 2009

=back

=cut

sub sets_url{ # begin sub sets_url
	my (${path})=@_; # path 
	my ${usr}=&gets_user_name;
	my ${mp}=(split(/${usr}/,${path}))[1];
	${usr}=&gets_url_base;
	return "${usr}/${mp}";
} # end sub sets_url

=head1 sub installDirectory(...)

Returns account where files for web are installed by default.

=head2 PARAMETER(S)

=over 4 

None.

=back

=head2 RETURNED VALUE

=over 4

Returns path

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

- I<Modified on:> May 21 2009

- I<Created on:> May 20 2009

=back

=cut

sub installDirectory{ # begin sub installDirectory
	my ${MY_REQUEST_URI}=$ENV{'REQUEST_URI'};
	my ${MY_SCRIPT_FILENAME}=$ENV{'SCRIPT_FILENAME'};
	my @a=();

	@a=split(/\//,${MY_REQUEST_URI});
	$a[1]=~s/\~//;
	${MY_SCRIPT_FILENAME}=~s/.*$a[1]//; # supress user account
	${MY_SCRIPT_FILENAME}=~s/$a[2].*//; # suppress cgi script
	${MY_SCRIPT_FILENAME}=~s/\///g; # we remove / character
	return ${MY_SCRIPT_FILENAME} ; 
} # end sub installDirectory

=head1 sub gets_server_name(...) 

Returns host name

=head2 PARAMETER(S)

=over 4 

None.

=back

=head2 RETURNED VALUE

=over 4

Returns host name

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

- I<Modified on:> Jul 04 2009

- I<Created on:> Jul 04 2009

=back

=cut

sub gets_server_name { # begin sub gets_server_name
	return $ENV{SERVER_NAME};
} # end sub gets_server_name

=head1 sub is_local_network_address(...)

This function that returns true if local network address.

=head2 PARAMETER(S)

=over 4

None.

=back

=head2 RETURNED VALUE

=over 4

True if local network else false.

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

- I<Created on:> Jun 03 2020. function reshaped entirely

=back

=cut

sub is_local_network_address { # begin sub is_local_network_address
	my $serv_addr=inet_ntoa((gethostbyname(hostname))[4]);
	my $remote_addr=$ENV{'REMOTE_ADDR'} if defined $ENV{'REMOTE_ADDR'};

	if ( $serv_addr !~ m/^$remote_addr$/) {
		#print "distant<br>";
		#print "1.1 distant address ". $remote_addr  . "<br>";
		#print "1.2 local address ". $serv_addr  . "<br>";
		return false;
	} else {
		#print "local<br>";
		#print "2.1 distant address ". $remote_addr  . "<br>";
		#print "2.2 local address ". $serv_addr  . "<br>";
		return true;
	}
} # end sub is_local_network_address

1;

=head1 AUTHOR

Current maintainer: sebush, <sebush@laposte.net>

=cut
