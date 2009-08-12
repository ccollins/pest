from FSEvents import *
import objc
import os, sys
from Growl import Image, GrowlNotifier

PASS = "PASS"
FAIL = "FAIL"
PENDING = "PENDING"

def watch(stream):
    FSEventStreamScheduleWithRunLoop(stream, CFRunLoopGetCurrent(), kCFRunLoopDefaultMode)
    assert FSEventStreamStart(stream), "Failed to start stream"
    timer = CFRunLoopTimerCreate(kCFAllocatorDefault, CFAbsoluteTimeGetCurrent() + 1.0, 1.0, 0, 
                                 0, lambda timer, stream: FSEventStreamFlushAsync(stream), stream)
    CFRunLoopAddTimer(CFRunLoopGetCurrent(), timer, kCFRunLoopDefaultMode)
    try:
        CFRunLoopRun()
    finally:
        FSEventStreamStop(stream)
        FSEventStreamInvalidate(stream)
        FSEventStreamRelease(stream)

def notify(growl, results):
    if growl:
        if results == 0:
            growl.notify(noteType=PASS, title="Tests Passed", description="All tests passed!", 
                         icon=Image.imageFromPath(os.path.join(os.path.dirname(__file__), "etc/images/pass.png")))
        else:
            growl.notify(noteType=FAIL, title="Tests Failed", description="FAIL!!!",
                         icon=Image.imageFromPath(os.path.join(os.path.dirname(__file__), "etc/images/fail.png")))
            
class Pest(object):
    def __init__(self, notifications=[]):
        self.init_growl(notifications)
        self.snapshot = {}
        self.target = os.path.abspath(os.curdir)

    def init_growl(self, notifications):
        try:
            self.gn = GrowlNotifier(applicationName='pest', notifications=notifications)
            self.gn.register()
        except:
            self.gn = None
            
    def exclude_dir(self):
        return False
        
    def exclude_file(self):
        return False
        
    def run(self, default_time):
        changes = self._check_changes(default_time)
        if changes:
            self.run_tests(changes)

    def _check_changes(self, default_time):
        changes = []
        current_files = []
        for root, dirs, files in os.walk(self.target):
            map(dirs.remove, [d for d in dirs if self.exclude_dir(d)])
            map(files.remove, [f for f in files if self.exclude_file(f)])
            for name in files:
                f = os.path.join(root, name)
                current_files.append(f)
                last_update = os.path.getmtime(f)
                last_known = self.snapshot.setdefault(f, default_time(f))
                if last_update != last_known:
                    changes.append(f)
                    self.snapshot[f] = last_update
        for k in self.snapshot.keys():
            if k not in current_files:
                changes.append(k)
                del self.snapshot[k]
        return changes


    def start(self):
        stream = FSEventStreamCreate(kCFAllocatorDefault,               # allocator 
                                      lambda *x: self.run(lambda f: 0), # callback  
                                      self.target,                      # path
                                      [self.target],                    # path
                                      kFSEventStreamEventIdSinceNow,    # since_when
                                      1.0,                              # latency   
                                      0)                                # flags     
        assert stream, "ERROR: FSEVentStreamCreate() => NULL"
        self.run(lambda f: 0)
        watch(stream)