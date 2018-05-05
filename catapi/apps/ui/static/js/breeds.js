function queryAPIforList(addr, handler) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var data = JSON.parse(this.responseText)
            if (data["status"] == "success") {
                handler(data["message"])
            }
        }
    };
    xhttp.open("GET", addr, true);
    xhttp.send();
}

function populateBreedsList(data) {
    ul = document.getElementById("breeds_list_id")
    for (elem in data) {
        all_url="/api/breeds/"+data[elem]["slug"]
        random_url="/api/breeds/"+data[elem]["slug"]+"/random"
        ul.innerHTML += "<li>"+data[elem]["name"]+': <a href="'+all_url+'">All</a>, <a href="'+random_url+'">Random</a></li>'
    }
}

queryAPIforList("/api/breeds", populateBreedsList)