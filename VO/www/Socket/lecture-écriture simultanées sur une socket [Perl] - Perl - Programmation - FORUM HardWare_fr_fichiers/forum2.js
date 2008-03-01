var opened_im= 0;
var allow_hide_im= 0;

function md_cursor_pointer() {
	document.body.style.cursor='pointer';
}
function md_cursor_hand() {
	document.body.style.cursor='auto';
}
function md_verif_size(obj,message,resize,resizevalue) {
	var largeur= obj.width;
	
	if (resize == 1) {
		if (largeur>resizevalue) {
			obj.width= resizevalue;
			obj.setAttribute("alt",message);
			obj.setAttribute("title",message);
			obj.setAttribute("onclick","md_size("+obj.src+")");
			obj.onclick= function() {md_size(obj.src);};
			obj.setAttribute("onmouseover","md_cursor_pointer()");
			obj.setAttribute("onmouseout","md_cursor_hand()");
			obj.onmouseover= function() {md_cursor_pointer();};
			obj.onmouseout= function() {md_cursor_hand();};
			
		}
	} else if (resize == 2) {
		var largeurlibre = 0, hauteur = 0;
		if( typeof( window.innerWidth ) == 'number' ) {
		  largeurlibre = window.innerWidth;
		  hauteurlibre = window.innerHeight;
		} else if( document.documentElement && ( document.documentElement.clientWidth || document.documentElement.clientHeight ) ) {
		  largeurlibre = document.documentElement.clientWidth;
		  hauteurlibre = document.documentElement.clientHeight;
		  }
		else if( document.body && ( document.body.clientWidth || document.body.clientHeight ) ) {
		  largeurlibre = document.body.clientWidth;
		  hauteurlibre = document.body.clientHeight;
		}
		if (largeurlibre == 0) {
			return;
		}
		largeurpossible= largeurlibre-resizevalue;
		//alert('largeur=> '+largeurlibre+'=>'+largeurpossible);
		if (largeur>largeurpossible) {
			obj.width= largeurpossible;
			obj.setAttribute("alt",message);
			obj.setAttribute("title",message);
			obj.setAttribute("onclick","md_size("+obj.src+")");
			obj.onclick= function() {md_size(obj.src);};
			obj.setAttribute("onmouseover","md_cursor_pointer()");
			obj.setAttribute("onmouseout","md_cursor_hand()");
			obj.onmouseover= function() {md_cursor_pointer();};
			obj.onmouseout= function() {md_cursor_hand();};
		}
	}
}

function md_size(url) {
	window.open(url);
}

function writeCookie(md_users_res_cookie) 
{
	var today = new Date();
	var the_date = new Date("December 31, 2023");
	var the_cookie_date = the_date.toGMTString();
	var the_cookie = md_users_res_cookie+"="+ screen.width +"x"+ screen.height;
	var the_cookie = the_cookie + ";expires=" + the_cookie_date + ";path=/";
	document.cookie=the_cookie 
}


function checkRes(width, height) {
    if(width != screen.width || height != screen.height) {
        writeCookie();
    } else {
        return true;
    }
}

function loadIm() {
	var lien= document.getElementsByTagName('A');
	for (var i= lien.length-1; i >= 0; --i) {
		if (lien[i].id.indexOf('lienim') != -1) {
			lien[i].onclick= changeim;
		}
	}
	var span= document.getElementsByTagName('SPAN');
	for (var i= span.length-1; i >= 0; --i) {
		if (span[i].className.indexOf('collapsable') != -1) {
			span[i].onclick= evtStop;
		}
	}
	var ol= document.getElementsByTagName('OL');
	for (var i= ol.length-1; i >= 0; --i) {
		if (ol[i].className == 'olcode') {
			ol[i].ondblclick= switchNumbering;
		}
	}
}
function evtStop() {
	allow_hide_im= 0;
}
function hideIm() {
	if (allow_hide_im == 1) {
		im_affichage_off(opened_im);
	}
	allow_hide_im= 1;
}
function changeim() {
	id= this.id.replace('lienim','');
	im_change_affichage(id);
	return false;
}
/*
function hide_all_im() {
	var span=document.getElementsByTagName('SPAN');
	for (var i=span.length-1; i>=0; --i) {
		if (span[i].className.indexOf('uncollapsed') !=-1) {
			span[i].className=span[i].className.replace('collapsed','uncollapsed');
		}
	}
}*/
function im_change_affichage(numreponse) {
	if (opened_im != 0 && opened_im != numreponse) {
		im_affichage_off(opened_im);
	}
	var im=document.getElementById('im'+numreponse);
	if (im.className.indexOf('uncollapsed') != -1) {
		im_affichage_off(numreponse);
	} else {
		im_affichage_on(numreponse);
	}
}
function im_affichage_on(numreponse) {
	var im= document.getElementById('im'+numreponse);
	im.className= im.className.replace('collapsed','uncollapsed');
	im.style.zIndex= 10000;
	opened_im= numreponse;
}
function im_affichage_off(numreponse) {
	var im=document.getElementById('im'+numreponse);
	if (im) {
		im.className=im.className.replace('uncollapsed','collapsed');
		opened_im= 0;
	}
}

