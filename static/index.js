$(document).ready(setup);

function setup(){
    parseWord();
}
var classCode = "";
var jsonFile = "HERE";
//Parse class code input

function parseWord(){
    $("#searchButton").click(function(){
        classCode = document.getElementById("classCode").value.toUpperCase();
        getPyData(classCode);
    });
}


function getPyData(classCode) {
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "../PMPLookup.py", true);
    xhttp.send();
    console.log("here");
}

/*function print(response){
    console.log(response);
}

postData('data to process');*/