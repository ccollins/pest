import objc
import os, sys, time
from Growl import Image, GrowlNotifier

PASS = "PASS"
FAIL = "FAIL"
    
class Pest(object):
    def __init__(self, notifications=[PASS, FAIL], root=os.path.abspath(os.curdir)):
        self.init_growl(notifications)
        self.root = root 
        self.last_search_time = 0
        self.name = root.split('/')[-1]
        
    def init_growl(self, notifications):
        try:
            self.gn = GrowlNotifier(applicationName='pest', notifications=notifications)
            self.gn.register()
        except:
            self.gn = None
            
    def notify(self, result):
        if self.gn:
            if result == PASS:
                self.gn.notify(noteType=PASS, title="%s: Tests Passed" % self.name.upper(), description="All tests passed!", 
                             icon=Image.imageFromPath(os.path.join(os.path.dirname(__file__), "images", "pass.png")))
            elif result == FAIL:
                self.gn.notify(noteType=FAIL, title="%s: Tests Failed" % self.name.upper(), description="FAIL!!!",
                             icon=Image.imageFromPath(os.path.join(os.path.dirname(__file__), "images", "fail.png")))
            else:
                self.gn.notify(noteType=PASS, title="%s: Running Tests" % self.name.upper(), description="Running tests...", 
                             icon=Image.imageFromPath(os.path.join(os.path.dirname(__file__), "images", "pending.png")))
    def grade_result(self, results):
        result = FAIL
        if results == 0:
            result = PASS
        return result
           
    def exclude_dir(self, name):
        return name.startswith('.') 

    def exclude_file(self, name):
        return (not name.endswith('.py') and not name.endswith('.html')) or name.startswith('.')
        
    def run_tests(self):
        self.notify('RUN') 
        
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