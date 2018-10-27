const start = async (params) => {
    const request = new Request("/dat" + "a/specs/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `q=${params}`,
        credentials: 'include'
    });
    try {
        const response = await fetch(request);
        const response_1 = await response.text();
        gen_results(response_1);
    } catch (e) {
        console.warn(e);
        nores_();
    }
}

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
        atag["href"] = encodeURI(`/movie/${names["movies"][i]["id"]}/${names["movies"][i]["movie"].replace(
    /(\(|\)|\s)/g, "-")}?id=${btoa(Math.random()).slice(0, 8)}`);
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

const fetch_2 = async data => {
    const _params = `data=${encodeURIComponent(data)}`;
    const reqs = new Request('/fetch-token/links/post/', {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: _params,
        credentials: 'include'
    });
    const ret = await fetch(reqs);
    const retcode = await ret.json();
    data = retcode['id'];
    setTimeout(start(data), 700);
}

(async (data) => {
    params = `data=${encodeURIComponent(data)}&rns=${btoa(Math.random().toString())}`;
    console.log(params)
    const reqs = new Request('/fetch-token/configs/', {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        credentials: 'include',
        body: params
    });
    const ret = await fetch(reqs);
    const retcode = await ret.json();
    data = retcode['id'];
    fetch_2(data);
})(window.__data)