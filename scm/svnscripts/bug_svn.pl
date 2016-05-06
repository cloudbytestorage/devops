#!/usr/bin/perl
# The contents of this file are subject to the Mozilla Public License
# Version 1.1 (the "License"); you may not use this file except in
# compliance with the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
# 
# Software distributed under the License is distributed on an "AS IS"
# basis, WITHOUT WARRANTY OF ANY KIND, either express or implied. See the
# License for the specific language governing rights and limitations
# under the License.
# 
# The Original Code is svn_bz_append.pl
# 
# The Initial Developer of the Original Code is Toby Thain.
# Portions created by Toby Thain are
# Copyright (C) Toby Thain <toby at telegraphics.com.au>. All Rights Reserved.
# 
# Contributor(s): Toby Thain, Matthew Curry
# Portions created by Matthew Curry are
# Copyright (C) Matthew Curry <mcurry at skarven.net>. All Rights Reserved.
#
# Based in part on Sean M. Foy's mail.pl 
# (http://sean-janus.optionpc.com/me/software/bugtraq/)

# works with Bugzilla 3.0.4; may require modification for other versions

# for Bugzilla 2.x, see http://www.telegraphics.com.au/svn/svn_bz/tags/

use strict;
use warnings;
#use Text::Wrap;
use Data::Dumper;
use lib qw(. lib);

BEGIN {
	chdir "/var/www/html/bugzilla";
	push @INC, "contrib";
	push @INC, "."; 
}
use Bugzilla;
use Bugzilla::Config;
use Bugzilla::Bug;

print STDERR "-"x10," commit hook\n";

die "usage: ",__FILE__," REPO_PATH REVISION" unless $#ARGV > 0;

my ($repo,$bugid,$rev) = @ARGV;
print STDERR "repo: $repo\n";

my $author = "cbauto\@cloudbyte.com";

# Find Bugzilla login from Svn committer user name.

# You will probably need to customise this for your site.
my @rec = Bugzilla->dbh->selectrow_array("SELECT login_name,userid FROM profiles \
         WHERE login_name = \'$author\';");
# this version assumes that Svn users are named fsmith (initial+surname) 
# and Bugzilla users are of the form fred.smith@some.domain
# my @rec = Bugzilla->dbh->selectrow_array("SELECT login_name,userid FROM profiles \
#          WHERE locate(\'.\',login_name)<locate(\'@\',login_name) \
#          and lower(concat(left(login_name,1),substring(login_name,locate(\'.\',login_name)+1, \
#                    locate(\'@\',login_name)-locate(\'.\',login_name)-1))) = \'$author\';");
my $login_name = shift @rec;
my $userid = shift @rec;
die("Bugzilla login_name not found for $author\n") unless defined($login_name) and defined($userid);
print STDERR "author $author -> login_name '$login_name', userid '$userid'\n";

my $message = "REPO=$repo  BUGID=$bugid REVISION=$rev auto updated by $author\n";
print STDERR $message;

# for docs about bugtraq properties, see
#  http://svn.collab.net/viewcvs/tortoisesvn/trunk/doc/issuetrackers.txt
 
# whatever the user enters for %BUGID%
#my $bugpat = '(bug|issue)s?\s*([\d\s,#]+)';
my $bugpat = '\[BUG-([\d\s,#]+)\]';

# Get bug number(s)

my @bugs;
#my $log = "[BUG-9000] STORE the log here";
#$message .= $log;

my $messagefile = "/etc/bugzilla.log";
local $/ = undef;
open my $INPUT, $messagefile or die "Unable to open '$messagefile': $!";
my $content = <$INPUT>;
close $INPUT or die $!;
$message .= $content;


#test the repository for proper viewvc url
if ( $repo eq  "/svnrepo/esmgmt" )
{
my $repository = "esmgmt";
my $viewvcurl = "\nhttp://10.10.1.102/viewvc/$repository?view=revision&revision=$rev \n";
$message .= $viewvcurl;
}

if ( "$repo" eq  "/svnrepo/esbuild" )
{
my $repository = "esbuild";
my $viewvcurl = "\nhttp://10.10.1.102/viewvc/$repository?view=revision&revision=$rev \n";
$message .= $viewvcurl;
}

if ( "$repo" eq  "/svnrepo/esos" )
{
my $repository = "esos";
my $viewvcurl = "\nhttp://10.10.1.102/viewvc/$repository?view=revision&revision=$rev \n";
$message .= $viewvcurl;
}

if ( "$repo" eq  "/svnrepo/esports" )
{
my $repository = "esports";
my $viewvcurl = "\nhttp://10.10.1.102/viewvc/$repository?view=revision&revision=$rev \n";
$message .= $viewvcurl;
}

#viewvc repo testing done

#my $viewvcurl = "\nhttp://10.10.1.102/viewvc/esmgmt?view=revision&revision$rev \n";
#$message .= $viewvcurl;
#print STDERR "log: $log\n";
# extract bug list, if present
#while($log =~ /$bugpat/gsi){ @bugs = (@bugs,$1 =~ /\d+/g) }
while($content =~ /$bugpat/gsi){ @bugs = (@bugs,$1 =~ /\d+/g) }

#warn "No bug references found" unless @bugs;
#print STDERR "saw bugs: @bugs\n";

print STDERR $message;
# AppendComment($bugid, $whoid, $comment, $isprivate, $timestamp, $work_time)
foreach my $bug (@bugs) {

my $user = new Bugzilla::User({ id => $userid}) 
 || ThrowUserError('invalid_username', { id => $userid}); #get the user from bugzilla
print STDERR 'user: '. Dumper($user); #pretty prints the user object

Bugzilla->set_user($user);

#AppendComment($bug,$userid,$message)

my $bug = Bugzilla::Bug->check($bugid); #gets the bug
print STDERR 'bug: '. Dumper($bug); #pretty prints the bug object

$bug->add_comment($message); #adds a comment to the bug
$bug->update(); #updated the bug - don't forget to do this!
print "$message";
} 

