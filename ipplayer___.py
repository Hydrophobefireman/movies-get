a=r.post(u+'/ip.file/swf/plugins/ipplugins.php',data={"ipplugins":1,"ip_film":"842","ip_server":'4','ip_name':'1','fix':'null'})
b=json.loads(a.text)
aa=r.post(u+'/ip.file/swf/ipplayer/ipplayer.php',data={"u":b['s'],"w":"100%25","h":"500","s":"4",'n':'0'})
aa.text
