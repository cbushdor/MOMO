//-------------------------------------------------------------
//  Nom Document : GFBULLE.JS
//  Auteur       : G.Ferraz
//  Objet        : Info Bulle...
//  Création     : 01.12.2003
//-------------------------------------------------------------
//  Mise à Jour  : 29.05.2006
//  Objet        : Compatibilité IE6 et DOCTYPE
//  -----------------------------------------------------------
//  Mise à Jour  : 21.06.2006
//  Objet        : Prise en compte des <SELECT>
//  -----------------------------------------------------------
//  Mise à Jour  : 15.09.2006
//  Objet        : Amélioration et modif suite à commentaires
//  -----------------------------------------------------------
//  Mise à Jour  : 10.11.2006
//  Objet        : Correction Bug sous FF si document <DIV style="float...">
//  -----------------------------------------------------------
var DOM = (document.getElementById ? true : false);
var IE  = (document.all && !DOM ? true : false);
var NAV_OK   = ( DOM || IE );
var NETSCAPE = ( navigator.appName == 'Netscape');
var EXPLORER = ( navigator.appName == 'Microsoft Internet Explorer');
var OPERA    = ( window.opera ? true : false);
var Mouse_X;          // Position X en Cours de la Mouse
var Mouse_Y;          // Position Y en Cours de la Mouse
var Client_Y;          // Position Y de la Mouse relative à la fenêtre
var Decal_X  = -10;   // Décalage X entre Pointeur Mouse et Bulle
var Decal_Y  = -10;   // Décalage Y entre Pointeur Mouse et Bulle
var bBULLE   = false; // Flag Affichage de la Bulle
// Flag pour présence Select sous IE
var bSELECT  = false; // ( navigator.appName =='Microsoft Internet Explorer') && !OPERA;
var bISSET = false;

