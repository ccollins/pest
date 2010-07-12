What is pest?
==============
Pest was created to give you the shortest feedback loop possible in your unit testing (much like autotest or autospec). 

Using pest
==========
Pester will execute a command anytime a file changes in a directory below it.  In a django project for instance, run pester at the topmost level (where manage.py is), and your tests will execute everytime a .py file changes in the project.

  $>pester

Pest will search its current path for an executable runtests script (this script can be anything, just make sure you want it ran each time a file is changed) and then a django manage.py script.  Pest also takes arguments to execute instead of runtests or manage.py.  If I wanted to execute only a certain django app's test suite, then I could run

  $>pester python manage.py test myapp