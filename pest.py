from FSEvents import *
import objc
import os, sys

class Pest(object):
    def __init__(self, force_initial_run=True, target=None,
                callback=lambda x: x, exclude=lambda x: False):
        self.snapshot = {}
        self.target = target or os.path.abspath(os.curdir)
        self.callback = callback
        self.exclude = exclude
        if force_initial_run:
            self._first_run_time = lambda f: 0
        else:
            self._first_run_time = os.path.getmtime

    def run(self, default_time):
        changes = self._check_changes(default_time)
        if changes:
            self.callback(changes)

    def _check_changes(self, default_time):
        changes = []
        current_files = []
        for root, dirs, files in os.walk(self.target):
            map(dirs.remove, [d for d in dirs if self.exclude(d)])
            map(files.remove, [f for f in files if self.exclude(f)])
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
        abspath = os.path.join(os.path.abspath(os.curdir), self.target)
        stream = FSEventStreamCreate(kCFAllocatorDefault,               # allocator 
                                      lambda *x: self.run(lambda f: 0), # callback  
                                      abspath,                          # path
                                      [abspath],                        # path
                                      kFSEventStreamEventIdSinceNow,    # since_when
                                      1.0,                              # latency   
                                      0)                                # flags     
        assert stream, "ERROR: FSEVentStreamCreate() => NULL"
        self.run(self._first_run_time)
        self._run_loop(stream)
    
    def _run_loop(self, stream):
        FSEventStreamScheduleWithRunLoop(stream, CFRunLoopGetCurrent(), kCFRunLoopDefaultMode)
        assert FSEventStreamStart(stream), "Failed to start stream"
        timer = CFRunLoopTimerCreate(kCFAllocatorDefault, 
                                    CFAbsoluteTimeGetCurrent() + 1.0, 
                                    1.0, 
                                    0, 
                                    0, 
                                    lambda timer, stream: FSEventStreamFlushAsync(stream),
                                    stream)
        CFRunLoopAddTimer(CFRunLoopGetCurrent(), timer, kCFRunLoopDefaultMode)
        try:
            CFRunLoopRun()
        finally:
            FSEventStreamStop(stream)
            FSEventStreamInvalidate(stream)
            FSEventStreamRelease(stream)
    
def main():
    def exclude(name):
        return name.startswith('.') or not name.endswith('.py')
    def dump(changes): 
        print changes
    Pest(exclude=exclude,callback=dump).start()

if __name__ == '__main__':
    main()