//-- Pour Test mode Cadre
var ZObjet = new RECT();   // Zone pour MouseMove
var ZBulle = new RECT();
var bCADRE = false;        // Flag Affichage du Cadre
var bINIT  = false;
var Fenetre = new RECT();
//=========================
// Définition pour le Cadre
//=========================
function RECT(){
	this.Left   =0;
	this.Top    =0;
	this.Right  =0;
	this.Bottom =0;
	this.InitRECT = RECT_Set;
	this.PtInRECT = RECT_PtIn;
}
//-------------------------------------------
function RECT_Set( left_, top_, larg_, haut_){
	with( this){
		Left   = ( left_ ? left_ : -1);
		Top    = ( top_  ? top_  : -1);
		Right  = Left + ( larg_ ? (larg_ -1): 0);
		Bottom = Top  + ( haut_ ? (haut_ -1): 0);
	}
}
//-------------------------
function RECT_PtIn( x_, y_){
	with( this){
		return(( x_ > Left) && ( x_ < Right) && ( y_ > Top ) && ( y_ < Bottom));
		if( x_ < Left || x_ > Right)  return( false);
		if( y_ < Top  || y_ > Bottom) return( false);
		return( true);
	}
}
//---------------------
function GetObjet(div_){
	if( DOM) return document.getElementById(div_);
	if( IE)  return document.all[div_];
	return( null);
}
//-----------------------------
function ObjWrite( div_, html_){
	var Obj = GetObjet( div_);
	if( Obj)
	Obj.innerHTML = html_;
}
//-- 10.11.2006 ----------------------------
// correction bug sur <DIV style="float...">
//------------------------------------------
function Get_DimFenetre(){
	var L_Doc;
	var H_Doc;
	var DocRef;

	with( Fenetre){
		if( window.innerWidth){
			with( window){
				Left   = pageXOffset;
				Top    = pageYOffset;
				Right  = innerWidth;
				Bottom = innerHeight;
				//-- Modif du 10.11.2006
				L_Doc = document.body.clientWidth;
				H_Doc = document.body.clientHeight;
				//-- fin modif.
				if( Right  > L_Doc) Right  = L_Doc;
				if( Bottom > H_Doc) Bottom = H_Doc;
			}
		}
		else{ // Cas Explorer à part
			if( document.documentElement && document.documentElement.clientWidth)
			DocRef = document.documentElement;
			else
			DocRef = document.body;

			with( DocRef){
				Left   = scrollLeft;
				Top    = scrollTop;
				Right  = clientWidth;
				Bottom = clientHeight;
			}
		}
		//-- limite Maxi Fenêtre Affichage
		Right  += Left;
		Bottom += Top;
	}
}
//------------------------------------
function ObjShowAll( div_, x_, y_, z_){
	var B_Obj = GetObjet( div_);
	var F_Obj = GetObjet( 'F' +div_);
	var MaxX, MaxY;
	var Haut, Larg;
	var SavY = y_;
	var SavX = x_;
    var Decal_Client_Y = Client_Y - Decal_Y;
	if( B_Obj){
		//-- Récup. dimension du DIV
		if( NETSCAPE){
			Larg = B_Obj.offsetWidth;
			Haut = B_Obj.offsetHeight;
		}
		else{
			Larg = B_Obj.scrollWidth;
			Haut = B_Obj.scrollHeight;
		}
		with( Fenetre){
			//-- Réajuste dimension fenêtre
			MaxX = Right  - Larg;
			MaxY = Bottom - Haut;

			//-- Application Bornage
			if( x_ > MaxX) x_ = MaxX;
			if( x_ < Left) x_ = Left;
			if( y_ > MaxY) y_ = MaxY;
			if( y_ < Top)  y_ = Top;
		}
		
		//-- si en bas On réajuste
		//-- pour que la bulle ne prenne pas le focus
		if( y_== MaxY && (Decal_Client_Y >= Larg)){
			var DeltaY = MaxY -SavY;
			y_ = MaxY - DeltaY -Haut -2*Decal_Y;
		}		
		// Si on est en bas à droite et qu'il ne reste plus assez de place pour l'élément à afficher
		else if(y_ >= MaxY && x_ >= MaxX) {
			/* Et Si la hauteur globale du document est inférieure à la hauteur de l'élement à afficher
			if(MaxX <= 0){
			    // Alors on désactive le bornage sur x pour que l'élement ne fasse pas perdre le focus
				x_ = SavX;
			}*/
			/* On désactive le bornage sur y pour que l'élement ne fasse pas perdre le focus*/
			y_ = SavY;			
		}	

		//-- On place la Bulle
		if( bSELECT){//-- Ajout pour SELECT sous IE
			with(F_Obj.style){
				left       = x_ +"px";
				top        = y_ +"px";
				zIndex     = z_-1;
				visibility = "visible";
			}
		}
		with(B_Obj.style){
			left       = x_ +"px";
			top        = y_ +"px";
			zIndex     = z_;
			visibility = "visible";
		}
		//-- Affectation Zone du Rectangle
		ZBulle.InitRECT( x_, y_, Larg, Haut);
	}
}
//-- 15.09.2006 ------------------------
// Ajout Fonction addEvent
//--------------------------------------
// written by Dean Edwards, 2005
// with input from Tino Zijdel, Matthias Miller, Diego Perini

// http://dean.edwards.name/weblog/2005/10/add-event/

function addEvent(element, type, handler) {
	if (element.addEventListener) {
		element.addEventListener(type, handler, false);
	} else {
		// assign each event handler a unique ID
		if (!handler.$$guid) handler.$$guid = addEvent.guid++;
		// create a hash table of event types for the element
		if (!element.events) element.events = {};
		// create a hash table of event handlers for each element/event pair
		var handlers = element.events[type];
		if (!handlers) {
			handlers = element.events[type] = {};
			// store the existing event handler (if there is one)
			if (element["on" + type]) {
				handlers[0] = element["on" + type];
			}
		}
		// store the event handler in the hash table
		handlers[handler.$$guid] = handler;
		// assign a global event handler to do all the work
		element["on" + type] = handleEvent;
	}
};
// a counter used to create unique IDs
addEvent.guid = 1;

function removeEvent(element, type, handler) {
	if (element.removeEventListener) {
		element.removeEventListener(type, handler, false);
	} else {
		// delete the event handler from the hash table
		if (element.events && element.events[type]) {
			delete element.events[type][handler.$$guid];
		}
	}
};

