function extractHostname(url) {
    try {
        var a;
        if (url.indexOf("://") > -1) {
            a = new URL(url);

        } else {
            url = "http://" + url;
            a = new URL(url);
        }
        return a.hostname;
    } catch (e) {
        return 'null'
    }
}
var movie_id = window.location.pathname.split("/")[2]
var keys = "set-id"

function start_player(key) {
    console.log(key);
    var params = eval('encodeURI("id=" + movie_id + "&nonce=" + nonce)');
    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/dat' + 'a-parser/' + 'plugin' + 's/player/', true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var data = xhr.response;
            build_player(data, key);
        }
    }
    xhr.onerror = function () {
        var ifr = document.getElementById('p' + 'l' + 'a' + 'y' + 'e' + 'r' + '-' + 'f' + 'r' + 'a' +
            'm' + 'e');
        fetch("/error-configs/")
            .then(response => response.blob()).then(ret => {
                ifr.src = window.URL.createObjectURL(ret);
            })
    }
    xhr.send(params);
}
document.getElementById("c" + "u" + "s" + "tom-dl").onclick = function () {

}

function build_player(data, key) {
    document.getElementById("custom-dl-box").style.display = 'block';
    data = JSON.parse(data);
    var url = data['url'];
    var alt1 = data['alt1'];
    var alt2 = data['alt2'];
    var btns1 = document.getElementById("source1");
    var btns2 = document.getElementById("source2");
    var btns3 = document.getElementById("source3");
    var btndl1 = document.getElementById("dl-s1");
    var btndl2 = document.getElementById("dl-s2");
    var btndl3 = document.getElementById("dl-s3");
    var linkdl1 = document.getElementById("link-s1");
    var linkdl2 = document.getElementById("link-s2");
    var linkdl3 = document.getElementById("link-s3");

    function btndata(btn, btndl, url, linkdl) {
        if (url.indexOf("://") > -1) {
            url = url.replace("http://", "https://");

        } else if (url.indexOf("//") == 0) {
            /* protocol relative url */
            url = "https:" + url;
        }

        btn.setAttribute("data", url);
        btn.innerHTML = extractHostname(url);
        if (extractHostname(url) == "null" || extractHostname(url).toLowerCase() == 'none') {
            btn.style.display = 'none'
        } else {
            btn.style.display = 'inline';
            btn.setAttribute('data', url.toString().replace("http://", "https://"));
            /* chrome will outright block any iframe in http */
        }
        btndl.style.display = btn.style.display;
        btndl.innerHTML = btn.innerHTML;
        linkdl.href = "/out?url=" + encodeURIComponent(url);
        btndl.innerHTML = btn.innerHTML;
        btn.onclick = function () {
            var ifr = document.getElementById('p' + 'l' + 'a' + 'y' + 'e' + 'r' + '-' + 'f' + 'r' + 'a' +
                'm' + 'e');
            document.getElementById("ifr-bx").removeChild(ifr);
            ifr.src = this.getAttribute("data");
            document.getElementById("ifr-bx").appendChild(ifr);
        }
        btndl.onclick = function () {
            window.location = '/out?url=' + encodeURIComponent(this.getAttribute("data-dl"));
        }
    }
    btndata(btns1, btndl1, url, linkdl1);
    btndata(btns2, btndl2, alt1, linkdl2);
    btndata(btns3, btndl3, alt2, linkdl3);
    var ifr = document.getElementById('p' + 'l' + 'a' + 'y' + 'e' + 'r' + '-' + 'f' + 'r' + 'a' + 'm' + 'e');
    ifr.src = url;
}
document.getElementById("downloader-info").onclick = function () {
    document.getElementById("hdn-info").style.display = 'block';
    document.getElementById("downloader-info").style.display = 'none';
}
start_player(keys);

document.getElementById("d-linker").onclick = function () {
    window.location = encodeURI("/report?id=" + movie_id);
};
document.getElementById("custom-dl").onclick = function () {
    document.getElementById("buttons-row").style.display = 'block';
}