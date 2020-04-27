import os
import threading
def spider():
    os.system("echo 'bash'")
    spiderCmmnd="wget -r -b -nd https://www.newhomesource.com --spider -o spiderfile"
    retrieveNmbr="echo spiderfile|grep ' 200' "
    os.system(spiderCmmnd)
    os.system(retrieveNmbr)
launchSpider=threading.Thread(target=spider)
launchSpider.start()
