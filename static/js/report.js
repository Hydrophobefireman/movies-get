(function () {
    (async function () {
        const repo = document.getElementById("report-box");
        const compat_url = window["URL"] || window["webkitURL"];
        const req = new Request(document.querySelector("meta[name='og:image']").content);
        const img = document.createElement("img");
        img.style.height = '200px';
        img.style.width = '150px;';
        img.onload = self => {
            compat_url.revokeObjectURL(self.target.src)
        }
        const response = await fetch(req);
        const blob = await response.blob();
        img.src = compat_url.createObjectURL(blob);
        repo.appendChild(img);
    })();
    const txtel = document.createElement("div");
    txtel.innerHTML = `Report for movie ${window._title}?`;
    repo.appendChild(txtel);
    document.getElementById("sbmit-report").onclick = async () => {
        const report = new Request("/submit/report/", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: `id=${encodeURIComponent(window.mid)}`
        });
        const response = await fetch(report);
        const ret = await response.text();
        document.getElementById("sub-success-error").innerHTML = ret;
    }
})()