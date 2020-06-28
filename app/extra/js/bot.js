/*This function gets response from user and then posts it to /livechat endpoint and views the response from the bot*/
function getBotResponse(s) {
  var dict = {"message" : s};
  var userHtml = '<p class="userText"><span>' + s + "</span></p>";
  $("#chatbox").append(userHtml);
  document.getElementById("userInput").scrollIntoView({ block: "start", behavior: "smooth" });
  $.ajax({
  type: 'POST',
  url: "/livechat_back",
  data: JSON.stringify(dict),
  contentType: 'application/json',
  success: function(data){
  var reply = JSON.parse(data);
  if (reply['options'].length != 0){
  var botHtml = '<p class="botText"><span>Select difficulty level<br>';
          for (vals in reply['options']){
          botHtml += '<button onclick="view_difficulty(this)" value="' + reply['options'][vals] + '">' + reply['options'][vals] + '</button>'
          }
          botHtml += "</span></p>";
  }
  if (reply['is_link'] == 1){
  var botHtml = '<p class="botText"><span>The ' + reply['type'] + ' are<br>';
          for (vals in reply['reply']){
          botHtml += '<a href="' + reply['reply'][vals] + '" target="_blank">' + reply['name'][vals] + '</a><br>';
          }
          botHtml += '</span></p>';
  }
  if (reply['is_link'] == 0 && reply['options'].length == 0){
  var botHtml = '<p class="botText"><span>' + reply['reply'] + "</span></p>";
  }
  $("#chatbox").append(botHtml);
  document.getElementById("userInput").scrollIntoView({ block: "start", behavior: "smooth" });
  }
  });
}

function view_difficulty(obj){
  reply = obj.value;
  var dict = {"message" : reply};
  var userHtml = '<p class="userText"><span>' + reply + "</span></p>";
  document.getElementById("userInput").scrollIntoView({ block: "start", behavior: "smooth" });
  $.ajax({
    type: 'POST',
    url: "/livechat_back",
    data: JSON.stringify(dict),
    contentType: 'application/json',
    success: function(data){
       var reply = JSON.parse(data);
       if (reply['options'].length != 0){
        var botHtml = '<p class="botText"><span>Select difficulty level<br>';
        for (vals in reply['options']){
          botHtml += '<button onclick = "view_difficulty(this)" value = "' + reply['options'][vals] + '">' + reply['options'][vals] + '</button>'
        }
        botHtml += "</span></p>";
       }
       if (reply['is_link'] == 1){
        var botHtml = '<p class="botText"><span>The ' + reply['type'] + ' are<br>';
        for (vals in reply['reply']){
          botHtml += '<a href = "' + reply['reply'][vals] + '" target="_blank">' + reply['name'][vals] + '</a><br>'
        }

        botHtml += '</span></p>';
       }
       if (reply['is_link'] == 0 && reply['options'].length == 0){
        var botHtml = '<p class="botText"><span>' + reply['reply'] + "</span></p>";
       }
    $("#chatbox").append(botHtml);
    document.getElementById("userInput").scrollIntoView({ block: "start", behavior: "smooth" });
      }
    });
}

/*This function takes the data from text field in real time and sends it to getresponse function when enter key is pressed*/
function edValueKeyPress(e) {
  var edValue = document.getElementById("textInput");
  var s = edValue.value;
  var code = (e.keyCode ? e.keyCode : e.which);
  if(code == 13) {
  $("#textInput").val("");
  getBotResponse(s);
  }
}