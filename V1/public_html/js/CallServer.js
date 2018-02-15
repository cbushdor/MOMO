// Constructeur de la "classe" Callserver
// http://www.xul.fr/xml-ajax.html

function CallServer () {
	this.xhr_object;
	this.server_response;

	this.createXMLHTTPRequest = createXMLHTTPRequest;
	this.sendDataToServer = sendDataToServer;
	this.displayAnswer = displayAnswer;
	this.launch = launch;
}

//On crée l'objet XMLHttpRequest

function createXMLHTTPRequest() {
	this.xhr_object = null;

	if(window.XMLHttpRequest) {
		this.xhr_object = new XMLHttpRequest();
	}
	else if(window.ActiveXObject) {
		this.xhr_object = new ActiveXObject("Microsoft.XMLHTTP");
	}
	else {
		alert("Your browser doesn't provide XMLHttprequest functionality");
		return;
	}
}

//On envoit des données au serveur et on reçoit la réponse en mode synchrone dans this.server_response

function sendDataToServer (data_to_send) {
	var xhr_object = this.xhr_object;

	xhr_object.open("POST", "../cgi-bin/Server.cgi", false);

	xhr_object.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

	xhr_object.send(data_to_send);

	if(xhr_object.readyState == 4) {
		this.server_response = xhr_object.responseText;
	}
}

//On injecte la réponse du serveur dans la div nommée resultat

function displayAnswer () {
	document.getElementById("resultat").innerHTML = this.server_response;
}

//Exécution du Javascript

function launch () {
	this.sendDataToServer(document.getElementById("yourtext").value);

	this.displayAnswer();
}

function myPing(url) {
	var xhttp = new XMLHttpRequest();
	var sta;
	var res;
	xhttp.onreadystatechange = function() {
		res = (this.status == 200);
		sta = this.status;
	};
	xhttp.open("GET", url, true);
	xhttp.send();
	return {StatusRes:res,Status:sta};
}
//Création de l'objet call_server

var call_server = new CallServer();
call_server.createXMLHTTPRequest();
