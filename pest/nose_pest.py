import os, pest

CMD = 'nosetests'

class NosePest(pest.Pest):
    def run_tests(self, changes): 
        pest.notify(self.gn, os.system(CMD))