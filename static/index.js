var classCode = "";
var jsonFile = "HERE";
//Parse class code input

    $("#searchButton").click(function(){
        classCode = document.getElementById("classCode").value.toUpperCase();
        console.log(classCode);
    });


function getPyData(classCode) {
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "../PMPLookup.py", true);
    xhttp.send();
    console.log("here");
}

/*function print(response){
    console.log(response);
}

postData('data to process');*/