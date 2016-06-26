package Conf_File;
# +-------------------------------+
# | Conf_File.pm		  |
# | Written     on 10/2004        |
# | Last update on May 23 2009    |
# +-------------------------------+

use CGI::Carp qw(fatalsToBrowser); 
use Exporter;
our @ISA = qw(Exporter);
our @EXPORT = qw(
		 $home_src $MY_HOST $root_gnuplot_stat $image_dir_name $colourText $cLink
		 $cvLink $email $stat_script_monthly $stub $plot_x $max_plot_x %store_coord_monthly
		 $gnuplot_exe $ppmtogif_exe $gnuplot_v $script_whole_year
		 $script_contains_formula_for_surface $img_surface_stat $tmp_surface_stat
		 $script_detailed @subject $image_stored_absolute_path $image_stored_relative_path
		 $file_stat $dte $dt $root $max_year_base $img_bkground
		 &set_title $COUNTER $BAR $SURFACE $file_surface_name $file_surface_local_stat_last_year 
		 );

# --------------------------------------------------------

${home_src} = (); 

# That the URL base
$MY_HOST = "localhost";

# All information are stored to make stats in the next file
${root_gnuplot_stat}="../.gnuplot";

# that's where images are stored
# Provide only the name of directory where image will be stored ie ${image_dir_name}="image" will store info in directory image
#${image_dir_name}="images";
${image_dir_name}="../.gnuplot";

# set image background
${img_bkground} = "${image_dir_name}/arcade.jpg";

# set text colour
${colourText}="yellow";

# set link colour
${cLink}="orange";

#set visited link colour
${cvLink}="#D2831C";

# ${email}
${email} = 'dorey.sebastien@free.fr';

# ------------------ DO NOT CHANGE FROM HERE ---------------------------

$file_surface_name = "./../.gnuplot/surface_image_stat.gif";

if (-f $file_surface_name) {
	$stat_surface_file_date = `ls -al ../.gnuplot/surface_image_stat.gif`;
	chomp $stat_surface_file_date;
} else {
	$stat_surface_file_date = "none";
}

$file_surface_local_stat_last_year = (split(/\ /,$stat_surface_file_date))[8];


# Name of script for monthly stat and where to store image
#if (defined($FILE_COUNTER_CGI)) {
	${stat_script_monthly}="packages/stat_month.gnuplot";
#} else {
   #${stat_script_monthly}="stat_month.gnuplot";
#}


${stub} = "./";


${plot_x} = 0;
${max_plot_x} = 0;
%store_coord_monthly = ();


# That's executable file
${gnuplot_exe} = "/usr/local/bin/gnuplot";
${ppmtogif_exe} = "/usr/local/netpbm/bin/ppmtogif";
${gnuplot_v}="Gnuplot 3.7"; # `gnuplot`;
#chomp ${ppmtogif_exe};
#chomp ${gnuplot_exe};
chomp ${gnuplot_v};


#script for gnuplot
# whole year
${script_whole_year} = "packages/stat.gnuplot";

# script to transform formula
# to modify here
#if (defined($FILE_COUNTER_CGI)) {
	${script_contains_formula_for_surface}="packages/surface_plot_definition.gnuplot";
#} else {
#    ${script_contains_formula_for_surface}="surface_plot_definition.gnuplot";
#}

# img for surface stat
${img_surface_stat}="../.gnuplot/surface_image_stat";

# temporary file for surface stat
${tmp_surface_stat}="../.gnuplot/tmp_surface_stat.gnuplot";

#detailed
${script_detailed} = "packages/stat_month.gnuplot";

# That's all fields used in first menu French/English menu
@subject = ('Qui Suis je / Who am I','Profil / Profile','Forum','Projets / Projects','Vee Eye','Guest Book');

# absolute and relative path to store image
${image_stored_absolute_path} = $ENV{"HOME"} . "/www/${image_dir_name}/";
${image_stored_relative_path}="${image_dir_name}/";
${file_stat} = "${root_gnuplot_stat}/counter.stat";

# We calculate date for the whole program once per each process running
${dte} = `date`;
${dt}=`date "+%m/%Y"`;
$mo = $ye = ();
($mo,$ye) = split(/\//,${dt});
chomp(${dt});
chomp(${dte});
chomp $mo;
chomp $ye;

# This is where all CGI scripts appear
${root}="../.";

# This is where all hits show up
#$temporary_files = "${root_gnuplot_stat}";

# Max year show up on board and base
${max_year_base}=5;

# type of graph
$COUNTER = 0;
$BAR = 1;
$SURFACE = 2;

#set_title("Stats on web hit frequencies \\non different subjects over one year","-6","$ymax",$Conf_File::BAR

# we set the graphic title basies then we add some neaw features
sub set_title { # Begin sub set_title
	my ($new_feature,$type_graph,$xmax,$ymax,$minx,$miny) = @_;

	#    my $new_feature = $_[0];
	#    my $type_graph = $_[1];
	#    my $xmax = $_[2];
	#    my $ymax = $_[3];

	if ($type_graph == $COUNTER) {
		return "set title \"$new_feature\\nLast update $dte\\n\"\n";
		#		"set label \"Last update $dte  -- $email\" at 6.5,-13 font \"Times,8\"\n"; # .
		# "set label \"email:$email\" at 0,-13 font \"Times,8\"\n"); 
	} elsif  ($type_graph == $BAR) { 
		return "set title \"$new_feature\\nLast update $dte\\n\"\n";
		#		"set label \"\\n\\nLast update $dte   $email\" at 43,-1.75\n" ;
		# .
		# "set label \"\\n\\nemail:$email\" at -6,-1.75\n"
		# ); 
	} elsif ($type_graph == $SURFACE) { 
		return "set title \"$new_feature\\n\\nLast update $dte\\n\"\n";
	#		"set label \"\\n\\nLast update $dte  $email\" at ($xmax),($miny-60)\n";
	# .
	#"set label \"\\n\\nemail:$email\" at ($xmax+200),($miny-60)\n" . "set xlabel \" \\n\\n\"\n"
	# ); 
	}
} # End sub set_title

1;
