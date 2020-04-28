import os
import threading
import time
targetSite="https://bdxapilink.com"
def spider(targetSite):
    os.system("echo 'bash'")
    #targetSite="https://bdxapilink.com"
    #targetSite="https://www.newhomesource.com"
    targetSite=targetSite
    spiderCmmnd="wget -r -b -nd "+targetSite+" --spider -o spiderfile"
    #spiderCmmnd="wget -r -b -nd https://www.newhomesource.com --spider -o spiderfile"
    retrieveNmbr="bash spiderGrep.sh"
    os.system(spiderCmmnd)
    #print("30 sec pause")
    #time.sleep(10)
    #print("_____________")
    #os.system(retrieveNmbr)
    #time.sleep(10)
    #os.system(retrieveNmbr)    
    #os.system("touch brokenLines")
    #os.system("cat spiderfile | grep -a ' broken' >brokenLines")
    os.system("bash midnighthowl.sh")
    time.sleep(10)
    os.system("bash midnighthowl.sh")
    
    spiderfile=open('spiderfile','r')
    spiderlines=spiderfile.readlines()
    print(spiderlines)
    spiderfile.close()
    """
    time.sleep(20)
    spiderfile=open('spiderfile','r')
    spiderlines=spiderfile.readlines()
    #print(spiderlines)
    spiderfile.close()
    """
    #os.system("bash spiderGrep.sh")
    #os.system("cat spiderfile | grep -a ' broken' >brokenLines")
    os.system("echo 'bash2'")
#launchSpider=threading.Thread(target=spider)
#launchSpider.start()
spider(targetSite)
