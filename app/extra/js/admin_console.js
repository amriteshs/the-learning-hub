/*This function opens a popup to display the clicked dataset and views all required data by making a POST request to
dataset_API endpoint and buttons for modification operation*/
function un_hide_datset(id, status) {
    document.getElementById("blur").style.filter = "blur(6px)";
    document.getElementById("display_contents").style.display = "block";
    document.getElementById("display_contents").style.zIndex = "100";
    document.getElementById('display_contents').innerHTML = '<img style="margin-top : 20%; float : center" src = "/extra/img/loading.gif" height="10%" width="20%">';
    $.ajax({
        type: 'GET',
        url: "/dataset_API/"+id,
        // data: JSON.stringify({ 'id': id }),
        // data : {id : id}
        contentType: 'application/json',
        success: function(data) {
            var HTML = '';
            var reply = JSON.parse(data);
            HTML += '<button style = "float : left;" onclick = "close_popup()">Close</button>'
            HTML += '<h1>' + reply['name'] + '</h1>'
            HTML += '<iframe width="100%" height="80%" class = "google-map" src="' + reply['visualisation_link'] + '"></iframe>';
            HTML += '<table id = "table-booking">';
            HTML += "<tr><th>category</th><th>dataset name</th><th>dataset discription</th><th>dataset owner</th><th>Link to api</th><th>Search tags</th><th>learning tags</th><th>File format</th></tr>"
            HTML += "<tr>";
            for (var key1 in reply) {
                if (key1 != 'dataset_id' && key1 != 'catogery_id' && key1 != 'uploader' && key1 != 'visualisation_link' && key1 != 'status' && key1 != 'last_update' && key1 != 'file_patch') {
                    HTML += "<td>" + reply[key1] + "</td>";
                }

            }
            HTML += "</tr></table>";
            if (status == 1) {
                HTML += '<button class = "button-submit" onclick = "approve_dataset(this)" data-value = "approve" value = "' + reply['dataset_id'] + '">approve</button></div>'
            }
            HTML += '<button class = "button-submit-delete" onclick = "approve_dataset(this)" data-value = "delete" value = "' + reply['dataset_id'] + '">delete</button></div>'
            document.getElementById('display_contents').innerHTML = HTML;
        }

    });
}

//This function is called to close the popup view of the dataset
function close_popup() {
    document.getElementById("blur").style.filter = "blur(0px)";
    document.getElementById("blur").style.blur = "0px";
    document.getElementById("display_contents").style.display = "none";
    document.getElementById("display_contents").style.zIndex = "-1";
}

/* This function is called by aprove dataset or delete dataset button and makes a POST request to /aprove_dataset to approve
 or delete dataset*/
function approve_dataset(objButton) {
    var id = objButton.value;
    if (objButton.getAttribute("data-value") == 'approve') {
        var dict = { "id": id, "action": 'approve' };
    } else {
        var dict = { "id": id, "action": 'delete' };
    }
    $.ajax({
        type: 'POST',
        url: "/approve_dataset",
        data: JSON.stringify(dict),
        contentType: 'application/json',
        success: function(data) {
            var reply = JSON.parse(data);
            if (reply['status'] == "success") {
                if (objButton.getAttribute("data-value") == 'approve') {
                    alert("Dataset was successfully aproved");
                } else {
                    alert("Dataset was successfully deleted");
                }
                close_popup();
                load_data();
                // document.getElementById(id).remove();
            } else {
                alert("There was error in aproval/delete");
            }
        }
    });
}

/*This function loads the dataset which are approved and unapproved my making "GET" request to multiple endpoints 
and view them as HTML tables*/
function load_data() {
    document.getElementById("unaproved_view").innerHTML = '<img style="margin-left : 40%; margin-top : 5%; vertical-align:center; float : center" src = "/extra/img/loading.gif" height="10%" width="20%">';
    document.getElementById("aproved_view").innerHTML = '<img style="margin-left : 40%; margin-top : 5%; vertical-align:center; float : center" src = "/extra/img/loading.gif" height="10%" width="20%">';
    $.ajax({
        type: 'GET',
        url: "/unapproved_dataset",
        contentType: 'application/json',
        success: function(data) {
            var reply = JSON.parse(data);
            if (data) {
                HTML = '<table id = "table-booking">';
                HTML += "<tr><th>category</th><th>dataset name</th><th>dataset discription</th><th>dataset owner</th><th>Link to api</th><th>Search tags</th><th>learning tags</th><th>File format</th><th>up votes</th><th>down votes</th><th>view</th></tr>"
                for (var key in reply) {
                    HTML += "<tr id = '" + reply[key]['dataset_id'] + "'>";
                    if (reply[key]) {
                        for (var key1 in reply[key]) {
                            if (key1 != 'dataset_id' && key1 != 'catogery_id' && key1 != 'uploader' && key1 != 'visualisation_link' && key1 != 'status' && key1 != 'last_update' && key1 != 'file_patch') {
                                HTML += "<td>" + reply[key][key1] + "</td>";
                            }
                        }
                    }
                    HTML += '<td><button onclick = "un_hide_datset(' + reply[key]['dataset_id'] + ', 1)">view</button></td></tr>';
                }
                HTML += "</table>"
                document.getElementById("unaproved_view").innerHTML = HTML;
            }
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            document.getElementById("unaproved_view").innerHTML = '<div class = "floating-rect"> No datasets for approval</div>';
        }
    });
    $.ajax({
        type: 'GET',
        url: "/approved_dataset",
        contentType: 'application/json',
        success: function(data) {
            var reply = JSON.parse(data);
            if (data) {
                var HTML = '<table id = "table-booking"><tr><th>Name</th><th>up votes</th><th>down votes</th><th>view</th></tr>'

                for (var key in reply) {
                    HTML += "<tr id = '" + reply[key]['dataset_id'] + "'>";
                    HTML += '<td>' + reply[key]['name'] + '</td><td>' + reply[key]['upvote'] + '</td><td>' + reply[key]['downvote'] + '</td><td><button onclick = "un_hide_datset(' + reply[key]['dataset_id'] + ', 0)">view</button></td></tr>'
                }
                document.getElementById("aproved_view").innerHTML = HTML;
            }
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            document.getElementById("unaproved_view").innerHTML = '<div class = "floating-rect"> No datasets for approval</div>';
        }
    });
}
