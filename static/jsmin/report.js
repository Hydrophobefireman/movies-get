!function(){!async function(){const e=document.getElementById("report-box"),t=window.URL||window.webkitURL,n=new Request(document.querySelector("meta[name='og:image']").content),o=document.createElement("img");o.style.height="200px",o.style.width="150px;",o.onload=(e=>{t.revokeObjectURL(e.target.src)});const c=await fetch(n),i=await c.blob();o.src=t.createObjectURL(i),e.appendChild(o)}();const e=document.createElement("div");e.innerHTML=`Report for movie ${window._title}?`,repo.appendChild(e),document.getElementById("sbmit-report").onclick=(async()=>{const e=new Request("/submit/report/",{method:"POST",headers:{"Content-Type":"application/x-www-form-urlencoded"},body:`id=${encodeURIComponent(window.mid)}`}),t=await fetch(e),n=await t.text();document.getElementById("sub-success-error").innerHTML=n})}();