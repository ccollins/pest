import os, pest

CMD = 'runtests.py'

class RunTestsPest(pest.Pest):
    def run_tests(self, changes): 
        pest.notify(self.gn, os.system("./%s" % CMD))