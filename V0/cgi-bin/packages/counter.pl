 
use FileHandle;
use Fcntl ':flock';

@months = (Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sept,Oct,Nov,Dec);

# Change stats file rights on graphic files
sub changeRights {
 $tmp_d = $_[0];
 $pid = $$;
 
 `chmod 755 $tmp_d/current_stat.gif`;
 `touch $tmp_d/printStat.html`;
 #`chmod 755 $tmp_d/img$pid.gif`;
 print "<img src='$tmp_d/img$pid.gif'>\n";
}

# Create URL for the board
sub my_url {
 $url = "http://$localhost/~dorey_s/counter.cgi?year=$_[0]&month=$_[1]&service=$_[2]";
 return "<a href='$url'>$_[1]</a>";
}

# Create header and init background
sub header {
 print "<body background='image/arcade.jpg' text='yellow' link=\"yellow\" vlink=\"LightBlue\" >";
}

# Print list
sub printList {
 $temporary_file = $_[0];
 $ye = $_[1];
 $mo = $_[2];
# $to_print = "ok";
 
 open(STAT,"${temporary_file}/counter.stat");
 STAT->autoflush(1);
 @line_stat = <STAT>;
 close(STAT);
 
 &header;
 
 $to_print_screen = "\n<center><h1>Statistics about connexions</h1><br>Created by Sebastien Dorey</center>\n<br><br>\nLast <a href='.gnuplot/printStat.html'>graph</a> generated<br>\n".&get_welcome_message_for_surface."<br><br><center>\n<table border=1>\n";
 $c_my_y = 0;
 $to_summup = ();
 for $i (@line_stat) {
 chomp($i);
 ($my_y,$my_m) = split(/\ /,$i);
 if ($c_my_y == 0) {
 $c_my_y = $my_y;
 } elsif ($c_my_y != $my_y) {
 $cmm = 1;
 if (-f "$store_img/monthly${c_my_y}.gif") {
 $new_line = "<tr>\n<td width='56' height='38'><font color='red'>" . &my_url($c_my_y,$c_my_y,"statY");
 } else {
 $new_line = "<tr>\n<td width='56' height='38'><font color='red'>$c_my_y</font>";
 }
 if (scalar(@line_stat) == 1) {
 $new_line = "$new_line<td>"; 
 }
 while ($cmm < 13) {
 if ($cmm < 10) {
 $new_line = "$new_line\n<td width='56' height='38' align=center valign=center>\n" . &my_url($c_my_y,"0$cmm","statM");
 } else {
 $new_line = "$new_line\n<td width='56' height='38' align=center valign=center>\n" . &my_url($c_my_y,"$cmm","statM");
 }
 $cmm++;
 }
 $new_line = "$new_line</tr>\n";
 $c_my_y = $my_y;
 $to_summup = "$to_summup$new_line\n";
 }
 }
 $cmm = 1;
 if (-f "$store_img/monthly${c_my_y}.gif") {
 $new_line = "<tr>\n<td width='56' height='38'>\n" . &my_url($c_my_y,$c_my_y,"statY");
 } else {
 $new_line = "<tr>\n<td width='56' height='38'>\n<font color='red'>$c_my_y</font>\n";
 }
 while ($cmm < 13) {
 if ($cmm < 10) {
 $new_line = "$new_line\n<td width='56' height='38' align=center valign=center>\n" . &my_url($c_my_y,"0$cmm","statM");
 } else {
 $new_line = "$new_line\n<td width='56' height='38' align=center valign=center>\n" . &my_url($c_my_y,"$cmm","statM");
 }
 $cmm++;
 }
 $to_summup = "$to_summup$new_line</tr>\n";
 $to_print_screen = "$to_print_screen$to_summup\n</table>\n</center>\n<br><br>Go <a href='JavaScript:history.back()'>back</a>\n";
 print "$to_print_screen";
}

# This is add on for presentation of surfacedrawinfg
# Welcome message that shows up at first page
sub get_welcome_message_for_surface {
 if (&is_surface_image_exists() != 0) {
 return "Surface graph is about to be calculated in 2 hairs :-))))) but click here for an <a href=\"http://dorey.sebastien.free.fr/Project/Perl/Gnuplot/exemple/index.html\">Exemple</a>";
 } else {
 return "<a href=\"http://$Conf_File::MY_HOST/\~dorey_s/cgi-bin/counter.cgi?service=surface\">go</a> for surface\n";
 }
}

#look if image $Conf_File::img_surface_stat.gif exists ok = 0 ko -1
sub is_surface_image_exists {
 return (-f "${Conf_File::stub}$Conf_File::img_surface_stat.gif") ? 0 : -1;
}



