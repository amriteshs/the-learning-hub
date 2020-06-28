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

/*This function allows the progress bar to float in div when 
scrollling the questions*/
$(document).scroll(function() {
  		var wrapper = $('#Middle');
  		var box = $('#scrolling-section');

  		var offsetTop = - wrapper.offset().top + $(window).scrollTop();
  		var offsetBottom = wrapper.offset().top - $(window).scrollTop() + wrapper.outerHeight() - box.outerHeight();

  		if (offsetBottom > 0 && offsetTop < 0) {
    		box.css({
      		'top': 0
    		});
  		} else if (offsetBottom > 0 && offsetTop > 0) {
     	box.css({
      		'top': offsetTop + 'px'
    	});
  		} else {
	    box.offset({
	      'top': $(window).scrollTop() + offsetBottom
	    });
		}

});

var id_a = 0;
var score = 0;
var questions_numbers = 0;
var current = 0;

/*This function makes a POST request to upload_score endpoint which stores the score for activity*/
function store_results(score, learning_id){
	dict = {'score' : (score/questions_numbers) * 100, 'activity_id' : learning_id};
	$.ajax({
        type: 'POST',
        url: "/upload_score",
        data: JSON.stringify(dict),
        contentType: 'application/json',
         success: function(data){
         }
     });
}

/*This function calculates if the answer is correct or not and also gets next question by making POST to /questions endpoint*/
function approve_dataset(objButton){
		current++;
		var percent = (current/questions_numbers) * 100
		document.getElementById("progress_bar").style.width = percent + "%";
		document.getElementById("progress_bar").innerHTML = percent + "%"
        var answer = objButton.getAttribute("answer")
        var learning_id = parseInt(objButton.getAttribute("learning_id"))
        var id = parseInt(objButton.getAttribute("q_id"))
        var id_ = parseInt(objButton.getAttribute("id"))
        var user_answer = objButton.value;
        if (user_answer == answer){
          score++;
          document.getElementById(id_).style.background = "green";
        }
        else{
          document.getElementById(id_).style.background = "red";
        }
        document.getElementById("add-Score").innerHTML = "<h3> Score = " + score + "</h3>";
        dict = {'init' : 0, 'question_id' : id, 'learning_id' : learning_id}
        $.ajax({
        type: 'POST',
        url: "/questions",
        data: JSON.stringify(dict),
        contentType: 'application/json',
         success: function(data){
              var reply = JSON.parse(data)
              if (reply['question'].length > 0){
              	HTML = "<ul><li><h3><b>" + reply['question'] + "</b></h3><br>";
              }
              else{
              	HTML = "";
              }
              var arrayLength = reply['options'].length;
              if (reply['options'].length == 0){
                store_results(score, learning_id);
                alert('You have completed the activity with score ' + score)
              }
              HTML += "<ol>"
              for (var i = 0; i < arrayLength; i++) {
                HTML += "<li><button class = 'answer_buttons' onclick = 'approve_dataset(this)' value = '" + reply['options'][i] + "' id = '" + id_a +"' q_id = '" + reply['question_id'] + "'learning_id = '" + reply['learning_id'] + "' answer = '" + reply['answer'] + "'>" + reply['options'][i] + "</button></li>";
                id_a++;
              }
              HTML += "</ol></li></ul><hr>"
              document.getElementById("active").innerHTML += HTML;
        }
    });
  }

/*Loads initial questions and displays them as HTML lists and buttons*/
function init_questions(){
	var url = document.URL;
	var n = url.lastIndexOf('/');
	var result = url.substring(n + 1);
	dict = {'init' : 1, 'learning_id' : parseInt(result)}
	$.ajax({
        type: 'POST',
        url: "/questions",
        data: JSON.stringify(dict),
        contentType: 'application/json',
        success: function(data){
        	  document.getElementById("pg1").innerHTML = '<div id = "progress_bar"class="w3-container w3-padding-large w3-red w3-center" style="height: 40px; width:0%">0%</div>'
              var reply = JSON.parse(data)
              questions_numbers = reply['number_question'];
            	HTML = "<ul><li><h3><b>" + reply['question'] + "</b></h3><br>";
              var arrayLength = reply['options'].length;
              HTML += "<ol>"
              for (var i = 0; i < arrayLength; i++) {
                HTML += "<li><button class = 'answer_buttons' onclick = 'approve_dataset(this)' value = '" + reply['options'][i] + "' id = '" + id_a +"' q_id = '" + reply['question_id'] + "'learning_id = '" + reply['learning_id'] + "' answer = '" + reply['answer'] + "'>" + reply['options'][i] + "</button></li>";
                id_a++;
              }
              HTML += "</ol></li></ul><hr>"
            	document.getElementById("active").innerHTML = HTML;
        }
    });
}

/*This function is called when the page is loaded and hides the profile view div*/
// window.onload = function() {
// 	document.getElementById('viewProfile').style.zIndex = "-1";
// 		document.getElementById('viewProfile').style.display = 'none';
// };

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