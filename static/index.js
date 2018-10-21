$(document).ready(setup);

function setup(){
    parseWord();
}
var classCode = "";
var jsonFile;
var nameItems;
var ratingItems;
var difficultyItems;

//Parse class code input
function parseWord(){
    $("#searchButton").click(function(){
        classCode = document.getElementById("classCode").value.toUpperCase();
        gotoEndpt(classCode, printList);
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

// Prints out the list of professors related to the class code
function printList(profList){
    console.log(jQuery.parseJSON(profList));
}