function handleEvent(event) {
	var returnValue = true;
	// grab the event object (IE uses a global event object)
	event = event || fixEvent(((this.ownerDocument || this.document || this).parentWindow || window).event);
	// get a reference to the hash table of event handlers
	var handlers = this.events[event.type];
	// execute each event handler
	for (var i in handlers) {
		this.$$handleEvent = handlers[i];
		if (this.$$handleEvent(event) === false) {
			returnValue = false;
		}
	}
	return returnValue;
};

function fixEvent(event) {
	// add W3C standard event methods
	event.preventDefault = fixEvent.preventDefault;
	event.stopPropagation = fixEvent.stopPropagation;
	return event;
};
fixEvent.preventDefault = function() {
	this.returnValue = false;
};
fixEvent.stopPropagation = function() {
	this.cancelBubble = true;
};
//-- 15.09.2006 ------------------------
// Utilisation de addEvent
//--------------------------------------
function Init_Bulle(){
	//-- Pour les SELECT on supprime l'événement hérite
	var Obj = document.body.getElementsByTagName('SELECT');
	if( Obj && Obj.length){
		for(var i=0; i < Obj.length; i++){
			if( Obj[i].size == 1){
				for(var k=0; k < Obj[i].options.length; k++){
					addEvent( Obj[i].options[k], 'mousemove', BulleHide);
				}
			}
			addEvent( Obj[i], 'mousedown', BulleHide);
			addEvent( Obj[i], 'scroll', BulleHide);
		}
	}
	else
	bSELECT = false; // Pas de SELECT dans le document
	bINIT =true;
}
////////////////////////////
// mode Cadre Indépendant //
////////////////////////////
//------------------------

function CadreWrite( txt_){
	var Html;
	var B_Obj = GetObjet( 'Bulle');
	var F_Obj = GetObjet( 'FBulle');
	if( !bINIT) Init_Bulle();
	if( B_Obj){
		//-- Récup dimension d'affichage
		Get_DimFenetre();
		Decal_X = -10;  // Decalage dans de la Bulle
		Decal_Y = -10;
		Html  = "<table border='1' bordercolor='#062a51' cellspacing=0 cellpadding=2 bgcolor='#e3ecff'>";
		Html += "<tr><td class='Bulle' nowrap>";
		Html += txt_;
		Html += "</td></tr></table>";
		B_Obj.innerHTML = Html;

		if( bSELECT){ //-- Ajout pour SELECT sous IE
			with(F_Obj.style){
				height = B_Obj.offsetHeight;
				width  = B_Obj.offsetWidth;
				left   = B_Obj.offsetLeft;
				top    = B_Obj.offsetTop;
			}
		}
		//-- On affiche le résultat
		//ObjShowAll('Bulle', Mouse_X +Decal_X, Mouse_Y +Decal_Y, 1000);
		bCADRE= true;
		return( true);
	}
	return(false);
}
////////////////////////////
// mode Bulle Indépendant //
////////////////////////////
//-- 15.09.2006 ------------------------
// Ajout paramètre x_ et y_
//--------------------------------------



