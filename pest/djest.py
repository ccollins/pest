import os, sys
from pest import pest

class Djest(pest.Pest):
    def __init__(self):
        super(Djest, self).__init__(notifications=[pest.PASS, pest.FAIL])
        
    def exclude_dir(self, name):
        return name.startswith('.') 

    def exclude_file(self, name):
        return not name.endswith('.py') and not name.endswith('.html')

    def run_tests(self, changes): 
        pest.notify(self.gn, os.system('./manage.py test'))

if __name__ == '__main__':
    Djest().start()