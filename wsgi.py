import sys
path = '/home/CarlosPedrosa/'
if path not in sys.path:
   sys.path.insert(0, path)

from flask_app import app as application