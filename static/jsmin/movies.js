var request=new Request("/data/search/",{method:"POST",headers:{"Content-Type":"application/x-www-form-urlencoded"},body:params});function nores_(){document.getElementById("main").style.display="none",document.getElementById("no-res").style.display="block"}function gen_results(e){(e=JSON.parse(e)).hasOwnProperty("no-res")&&nores_();var t=0;for(document.getElementById("skelly").style.display="none";t<e.movies.length;t++){var n=document.createElement("img");n.style.backgroundColor="#e3e3e3",gen_img(n,e.movies[t].thumb);var o=document.createElement("div");o.className="img-box";var a=document.createElement("a");a.href=encodeURI("/movie/"+e.movies[t].id+"/"+e.movies[t].movie.replace(/[^\w]/g,"-")+"?id="+btoa(Math.random()).slice(0,8)),a.appendChild(n),o.appendChild(a),n.className="display-img";var s=document.createElement("span");s.className="text-box",s.innerHTML=e.movies[t].movie,o.appendChild(s),document.getElementById("content").appendChild(o)}}function gen_img(e,t){var n=window.URL||window.webkitURL,o=new Request(t);e.onload=function(){n.revokeObjectURL(this.src)},fetch(o).then(e=>e.blob()).then(e=>n.createObjectURL(e)).then(t=>{e.src=t,e.style.backgroundColor=""})}fetch(request).then(e=>e.text()).then(e=>{gen_results(e)}).catch(e=>{nores_()});