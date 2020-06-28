var votes;
/*This function updates the upvote or down vote by user to database by making a POST request to endpoint add_votes*/
function upload_vote(status){
	if (status == 'pos'){
		votes['upvote'] += 1
	}
	if (status == 'neg'){
		votes['downvote'] += 1
	}
	document.getElementById('up-votes').innerHTML = votes['upvote'];
    document.getElementById('down-votes').innerHTML = votes['downvote'];
	var url = document.URL;
	var n = url.lastIndexOf('/');
	var result = url.substring(n + 1);
	var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "POST", "/add_votes", false );
    xmlHttp.send( JSON.stringify({'id' : result, 'upvote' : votes['upvote'], 'downvote' : votes['downvote']}) );
}

/*This function gets the votes for the loaded dataset and inserts a HTML code to make them visible to users*/
function get_votes(){
	var url = document.URL;
	var n = url.lastIndexOf('/');
	var result = url.substring(n + 1);
	var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "/get_votes/"+result, false );
    xmlHttp.send( null );
    obj = JSON.parse(xmlHttp.responseText);
    votes = obj;
    document.getElementById('up-votes').innerHTML = votes['upvote'];
    document.getElementById('down-votes').innerHTML = votes['downvote'];
    
}

/*This function hides or views the chat window when user clicks the show chat of hide chat button*/
function hide_chat(){
	if (document.getElementById("chat_body").style.visibility == "visible"){
		// document.getElementById("chat_button").style.opacity = "1";
		document.getElementById("chat_body").style.display = "none";
		document.getElementById("chat_button").innerHTML = '<button onclick="hide_chat()" style="float:right; margin-right: 30px; margin-bottom: 30px; background-color: black; " class="chat card-5"><img style="vertical-align:middle" src = "/extra/img/chat.png" height="50px" width="50px"></button>';
		document.getElementById("chat_body").style.visibility = "hidden";
	}
	else{
		document.getElementById("chat_body").style.display = "block";
		// document.getElementById("chat_button").style.opacity = "0";
		document.getElementById("chat_button").innerHTML = '<button onclick="hide_chat()" style="float:right; margin-right: 30px; margin-bottom: 30px; background-color: #438bde; " class="chat card-5"><img style="vertical-align:middle" src = "/extra/img/close.png" height="50px" width="50px"></button>';
		document.getElementById("chat_body").style.visibility = "visible";
	}
}

/*This function opens up the pop up window and also blurs the html objects which are not in the window*/
function pop_up(objecta){
	document.getElementById("blur").style.filter = "blur(6px)";
	// document.getElementById("display_contents").style.filter = "blur(0px)";
	var category = objecta.getAttribute("value");
	document.getElementById("display_contents").style.display = "block";
	document.getElementById("display_contents").style.zIndex = "100";
	document.getElementById("display_contents").innerHTML = '<button style = "float : right" onclick="close_popup()">close</button><br><h1 style = "background-color : black;" class = "floating-rect-heading">' + category + "<h1>";
	dataset_cat(category);

}

/*This function is called when the page is loaded and hides the profile view div*/
window.onload = function() {
	// document.getElementById('viewProfile').style.zIndex = "-1";
	// document.getElementById('viewProfile').style.display = 'none';
	get_votes();
};

/*This function is called when the user clicks on profile and it views or hides the profile div*/
function hide_profile(){
	var x = document.getElementById("viewProfile");
	if (x.style.display === "none") {
		x.style.zIndex = "10";
    	x.style.display = "block";
  	} else {
  		x.style.zIndex = "-1";
    	x.style.display = "none";
    }
}
