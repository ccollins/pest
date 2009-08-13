import os, pest

CMD = 'runtests.py'

class RunTestsPest(pest.Pest):
    def run_tests(self): 
        self.notify(self.grade_result(os.system("%s/%s" % (self.root, CMD))))