# List month table
sub listMonth {
 $file = $_[0];
 $y = $_[1];
 $m = $_[2];
 $cur_year = $_[3];
 $cur_month = $_[4];
 
 open(R,"$file");
 @fi = <R>;
 close(R);
 
 $last_hit_num = 0;
 for $k (@fi) {
 chomp($k);
# print "$k\n";
 $k =~ s/\ +/\ /g;
 ($y2,$m2,$t2,@r) = split(/\ /,$k);
 $last_hit_num = $last_hit_num + $t2;
 }
 
 if ($cur_year == $y) {
 if ($cur_month < $m) {
 &header;
 print "<br><br><br><br><center>This is future $y-$m current $cur_year-$cur_month</center><br><br><br><br>";
 print "<br><br><br><a href='JavaScript:history.back()'> <center><img src='image/clock1-c.gif' border=0></center></a>";
 return -1; 
 }
 }
 for $k (@fi) {
 chomp($k);
# print "$k\n";
 $k =~ s/\ +/\ /g;
 ($y2,$m2,$t2,@r) = split(/\ /,$k);
 $max_in_month = 0;
 for $m (@r) {
 $max_in_month += $m;
 }
 if (($y == $y2)&&($m == $m2)) { 
 &header;
 $to_p = "<center><h1>$y on $m<h1></center><br><br><br><center><table border=1>\n<tr><td><td>Per. on max hit(s)<td>Monthly hit(s)<td>Per. hit(s) in one month</tr>\n";
 $cpt = 0;
 for $m3 (@subject) {
 $m3 =~ s/\"//g;
 $l = $r[$cpt++];
 $to_p = "$to_p<tr><td>$m3<td align=center>";
 if ($max_in_month == 0) {
 $to_p = "<td align=center>$to_p 0";
 } else {
 $to_p = "<td align=center>$to_p".(&round(2,(($l*100)/$last_hit_num)));
 }
 if ($t2 == 0) {
 $to_p = "$to_p<td align=center>".$l."<td align=center>0</tr>\n";
 } else {
 $to_p = "$to_p<td align=center>".$l."<td align=center>".(&round(2,(($l*100)/$t2)))."</tr>\n";
 }
 }
 $to_p = "$to_p</table></center>";
 $global_stat = "<center>\n<table>\n<tr><td>Max hit(s) from begining<td> $last_hit_num</tr>\n<tr><td>Max hit(s) in month<td>$t2</tr></table>\n</center><br><br>";
 print "$to_p\n$global_stat";
 print "<br>Go <a href='JavaScript:history.back()'>back</a>";
 return 0;
 }
 }
}

# Make round on number with a precision specified
sub round {
 my ($precision,$floatting);
 
 $precision = $_[0];
 $floatting = $_[1];
 return sprintf "%.${precision}f",$floatting;
}

# Print stats on the screen
sub print_stat_screen { 
 local ($file_st);
 
 $file_st = $_[0];
 open(S,"$file_st");
 S->autoflush(1);
 @p = <S>;
 close(S);
}

# Script that call gnuplot
sub callGnuplot {
 $root_f = $_[0];
 $tmp_f = $_[1];
 $home_p = $_[2];
 $pid = $$;
 
 $current_dir = `pwd`;
 chomp($current_dir);
 open(GPF,"$script_whole_year ") or die "Curent directory:$current_dir\nscript stat.gnuplot does not exists in ${root_f}packages/";
 @gnuplot_file_conf = <GPF>;
 close(GPF);
 
 @plot_instructions = &createFilesToPlot("${root_f}gnuplot",${tmp_f},${home_p});
 @gnuplot_file_conf = (@gnuplot_file_conf,@plot_instructions);

 open(GP,"|${gnuplot_exe} -persist |${ppmtogif_exe} >$tmp_f/img${pid}.gif") or die "no gnuplot";
 GP->autoflush(1);
 print GP "@gnuplot_file_conf";
 close(GP);
 system("cp $tmp_f/img${pid}.gif $tmp_f/current_stat.gif");
 system("rm $tmp_f/img* $tmp_f/mob*");
}

