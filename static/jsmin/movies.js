const params=`q=${encodeURIComponent(document.getElementById("jinja-data-query").getAttribute("content"))}`,request=new Request("/data/search/",{method:"POST",headers:{"Content-Type":"application/x-www-form-urlencoded"},body:params});!async function(){try{const e=await fetch(request),t=await e.text();Beacon.send("/collect/",{type:"search",main:{ua:navigator.userAgent,touch:touch=navigator.maxTouchPoints>0,data:[{query:document.getElementById("jinja-data-query").getAttribute("content")}]}}),gen_results(t)}catch(e){console.log(e),nores_()}}();const nores_=()=>{document.getElementById("main").style.display="none",document.getElementById("no-res").style.display="block"},gen_results=e=>{(e=JSON.parse(e)).hasOwnProperty("no-res")&&nores_();let t=0;for(document.getElementById("skelly").style.display="none";t<e.movies.length;t++){const n=document.createElement("img");n.style.backgroundColor="#e3e3e3",gen_img(n,e.movies[t].thumb);const o=document.createElement("div");o.className="img-box";const a=document.createElement("a");a.href=encodeURI(`/movie/${e.movies[t].id}/${e.movies[t].movie.replace(/[^\w]/g,"-")}`),a.appendChild(n),o.appendChild(a),n.className="display-img";const s=document.createElement("span");s.className="text-box",s.innerHTML=e.movies[t].movie,o.appendChild(s),document.getElementById("content").appendChild(o)}},gen_img=async(e,t)=>{const n=window.URL||window.webkitURL,o=new Request(t);e.onload=(({target:e})=>{n.revokeObjectURL(e.src)});const a=await fetch(o),s=await a.blob(),c=n.createObjectURL(s);e.src=c,e.style.backgroundColor=""};