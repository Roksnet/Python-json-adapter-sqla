# WSGI application for Apache 

activate_this = '/srv/python-json-demo/bin/activate_this.py'
exec(open(activate_this).read(), dict(__file__=activate_this))

from pyramid.paster import get_app, setup_logging
ini_path = '/srv/python-json-demo/etc/populationdb.ini'
setup_logging(ini_path)
application = get_app(ini_path, 'main')