# Create the files that helps to plot info on the screen with different colors for the year
sub createFilesToPlot {
 local (@line_stat,@file_name,@to_sto,$cy,$y,$m,$line);
 $root_file = $_[0];
 $temporary_files = $_[1];
 $home_path = $_[2];
 $process_id = $$;
 
 open(STAT,"${temporary_files}/counter.stat");
 STAT->autoflush(1);
 @line_stat = <STAT>;
 close(STAT);
 $date_for_graph = `date +%Y-%m-%d`;
 chomp($date_for_graph);
 $date_to_print = "set title \"Hit(s) by user Last updte done on $date_for_graph\"";
 @line_stat = ( "$date_to_print\n" , @line_stat );
 
 $file_name = ();
 $file_name_smooth_unique = ();
 @to_sto = ();
 for $line (@line_stat) {
 chomp($line);
 ($cy,$mmmm,$t) = split(/\ /,$line);
 #print "$cy,$mmm,$t\n";
 last;
 }
 for $line (@line_stat) {
 chomp($line);
 ($y,$m) = split(/\ /,$line);
 if ($cy < $y) {
 if ($cy != 0) {
 if ($file_name eq "") {
 $file_name = "'${temporary_files}/mob${process_id}.$cy' using 2:3 title 'Year $cy'";
 $file_name_smooth_unique = "'${temporary_files}/mob${process_id}.$cy' using 2:3 smooth unique title 'Year $cy'";
 } else {
 $file_name = "$file_name, '${temporary_files}/mob${process_id}.$cy' using 2:3 title 'Year $cy',";
 $file_name_smooth_unique = "$file_name_smooth_unique, '${temporary_files}/mob${process_id}.$cy' using 2:3 smooth unique title 'Year $cy',";
 }
 $line = "$line\n";
 open(W,">${temporary_files}/mob${process_id}.$cy");
 W->autoflush(1);
 for $i (@to_sto) {
 chomp($i);
 print W "$i\n";
 }
 close(W);
 #&calculateMonthlyAndCreateGraph("${temporary_files}/mob${process_id}.$cy",$script_detailed,$home_path);
 @to_sto = ($line);
 } else {
 @to_sto = ("$line\n");
 }
 $cy = $y;
 } else {
 @to_sto = (@to_sto,"$line\n");
 } 
 }
 $yrange = &calculateYmax($temporary_files);
 $yMaxRanges = $yrange/10;
 if ($cy != 0) {
 $file_name = "plot [1:12] [0:$yrange] $file_name '${temporary_files}/mob${process_id}.$cy' using 2:3 title 'Year $cy' \n";
 $file_name =~ s/\,\,/\,/g;
 $file_name =~ s/\'\ \'/\'\,\'/g;
 $file_name_smooth_unique = "plot [1:12] [0:$yrange] ${file_name_smooth_unique} '${temporary_files}/mob${process_id}.$cy' using 2:3 smooth unique title 'Year $cy'\n";
 $file_name_smooth_unique =~ s/\,\,/\,/g;
 $file_name_smooth_unique =~ s/\'\ \'/\'\,\'/g;
 open(W,">${temporary_files}/mob${process_id}.$cy");
 W->autoflush(1);
 for $i (@to_sto) {
 chomp($i);
 print W "$i\n";
 }
 close(W);
 print "we go into ====\n";
 #&calculateMonthlyAndCreateGraph("${temporary_files}/mob${process_id}.$cy",$script_detailed,"$home_path");
 print "nitty greety\n";
 }
 @to_p = ("set title 'Hit(s) in a year $dte'\n","set ytics 0,$yMaxRanges\n","$file_name","$file_name_smooth_unique");
 return @to_p;
}


# Create a counter when file that help to coun are not present
sub CreateCounter {
 $fi = $_[0];
 $y = $_[1];
 $ly = $_[2];
 $s = ();
 
 for $subj (@subject) {
 chomp($subj);
 $s = "$s 0";
 }
 
 if (!-f "$fi") {
 print "File doesn't exists:$fi<br>";
 $i = 1;
 open(W,">$fi");
 while ($i <= 12) { 
 print W "$y $i 0 $s\n";
 $i++;
 }
 close(W);
 } elsif (-z "$fi") {
 print "file exists but is empty<br>\n";
 $i = 1;
 open(W,">$fi");
 while ($i <= 12) { 
 print W "$y $i 0 $s\n";
 $i++;
 }
 close(W);
 } elsif ($ly == 0) {
 print "File does exist but is empty:$fi<br>";
 $i = 1;
 open(W,">$fi");
 while ($i <= 12) { 
 print W "$y $i 0 $s\n";
 $i++;
 }
 close(W);
 } else {
 if ($y > $ly) {
 print "file exists and is updated -$ly-$y-<br>\n";
 open(W,">>$fi");
 while ($ly < $y) {
 $ly++;
 $nm = 1;
 while ($nm != 13) {
 print W "$ly $nm 0 $s\n";
 $nm++;
 }
 }
 close(W);
 }
 }
 print "Counter created<br>";
}

# Check the last year stored
sub lastYearStored {
 local ($m,$y);
 
 if (!-f "$_[0]") {
 print "$_[0] doesn't exists value retutned $_[1]<br>\n";
 return $_[1];
 } 
 open(R,"$_[0]");
 @lu = <R>;
 close(R);
 
 for $i (@lu) {
 chomp($i);
 ($y,$m) = split(/\n/,$i);
 }
 return $y;
}

