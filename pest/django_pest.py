import os, pest

CMD = "manage.py"

class DjangoPest(pest.Pest):
    def run_tests(self, changes): 
        pest.notify(self.gn, os.system("./%s test" % CMD))