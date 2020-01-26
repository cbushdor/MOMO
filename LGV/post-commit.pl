#!/usr/bin/perl-5.30.1
# #!/opt/local/bin/perl 

use 5.010;

# ------------------------------------------------------
q##//q#
* Created By : sdo
* File Name : post-commit.pl
* Creation Date : Mon Sep 17 00:58:28 2018
* @modify date 2020-01-14 03:23:17
* Email Address : sdo@macbook-pro-de-sdo.home
* Version : 0.0.0.0
* License:
* 	Permission is granted to copy, distribute, and/or modify this document under the terms of the Creative Commons Attribution-NonCommercial 3.0 
* 	Unported License, which is available at http: //creativecommons.org/licenses/by- nc/3.0/.
* Purpose :
#;
# ------------------------------------------------------


use Scalar::Util 'blessed';
use POSIX qw(strftime);
use Cwd;
use File::Basename;
use Data::Dumper qw(Dumper);

use strict;
use warnings;
use Net::Twitter::Lite::WithAPIv1_1;
use Try::Tiny;

use constant MAX_CHAR_COMMENT => 50;
use constant MAX_CHAR_BRANCH_NAME => 20;

sub tweet
{
  my ($text) = @_;

  die 'tweet requires text as an argument' unless $text;

  unless ($ENV{TWITTER_CONSUMER_KEY}
          && $ENV{TWITTER_CONSUMER_SECRET}
          && $ENV{TWITTER_ACCESS_TOKEN}
          && $ENV{TWITTER_ACCESS_SECRET})
  {
    die 'Required Twitter Env vars are not all defined';
  }

  try
  {
    my $twitter = Net::Twitter::Lite::WithAPIv1_1->new(
      access_token_secret => $ENV{TWITTER_ACCESS_SECRET},
      consumer_secret     => $ENV{TWITTER_CONSUMER_SECRET},
      access_token        => $ENV{TWITTER_ACCESS_TOKEN},
      consumer_key        => $ENV{TWITTER_CONSUMER_KEY},
      user_agent          => 'TwitterBotExample',
      ssl => 1,
    );
    $twitter->update($text);
  }
  catch
  {
    die join(' ', "Error tweeting $text",
                   $_->code, $_->message, $_->error);
  };
}


my $curpa=getcwd();# We save the current path
my $datestring = strftime '%Y-%m-%d_%H:%M:%S', localtime(); # set date format + time format
my $mpwd=`git rev-parse --git-dir`;# we get the path home repository
my $dir_store="bkUps";# Where are data?

chomp($mpwd); # We remove last character \n
chdir("$mpwd"); # We got to directory

if(! -d "$dir_store"){ # Begin If directory does not exist
	mkdir("$dir_store")||die("Error: $!\n"); # We create the directory to store message to send
} # End If directory does not exist
chdir("$dir_store")||die("Error: $!\n"); # We go into the directory

#open(R,"<credential_twitter.txt")||die("Error: $!\n");
#my @l=<R>;
#close(R)||die("Error: $!\n");
#my ($mtwitter,$consumer_key,$consumer_secret,$token,$token_secret)=@l;
#chomp($mtwitter);
#chomp($consumer_key);
#chomp($consumer_secret);
#chomp($token);
#chomp($token_secret);
chdir($curpa);

#my $nt = Net::Twitter->new(
#traits   => [qw/API::RESTv1_1/],
#consumer_key        => $consumer_key,
#consumer_secret     => $consumer_secret,
#access_token        => $token,
#access_token_secret => $token_secret,
#); # Set file handler for twitter account

my $remoteOrigin=`git config remote.origin.url`; # Got url with .git
$remoteOrigin=~m/\/([^\/\n]+\/[^\/\n]+)(.git){0,1}$/i; # Select the name in $1
my $baseName=$1; # Gets base name of the repo
chomp($baseName); # Remove end character \n
$baseName=~s/(.git){0,1}$//i; # Remove .git end characters
my $myHashValueCommit=`git log -n 1 --pretty=format:"%H"`; # Get hash value to reach info on repo
my $whoDidIt=`git var GIT_COMMITTER_IDENT`; # Get committer info 
chomp($whoDidIt); # Remove end character \n
my $curBranch=`git branch`; # We get the all the branch names

# Find branch name and concatenate if lenght >MAX_CHAR_BRANCH_NAME with ...
foreach my $mlb (split(/\n/,$curBranch)){ # Begin enter the loop 
	if ($mlb=~m/^\ *\*\ /){ # Begin Check for selected branch
		$mlb=~s/^\ *\*\ *//; # We remove the selected
		$curBranch=(length("$mlb") >MAX_CHAR_BRANCH_NAME ) ? substr($mlb,0,MAX_CHAR_BRANCH_NAME-1)."...":$mlb; # We concatenate ... if larger >MAX_CHAR_BRANCH_NAME
		#print "----------------------------->$curBranch\n";
	} # End Check for selected branch
} # End enter the loop 

open(R,getcwd()."/.git/COMMIT_EDITMSG")||die("Error $!");
my $commit_msg=<R>;
close(R)||die("Error $!");
chomp($commit_msg);
my $mtosend=(); # Message to send

$remoteOrigin=~s/(.git){0,1}$/\/commit\/$myHashValueCommit/; # We create the url to get the committed info
if(length($commit_msg)>=MAX_CHAR_COMMENT){ # Begin Truncate the message
	$mtosend="$whoDidIt\n[$baseName,$curBranch] ". substr($commit_msg,0,MAX_CHAR_COMMENT-1) ."...\n$remoteOrigin"; # Message to send
} # End Truncate the message
else { # Begin Orignal message
	$mtosend="$whoDidIt\n[$baseName,$curBranch] $commit_msg\n$remoteOrigin"; # Message to send
} # End Orignal message

my $lt=localtime(); # We create memory to get time 
open(W,">bakups_${lt}_$$.txt") || die("Error: $!\n");# We create a file to store the message
print W "$mtosend"; # We store data
close(W) || die("Error: $!\n"); # We close file
opendir(my $dh,".") || die("Error: $!\n"); # We read current directory
my @f=sort { (stat($a))[9] <=> (stat($b))[9] }  grep { !/^\.{1,2}$/ && /^bakups\_[a-zA-Z\ \:0-9]+\_[0-9]+\.txt$/ } readdir($dh); # We store in an array file that old messages
closedir $dh || die("Error: $!\n"); # We close directory
foreach my $fn (@f){ # Begin Read file list
	open(R,"<$fn") || die("Error: $_\n"); # We open a file
	my @u=<R>; # We create a memory and we store the file content
	close(R)||die("Error:$$\n");# We close the file
	$datestring = strftime '%Y-%m-%d_%H:%M:%S', localtime(); # Calculte the date before sending
	$mtosend=join("",("$datestring\n",@u)); # create a memory that old content of current file as and array in a string
	#my $result = $nt->update("$mtosend"); # We sendout the string to twitter account
	tweet("$mtosend"); # We sendout the string to twitter account
	if(my $err=$@){ # Begin We check if error occured
		warn  "HTTP Response Code: ",$err->code, "\n"; # If there is an error we printout the code of error
	} # End We check if error occured
	else { # Begin else 
		print "Remove $fn\n"; # Prompt that the message will be destroyed because it was well sent
		unlink($fn) || die("Error: $$\n"); # We remove the file
	} # End else 
} # End Read file list
chdir("$curpa"); # We come back to the current path from the begining
