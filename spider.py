import os
import threading
import time
def spider():
    os.system("echo 'bash'")
    spiderCmmnd="wget -r -b -nd https://www.newhomesource.com --spider -o spiderfile"
    retrieveNmbr="bash spiderGrep.sh"
    os.system(spiderCmmnd)
    print("10 sec pause")
    time.sleep(10)
    print("_____________")
    #os.system(retrieveNmbr)
    #time.sleep(10)
    #os.system(retrieveNmbr)    
    #os.system("touch brokenLines")
    #os.system("cat spiderfile | grep -a ' broken' >brokenLines")
    os.system("bash midnighthowl.sh")
    os.system("echo 'bash2'")
launchSpider=threading.Thread(target=spider)
launchSpider.start()
#spider()
