var script = (function () {
    var queryAPIforList = function (addr, handler) {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState === 4 && this.status === 200) {
                var data = JSON.parse(this.responseText);
                if (data["status"] === "success") {
                    handler(data["message"]);
                };
            };
        };
        xhttp.open("GET", addr, true);
        xhttp.send();
    };

    var populateBreedsList = function (list) {
        var ul = document.getElementById("breeds_list_id");
        list.forEach(function() {
            all_url="/api/breeds/"+li["slug"];
            random_url="/api/breeds/"+li["slug"]+"/random";
            ul.innerHTML += "<li>"+li["name"]+': <a href="'+all_url+'">All</a>, <a href="'+random_url+'">Random</a></li>';
        });
    };

    return {
        init: function() {
            queryAPIforList("/api/breeds", populateBreedsList);
        }
    };
}());

script.init();