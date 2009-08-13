import os, pest

CMD = 'nosetests'

class NosePest(pest.Pest):
    def run_tests(self): 
        self.notify(self.grade_result(os.system("%s --where=%s" % (CMD, self.root))))