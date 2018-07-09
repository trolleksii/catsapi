var script = (function () {
    var queryAPIforList = function (addr, handler) {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState === 4 && this.status === 200) {
                var data = JSON.parse(this.responseText)
                if (data["status"] === "success") {
                    handler(data["message"])
                };
            };
        };
        xhttp.open("GET", addr, true);
        xhttp.send();
    };
    var populateCatList = function (data) {
        var sel = document.getElementById("breed_selector")
        data.forEach(function () {
            sel.options.add( new Option(breed["name"], breed["slug"]));
        });
    };
    var getRandomImage = function () {
        var slug = document.getElementById("breed_selector").selectedOptions[0].value;
        queryAPIforList("/api/breeds/" + slug + "/random", displayImage);
    }
    var displayImage = function (address) {
        var imgHolder = document.getElementById("img_holder");
        imgHolder.innerHTML = '<a href="' + address + '"><img id="img_preview" src="' + address + '"></a>';
    }
    return {
        init: function() {
            queryAPIforList("/api/breeds", populateCatList);
            document.querySelector('#cat_img_btn').addEventListener('click', getRandomImage);
        }
    };
}());
script.init()