function BulleWrite( txt_, e_, x_, y_){
	if(!bISSET){
		bISSET=true;
		addEvent( document, 'mousemove', WhereMouse);

		if(e_){
			WhereMouse(e_);
		}
		else {
			var fireOnThis = document/*.getElementById('someID')*/;
			if( document.createEvent ) {
				var evObj = document.createEvent('MouseEvents');
				
				/*if(e_) evObj.initMouseEvent( 'mousemove', true, false, window, 0, e_.screenX, e_.screenY, e_.clientX, e_.clientY, false, false, true, false, 0, null );			
				else*/			
				evObj.initEvent( 'mousemove', true, false );
				fireOnThis.dispatchEvent(evObj);
			} else if( document.createEventObject ) {
				fireOnThis.fireEvent('onmousemove');
			}
		}


	}
	var B_Obj = GetObjet( 'Bulle');
	var F_Obj = GetObjet( 'FBulle');
	var Html;
	if( !bINIT) Init_Bulle();
	if( B_Obj){
		//-- Récup dimension d'affichage
		Get_DimFenetre();
		// Decalage hors de la Bulle
		Decal_X =( x_ ? x_: 15);//    Decal_X = 5 par défaut
		Decal_Y =( y_ ? y_: 15);//    Decal_Y = 5 par défaut
		//-- Ecriture de la Bulle
		//Html  = "<table border=0 cellspacing=0><tr><td bgcolor='#062a51'>";
		//Html += "<table border=0 cellspacing=0 cellpadding=0 width='100%' bgcolor='#e3ecff'>";
		//Html += "<tr><td class='Bulle' nowrap>";
		//Html += txt_;
		Html = txt_;
		//Html += "</td></tr></table></td></tr></table>";
		B_Obj.innerHTML = Html;
		//-- Ajout pour SELECT sous IE
		if( bSELECT){
			with(F_Obj.style){
				height = B_Obj.offsetHeight;
				width  = B_Obj.offsetWidth;
				left   = B_Obj.offsetLeft;
				top    = B_Obj.offsetTop;
			}
		}
		//-----------------------------------------//
		// IMPORTANT on n'affiche pas la Bulle     //
		// l'événement MouseOver va avec MouseMove //
		//-----------------------------------------//
		ObjShowAll('Bulle', Mouse_X +Decal_X, Mouse_Y +Decal_Y, 1000);
		bBULLE= true;
		return( true);
	}
	return(false);
}


//------------------
function BulleHide(){
	var B_Obj = GetObjet( 'Bulle');
	var F_Obj = GetObjet( 'FBulle');

	if( bSELECT){ //-- Ajout pour SELECT sous IE
		F_Obj.style.height = 0 +"px";
	}
	with(B_Obj){
		innerHTML        = "&nbsp;"
		style.left       = -1000 +"px";
		style.top        = -1000 +"px";
		style.zIndex     = 0;
		style.visibility = "hidden";
	}
	//-- Pose les Flags
	bCADRE = false;
	bBULLE = false;
	if(bISSET){
		bISSET=false;
		removeEvent(document, "mousemove", WhereMouse);
	}

	return(true);
}
//--------------------
function WhereMouse(e){
	var DocRef;
	var Obj  = null;
	var bRECT= true;
	//-- On traque les hybrides
	if( e && e.target){
		Mouse_X = e.pageX;
		Mouse_Y = e.pageY;
		Client_Y = e.clientY;
		Obj     = e.target;
		//-- Spécifique FireFox
		if( Obj.boxObject){
			with( Obj){
				//-- La Zone de prise en compte
				ZObjet.InitRECT( boxObject.x, boxObject.y, boxObject.width, boxObject.height);
			}
			//-- Barre de défilement et autre sous FireFox
			Obj = e.originalTarget;
			if( Obj)
			if( Obj.prefix =="xul"){
				BulleHide();
				return( true);
			}
			//-- Test pour SELECT sous FireFox
			bRECT = ZObjet.PtInRECT( Mouse_X, Mouse_Y);
		}
	}//-- Endif NETSCAPE
	else{
		
		var e = window.event||window.Event;
		if( document.documentElement && document.documentElement.clientWidth)
		DocRef = document.documentElement;
		else
		DocRef = document.body;

		Client_Y = e.clientY;
		Mouse_X = e.clientX +DocRef.scrollLeft;
		Mouse_Y = e.clientY +DocRef.scrollTop;
	}
	
	if(window.Event && document.captureEvents) document.captureEvents(Event.MOUSEMOVE);

	if( bBULLE)
	if( bRECT)
	ObjShowAll('Bulle', Mouse_X +Decal_X, Mouse_Y +Decal_Y, 1000);

	if( bCADRE)// on ne move pas on test juste si dans Rect
	if( !ZBulle.PtInRECT( Mouse_X, Mouse_Y))
	BulleHide();

	return( true);
}
//== INITIALISATION ==================================
//-- 15.09.2006 ------------------------
// Ajout Fonction addEvent
// Permet de faire autre chose...
//--------------------------------------

function MM_swapImgRestore() { //v3.0
	var i,x,a=document.MM_sr; for(i=0;a&&i<a.length&&(x=a[i])&&x.oSrc;i++) x.src=x.oSrc;
}

