import objc
import os, sys, time
from Growl import Image, GrowlNotifier

PASS = "PASS"
FAIL = "FAIL"
PENDING = "PENDING"

def notify(growl, results):
    if growl:
        if results == 0:
            growl.notify(noteType=PASS, title="Tests Passed", description="All tests passed!", 
                         icon=Image.imageFromPath(os.path.join(os.path.dirname(__file__), "etc/images/pass.png")))
        else:
            growl.notify(noteType=FAIL, title="Tests Failed", description="FAIL!!!",
                         icon=Image.imageFromPath(os.path.join(os.path.dirname(__file__), "etc/images/fail.png")))
    
class Pest(object):
    def __init__(self, notifications=[PASS, FAIL], root=os.path.abspath(os.curdir)):
        self.init_growl(notifications)
        self.root = root 
        self.last_search_time = 0

    def init_growl(self, notifications):
        try:
            self.gn = GrowlNotifier(applicationName='pest', notifications=notifications)
            self.gn.register()
        except:
            self.gn = None
            
    def exclude_dir(self, name):
        return name.startswith('.') 

    def exclude_file(self, name):
        return not name.endswith('.py') and not name.endswith('.html')
        
    def has_changed(self):
        last_search_time = self.last_search_time
        self.last_search_time = time.time()
        
        for root, dirs, files in os.walk(self.root):
            map(dirs.remove, [d for d in dirs if self.exclude_dir(d)])
            map(files.remove, [f for f in files if self.exclude_file(f)])
            for name in files:
                f = os.path.join(root, name)
                if os.path.getmtime(f) > last_search_time:
                    return True
        return False