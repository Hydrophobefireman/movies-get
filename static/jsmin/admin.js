(()=>{const e=document.querySelector.bind(document),t=e("#go"),n=e("#content"),o=e("#json-res"),a=e("#postit"),c=async e=>{o.innerHTML="Fetching Results";const t=await fetch("/admin/get-data/",{method:"POST",body:`type=${encodeURIComponent(e)}`,headers:{"content-type":"application/x-www-form-urlencoded"}}),n=(await t.json()).result;for(var a of(o.innerHTML="",n)){var c=document.createElement("pre");c.innerHTML=JSON.stringify(a,null,3),o.appendChild(c),c.style.border="2px solid"}};t.onclick=(async()=>{const e=await fetch("/admin/",{method:"POST",body:`pass=${a.value.trim()}`,headers:{"content-type":"application/x-www-form-urlencoded"}}),o=(await e.json()).response;1===o|-1===o&&(t.remove(),a.remove(),function(){n.innerHTML="",_types=["search","moviewatch","recommend","movieclick"];const e=document.createElement("div");for(const t of _types){const n=document.createElement("button");n.innerHTML=t,e.appendChild(n),n.dataset.action=t,n.className="aval-type",n.onclick=function(){c(this.dataset.action)}}n.appendChild(e)}())})})();