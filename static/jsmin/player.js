const extractHostname=e=>{try{let t;return e.includes("://")?t=new URL(e):(e=`http://${e}`,t=new URL(e)),t.hostname}catch(e){return"null"}},movie_id=window.location.pathname.split("/")[2],keys="set-id",start_player=key=>{console.log(key);const params=eval('encodeURI("id=" + movie_id + "&nonce=" + nonce)'),xhr=new XMLHttpRequest;xhr.open("POST","/data-parser/plugins/player/",!0),xhr.setRequestHeader("Content-type","application/x-www-form-urlencoded"),xhr.onreadystatechange=(()=>{if(4==xhr.readyState&&200==xhr.status){const e=xhr.response;build_player(e,key)}}),xhr.onerror=(()=>{const e=document.getElementById("player-frame");fetch("/error-configs/").then(e=>e.blob()).then(t=>{e.src=window.URL.createObjectURL(t)})}),xhr.send(params)},build_player=(e,t)=>{document.getElementById("custom-dl-box").style.display="block";const n=(e=JSON.parse(e)).url,o=e.alt1,d=e.alt2,r=document.getElementById("source1"),l=document.getElementById("source2"),a=document.getElementById("source3"),c=document.getElementById("dl-s1"),m=document.getElementById("dl-s2"),s=document.getElementById("dl-s3"),i=document.getElementById("link-s1"),u=document.getElementById("link-s2"),y=document.getElementById("link-s3");btndata(r,c,n,i),btndata(l,m,o,u),btndata(a,s,d,y),document.getElementById("player-frame").src=n},btndata=(e,t,n,o)=>{if(n.includes("://")?n=n.replace("http://","https://"):0==n.indexOf("//")&&(n=`https:${n}`),e.setAttribute("data",n),e.innerHTML=extractHostname(n),"null"==extractHostname(n)||"none"==extractHostname(n).toLowerCase())return e.remove(),t.remove(),void o.remove();e.style.display="inline",e.setAttribute("data",n.toString().replace("http://","https://")),t.style.display=e.style.display,t.innerHTML=e.innerHTML,o.href=`/out/?url=${encodeURIComponent(n)}`,t.innerHTML=e.innerHTML,e.onclick=(({target:e})=>{const t=document.getElementById("player-frame");document.getElementById("ifr-bx").removeChild(t),Beacon.send("/collect/",{type:"moviewatch",main:{data:[{movie:document.querySelector('meta[name="movie"]').content,url:e.getAttribute("data")}],ua:navigator.userAgent,touch:navigator.maxTouchPoints>0}}),t.src=e.getAttribute("data"),document.getElementById("ifr-bx").appendChild(t)}),t.onclick=(({target:e})=>{window.location=`/out/?url=${encodeURIComponent(e.getAttribute("data-dl"))}`})};document.getElementById("downloader-info").onclick=(()=>{document.getElementById("hdn-info").style.display="block",document.getElementById("downloader-info").style.display="none"}),start_player(keys),document.getElementById("d-linker").href=encodeURI(`/report?id=${movie_id}`),document.getElementById("custom-dl").onclick=(()=>{document.getElementById("buttons-row").style.display="block"});