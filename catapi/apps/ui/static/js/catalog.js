function queryAPIforList(addr, handler) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var data = JSON.parse(this.responseText)
            console.log(data)
            if (data["status"] == "success") {
                handler(data["message"])
            }
        }
    };
    xhttp.open("GET", addr, true);
    xhttp.send();
}

function populateCatList(data) {
    sel = document.getElementById("breed_selector")
    for (elem in data) {
        sel.options.add( new Option(data[elem]["name"], data[elem]["slug"]))
    }
}

function showImgKeypress() {
    sel = document.getElementById("breed_selector")
    slug = document.getElementById("breed_selector").selectedOptions[0].value
    queryAPIforList("/api/breeds/" + slug + "/random", displayImage)
}

function displayImage(data) {
    holder = document.getElementById("img_holder")
    holder.innerHTML = '<a href="' + data + '"><img id="img_preview" src="' + data + '"></a>'
}

queryAPIforList("/api/breeds", populateCatList)