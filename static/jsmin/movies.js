const request=new Request("/data/search/",{method:"POST",headers:{"Content-Type":"application/x-www-form-urlencoded"},body:params});fetch(request).then(e=>e.text()).then(e=>{gen_results(e)}).catch(e=>{console.log(e),nores_()});const nores_=()=>{document.getElementById("main").style.display="none",document.getElementById("no-res").style.display="block"},gen_results=e=>{(e=JSON.parse(e)).hasOwnProperty("no-res")&&nores_();let t=0;for(document.getElementById("skelly").style.display="none";t<e.movies.length;t++){const n=document.createElement("img");n.style.backgroundColor="#e3e3e3",gen_img(n,e.movies[t].thumb);const o=document.createElement("div");o.className="img-box";const s=document.createElement("a");s.href=encodeURI(`/movie/${e.movies[t].id}/${e.movies[t].movie.replace(/[^\w]/g,"-")}`),s.appendChild(n),o.appendChild(s),n.className="display-img";const c=document.createElement("span");c.className="text-box",c.innerHTML=e.movies[t].movie,o.appendChild(c),document.getElementById("content").appendChild(o)}},gen_img=(e,t)=>{const n=window.URL|window.webkitURL,o=new Request(t);e.onload=(({target:e})=>{n.revokeObjectURL(e.src)}),fetch(o).then(e=>e.blob()).then(e=>n.createObjectURL(e)).then(t=>{e.src=t,e.style.backgroundColor=""})};