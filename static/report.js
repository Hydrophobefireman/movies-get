var repo = document.getElementById("report-box");
var compat_url = window["URL"] || window["webkitURL"];
var req = new Request("{{thumb|safe}}");
var img = document.createElement("img");
img.style.height = '200px';
img.style.width = '150px;';
fetch(req).then(function (response) {
    return response.blob();
}).then(function (blob) {
    img.src = compat_url.createObjectURL(blob);
});
img.onload = function (self) {
    compat_url.revokeObjectURL(self.target.src);
};
repo.appendChild(img);
var repo = document.getElementById("report-box");
repo.appendChild(img);
var txtel = document.createElement("div");
txtel.innerHTML = "Report for movie {{title}}?";
repo.appendChild(txtel);

document.getElementById("sbmit-report").onclick = function () {
    var report = new Request("/submit/report/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: 'id=' + encodeURIComponent("{{m_id|safe}}")
    });
    fetch(report).then(function (response) {
        return response.text();
    }).then(function (ret) {
        document.getElementById("sub-success-error").innerHTML = ret;
    });
};