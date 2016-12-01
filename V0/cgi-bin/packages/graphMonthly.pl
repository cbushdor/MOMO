@months = (Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sept,Oct,Nov,Dec);

sub start_stat {
 local ($name,$name_script_gnuplot,@list_all_years ,@gnuplot);
 $name = $_[0];
 $name_script_gnuplot = $_[1];

 @list_all_years = &update("$name");

 for $one_year (@list_all_years) {
 $max_plot_x = 0;
 @gnuplot = &xtics_set("$name","$name_script_gnuplot",2,"$one_year");
 print "@gnuplot";
 
 open(G,"|${gnuplot_exe}");
 print G "set term pbm color\n";
 print G "set out \"|${ppmtogif_exe}>$store_img/monthly$one_year.gif\"\n";
 print "set out \"|${ppmtogif_exe}>$store_img/monthly$one_year.gif\"\n";
 print G @gnuplot;
 print G "quit";
 close(G);
 system("chmod 755 $store_img/monthly$one_year.gif");
 $plot_x = 0;
 $max_plot_x = 0;
 }
}

sub update {
 local ($name,@list_years,@o,$prev,$my_line,$my_new_year,@oth);
 $name = $_[0];

 @list_years = ();
 open(R,"$name");
 @o = <R>;
 close(R);
 $prev = 0;
 for $my_line (@o) {
 chomp($my_line);
 ($my_new_year,@oth) = split(/\ +/,$my_line);
 if ($my_new_year != $prev) {
 @list_years = ($my_new_year,@list_years);
 $prev = $my_new_year;
 }
 }
 return @list_years;
}

#----
sub sumUp {
 $name = $_[0];
 $precision = $_[1];
 $local_year = $_[2];
 
 open(R,"$name");
 @o = <R>;
 close(R);
 $sum = 0;
 for $m (@o){
 chomp($m);
 ($y,$f,$t,@k) = split(/\ +/,$m);
 if ($local_year == $y) {
 $sum += $t;
 }
 }
 open(R,">$name.tmp");
 for $m (@o){
 chomp($m);
 ($y,$f,$t,@k) = split(/\ +/,$m);
 $res = "$y $f $t ";
 for $l (@k) {
 if ($sum == 0) {
 $res = "$res 0 ";
 } else {
 $st = (($l*100) / $sum);
 $st = sprintf "%.${precision}f",$st;
 $res = "$res $st ";
 }
 }
 print R "$res\n";
 }
 close(R);
# return $sum;
}
#----|

sub xtics_set {
 local ($name,$script,$precision,$xtics_year,$label_absice_ord,$counter,$xtiqs,$labels,$c,$first_pass,$num_subj);
 local ($counter_label, $newlab,$using_plot,$using_plot2,$loc, @boxes_arr);
 local ($newlab,$labels,$boxes,$count,$loc,@boxes_arr,$dat);

 $name = $_[0];
 $script = $_[1];
 $precision = $_[2];
 $xtics_year = $_[3];

 $label_absice_ord = "set xlabel \"Months year $xtics_year\"\nset ylabel \"Hits(Months year $xtics_year)\"\n";
 unlink("$name.tmp2"); 

 open(R,"$stat_script_monthly");
 @rr = <R>;
 close(R);
 &sumUp($name,$precision,$xtics_year);

 $counter = 1;
 $xtiqs = ();
 $labels = ();
 $c = 1;
 $labels = ();
 $first_pass = 1;
 $num_subj = $#subject;
# ------------------------>$num_subj\n";
 $counter_label = 1.5;
 for $i (@months) {
# print "\n$i:\n";
 $newlab = &setLabelsOnGraphics($name,$xtics_year,$i);
 $labels = "$labels\n$newlab";
 
 $xtiqs = "$xtiqs,\"$i\" " . $counter_label;
 $counter_label += ($num_subj+2);
 $counter++;
 }
#----| 
 $using_plot = ();
 $using_plot2 = ();
 $count = 2;
 $boxes = ();
 $loc = 0;
 @boxes_arr = ();
 for $pp (@subject) {
 $using_plot2 = "$using_plot2:$count";
# ---
 $boxes = "$boxes,\"$name.tmp2\" using 2:".($count+1)." title \"".$subject[$loc]."\" with boxes"; 
#----| 
 $loc++;
 $count++;
 }
 $boxes =~ s/^\,//g;
 $using_plot = "$using_plot+\$$count";
 $xtiqs =~ s/^\,//g;
 $xtiqs = "set xtics ($xtiqs)\n";
 $using_plot =~ s/^\+//g;
 $using_plot2 =~ s/^\://g;
# ----
 $using_plot = "plot [0:".&returnMaxXToPlot("$name")."] [0:".(&returnMaxYToPlot("$name")+10)."] $boxes\n";

 $dat = `date`;
 chomp($dat);
 return ("set title \"Stats on web hit frequencies on different subjects in one year\\nLast update $dat\\nGraphic generated with gnuplot by Sebastien Dorey\"\n$labels\n","$label_absice_ord",@rr,"$xtiqs","$using_plot");
#---|
}