function MM_preloadImages() { //v3.0
	var d=document; if(d.images){ if(!d.MM_p) d.MM_p=new Array();
	var i,j=d.MM_p.length,a=MM_preloadImages.arguments; for(i=0; i<a.length; i++)
	if (a[i].indexOf("#")!=0){ d.MM_p[j]=new Image; d.MM_p[j++].src=a[i];}}
}

function MM_findObj(n, d) { //v4.01
	var p,i,x;  if(!d) d=document; if((p=n.indexOf("?"))>0&&parent.frames.length) {
		d=parent.frames[n.substring(p+1)].document; n=n.substring(0,p);}
		if(!(x=d[n])&&d.all) x=d.all[n]; for (i=0;!x&&i<d.forms.length;i++) x=d.forms[i][n];
		for(i=0;!x&&d.layers&&i<d.layers.length;i++) x=MM_findObj(n,d.layers[i].document);
		if(!x && d.getElementById) x=d.getElementById(n); return x;
}

function MM_swapImage() { //v3.0
	var i,j=0,x,a=MM_swapImage.arguments; document.MM_sr=new Array; for(i=0;i<(a.length-2);i+=3)
	if ((x=MM_findObj(a[i]))!=null){document.MM_sr[j++]=x; if(!x.oSrc) x.oSrc=x.src; x.src=a[i+2];}
}

// Affiche-Masque Calques

function HideContent(d) {
	if(d.length < 1) { return; }
	document.getElementById(d).style.display = "none";
}
function ShowContent(d) {
	if(d.length < 1) { return; }
	document.getElementById(d).style.display = "block";
}
function ReverseContentDisplay(d) {
	if(d.length < 1) { return; }
	if(document.getElementById(d).style.display == "none") { document.getElementById(d).style.display = "block"; }
	else { document.getElementById(d).style.display = "none"; }
}



// Routage liste déroulante

function MM_jumpMenu(targ,selObj,restore){ //v3.0
	eval(targ+".location='"+selObj.options[selObj.selectedIndex].value+"'");
	if (restore) selObj.selectedIndex=0;
}


var ie = (navigator.appName == "Microsoft Internet Explorer") ? 1:0;

function afficheMasque(id,link){
	var element = document.getElementById(id);
	if(element){
		if(link.innerHTML.indexOf('Afficher')>=0){
			element.style.display = 'block';
			element.style.visible = 'visible';
			element.style.width = '100%';
			link.innerHTML = link.innerHTML.replace(/Afficher/,'Masquer');
		}
		else{
			element.style.display = 'none';
			element.style.visible = 'hidden';
			link.innerHTML = link.innerHTML.replace(/Masquer/,'Afficher');
		}
	}
}


function showAddLink(){
	Window.keepMultiModalWindow=true;
	if (Windows.getWindow('showAddLink') == undefined ) {
		var	win = new Window('showAddLink', {width:400, height:210, zIndex:100, resizable:false, title:"Ajouter un lien", hideEffect:Element.hide, showEffect:Element.show, draggable: true, wiredDrag: true})
	}
	else {
		var win = Windows.getWindow('showAddLink');
	}
	win.setHTMLContent('<table class="no" style="width:100%;height:100%;"><tr><td style="text-align:center;vertical-align:middle"><img src="/remote/images/progress.gif" alt=""></td></tr></table>');
	win.setAjaxContent("/remote/ajoutlien.php3", {method: 'get'}, false, false)
	win.setDestroyOnClose();
	win.showCenter(true);
}

function LinkLoad(Mot,dest){
	if ( Windows.getWindow('showAddLink') != undefined ) {
		var win = Windows.getWindow('showAddLink');
		win.setAjaxContent( '/remote/ajoutlien.php3?keyword='+Mot+'&dest='+dest, {method:'get'}, false, false);
	}
}

function insertLink (url, alt) {
	var link = '['+url+' '+alt+']';
	insertText('document.ajout.message', link+' ');
	return false;
}

