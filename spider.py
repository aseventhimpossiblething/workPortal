import os
os.system("echo 'bash'")
spiderCmmnd="wget -r -nd -nv https://www.newhomesource.com --spider -o spiderfile"
retrieveNmbr="echo spiderfile|grep ' 200' "
os.system(spiderCmmnd)
os.system(retrieveNmbr)
