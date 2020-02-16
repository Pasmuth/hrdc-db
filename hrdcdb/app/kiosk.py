import os
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from app import app, db
from app.models import *

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
path = os.path.dirname(os.path.realpath(__file__))
creds = ServiceAccountCredentials.from_json_keyfile_name('{}\\client_secret.json'.format(path), scope)
client = gspread.authorize(creds)

# sheet = client.open_by_key('1Yo4ibOuL5mFcHOuYrJ-tEuEI93HuS5zGptua_sakugs')


def checkin_to_db():
	sheet = client.open_by_key('1Yo4ibOuL5mFcHOuYrJ-tEuEI93HuS5zGptua_sakugs')
	ws = sheet.get_worksheet(0)

	while len(ws.row_values(2)) > 0:
		data = ws.row_values(2)
		if len(data) == 6:
			chk = Kiosk(timestamp = datetime.strptime(data[0],'%m/%d/%Y %H:%M:%S'), first_name = data[1],
		            middle_name = data[2], last_name = data[3],
		            dob = datetime.strptime(data[4], '%m/%d/%Y'), SSN = data[5],
		            seen = False, cleared = False)
		else:
			chk = Kiosk(timestamp = datetime.strptime(data[0],'%m/%d/%Y %H:%M:%S'), first_name = data[1],
		            middle_name = data[2], last_name = data[3],
		            dob = datetime.strptime(data[4], '%m/%d/%Y'),
		            seen = False, cleared = False)
		db.session.add(chk)
		db.session.commit()
		ws.delete_row(2)



