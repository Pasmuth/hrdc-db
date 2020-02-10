import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
	# SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
	# 	'mysql+mysqldb://root@/flaskdb?unix_socket=/cloudsql/hrdc-db:flaskdb' or \
	# 	'sqlite:///' + os.path.join(basedir, 'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	USER = 'root'
	PASSWORD = ''
	DATABASE = 'flaskdb'
	# connection_name is of the format `project:region:your-cloudsql-instance`
	CONNECTION_NAME = 'hrdc-db:us-west1:flaskdb' 

	SQLALCHEMY_DATABASE_URI = (
	    'mysql+pymysql://{user}:{password}@localhost/{database}'
	    '?unix_socket=/cloudsql/{connection_name}').format(
	        user=USER, password=PASSWORD,
	        database=DATABASE, connection_name=CONNECTION_NAME)