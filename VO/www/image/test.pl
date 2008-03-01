#!/usr/bin/perl

use Image::Size 'html_imgsize';

$size = html_imgsize("download1.jpg");
print "--- $size\n";
