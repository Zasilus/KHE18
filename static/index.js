$(document).ready(setup);

function setup(){
    parseWord();
}
var classCode = "";
var jsonFile;
var length;
var nameItems = [];
var ratingItems = [];
var difficultyItems = [];

//Parse class code input
function parseWord(){
    $("#searchButton").click(function(){
        classCode = document.getElementById("classCode").value.toUpperCase();
        gotoEndpt(classCode, getList);
    });
}

// Goes to endpoint / route
function gotoEndpt(upd_data, upd_callback){
    var cd_url;
    cd_url = '../RMPLookup.py'+ encodeURIComponent(upd_data);
    callRMPLookup(cd_url,upd_callback);
}

// Passes the classCode and calls RMPLookup to generate list of profs teaching the class 
function callRMPLookup(url, callback){
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function()
    {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200)
            {
                callback(xmlhttp.responseText);
            }
    }
    xmlhttp.open("GET", url, true);
    xmlhttp.send(classCode);
}

// Gets the list of professors related to the class code
function getList(profList){
    console.log(profList);
    jsonFile = jQuery.parseJSON(profList);
    length = Object.keys(jsonFile).length;
        for (i = 0; i < length; i++){
           nameItems[i] = jsonFile[i].name;
           ratingItems[i] = jsonFile[i].rating;
           difficultyItems[i] = jsonFile[i].difficulty;
        }
    createTable();
}

function createTable(){
    document.write("<table border='1' width='200'>")
    document.write("<tr><th>Professor</th><th>Rating</th><th>Difficulty</th></tr>");
    for(var i=0; i<length;i++) {
	    document.write("<tr><td>" + nameItems[i] + "</td><td>" + ratingItems[i] + "</td><td>" + difficultyItems[i] +"</td></tr>");
    }
    document.write("</table>")
}



