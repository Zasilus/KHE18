$(document).ready(setup);

function setup(){
    parseWord();
}
var classCode = "";
var jsonFile = "";
var length = 0;
var profArray = [];
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
    jsonFile = jQuery.parseJSON(profList);
    length = Object.keys(jsonFile).length;
        for (i = 0; i < length; i++){
           profArray[i] = [jsonFile[i].name, jsonFile[i].rating, jsonFile[i].difficulty];
           console.log(profArray[i])
        }
    createTable();
    document.getElementById("computer").style.visibility = 'hidden';
}


function createTable(){
    var html = document.getElementsByTagName("body")[0]
    var table = document.getElementById("table");
    var body = document.createElement("tbody");
    var row = document.createElement("tr");
    var profHead = document.createElement("td");
    var rankingHead = document.createElement("td");
    var difficultyHead = document.createElement("td");
    row.appendChild(profHead);
    profHead.innerHTML = 'Professor';
    row.appendChild(rankingHead);
    rankingHead.innerHTML = 'Rating';
    row.appendChild(difficultyHead);
    difficultyHead.innerHTML = 'Difficulty';
    body.appendChild(row);
     for(var i=0; i<length; i++) {
	        row = document.createElement("tr");
	    for(var j = 0; j < 3; j++){
	      var col = document.createElement("td");
	      col.appendChild(document.createTextNode(profArray[i][j]));
	      row.appendChild(col);
	    }
	    body.appendChild(row);
    }
    table.appendChild(body);
    html.appendChild(table);
}