function warning1(value,texte) {
	if (confirm(texte)) {
		location=value;
		return true;
	} else {
		return false;
	}
}
function montrer_spoiler(value) {
	var actual=document.getElementById(value).style.visibility;
	if (actual=='visible') {
		document.getElementById(value).style.visibility='hidden';
	} else {
		document.getElementById(value).style.visibility='visible';
	}
}

function quoter(add,cat,post,numreponse) {
	var date=new Date;
	date.setHours(date.getHours()+1);
	var name='quotes'+ add +'-'+ cat +'-'+ post;
	quotes=LireCookie(name);
	if (document.getElementById('plus'+numreponse).style.display!='none') {
		quotes=quotes.replace('|'+numreponse, '');
		quotes=quotes+"|"+numreponse;
		document.getElementById('plus'+numreponse).style.display='none';
		document.getElementById('moins'+numreponse).style.display='inline';
		document.getElementById('viderliste').style.display='inline';
	} else {
		quotes=quotes.replace('|'+numreponse, '');
		document.getElementById('plus'+numreponse).style.display='inline';
		document.getElementById('moins'+numreponse).style.display='none';
	}
	if (quotes=='') vider_liste(name);
	else EcrireCookie(name, quotes, date, '/');
}



// http://www.actulab.com/ecrire-les-cookies.php
function EcrireCookie(nom, valeur) {
	var argv=EcrireCookie.arguments;
	var argc=EcrireCookie.arguments.length;
	var expires=(argc > 2) ? argv[2] : null;
	var path=(argc > 3) ? argv[3] : null;
	var domain=(argc > 4) ? argv[4] : null;
	var secure=(argc > 5) ? argv[5] : false;
	document.cookie=nom+'='+escape(valeur)+
	((expires ==null) ? '' : ('; expires='+expires.toGMTString()))+
	((path ==null) ? '' : ('; path='+path))+
	((domain ==null) ? '' : ('; domain='+domain))+
	((secure ==true) ? '; secure' : '');
}

// http://www.actulab.com/lire-les-cookies.php
function getCookieVal(offset) {
	var endstr=document.cookie.indexOf (';', offset);
	if (endstr==-1) endstr=document.cookie.length;
	return unescape(document.cookie.substring(offset, endstr));
}
function LireCookie(nom) {
	var arg=nom+'=';
	var alen=arg.length;
	var clen=document.cookie.length;
	var i=0;
	while (i<clen) {
		var j=i+alen;
		if (document.cookie.substring(i, j)==arg) return getCookieVal(j);
		i=document.cookie.indexOf(' ',i)+1;
		if (i ==0) break;
	}
	return '';
}

// http://www.actulab.com/effacer-les-cookies.php
function EffaceCookie(nom) {
	var date=new Date;
	date.setFullYear(date.getFullYear()-1);
	EcrireCookie(nom,null,date,'/');
}

function choper_reponse_rapide(numrep,ref) {
	document.getElementById('repondre_form').action=document.getElementById('repondre_form').action.replace('?','?ref=' + ref + '&numrep=' + numrep + '&');
	if (document.hop) {
		document.getElementById('repondre_contenu').value=document.hop.contenu.value;
	}
	document.getElementById('repondre_form').submit();
}

function vider_liste(nom) {
	for (i=0; i < listenumreponse.length; i++) {
		var numreponse=listenumreponse[i];
		if (document.getElementById('plus'+numreponse)) {
			document.getElementById('plus'+numreponse).style.display='inline';
			document.getElementById('moins'+numreponse).style.display='none';
		}
	}
	document.getElementById('viderliste').style.display='none';
	EffaceCookie(nom);
}

function switchNumbering() {
	var papa= this.parentNode;
	var change= (this.nodeName.toLowerCase() == 'ol');
	
	var container= change ? 'div' : 'ol';
	var toTag= change ? 'div' : 'li';
	var fromTag= change ? 'li' : 'div';

	var newNode= document.createElement(container);
	newNode.className= 'olcode';
	newNode.ondblclick= switchNumbering;
	
	var lst= this.getElementsByTagName(fromTag);
	
	for(var i= 0; i < lst.length; ++i) {
		var tag= document.createElement(toTag);
		tag.innerHTML = lst[i].innerHTML;
		newNode.appendChild(tag);
	}
	papa.insertBefore(newNode, this);
	papa.removeChild(this);
}

function switchNumbering2(that) {

	var papa = that.getElementsByTagName('pre')[0];
	var oldContainer = papa.firstChild;
	var change = (oldContainer.nodeName.toLowerCase() == "ol");

    var container = change ? "dl" : "ol";
    var toTag = change ? "dd" : "li";
    var fromTag = change ? "li" : "dd"; 

	var newNode = document.createElement(container);

	var lst = oldContainer.getElementsByTagName(fromTag);

	for(var i = 0; i < lst.length; ++i) {
		var tag = document.createElement(toTag);
        // faut que ie fasse différemment de tous le monde :o
        if (document.all) {
            tag.innerText = lst[i].innerText;
        } else {
            tag.innerHTML = lst[i].innerHTML;
        }

        newNode.appendChild(tag);
	}
	papa.insertBefore(newNode, oldContainer);
	papa.removeChild(oldContainer);
}

