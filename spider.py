import os
import threading
def spider():
    os.system("echo 'bash'")
    spiderCmmnd="wget -r -b -nd https://www.newhomesource.com --spider -o spiderfile"
    retrieveNmbr="cat spiderfile"
    os.system(spiderCmmnd)
    print("_____________")
    os.system(retrieveNmbr)
    os.system("echo 'bash2'")
#launchSpider=threading.Thread(target=spider)
#launchSpider.start()
spider()
