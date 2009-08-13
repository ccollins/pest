import os, pest

CMD = "manage.py"

class DjangoPest(pest.Pest):
    def run_tests(self): 
        self.notify(self.grade_result(os.system("%s/%s test" % (self.root, CMD))))