from FSEvents import *
import objc
import os, sys

class Pest(object):
    def __init__(self):
        self.snapshot = {}
        self.target = os.path.abspath(os.curdir)
        self.callback = lambda x: x

    def run(self):
        changes = self._check_changes()
        if changes:
            self.callback(changes)

    def _remove_from(self, l, items):
        for i in items:
            l.remove(i)

    def _check_changes(self):
        changes = []
        for root, dirs, files in os.walk(self.target):
            self._remove_from(dirs, [d for d in dirs if d.startswith('.')])
            self._remove_from(files, [f for f in files if not f.endswith('.py')])
            for name in files:
                f = os.path.join(root, name)
                last_update = os.path.getmtime(f)
                last_known = self.snapshot.setdefault(f, last_update)
                if last_update != last_known:
                    changes.append(f)
                    self.snapshot[f] = last_update
        return changes

    def timer_callback(self, timer, stream):
        FSEventStreamFlushAsync(stream)
    
    def fsevents_callback(self, stream, clientInfo, numEvents, eventPaths, eventMasks, eventIDs):
        self.run()
    
    def createStream(self, full_path):
        stream = FSEventStreamCreate(kCFAllocatorDefault,            # allocator 
                                      self.fsevents_callback,             # callback  
                                      full_path,                     # path      
                                      [full_path],                   # path
                                      kFSEventStreamEventIdSinceNow, # since_when
                                      1.0,                           # latency   
                                      0)                             # flags     

        assert stream, "ERROR: FSEVentStreamCreate() => NULL"
        return stream

    def run_loop(self, stream):
        FSEventStreamScheduleWithRunLoop(stream, CFRunLoopGetCurrent(), kCFRunLoopDefaultMode)
        assert FSEventStreamStart(stream), "Failed to start stream"
        timer = CFRunLoopTimerCreate(kCFAllocatorDefault, 
                                    CFAbsoluteTimeGetCurrent() + 1.0, 
                                    1.0, 
                                    0, 
                                    0, 
                                    self.timer_callback,
                                    stream)
        CFRunLoopAddTimer(CFRunLoopGetCurrent(), timer, kCFRunLoopDefaultMode)
        try:
            CFRunLoopRun()
        finally:
            FSEventStreamStop(stream)
            FSEventStreamInvalidate(stream)
            FSEventStreamRelease(stream)
    
    def start(self):
        abspath = os.path.join(os.path.abspath(os.curdir), self.target)
        self.run_loop(self.createStream(abspath))
    
def main():
    pest = Pest()
    def dump(changes): print changes
    pest.target = sys.argv[1]
    pest.callback = dump
    pest.start()

if __name__ == '__main__':
    main()