function delProd(elementId){
	var num = 0;
	var txtObj = document.getElementById('products_list');
	for (i=0; i<txtObj.options.length; i++) {
		if (txtObj.options[i].selected == true) {
			num++;
		}
		if(num > 0){
			for(i=0;i<txtObj.options.length;i++){
				if(txtObj.options[i].selected == true){
					txtObj.options[i] = null;
				}
			}
			delProd(elementId);
		}
	}
}

function insertProd(elementId, idxToAdd, txtToAdd){
	var txtObj = document.getElementById('products_list');
	var deja=0;
	for (i=0; i<txtObj.options.length; i++) {
		if (txtObj.options[i].value==idxToAdd) {
			deja=1;
		}
	}
	if(!deja){
		txtObj.options[txtObj.options.length] = new Option(txtToAdd,idxToAdd);
	}
}

function insertText ( formName, txtToAdd) {
	var txtObj = eval ( formName );
	if (ie==1)
	{
		var str = document.selection.createRange().text;
		txtObj.focus();
		var sel = document.selection.createRange();
		sel.text = str + txtToAdd;
		return;
	}
	else
	{
		// position du scroll
		oldPos = txtObj.scrollTop;
		oldHght = txtObj.scrollHeight;

		// position du curseur
		pos = txtObj.selectionEnd + txtToAdd.length;

		txtObj.value = txtObj.value.substr(0, txtObj.selectionStart) +
		txtObj.value.substr(txtObj.selectionStart,
		txtObj.selectionEnd-txtObj.selectionStart) +
		txtToAdd + txtObj.value.substr(txtObj.selectionEnd);

		// repositionnement cuseur aprés la balise fermante
		// peut être grandemant amélioré ;-)
		txtObj.selectionStart = pos;
		txtObj.selectionEnd = pos;

		// calcul et application de la nouvelle bonne postion du scroll
		newHght = txtObj.scrollHeight - oldHght;
		txtObj.scrollTop = oldPos + newHght;
	}
	txtObj.focus();
}


/* menuDropdown.js - implements a dropdown menu based on a HTML list
* Author: Dave Lindquist (http://www.gazingus.org)
* Modified by: Nicolas Lesbats (nicolas lesbats at laposte net)
* Version: 0.1b (2004-03-11)
*/
var isMenu = true;
var maxWidth = 50;
/* maximum width of the submenus (in 'em' units) */
var borderBox  = false;
var horizontal = new Array();
var menuTop    = new Array();
var menuHeight = new Array();
var menuLeft   = new Array();
var menuWidth  = new Array();

//window.onload = function() { loadMenu(); }

function loadMenu(i) {
	
	if (!document.getElementById) return;
	var /*i = 0,*/ j, root, submenus, node, li, link, division;
	/*while (true) {*/
		root = document.getElementById("menuList" + (i + 1));
		if (root == null)
		/*break;*/ return;
		submenus = root.getElementsByTagName("ul");
		division = root.parentNode;

		if (document.createElement) {
			/* Win/IE5-6 trick: makes the whole width of the submenus clickable
			*/
			for (j = 0; j < submenus.length; j++) {
				node = submenus.item(j);
				if (node.className == "menux" && node.getElementsByTagName("ul").length == 0) {
					li = document.createElement("li");
					node.appendChild(li);
					li.style.position = "absolute";
					li.style.visibility = "hidden";
				}
			}
			/* checks whether the 'width' property applies to the border box or
			* the content box of an element
			*/
			if (i == 0) {
				li.style.display = "block";
				li.style.padding = "0";
				li.style.width   = "2px";
				li.style.border  = "1px solid";
				if (li.offsetWidth == 2)
				borderBox = true;
			}
		}

		initializeMenu(root, division, i);

		for (j = 0; j < submenus.length; j++) {
			node = submenus.item(j);
			if (node.className == "menux") {
				link = node.previousSibling;
				while (link != null) {
					if (link.className == "actuator") {
						initializeSubmenu(node, link, root, division);
						node.set();
						break;
					}
					link = link.previousSibling;
				}
			}
		}
	/*	i++;
	}*/
}

