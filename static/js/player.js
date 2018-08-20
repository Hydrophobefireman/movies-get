(() => {
    if (!String.prototype.includes) {
        String.prototype.includes = (search, start) => {
            'use strict';
            if (typeof start !== 'number') {
                start = 0;
            }

            if (start + search.length > this.length) {
                return false;
            } else {
                return this.indexOf(search, start) !== -1;
            }
        };
    }
})();
const extractHostname = (url) => {
    try {
        let a;
        if (url.includes("://")) {
            a = new URL(url);

        } else {
            url = 'http://' + url;
            a = new URL(url);
        }
        return a.hostname;
    } catch (e) {
        return 'null'
    }
}

const movie_id = window.location.pathname.split("/")[2];
const keys = "set-id";

const start_player = (key) => {
    console.log(key);
    var params = eval('encodeURI("id=" + movie_id + "&nonce=" + nonce)');
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/data-parser/plugins/player/", true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.onreadystatechange = () => {
        if (xhr.readyState == 4 && xhr.status == 200) {
            const data = xhr.response;
            build_player(data, key);
        }
    }
    xhr.onerror = () => {
        var ifr = document.getElementById("player-frame")
        fetch("/error-configs/")
            .then(response => response.blob()).then(ret => {
                ifr.src = window.URL.createObjectURL(ret);
            })
    }
    xhr.send(params);
}

const build_player = (data, key) => {
    document.getElementById("custom-dl-box").style.display = 'block';
    data = JSON.parse(data);
    const url = data.url;
    const alt1 = data.alt1;
    const alt2 = data.alt2;
    const btns1 = document.getElementById("source1");
    const btns2 = document.getElementById("source2");
    const btns3 = document.getElementById("source3");
    const btndl1 = document.getElementById("dl-s1");
    const btndl2 = document.getElementById("dl-s2");
    const btndl3 = document.getElementById("dl-s3");
    const linkdl1 = document.getElementById("link-s1");
    const linkdl2 = document.getElementById("link-s2");
    const linkdl3 = document.getElementById("link-s3");
    btndata(btns1, btndl1, url, linkdl1);
    btndata(btns2, btndl2, alt1, linkdl2);
    btndata(btns3, btndl3, alt2, linkdl3);
    const ifr = document.getElementById("player-frame");
    ifr.src = url;
}

const btndata = (btn, btndl, url, linkdl) => {
    if (url.includes("://")) {
        url = url.replace("http://", "https://");

    } else if (url.indexOf("//") == 0) {
        /* protocol relative url */
        url = 'https:' + url;
    }
    btn.setAttribute("data", url);
    btn.innerHTML = extractHostname(url);
    if (extractHostname(url) == "null" || extractHostname(url).toLowerCase() == 'none') {
        btn.remove();
        btndl.remove();
        linkdl.remove();
        return
    } else {
        btn.style.display = 'inline';
        btn.setAttribute('data', url.toString().replace("http://", "https://"));
        /* chrome will outright block any iframe in http */
    }
    btndl.style.display = btn.style.display;
    btndl.innerHTML = btn.innerHTML;
    linkdl.href = "/out?url=" + encodeURIComponent(url);
    btndl.innerHTML = btn.innerHTML;
    btn.onclick = e => {
        const ifr = document.getElementById("player-frame");
        document.getElementById("ifr-bx").removeChild(ifr);
        ifr.src = e.target.getAttribute("data");
        document.getElementById("ifr-bx").appendChild(ifr);
    }
    btndl.onclick = e => {
        window.location = "/out?url=" + encodeURIComponent(e.target.getAttribute("data-dl"));
    }
}

(() => {
    document.getElementById("downloader-info").onclick = () => {
        document.getElementById("hdn-info").style.display = 'block';
        document.getElementById("downloader-info").style.display = 'none';
    }
    start_player(keys);

    document.getElementById("d-linker").href = encodeURI("/report?id=" + movie_id);

    document.getElementById("custom-dl").onclick = () => {
        document.getElementById("buttons-row").style.display = 'block';
    }
})()