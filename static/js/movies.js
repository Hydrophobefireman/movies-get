const params = `q=${encodeURIComponent(document.getElementById('jinja-data-query').getAttribute("content"))}`;
const request = new Request("/dat" + "a/search/", {
    method: "POST",
    headers: {
        "Content-Type": "application/x-www-form-urlencoded"
    },
    body: params
});

(async function () {
    try {
        const response = await fetch(request);
        const response_1 = await response.text();
        Beacon.send('/collect/', {
            type: 'search',
            main: {
                ua: navigator.userAgent,
                touch = (navigator.maxTouchPoints > 0),
                data: [{
                    query: document.getElementById('jinja-data-query').getAttribute("content")
                }]
            }
        });
        gen_results(response_1);
    } catch (e) {
        console.log(e);
        nores_();
    }
})()

const nores_ = () => {
    document.getElementById("main").style.display = 'none';
    document.getElementById("no-res").style.display = 'block';
}
const gen_results = (names) => {
    var names = JSON.parse(names);
    if (names.hasOwnProperty("no-res")) {
        nores_()
    }
    let i = 0;
    document.getElementById("skelly").style.display = 'none';
    for (; i < names["movies"]["length"]; i++) {
        const img = document.createElement("img");
        img.style.backgroundColor = '#e3e3e3';
        gen_img(img, names["movies"][i]["thumb"]);
        const dv = document.createElement("div");
        dv["className"] = "img-box";
        const atag = document.createElement("a");
        atag["href"] = encodeURI(`/movie/${names["movies"][i]["id"]}/${names["movies"][i]["movie"].replace(/[^\w]/g, "-")}`);
        atag.appendChild(img);
        dv.appendChild(atag);
        img.className = 'display-img';
        const sp = document.createElement("span");
        sp["className"] = "text-box";
        sp["innerHTML"] = names["movies"][i]["movie"];
        dv.appendChild(sp);
        document.getElementById("content").appendChild(dv);
    }
}

const gen_img = async (img, imgURL) => {
    const compat_url = window["URL"] || window["webkitURL"];
    const req = new Request(imgURL);
    img.onload = ({
        target
    }) => {
        compat_url.revokeObjectURL(target.src)
    }
    const response = await fetch(req);
    const blob = await response.blob();
    const res = compat_url.createObjectURL(blob);
    img.src = res;
    img.style.backgroundColor = '';
};