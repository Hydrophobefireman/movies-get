const extractHostname = (url) => {
    try {
        let a;
        if (url.includes("://")) {
            a = new URL(url);

        } else {
            url = `http://${url}`;
            a = new URL(url);
        }
        return a.hostname;
    } catch (e) {
        return 'null'
    }
}
Beacon.send('/collect/', {
    type: 'moviewatch',
    main: {
        data: [{
            movie: document.querySelector('meta[name="movie"]').content,
        }],
        ua: navigator.userAgent,
        touch: (navigator.maxTouchPoints > 0)
    }
})
const movie_id = window.location.pathname.split("/")[2];
const keys = "set-id";

const start_player = (key) => {
    console.log(key);
    const params = eval('encodeURI("id=" + movie_id + "&nonce=" + nonce)');
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/data-parser/plugins/player/", true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.onreadystatechange = () => {
        if (xhr.readyState == 4 && xhr.status == 200) {
            const data = xhr.response;
            build_player(data, key);
        }
    }
    xhr.onerror = async () => {
        const ifr = document.getElementById("player-frame");
        const response = await fetch("/error-configs/");
        const ret = await response.blob();
        ifr.src = window.URL.createObjectURL(ret);
    }
    xhr.send(params);
}

const build_player = (data, key) => {
    document.getElementById("custom-dl-box").style.display = 'block';
    data = JSON.parse(data);
    const url = data.url,
        alt1 = data.alt1,
        alt2 = data.alt2,
        btns1 = document.getElementById("source1"),
        btns2 = document.getElementById("source2"),
        btns3 = document.getElementById("source3"),
        btndl1 = document.getElementById("dl-s1"),
        btndl2 = document.getElementById("dl-s2"),
        btndl3 = document.getElementById("dl-s3"),
        linkdl1 = document.getElementById("link-s1"),
        linkdl2 = document.getElementById("link-s2"),
        linkdl3 = document.getElementById("link-s3");
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
        url = `https:${url}`;
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
    linkdl.href = `/out/?url=${encodeURIComponent(url)}`;
    btndl.innerHTML = btn.innerHTML;
    btn.onclick = ({
        target
    }) => {
        const ifr = document.getElementById("player-frame");
        document.getElementById("ifr-bx").removeChild(ifr);
        ifr.src = target.getAttribute("data");
        document.getElementById("ifr-bx").appendChild(ifr);
    }
    btndl.onclick = ({
        target
    }) => {
        window.location = `/out/?url=${encodeURIComponent(target.getAttribute("data-dl"))}`;
    }
}

(() => {
    document.getElementById("downloader-info").onclick = () => {
        document.getElementById("hdn-info").style.display = 'block';
        document.getElementById("downloader-info").style.display = 'none';
    }
    start_player(keys);

    document.getElementById("d-linker").href = encodeURI(`/report?id=${movie_id}`);

    document.getElementById("custom-dl").onclick = () => {
        document.getElementById("buttons-row").style.display = 'block';
    }
})()