sub date_choice {
 local ($choice,$counter);
 $counter = 1;
 $choice = $_[0];
 # print "====\n";
 for $i (@months) {
 if ($i eq $choice) {
# print "--->$i\n";
 return $counter;
 }
 $counter++;
 }
 print "==+==\n";
}
 
# set labels for the screen according to some specific sets
sub setLabelsOnGraphics {
 local ($file_stat_name, $file_stat_name,$m,@file,$y,$m,$t,@o,$max,$lab,@percent_in_month_hit,@percent_in_month);

 @percent_in_month = ();
 @percent_in_month_hit = ();

# unlink("$name.tmp2"); 
 $file_stat_name = $_[0];
 $cur_year = $_[1];
 $rank_month = &date_choice($_[2]);
 
 open(W,">>$file_stat_name.tmp2");
 open(R,"$file_stat_name.tmp"); 
 @file = <R>;
 close(R);
 $lab = ();

 for $l (@file) {
 chomp($l);
 ($y,$m2,$t,@o) = split(/\ +/,$l);
 # $plot_x++;
 $max = 0;
 $c = 0;

 if ($cur_year == $y) {
 for $percent (@o) {
 if ($rank_month == $m2) {
 # print "=$c===>$y ".($plot_x+$m)." ".(&fillBlanck($c)) ."$percent\n";
 print W "$y ".($plot_x+$m2)." ".&fillBlanck($c) ."$percent\n";
 if (&isAlreadyIn($percent,@percent_in_month) < 0) {
 @percent_in_month = (@percent_in_month,$percent);
 if ($percent > 3) {
 $lab = "set label \"$percent\%\" at ($plot_x+$m2),($percent+4) right rotate\n$lab";
 }
 }
 if (&isAlreadyHitsIn($t,@percent_in_month_hit) < 0) {
 @percent_in_month_hit = (@percent_in_month_hit,$t);
 if ($percent > 0) {
 $lab = "set label \"$t\" at ($plot_x+$m2+3),($percent+6) right\n$lab";
 }
 }

 $c++;
 $plot_x++;
 }
 }
 }
 }
 print "$lab";
 close(W);# $max_plot_x = 0;
 return $lab;
}

sub fillBlanck {
 local ($blanck_lack,$j,$return_value);

 $blanck_lack = $_[0];
# print "morback($i < $blanck_lack)\n";
 $j=1;
 $return_value = ();
 while ($j <= $blanck_lack) {
# print "toto\n";
 $return_value = "0 $return_value";
 $j++;
 }
 return $return_value;
}

sub returnMaxXToPlot {
 local ($max,$max_y,$yrs,$month_tmp,@tmp_rst,@file, $file_stat_name);
 $file_stat_name = $_[0];
 
 open(R,"$file_stat_name.tmp2"); 
 @file = <R>;
 close(R);

 for $line_tmp (@file) {
 chomp($line_tmp);
 ($yrs,$month_tmp,@tmp_rst) = split(/\ +/,$line_tmp);
 }
 return $month_tmp;
}

sub returnMaxYToPlot {
 local ($max,$max_y,$yrs,$month_tmp,@tmp_rst,@file, $file_stat_name);
 local ($yrs,$month_tmp,@tmp_rst);

 $file_stat_name = $_[0];
 
 open(R,"$file_stat_name.tmp2"); 
 @file = <R>;
 close(R);
 $max = 0;

 for $line_tmp (@file) {
 chomp($line_tmp);
 ($yrs,$month_tmp,@tmp_rst) = split(/\ +/,$line_tmp);
 for $max_y (@tmp_rst) {
 if ($max < $max_y) {
 $max = $max_y;
 }
 }
 }
 return $max;
}

# We store statistics in array to avoid printing twice on screen same value in month
# This function check value stored
sub isAlreadyIn {
local ($current_per,@rest_per);

($current_per,@rest_per) = @_;
for $cur_per (@rest_per) {
if ($cur_per == $current_per) {
return 0;
}
}
return -1;
}

# We store hits in array to avoid printing twice on screen same value in month
# This function check value stored
sub isAlreadyHitsIn {
local ($current_per,@rest_per);

($current_per,@rest_per) = @_;
for $cur_per (@rest_per) {
if ($cur_per == $current_per) {
return 0;
}
}
return -1;
}


1;
