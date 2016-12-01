
var timeout;

function getCheckedValue(radioObj) {
	if(!radioObj)
		return "";
	var radioLength = radioObj.length;
	if(radioLength == undefined)
		if(radioObj.checked)
			return radioObj.value;
		else
			return "";
	for(var i = 0; i < radioLength; i++) {
		if(radioObj[i].checked) {
			return radioObj[i].value;
		}
	}
	return "";
}

function infoTimeout(id) { 
   timeout--; 
   if (timeout >0) {
         setTimeout("infoTimeout("+id+")", 1000);
   }
   else { 
		Windows.close('showPop'+id);
   } 
}

function EvaluationLoad(id){
	if ( Windows.getWindow('showPop'+id) != undefined ) {
		var win = Windows.getWindow('showPop'+id);
		win.setAjaxContent( '/forum/evaluer.php3?ID='+id+'&evaluation='+getCheckedValue(document.getElementById('ajoutEvaluation'+id).evaluation), {method:'get'}, false, false);
		timeout=2; 
		setTimeout("infoTimeout("+id+")", 1000);
	}
}

function showPop(id){
	Window.keepMultiModalWindow=false;
	if (Windows.getWindow('showPop'+id) == undefined ) {
		var	win = new Window('showPop'+id, {width:400, height:210, zIndex:100, resizable:false, title:"Evaluer le message", hideEffect:Element.hide, showEffect:Element.show, draggable: true, wiredDrag: true})
	}
	else {
		var win = Windows.getWindow('showPop'+id);
	}
	win.setHTMLContent('<table class="no" style="width:100%;height:100%;"><tr><td style="text-align:center;vertical-align:middle"><img src="/remote/images/progress.gif" alt=""></td></tr></table>');
	win.setAjaxContent("/forum/evaluer.php3?ID="+id, {method: 'get'}, false, false)
	win.setDestroyOnClose();
	win.showCenter(true);
	//win.toFront();
}

function Check() {
    if (!(document.ajout.email.value)&&(document.ajout.view.checked))
    {
        alert("Prière de saisir une adresse électronique");
        return false;
    }
    return true;
}

function Suivi() {
    if (document.ajout.email.value) document.ajout.view.checked = true;
    return true;
}

function montre(id) {
if (document.getElementById) {
document.getElementById(id).style.display="block";
} else if (document.all) {
document.all[id].style.display="block";
} else if (document.layers) {
document.layers[id].display="block";
}
return true;
}

function cache(id) {
if (document.getElementById) {
document.getElementById(id).style.display="none";
} else if (document.all) {
document.all[id].style.display="none";
} else if (document.layers) {
document.layers[id].display="none";
}
return true;
}
