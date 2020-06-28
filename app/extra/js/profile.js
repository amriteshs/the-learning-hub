var id_a = 0;
var score = 0;
var questions_numbers = 0;
var current = 0;
// var jsonStr = '{"L1":"34","L2":"436","L3":"547"}';   //test data
// var obj = JSON.parse(jsonStr);

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

/*This function gets score of the user for each activity by making GET request to /get_score*/
function init(){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "/get_score", false );
    xmlHttp.send( null );
    obj = JSON.parse(xmlHttp.responseText);
    document.getElementById('viewProfile').style.zIndex = "-1";
    document.getElementById('viewProfile').style.display = 'none';
    var selector = document.getElementById("selector");
    for(var key in obj){
        var opt = document.createElement("option");
        opt.innerText = key;
        opt.value = obj[key];
        selector.appendChild(opt);
    }
    getIndex();
}

/*Ititalise the dropdown to first activity*/
function getIndex() {
    document.getElementById("demo").innerHTML =
    document.getElementById("selector").value;
}