function initializeMenu(root, div, index) {

	horizontal[index] = menuIsHorizontal(root);
	menuTop[index]    = div.offsetTop;
	menuHeight[index] = div.offsetHeight;
	menuLeft[index]   = div.offsetLeft;
	menuWidth[index]  = div.offsetWidth;

	div.horizontal = function() {
		return horizontal[index];
	}

	div.checkMove = function() {
		if (this.hasMoved()) this.resetMenu();
	}

	div.hasMoved = function() {
		if (menuTop[index]    == this.offsetTop    &&
		menuHeight[index] == this.offsetHeight &&
		menuLeft[index]   == this.offsetLeft   &&
		menuWidth[index]  == this.offsetWidth)
		return false;
		return true;
	}

	div.resetMenu = function() {
		horizontal[index] = menuIsHorizontal(root);
		menuTop[index]    = this.offsetTop;
		menuHeight[index] = this.offsetHeight;
		menuLeft[index]   = this.offsetLeft;
		menuWidth[index]  = this.offsetWidth;

		var submenus = root.getElementsByTagName("ul");
		for (var j = 0; j < submenus.length; j++) {
			var node = submenus.item(j);
			if (node.className == "menux") {
				node.style.right = "";
				node.style.left  = "";
				if (!window.opera)
				node.style.width = "";
				node.set();
			}
		}
	}
}

function menuIsHorizontal(root) {
	var first = firstElement(root, "LI");
	if (first != null) {
		var second = first.nextSibling;
		while (second != null) {
			if (second.tagName == "LI") {
				first  = firstElement(first,  "A");
				second = firstElement(second, "A");
				if (first != null && second != null)
				if (first.offsetLeft == second.offsetLeft)
				return false;
				return true;
			}
			second = second.nextSibling;
		}
	}
	return true;
}

function initializeSubmenu(menu, actuator, root, div) {

	var parent = menu.parentNode;

	parent.onmouseover = function() {
		div.checkMove();
		menu.style.visibility = "visible";
	}

	actuator.onfocus = function() {
		div.checkMove();
		menu.style.visibility = "visible";
	}

	parent.onmouseout = function() {
		menu.style.visibility = "";
	}

	var tags = menu.getElementsByTagName("a");
	var link = tags.item(tags.length - 1);
	if (!link.onblur)
	link.onblur = function() {
		var node = link.parentNode.parentNode;
		while (node != menu) {
			node.style.visibility = "";
			node = node.parentNode.parentNode;
		}
		menu.style.visibility = "";
	}

	if (parent.parentNode == root) {
		menu.set = function() {
			setLocation1(this, actuator, root, div);
		}
	} else {
		menu.set = function() {
			setLocation2(this, actuator, div);
		}
	}
}

function setLocation1(menu, actuator, root, div) {
	var first = firstElement(menu, "LI");
	if (first != null)
	if (first.offsetParent == menu)
	setWidth(menu);
	if (div.horizontal()) {
		if (actuator.offsetParent == menu.offsetParent) {
			menu.style.left = actuator.offsetLeft + "px";
			menu.style.top  = actuator.offsetTop  + actuator.offsetHeight + "px";
		} else {
			/* happens in Win/IE5-6 when some ancestors are 'static' and have their
			* 'width' or 'height' different than 'auto' */
			var parent = actuator.offsetParent;
			var top  = 0;
			var left = 0;
			while (parent != menu.offsetParent && parent != null) {
				top  = top  + parent.offsetTop;
				left = left + parent.offsetLeft;
				parent = parent.offsetParent;
			}
			menu.style.left = left + actuator.offsetLeft + "px";
			menu.style.top  = top  + actuator.offsetTop  + actuator.offsetHeight + "px";
		}
	} else {
		menu.style.top = actuator.offsetTop + "px";
		menu.style.left = (div.offsetWidth + actuator.offsetWidth) / 2 + "px";
	}
}

function setLocation2(menu, actuator, div) {
	if (menu.offsetParent != document.body)
	setWidth(menu);
	menu.style.top = actuator.offsetTop + "px";
	menu.style.left = actuator.offsetWidth + "px";
}

