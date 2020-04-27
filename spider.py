import os
import threading
def spider:
    os.system("echo 'bash'")
    spiderCmmnd="wget -r -nd https://www.newhomesource.com --spider -o spiderfile"
    retrieveNmbr="echo spiderfile|grep ' 200' "
    os.system(spiderCmmnd)
    os.system(retrieveNmbr)
launchSpider=threading.Thread(spider)
launchSpider.start()