# Increment month when hit on a specific menu
sub incremMonth {
 local ($current_month,$current_year,$stat,$m,$y);
 $y = $_[0];
 $m = $_[1];
 $f = $_[2];
 
 $pppo = `pwd`;
 open(STAT,"$f");
 @line_stat = <STAT>;
 close(STAT);
 
 @final_stat_line = ();
 for $lnes_stat (@line_stat) {
 chomp($lnes_stat);
 $lnes_stat =~ s/\ +/\ /g;
 #print "$lnes_stat\n<br>";
 ($current_year,$current_month,$stat,@lst) = split(/\ /,$lnes_stat);
 
 if ($y == $current_year) {
 if ($m == $current_month) {
 $stat++;
 $p = "$current_year $current_month $stat @lst";
 @final_stat_line = (@final_stat_line,$p);
 } else {
 @final_stat_line = (@final_stat_line,$lnes_stat);
 }
 } else {
 @final_stat_line = (@final_stat_line,$lnes_stat);
 }
 }
 open(STAT,">$f");
 flock(STAT,LOCK_EX);
 seek(STAT, 0, 2);
 for $fl (@final_stat_line) {
 chomp($fl);
 if (length($fl) != 0) {
 print STAT "$fl\n";
 }
 }
 flock(STAT,LOCK_UN);
 close(STAT);
}

# When material hit the increm sbject material
sub incremMonthMaterial {
 local ($current_month,$current_year,$stat,$m,$y);
 $y = $_[0];
 $m = $_[1];
 $f = $_[2];
 $material = $_[3];
 
 $pppo = `pwd`;
 open(STAT,"$f");
 @line_stat = <STAT>;
 close(STAT);
 
 @final_stat_line = ();
 for $lnes_stat (@line_stat) {
 chomp($lnes_stat);
 $lnes_stat =~ s/\ +/\ /g;
 ($current_year,$current_month,$stat,@lst) = split(/\ /,$lnes_stat);
 $tmp_material = 1;
 if ($y == $current_year) {
 if ($m == $current_month) {
 for $k (@lst) {
 if ($tmp_material == $material) {
 $k++;
 }
 $tmp_material++;
 }
 $p = "$current_year $current_month $stat @lst";
 @final_stat_line = (@final_stat_line,$p);
 } else {
 @final_stat_line = (@final_stat_line,$lnes_stat);
 }
 } else {
 @final_stat_line = (@final_stat_line,$lnes_stat);
 }
 }
 open(STAT,">$f");
 flock(STAT,LOCK_EX);
 seek(STAT, 0, 2);
 
 for $fl (@final_stat_line) {
 chomp($fl);
 if (length($fl) != 0) {
 print STAT "$fl\n";
 }
 }
 flock(STAT,LOCK_UN);
 close(STAT);
}

# Parse form
sub parse_form {
 $buffer = ();
 read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
 if (length($buffer) < 5) {
 $buffer = $ENV{QUERY_STRING};
 }
 @pairs = split(/\&/, $buffer);
 foreach $pair (@pairs) {
 ($name, $value) = split(/=/, $pair); 
 $value =~ tr/+/ /;
 $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg; 
 $input{$name} = $value;
 }
}

# Calculate Y max on board
sub calculateYmax {
 $t = ();
 $m = ();
 $y = ();
 $stat_file = $_[0];
 $to_return = 0;
 open(K,"$stat_file/counter.stat");
 @lines = <K>;
 close(K);
 for $i (@lines) {
 chomp($i);
 ($y,$m,$t) = split(/\ /,$i); 
 if ($to_return == 0 && $t < 10) {
 $to_return = 10;
 } else {
 if (($t > $to_return) && ($t > 10)) {
 $to_return = $t;
 }
 }
 }
 return $to_return;
}

#&remove("../img/counter.stat","../img/counter.stat",1,2012);
sub remove {
 my ($src,$dst,$laps,$last_y,$first_y,@to_sto);
 
 $src = $_[0];
 $dst = $_[1]; 
 $laps = $_[2]; # for ie 5 years
 $last_y = $_[3];
 $home = $_[4];
 $image_home = "$home/www/image/";
 $first_y = ($last_y - $laps); # first year to start
 
#print "$src\n$dst\n$laps\n$last_y";
 
 open(R,"$src") or die "can't read $src";
 @read_src = <R>;
 close(R);
 
 @to_sto = ();
 for $lines (@read_src) {
 chomp($lines);
 ($y_sto,@other) = split(/\ /,$lines);
 if ($y_sto >= $first_y) {
 @to_sto = (@to_sto,$lines);
 } else { 
 system("rm -f $image_home/monthly$y_sto.gif");
 }
 }
 
 open(W,">$dst") or die "can't write in $dst";
 flock(W,LOCK_EX|LOCK_SH) or die "can't lock filehandle";
 for $l (@to_sto) {
 print W "$l\n";
 }
 close(W);
 system("rm -f $src.tmp2");
}



1;
