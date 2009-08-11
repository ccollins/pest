import os, sys, pest

def exclude_dir(name):
    return name.startswith('.') 

def exclude_file(name):
    return not name.endswith('.py')

def run(module, growl): 
    cmd = './manage.py test'
    if module:
        cmd += ' ' + module
    def callback(changes):
        pest.notify(growl, os.system(cmd))
    return callback

def main():
    try:
        from Growl import GrowlNotifier
        gn = GrowlNotifier(applicationName='pest', notifications=[pest.PASS, pest.FAIL])
        gn.register()
    except:
        gn = None
    
    app = None
    if len(sys.argv) == 1:
        app = sys.argv[1]

    cb = run(app, gn)
    pest.Pest(exclude_file=exclude_file, exclude_dir=exclude_dir,callback=cb).start()
    

if __name__ == '__main__':
    main()