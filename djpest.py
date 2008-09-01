from pest import Pest
import os, sys

    
def exclude_dir(name):
    return name.startswith('.') 

def exclude_file(name):
    return not name.endswith('.py')

def notify(growl, results):
    if growl:
        if results == 0:
            growl.notify(noteType='pass', title="Tests Pass", description="All tests passed!")
        else:
            growl.notify(noteType='fail', title="Tests Failed", description="FAIL!!!")

def run(module, growl): 
    cmd = './manage.py test'
    if module:
        cmd += ' ' + module
    def callback(changes):
        notify(growl, os.system(cmd))
    return callback

def main():
    try:
        from Growl import GrowlNotifier
        gn = GrowlNotifier(applicationName='djpest', notifications=['pass', 'fail'])
        gn.register()
    except:
        gn = None
    
    app = None
    if len(sys.argv) == 1:
        app = sys.argv[1]

    cb = run(app, gn)
    Pest(exclude_file=exclude_file, exclude_dir=exclude_dir,callback=cb).start()
    

if __name__ == '__main__':
    main()