!function(){const n=function(n="/beacon-test",e="ok"){return navigator.sendBeacon(n,e)}();window.Beacon={send:async function(e,o){return n?("object"==typeof o&&(o=JSON.stringify(o)),navigator.sendBeacon(e,o)):(new Image).src=e+(t=o,"?"+Object.keys(t).map(function(n){return encodeURIComponent(n)+"="+encodeURIComponent(t[n])}).join("&"));var t}}}();