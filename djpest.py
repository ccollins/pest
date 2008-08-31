from pest import Pest
import os, sys

def exclude_dir(name):
    return name.startswith('.') 

def exclude_file(name):
    return not name.endswith('.py')

def run(module=None): 
    cmd = './manage.py test'
    if module:
        cmd += ' ' + module
    def callback(changes):
        print changes
        os.system(cmd)
    return callback

def main():
    if len(sys.argv) == 1:
        cb = run(sys.argv[1])
    else:
        cb = run()
    Pest(exclude_file=exclude_file, exclude_dir=exclude_dir,callback=cb).start()
    

if __name__ == '__main__':
    main()