function setWidth(menu) {
	menu.style.right = - maxWidth + "em";
	var width  = 0;
	var height = 0;
	var items = menu.getElementsByTagName("a");
	for (var i = 0; i < items.length; i++) {
		var link = items.item(i);
		if (link.parentNode.parentNode == menu) {
			height = height + link.offsetHeight;
			if (link.offsetWidth > width)
			width = link.offsetWidth;
		}
	}
	if (borderBox)
	width = width + (menu.offsetHeight - height);
	menu.style.width = width + "px";
}

function firstElement(node, name) {
	var first = node.firstChild;
	while (first != null) {
		if (first.tagName == name)
		return first;
		first = first.nextSibling;
	}
	return null;
}

// Rollover image

function MM_swapImgRestore() { //v3.0
	var i,x,a=document.MM_sr; for(i=0;a&&i<a.length&&(x=a[i])&&x.oSrc;i++) x.src=x.oSrc;
}

function MM_preloadImages() { //v3.0
	var d=document; if(d.images){ if(!d.MM_p) d.MM_p=new Array();
	var i,j=d.MM_p.length,a=MM_preloadImages.arguments; for(i=0; i<a.length; i++)
	if (a[i].indexOf("#")!=0){ d.MM_p[j]=new Image; d.MM_p[j++].src=a[i];}}
}

function MM_findObj(n, d) { //v4.01
	var p,i,x;  if(!d) d=document; if((p=n.indexOf("?"))>0&&parent.frames.length) {
		d=parent.frames[n.substring(p+1)].document; n=n.substring(0,p);}
		if(!(x=d[n])&&d.all) x=d.all[n]; for (i=0;!x&&i<d.forms.length;i++) x=d.forms[i][n];
		for(i=0;!x&&d.layers&&i<d.layers.length;i++) x=MM_findObj(n,d.layers[i].document);
		if(!x && d.getElementById) x=d.getElementById(n); return x;
}

function MM_swapImage() { //v3.0
	var i,j=0,x,a=MM_swapImage.arguments; document.MM_sr=new Array; for(i=0;i<(a.length-2);i+=3)
	if ((x=MM_findObj(a[i]))!=null){document.MM_sr[j++]=x; if(!x.oSrc) x.oSrc=x.src; x.src=a[i+2];}
}

// Affiche-Masque Calques

function HideContent(d) {
	if(d.length < 1) { return; }
	document.getElementById(d).style.display = "none";
}
function ShowContent(d) {
	if(d.length < 1) { return; }
	document.getElementById(d).style.display = "block";
}
function ReverseContentDisplay(d) {
	if(d.length < 1) { return; }
	if(document.getElementById(d).style.display == "none") { document.getElementById(d).style.display = "block"; }
	else { document.getElementById(d).style.display = "none"; }
}



// Routage liste déroulante

function MM_jumpMenu(targ,selObj,restore){ //v3.0
	eval(targ+".location='"+selObj.options[selObj.selectedIndex].value+"'");
	if (restore) selObj.selectedIndex=0;
}

function insertTag ( txtName, tag, enclose ) {
	var closeTag = ((enclose) ? "</" + tag + ">" : "");
	var Tag = "<" + tag + ">";
	var txtObj = eval ( txtName );
	if (ie==1)
	{
			var str = document.selection.createRange().text;
			txtObj.focus();
		var sel = document.selection.createRange();
			sel.text = Tag + str + closeTag;
			return;
	}
	else
	{
		// position du scroll
		oldPos = txtObj.scrollTop;
		oldHght = txtObj.scrollHeight;

		// position du curseur
		pos = txtObj.selectionEnd + Tag.length + closeTag.length;

		txtObj.value = txtObj.value.substr(0, txtObj.selectionStart) + Tag +
		txtObj.value.substr(txtObj.selectionStart,
		txtObj.selectionEnd-txtObj.selectionStart) +
		closeTag + txtObj.value.substr(txtObj.selectionEnd);

		// repositionnement cuseur aprés la balise fermante
		// peut être grandemant amélioré ;-)
		txtObj.selectionStart = pos;
		txtObj.selectionEnd = pos;

		// calcul et application de la nouvelle bonne postion du scroll
		newHght = txtObj.scrollHeight - oldHght;
		txtObj.scrollTop = oldPos + newHght;
	}
txtObj.focus();
}