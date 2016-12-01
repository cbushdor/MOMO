#!/usr/bin/perl

# Graph.pm example File
# Please see documentation for more info

use Graph;
$Graph::debug = 1;

$graph = new Graph;
srand();
for ($i=0; $i<30; $i++) {
	$num = int( rand()*20000 + 10000);
	if (($i % 5) == 0) {
		$label = "Sun";
		}
	else {
		$label="";
		}
	$graph->data($num,$label);
	}
$graph->title("Daily Web Site Hits");
$graph->subtitle("Content pages only");
$graph->keys_label("Day of the Week");
$graph->values_label("Hits");
$graph->value_min(0);
$graph->value_max(35000);
$graph->value_labels("10000,20000,30000");
$graph->background_image("bg.gif");
$graph->output("example.gif");




