<script language="javascript" src="../../Project/js/menu.js"></script>
<script>
    my_menu("../../Project", 
		  new Array("Admin",              "Administration",
    			    "Calculus/default.htm",    "Calculus",
    			    "Methodology",     "Methodology",
    			    "NFS",             "Network File System",
    			    "Perl",            "Perl",
    			    "teamProject",     "Team"),
                   "Bac à sable/ <font color=orange>Sandbox</font>");
   </script>
   <br><br>
   <br><br>
   <br><br>
<?php
	$firstPass=TRUE;
	$t= Array();
	$handle=opendir(".");
	
	print "<center>\n";
	print "<div id='Perl_project'>\n";
	print "<table border=0>\n";
	$counter=0;
	while(($file=readdir($handle))){ // Begin while(($file=readdir($handle)))
		if(preg_match("/^\.{1,2}$/i", $file)==true){ // Begin if(preg_match("/^\.{1,2}$/i", $file)==true)
		} // End if(preg_match("/^\.{1,2}$/i", $file)==true)
		elseif (preg_match("/index\./i", $file)==true) { // Begin elseif (preg_match("/index\./i", $file)==true)
		} // End elseif (preg_match("/index\./i", $file)==true)
		else { // Begin else
			if($firstPass==TRUE){// Begin if($firstPass==TRUE)
				$firstPass=FALSE;
			}// End if($firstPass==TRUE)
			$a=$file;
			if(preg_match("/.php$/i", $a)==TRUE){ // Begin if(preg_match("/.php$/i", $a)==TRUE)
				$k=filemtime($file) ; $m=gmdate('Y/m/d H:i:s',$k); 
				$a=preg_replace("/.php/i","", $a);
				array_push($t, "<tr><td align=right><a href='$file'>$a</a></td><td> (Derniere maj/<font color=orange>Last update</font> ".$m.")</td></tr>\n");
				$counter++;
			} // End if(preg_match("/.php$/i", $a)==TRUE)
			elseif (preg_match("/.html$/i", $a)==TRUE){ // Begin elseif (preg_match("/.html$/i", $a)==TRUE)
				$k=filemtime($file) ; $m=gmdate('Y/m/d H:i:s',$k); 
				$a=preg_replace("/.html/i","", $a);
				array_push($t,"<tr><td align=right><a href='$file'>$a</a></td><td> (Derniere maj/<font color=orange>Last update</font> ".$m.")</td></tr>\n");
				$counter++;
			} // End elseif (preg_match("/.html$/i", $a)==TRUE)
			elseif (preg_match("/\#$/i", $file)==true) { // Begin elseif (preg_match("/\#$/i", $file)==true)
				$k=filemtime($file) ; $m=gmdate('Y/m/d H:i:s',$k); 
				$file=preg_replace('/#$/',"",$file);
				$a=$file;
				array_push($t, "<tr><td align=right>$a</td><td> (Derniere maj/<font color=orange>Last update</font> ".$m.")</td></tr>\n");
				$counter++;
			} // End elseif (preg_match("/\#$/i", $file)==true)
			elseif (preg_match("/.htm$/i", $a)==TRUE){ // Begin elseif (preg_match("/.htm$/i", $a)==TRUE)
				$k=filemtime($file) ; $m=gmdate('Y/m/d H:i:s',$k); 
				$a=preg_replace("/.htm/i","", $a);
				array_push($t,"<tr><td align=right><a href='$file'>$a</a></td><td> (Derniere maj/<font color=orange>Last update</font> ".$m.")</td></tr>\n");
				$counter++;
			} // End elseif (preg_match("/.htm$/i", $a)==TRUE)
		} // End else
	} // End while(($file=readdir($handle)))
	rsort($t);
	for($i=0;$i<$counter;$i++){
	// begin for($i=0;$i<$counter;$i++)
		print $t[$i];
	}
	// end for($i=0;$i<$counter;$i++)
	print "</table>\n";
	if($firstPass==TRUE){ // Begin if($firstPass==TRUE)
		print "under construction";
	} // End if($firstPass==TRUE)
	print "</div>";
	print "</center>\n";
	closedir($handle);
?>
   <br><br>
   <br><br>
   <br><br>
   <br><br>
<script>
footer("http://dorey.sebastien.free.fr","javascript:history.back()");
</script>
