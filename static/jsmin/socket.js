String.prototype.trunc=function(e){return this.length>e?this.substr(0,e-1)+"...":this};var dynamic_inp=document.getElementById("dynamic_inp"),inp_res=document.getElementById("inp-results");function make_req(e,t){var n=e.value;check_inp(n)&&t.send(n)}function check_inp(e){return 0!==e.replace(/([^\w]|_)/g,"").length}(()=>{if(window.WebSocket){var e=("https:"===window.location.protocol?"wss://":"ws://")+window.location.host+"/suggestqueries",t=new WebSocket(e);dynamic_inp.oninput=function(){inp_res.innerHTML="",make_req(this,t)},t.onopen=function(e){console.log(e)},t.onmessage=function(e){_msg=e.data;var t=JSON.parse(_msg),n=t.data;console.log("Response Cached:"+t.Cached);for(var i=0;i<n.length;i++){var o=n[i],s=document.createElement("div"),r=document.createElement("span");s.setAttribute("data-im",o.id),s.onclick=function(){window.location="/movie/"+this.getAttribute("data-im")+"/movie"},s.style.cursor="pointer",s.style.listStyle="none",s.style.width="80%",s.appendChild(r),s.style.margin="auto",img.style.height="80px",img.style.margin="10px",r.innerHTML=o.movie,inp_res.appendChild(s),s.style.textAlign="left",s.style.border="2px solid #e3e3e3",s.style.borderRadius="5px"}}}})();