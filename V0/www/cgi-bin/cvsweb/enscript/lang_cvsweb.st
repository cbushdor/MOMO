/*
   GNU Enscript language file for FreeBSD-CVSweb.
   $FreeBSD: projects/cvsweb/enscript/lang_cvsweb.st,v 1.2 2003/05/04 10:42:20 scop Exp $
 */

state lang_cvsweb
{
  BEGIN {
    /* RGB -> HTML color mapper function. */
    sub map_color (r, g, b)
      {
	return sprintf ("#%02X%02X%02X", r, g, b);
      }

    LANGUAGE_SPECIALS = /[<>\&\"]/;

    sub language_print (str)
      {
	str = regsuball (str, /\&/, "&amp;");
	str = regsuball (str, /</, "&lt;");
	str = regsuball (str, />/, "&gt;");
	str = regsuball (str, /\"/, "&quot;");
	print (str);
      }

    sub language_symbol (symbol)
      {
	return false;
      }

    sub header ()
      {
      }

    sub trailer ()
      {
      }

    sub face_on (face)
      {
	if (face[boldp])
	  print ("<b>");
	if (face[italicp])
	  print ("<i>");

	if (face[fg_color])
	  print ("<span style=\"color: ", face[fg_color], "\">");
	if (face[bg_color])
	  print ("<span style=\"background-color: ", face[bg_color], "\">");
      }

    sub face_off (face)
      {
 	if (face[fg_color])
	  print ("</span>");
 	if (face[bg_color])
	  print ("</span>");

	if (face[italicp])
	  print ("</i>");
	if (face[boldp])
	  print ("</b>");
      }

    return;
  }
}


/*
Local variables:
mode: c
End:
*/
