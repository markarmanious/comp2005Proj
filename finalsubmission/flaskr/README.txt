This is the COMP2005 group project submission for:
George Neonakis 201311883
Isaac Murisa 201534328
Mark Armanious 201631918
Jared Pope 200737872

The package includes:

Module files- files for the modules used by flask, test data bases, README, and other flask required files

flaskr/:
templates - jinja templates folder for flask
docs - Documents relating to the project, including all requirements (HLD, interface design, requirements, gant chart, etc) NOTE: The group member handling the gant chart dropped the course the weekend it was due so the gant chart submitted is a bit wobbly).
tests - folder for the unit tests.
        TO RUN THE TESTS: the unit tests can be run with 'python3 -m unittest', 
        but must be run from inside the install directory (directory with this README file), since the modules are not exported.
        The package __init__.py files could be changed to export the modules,
        but this was not covered in class or tutorials.
static - contains the .css file used by flaskr

Derivable Location:
1. Project management plan: flaskr/flaskr/Docs folder
2. Requirements document: flaskr/flaskr/Docs folder
3. Design document: flaskr/flaskr/Docs folder
4. Developed source code: install directory, flaskr/flaskr folder
5. test suites: flaskr/flaskr/tests folder
6. Documentation explaining the state of the prototype: flaskr/flaskr/Docs folder
7. pip compliant zip file: D2L


TO RUN THE FLASK APPLICATION:
    with flask installed the shell commands are:
        $ export FLASK_APP=flaskr/flaskr.py
        $ flask run
TO RUN THE TESTS: the unit tests can be run with 'python3 -m unittest'