/*====================================================*/
/*   Initialisation des onglets et des menus associé  */
/*====================================================*/
if(window.attachEvent) {
	window.attachEvent('onload', loadIm);//IE
	document.attachEvent('onclick', hideIm);
} else if(window.addEventListener) {
	window.addEventListener('load', loadIm, false);//Gecko compatible
	document.addEventListener('click', hideIm, false);
} else if(window.onload !=null) {
	OL = window.onload;  //Old browser sucks
	window.onload = function() {
		loadIm();
		OL();
	}
	document.onclick = hideIm;
} else {
	//browser really sucks
	window.onload = loadIm;
	document.onclick = hideIm;
}

/*====================================================*/
/*   function to get xhttpxmlrequest         */
/*====================================================*/

function xhttprequest_forum2() {
	if (window.XMLHttpRequest)	{
		req = new XMLHttpRequest();
	}	else if (window.ActiveXObject) 	{
		try {	req = new ActiveXObject("Msxml2.XMLHTTP");	} 
		catch (e)	{
			try {
				req = new ActiveXObject("Microsoft.XMLHTTP");
			} catch (e) {}
		}
	}
	return req;
}

/*====================================================*/
/*   Gestion du star rating                           */
/*====================================================*/

function star_rating(nonumreponse,nbstar,total,vote_img,img_path) {
	idstardiv= document.getElementById('affstarrating'+nonumreponse);
	var inneraff = '';
	for (i=1;i<(total+1);i++) {
		if (i > nbstar) {
			document.getElementById('star-'+nonumreponse+'-'+i).src=img_path+'/icones/trans.gif';
		} else {
			document.getElementById('star-'+nonumreponse+'-'+i).src=vote_img;
		}
	}
}

function star_rating_vote(idelu,novote,repmodif,idsite,path,centerornot,config) {
	var req = null; 

	req= xhttprequest_forum2();

	req.onreadystatechange = function() 
	{ 
		if(req.readyState == 4) 
		{
			if(req.status == 200)	{
				retour=req.responseText;
				document.getElementById('managestarrating'+repmodif).innerHTML=retour;
			} 
		} 
	}; 

	req.open("GET",path+'/user/starrating.php?operation=1&config='+config+'&idelu='+idelu+'&novote='+novote+'&repmodif='+repmodif+'&idsite='+idsite+'&centerornot='+centerornot, true); 
	req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded"); 
	req.send(null); 
}

var save_para_editin= new Array();

function edit_in_restore(numreponse) {
	document.getElementById('para'+numreponse).innerHTML= save_para_editin[numreponse];
}
function edit_in(config,cat,post,numreponse,path) {
	if (!save_para_editin[numreponse]) {
		save_para_editin[numreponse]= document.getElementById('para'+numreponse).innerHTML;
	}
	var req = null; 

	req= xhttprequest_forum2();

	req.onreadystatechange = function() 
	{ 
		if(req.readyState == 4) 
		{
			if(req.status == 200)	{
				retour=req.responseText;
				if (retour != 'errorlimit' && retour != 'errorjs') {
					document.getElementById('para'+numreponse).innerHTML= retour;
					if (document.getElementById('submitreprap')) {
						document.getElementById('submitreprap').accessKey='';
					}
				}
			} 
		} 
	}; 

	req.open("GET",path+'/user/editin.php?opeajax=1&config='+config+'&cat='+cat+'&post='+post+'&numreponse='+numreponse, true); 
	req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded"); 
	req.send(null); 

}

function edit_in_post(config,cat,post,numreponse,path) {
	var rep_edit= document.getElementById('rep_editin_'+numreponse).value;
	
	var req = null; 

	req= xhttprequest_forum2();

	req.onreadystatechange = function() 
	{ 
		if(req.readyState == 4) 
		{
			if(req.status == 200)	{
				retour=req.responseText;
				if (retour != 'errorjs') {
					document.getElementById('para'+numreponse).innerHTML= retour;
					save_para_editin[numreponse]= document.getElementById('para'+numreponse).innerHTML;
				} else {
					edit_in_restore(numreponse);
				}
			} 
		} 
	}; 

	req.open("POST",path+'/user/editin.php?opeajax=2&config='+config+'&cat='+cat+'&post='+post+'&numreponse='+numreponse, true); 
	req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded"); 
	rep_edit = rep_edit.replace(/(\+)/g, "&plus;"); 
	rep_edit = rep_edit.replace(/(€)/g, "&euro;"); 
	req.send('newrep='+encodeURIComponent(rep_edit)); 
	document.getElementById('submitreprap').accessKey='s';
}

