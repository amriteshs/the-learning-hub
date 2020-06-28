//this function is called when the user clicks the profile and will  make the profile dropdown visiable or invisiable.
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
