import os, pest

CMD = "manage.py"

class DjangoPest(pest.Pest):
    def run_tests(self): 
        pest.notify(self.gn, os.system("%s/%s test" % (self.root, CMD)))