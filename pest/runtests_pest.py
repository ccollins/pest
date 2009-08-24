import os, pest

CMD = 'runtests'

class RunTestsPest(pest.Pest):
    def run_tests(self): 
        super(RunTestsPest, self).run_tests()
        self.notify(self.grade_result(os.system("%s/%s" % (self.root, CMD))))