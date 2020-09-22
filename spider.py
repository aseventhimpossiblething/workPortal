#clear associated file spiderGrep and midnighhowl
"""
import os
import threading
import time
target_Site="https://www.newhomesource.com"
def sendSpider(targetSite):
    os.system("echo 'bash'")
    os.system("sudo touch spiderfile")
    targetSite=targetSite
    spiderCmmnd="sudo wget -r -b -nd "+targetSite+" --spider -o spiderfile"
    retrieveNmbr="bash spiderGrep.sh"
    os.system(spiderCmmnd)
    
    #os.system("bash midnighthowl.sh")
    
    spiderfile=open('spiderfile','r')
    spiderlines=spiderfile.readlines()
    spiderfile.close()
    
    #print("=",spiderlines)
    """
    time.sleep(20)
    spiderfile=open('spiderfile','r')
    spiderlines=spiderfile.readlines()
    #print(spiderlines)
    spiderfile.close()
    """
    #os.system("bash spiderGrep.sh")
    #os.system("cat spiderfile | grep -a ' broken' >brokenLines")
    #os.system("echo 'bash2'")
#launchSpider=threading.Thread(target=sendSpider, args=(target_Site,))
#launchSpider.start()
#sendSpider(target_Site)
"""
