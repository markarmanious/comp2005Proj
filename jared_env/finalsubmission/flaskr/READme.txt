This is the COMP2005 group project submission for [INSERT GROUP INFO HERE]

The package includes:

templates - jinja templates folder for flask
docs - an empty folder for docs
tests - folder for the unit test examples.
        TO RUN THE TESTS: the unit tests can be run with 'python3 -m unittest', 
        but must be run from inside the install directory, since the modules are not exported.
        The package __init__.py files could be changed to export the modules,
        but this was not covered in class or tutorials.

TO RUN THE FLASK APPLICATION:
    with flask installed the shell commands are:
        $ export FLASK_APP=flaskr/flaskr.py
        $ flask run
