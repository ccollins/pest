import os, pest

class CustomPest(pest.Pest):
    cmd = ''
    
    def set_command(self, cmd):
        self.cmd = cmd
        
    def run_tests(self): 
        super(CustomPest, self).run_tests()
        self.notify(self.grade_result(os.system(self.cmd)))