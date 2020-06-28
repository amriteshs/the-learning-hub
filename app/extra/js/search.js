/*This function gets the total score for top 10 users and dsiplays them as HTML table this loads the score by making GET request to 
leader_boards endpoint*/
function get_leaderbords(){
	var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "/leader_boards", false );
    xmlHttp.send( null );
    obj = JSON.parse(xmlHttp.responseText);
    var HTML = '';
    for(var key in obj){
    	HTML += '<tr><td>' + key + '</td><td>' + obj[key][1] + ' ' + obj[key][2] + '</td><td>' + obj[key][0] + '</td></tr>'; 
    }
    document.getElementById('socreboard').innerHTML += HTML;
}

/*This function hides or views the chat window when user clicks the show chat of hide chat button*/
function hide_chat(){
	if (document.getElementById("chat_body").style.visibility == "visible"){
		document.getElementById("chat_body").style.display = "none";
		document.getElementById("chat_button").innerHTML = '<button onclick="hide_chat()" style="float:right; margin-right: 30px; margin-bottom: 30px; background-color: black; " class="chat card-5"><img style="vertical-align:middle" src = "/extra/img/chat.png" height="50px" width="50px"></button>';
		document.getElementById("chat_body").style.visibility = "hidden";
	}
	else{
		document.getElementById("chat_body").style.display = "block";
		document.getElementById("chat_button").innerHTML = '<button onclick="hide_chat()" style="float:right; margin-right: 30px; margin-bottom: 30px; background-color: #438bde; " class="chat card-5"><img style="vertical-align:middle" src = "/extra/img/close.png" height="50px" width="50px"></button>';
		document.getElementById("chat_body").style.visibility = "visible";
	}
}

/*This function opens up the pop up window and also blurs the html objects which are not in the window*/
function pop_up(objecta){
	document.getElementById("blur").style.filter = "blur(6px)";
	var category = objecta.getAttribute("value");
	document.getElementById("display_contents").style.display = "block";
	document.getElementById("display_contents").style.zIndex = "100";
	document.getElementById("display_contents").innerHTML = '<button style = "float : right" onclick="close_popup()">close</button><br><h1 style = "background-color : black;" class = "floating-rect-heading">' + category + "<h1>";
	dataset_cat(category);

}

/*This function gets for categories and display them*/
function dataset_cat(name){
	var search_term = name;
	var dict = {"search_term" : search_term};
	$.ajax({
        type: 'GET',
        url: "/search_dataset/"+search_term,
        // data: JSON.stringify(dict),
        contentType: 'application/json',
        success: function(data){
        	var HTML = '<hr>';
        	var reply = JSON.parse(data);
        	if (isnotEmpty(reply)){
        		HTML += '<ul style = "list-style-type: none;">';
        		for (var key in reply){
        			HTML += '<li><a href = "/dataset/' + reply[key]['dataset_id'] + '">' + reply[key]['name'] + '</a><br><span>' + reply[key]['discription'] + '</li><hr>';
        		}
        		document.getElementById("display_contents").innerHTML += HTML;
        	}
        	else{
        		document.getElementById("display_contents").innerHTML += "No results found";
        	}
        	
        }
    });
}

/*This function closes the popup when close button on the popup is clicked*/
function close_popup(){
	document.getElementById("blur").style.filter = "blur(0px)";
	document.getElementById("blur").style.blur = "0px";
	document.getElementById("display_contents").style.display = "none";
	document.getElementById("display_contents").style.zIndex = "-1";
}

/*This function is called when the page is loaded and hides the profile view div*/
window.onload = function() {
	// document.getElementById('viewProfile').style.zIndex = "-1";
	// document.getElementById('viewProfile').style.display = 'none';
	get_leaderbords();
};

/*Checks if the list is not empty*/
function isnotEmpty(obj) {
    for(var key in obj) {
        if(obj.hasOwnProperty(key))
            return true;
    }
	return false;
}

/*This function search for dataset using term given by user and shows the retrived datasets as links*/
function search_dataset(){
	var search_term = document.getElementById("search_term").value;
    if (search_term.length != 0){
	// var dict = {"search_term" : search_term};
    	document.getElementById("search_results").innerHTML = '<img style = "height: 85px; width: 300px;" src = "/extra/img/loading.gif">';
    	$.ajax({
            type: 'GET',
            url: "/search_dataset/"+search_term,
            // data: JSON.stringify(dict),
            contentType: 'application/json',
            success: function(data){
            	var HTML = '<hr>';
            	var reply = JSON.parse(data);
            	if (isnotEmpty(reply)){
            		HTML += '<ul style = "list-style-type: none;">';
            		for (var key in reply){
            			HTML += '<li><a href = "/dataset/' + reply[key]['dataset_id'] + '">' + reply[key]['name'] + '</a><br><span>' + reply[key]['discription'] + '</li><hr>';
            		}
            		document.getElementById("search_results").innerHTML = HTML;
            	}
            	else{
            		document.getElementById("search_results").innerHTML = "No results found";
            	}
            	
            }
        });
    }
    else{
        alert('Search field not empty')
    }
}

/*This function searchs for learning activities using the term given by user and makes a POST request to /search_learning_activity endpoint*/
function search_learning(){
	var search_term = document.getElementById("search_term").value;
    if (search_term.length != 0){
	// var dict = {"search_term" : search_term};
    	document.getElementById("search_results").innerHTML = '<img style = "height: 85px; width: 300px;" src = "/extra/img/loading.gif">';
    	$.ajax({
            type: 'GET',
            url: "/search_learning_activity/"+search_term,
            // data: JSON.stringify(dict),
            contentType: 'application/json',
            success: function(data){
            	var HTML = '<hr>';
            	var reply = JSON.parse(data);
            	if (isnotEmpty(reply)){
            		HTML += '<ul style = "list-style-type: none;">';
            		for (var key in reply){
            			HTML += '<li><a href = "/learning/' + reply[key]['id'] + '">' + reply[key]['name'] + '</a><br><span>' + reply[key]['description'] + '</li><hr>';
            		}
            		document.getElementById("search_results").innerHTML = HTML;
            	}
            	else{
            		document.getElementById("search_results").innerHTML = "No results found";
            	}
            	
            }
        });
    }
    else{
        alert('Search field not empty')
    }
}

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

/*This function helps in changing the button coloer and view relevent activities to skill level*/
function show_activity(obj, id1, id2, b1, b2) {
    id0 = obj.value
    obj.style = "background-color: gray;";
    document.getElementById(id0).style.display = "block";
    document.getElementById(id1).style.display = "none";
    document.getElementById(id2).style.display = "none";
    document.getElementById(b1).style = "background-color: white;";
    document.getElementById(b2).style = "background-color: white;";
}