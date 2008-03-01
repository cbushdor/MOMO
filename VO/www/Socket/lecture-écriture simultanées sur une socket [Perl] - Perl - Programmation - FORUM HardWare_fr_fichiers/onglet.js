var active_onglet= 0;
var no_hide= 0;
var sous_menu_actived= 0;
var stop_hide= 0;

function loadOnglet() {
	var lien= document.getElementsByTagName('A');
	for (var i= lien.length-1; i >= 0; --i) {
		if (lien[i].className.indexOf('onglet') != -1) {
			lien[i].onmouseover= OngletHoverIn;
			lien[i].onmouseout= OngletHoverOut;
			
			id=lien[i].id.replace('onglet','');
			if (document.getElementById('onglet_menu'+id)) {
				lien[i].onclick= OngletSelect;
			}
		}
	}
}
function OngletHoverIn() {
	var id=this.id.replace('onglet','');
	select_onglet(id);
}
function OngletHoverOut() {
	var id=this.id.replace('onglet','');
	if (!document.getElementById('onglet_menu'+id)
		|| document.getElementById('onglet_menu'+id).style.display!='block') {
		unselect_onglet(id);
	}
}

function select_onglet(num) {
	if (document.getElementById('befor'+num) && !document.getElementById('onglet_menu'+num)) {
		select_onglet_sub(num);
	}
	if (active_onglet != num) {
		hide_all_menu();
	}
	glisse_menu(num);
}
function unselect_onglet(num) {
	if (document.getElementById('befor'+num)
		&& document.getElementById('onglet'+num).className == 'ongletonmouseover') {
		document.getElementById('befor'+num).className='beforonglet';
		document.getElementById('onglet'+num).className='onglet';
		document.getElementById('after'+num).className='afteronglet';
	}
}
function select_onglet_sub(num) {
	if (document.getElementById('onglet'+num).className == 'onglet') {
		document.getElementById('befor'+num).className='beforongletsel';
		document.getElementById('onglet'+num).className='ongletonmouseover';
		document.getElementById('after'+num).className='afterongletsel';
	}
}

function hide_all_menu() {
	if (no_hide == 0) {
		var div=document.getElementsByTagName('DIV');
		for(var i=div.length-1; i>=0; --i) {
			if(div[i].id.indexOf('onglet_menu') !=-1 && div[i].style.display != 'none') {
				div[i].style.display='none';
				
				var id=div[i].id.replace('onglet_menu','');
				unselect_onglet(id);
			}
		}
	}
	no_hide= 0;
}
function glisse_menu(num) {
	if (sous_menu_actived == 1) {
		if (document.getElementById('onglet_menu'+num)) {
			document.getElementById('onglet_menu'+num).style.display='block';
			select_onglet_sub(num);
		}
		active_onglet= num;
	}
}
function OngletSelect() {
	var id= this.id.replace('onglet','');
	if (document.getElementById('onglet_menu'+id).style.display != 'block') {
		document.getElementById('onglet_menu'+id).style.display='block';
		select_onglet_sub(id);
		sous_menu_actived= 1;
		active_onglet= id;
		stop_hide= 1;
	} else {
		document.getElementById('onglet_menu'+id).style.display='none';
		unselect_onglet(id);
		sous_menu_actived= 0;
		active_onglet= 0;
		stop_hide= 1;
	}
	return false;
}
/*====================================================*/
/*   Evenements associés aux onmouseover/onmouseout   */
/*====================================================*/

function hideMenu() {
	if (stop_hide == 0) {
		hide_all_menu();
		sous_menu_actived= 0;
	}
	stop_hide= 0;
}
/*====================================================*/
/*   Initialisation des onglets et des menus associé  */
/*====================================================*/
if(window.attachEvent) {
	window.attachEvent('onload', loadOnglet);//IE
	document.attachEvent('onclick', hideMenu);
} else if(window.addEventListener) {
	window.addEventListener('load', loadOnglet, false);//Gecko compatible
	document.addEventListener('click', hideMenu, false);
} else if(window.onload !=null) {
	OL = window.onload;  //Old browser sucks
	window.onload = function() {
		loadOnglet();
		OL();
	}
	document.onclick = hideMenu;
} else {
	//browser really sucks
	window.onload = loadOnglet;
	document.onclick = hideMenu;
}
