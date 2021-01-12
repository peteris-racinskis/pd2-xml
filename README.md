#pd2-xml - a task-specific wrapper for SQLite
This piece of software is not intended for any practical application, as it was developed to meet a rather specific set of requirements for a university progamming assignment.
###Installation
No packaging provided, but since this tool only uses the Python standard library, no addtional software is required.

'''
$ git clone git@github.com:peteris-racinskis/pd2-xml.git
...
$ cd pd2-xml/
$ ./main.py [ ... ARGUMENTS ... ]
'''
###Usage
Updating values in the database file:
'''
# updating values in the database:
$ ./main.py update file.xml
'''
Supports multiple filenames in arguments:
'''
# supports arbitary number of input files:
$ ./main.py update ${path_to_directory}/*
'''
Displaying statistics:
'''
$ ./main.py display [ Option ]
'''
