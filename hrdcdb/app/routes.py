import sys
import pdfkit
import os
import json
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, jsonify, send_file, make_response, json
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import *
from app.models import *
from app.kiosk import checkin_to_db

@app.route('/login', methods = ['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username = form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember = form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', title = 'Sign In', form = form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/')
@app.route('/index')
@login_required
def index():
	return render_template('index.html', title = 'Home')


@app.route('/register', methods = ['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username = form.username.data, email = form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Now Registered')
		return redirect(url_for('login'))
	return render_template('form_view.html', title = 'Register', form = form)


@app.route('/create_client', methods = ['GET','POST'])
@login_required
def create_client():
	form = CreateClient()
	if form.validate_on_submit():
		client = Client(first_name = form.first_name.data,
						middle_name = form.middle_name.data,
						last_name = form.last_name.data,
						dob = form.dob.data,
						SSN = form.SSN.data,
						veteran = form.veteran.data,
						activeMilitary = form.activeMilitary.data,
						disability = form.disability.data,
						foreignBorn = form.foreignBorn.data,
						ethnicity = form.ethnicity.data,
						gender = form.gender.data,
						created_by = current_user.id)
		db.session.add(client)
		db.session.commit()
		clientRace = ClientRace(client_id = client.id, race_id = form.race.data, created_by = current_user.id)
		db.session.add(clientRace)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('form_view.html', title = 'Add Client', form = form)


@app.route('/<form>_form', methods = ['GET', 'POST'])
@login_required
def render_form(form):
	form_class = globals()[form]
	instance = form_class()
	if instance.validate_on_submit():
		instance.execute_transaction()
		return redirect(url_for('render_form', form = form))
	return render_template('form_view.html', title = instance.form_title, form = instance)


@app.route('/find_clients_', defaults = {'client_data':None}, methods = ['GET','POST'])
@app.route('/find_clients_<client_data>', methods = ['GET', 'POST'])
@login_required
def view_clients(client_data = None):
	if client_data != 'None':
		search_data = Kiosk.query.filter(Kiosk.id == client_data).first()
		form = FilterClients(data = search_data.__dict__)
	else:
		form = FilterClients()
	if form.validate_on_submit():
		clients = Client.query
		if form.first_name.data:
			clients = clients.filter(Client.first_name.like('%{}%'.format(form.first_name.data)))
		if form.last_name.data:
			clients = clients.filter(Client.last_name.like('%{}%'.format(form.last_name.data)))
		return render_template('search_results.html', title = 'Search Results', form = form, clients = clients)
	return render_template('search_results.html', title = 'Client Search', form = form)


@app.route('/family_client_search', methods = ['GET','POST'])
def family_client_search():
	first_name = request.args.get('first_name')
	middle_name = request.args.get('middle_name')
	last_name = request.args.get('last_name')
	dob = request.args.get('dob')
	SSN = request.args.get('SSN')

	clients = Client.query
	if first_name != '':
		clients = clients.filter(Client.first_name.like('%{}%'.format(first_name)))
	if middle_name != '':
		clients = clients.filter(Client.middle_name.like('%{}%'.format(middle_name)))
	if last_name != '':
		clients = clients.filter(Client.last_name.like('%{}%'.format(last_name)))
	if dob != '':
		clients = clients.filter(Client.dob == dob)

	return jsonify({'data': render_template('ajax_search_results.html', clients = clients.all())})


@app.route('/client_search', methods = ['GET','POST'])
def client_search():
	first_name = request.args.get('first_name')
	middle_name = request.args.get('middle_name')
	last_name = request.args.get('last_name')
	dob = request.args.get('dob')
	SSN = request.args.get('SSN')

	clients = Client.query
	if first_name != '':
		clients = clients.filter(Client.first_name.like('{}%'.format(first_name)))
	if middle_name != '':
		clients = clients.filter(Client.middle_name.like('{}%'.format(middle_name)))
	if last_name != '':
		clients = clients.filter(Client.last_name.like('{}%'.format(last_name)))
	if dob != '':
		clients = clients.filter(Client.dob == dob)

	return jsonify({'data': render_template('indiv_search_results.html', clients = clients.all())})


@app.route('/client_<clientid>_dashboard', methods = ['GET','POST'])
@login_required
def client_dashboard(clientid):
	client = Client.query.filter(Client.id == clientid).first()
	relations = ClientRelationship.query.filter(ClientRelationship.client_a_id == clientid).all()
	client_families = FamilyMember.query.filter(FamilyMember.client_id == clientid).all()
	families = []
	for f in client_families:
		families.append(Family.query.filter(Family.id == f.family_id).first())

	contact_info = ClientContact.query.filter(ClientContact.client_id == clientid).all()
	services = Service.query.filter(Service.client_id == clientid).all()
	assessments = Assessment.query.filter(Assessment.client_id == clientid).all()
	try:
		address = ClientAddress.query.filter(ClientAddress.client_id == clientid).all()[-1]
	except IndexError:
		address = None
	return render_template('client_dashboard.html', 
							title = '{} {} Dashboard'.format(client.first_name, client.last_name),
							client = client, relations = relations, contact_info = contact_info,
							address = address, services = services, assessments = assessments,
							families = families)


@app.route('/client_<clientid>_contact', methods = ['GET', 'POST'])
@login_required
def create_contact(clientid):
	form = CreateClientContact()
	contact_info = ClientContact.query.filter(ClientContact.client_id == clientid).all()
	if form.validate_on_submit():
		new_contact = ClientContact(client_id = clientid,
									contact = form.contact_info.data,
									contact_type = form.contact_type.data,
									created_by = current_user.id)
		db.session.add(new_contact)
		db.session.commit()
		return redirect(url_for('create_contact', clientid = clientid))
	return render_template('create_contact.html', title = 'Create Contact', form = form, contact_info = contact_info, cid = clientid)


@app.route('/create_relationship_<clientid>', defaults = {'second_client':None}, methods = ['GET','POST'])
@app.route('/create_relationship_<clientid>_<second_client>', methods = ['GET','POST'])
@login_required
def create_relationship(clientid, second_client):
	form = CreateRelationship()
	rels = ClientRelationship.query.filter(ClientRelationship.client_a_id == clientid).all()
	if form.validate_on_submit():
		rel = ClientRelationship(client_a_id = form.first_client.data,
								 client_b_id = form.second_client.data,
								 a_to_b_relation = form.relationship.data,
								 created_by = current_user.id)
		if form.relationship.data in [1,6,7,8,9]:
			back_rel = ClientRelationship(client_a_id = form.second_client.data,
								 		  client_b_id = form.first_client.data,
								 		  a_to_b_relation = form.relationship.data,
								 		  created_by = current_user.id)
		elif form.relationship.data == 2:
			back_rel = ClientRelationship(client_a_id = form.second_client.data,
								 		  client_b_id = form.first_client.data,
								 		  a_to_b_relation = 5,
								 		  created_by = current_user.id)
		elif form.relationship.data == 5:
			back_rel = ClientRelationship(client_a_id = form.second_client.data,
								 		  client_b_id = form.first_client.data,
								 		  a_to_b_relation = 2,
								 		  created_by = current_user.id)
		elif form.relationship.data == 3:
			back_rel = ClientRelationship(client_a_id = form.second_client.data,
								 		  client_b_id = form.first_client.data,
								 		  a_to_b_relation = 4,
								 		  created_by = current_user.id)
		elif form.relationship.data == 4:
			back_rel = ClientRelationship(client_a_id = form.second_client.data,
								 		  client_b_id = form.first_client.data,
								 		  a_to_b_relation = 3,
								 		  created_by = current_user.id)
		db.session.add(rel)
		db.session.add(back_rel)
		db.session.commit()
		return redirect(url_for('create_relationship', clientid = clientid))
	return render_template('create_relationship.html', title = 'Create Relationship', data = rels, form = form, cid = clientid)	


@app.route('/edit_client_<clientid>', methods = ['GET','POST'])
@login_required
def edit_client(clientid):
	client = Client.query.filter(Client.id == clientid).first()
	form = EditClient(data = client.__dict__)
	if form.validate_on_submit():
		client.first_name = form.first_name.data
		client.middle_name = form.middle_name.data
		client.last_name = form.last_name.data
		client.dob = form.dob.data
		client.SSN = form.SSN.data
		client.veteran = form.veteran.data
		client.activeMilitary = form.activeMilitary.data
		client.gender = form.gender.data
		client.ethnicity = form.ethnicity.data
		db.session.commit()
		return redirect(url_for('client_dashboard', clientid = clientid))
	return render_template('form_view.html', form = form, cid = clientid)


# record_type is the name of the model as a string
# e.g. 'Program'
@app.route('/add_<record_type>', methods = ['GET','POST'])
def add_record(record_type):
	record_class = globals()[record_type]
	record_form = globals()['Create'+record_type]
	instance = record_form()
	records = record_class.query.all()
	if instance.validate_on_submit():
		instance.execute_transaction()
		return redirect(url_for('add_record', record_type = record_type))
	return render_template('add_record.html', title = instance.form_title, form = instance, data = records)


@app.route('/add_Service_<clientid>', methods = ['GET','POST'])
def add_service(clientid):
	services = Service.query.filter(Service.client_id == clientid).all()
	prefill = {'client_id':clientid,'created_by':current_user.id}
	form = CreateService(data = prefill)
	if form.validate_on_submit():
		form.execute_transaction()
		return redirect(url_for('add_service', clientid = clientid))
	elif request.method == 'GET':
		# check for request parameters
		if request.args.get('recordID'):
			#get the recorde id that needs to be deletedf
			recordID = request.args.get('recordID')
			# update database
			recordToDel = Service.query.filter(Service.id == recordID).first()
			# do some validation
			if str(recordToDel.client_id) == clientid:
				db.session.delete(recordToDel)
				db.session.commit()
				return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
			else:
				return json.dumps({'error': True}), 404, {'ContentType': 'application/json'}
		# if no parameters are present, its just a regular get
		else:
			return render_template('add_service.html', title = 'Add Service', form = form, data = services)
	# if the submit and validate fails
	else:
		return render_template('add_service.html', title='Add Service', form=form, data=services, cid = clientid)



@app.route('/_get_service_types')
def _get_service_types():
	program = request.args.get('program_id')
	service_types = ProgramServiceType.query.filter(ProgramServiceType.program_id == program).all()
	program_service_types = [(pst.service_type.id, pst.service_type.name) for pst in service_types]
	print(program_service_types, file = sys.stderr)
	return json.dumps(dict(program_service_types))


@app.route('/add_family_service_<familyid>', methods = ['GET','POST'])
def add_family_service(familyid):
	services = Service.query.filter(Service.family_id == familyid).all()
	prefill = {'is_family': True, 'family_id':familyid,'created_by':current_user.id}
	form = CreateService(data = prefill)
	if form.validate_on_submit():
		form.execute_transaction()
		return redirect(url_for('add_family_service', familyid = familyid))
	return render_template('add_service.html', title = 'Add Family Service', form = form, data = services, fid = familyid)


@app.route('/client_checkin', methods = ['GET','POST'])
def client_checkin():
	checkin_to_db()
	today = datetime.today()
	lobby = Kiosk.query.filter(Kiosk.timestamp.date() == datetime.today.date())
	return render_template('client_checkin.html', lobby = lobby)


@app.route('/universal_form_<clientid>', methods = ['GET','POST'])
def universal_form(clientid):
	client = Client.query.filter(Client.id == clientid).first()
	try:
		address = ClientAddress.query.filter(ClientAddress.client_id == clientid).all()[-1]
	except IndexError:
		address = None
	try:
		cell = ClientContact.query.filter(ClientContact.client_id == clientid).filter(ClientContact.contact_type == 3).first()
	except:
		cell = None
	try:
		email = ClientContact.query.filter(ClientContact.client_id == clientid).filter(ClientContact.contact_type == 5).first()
	except:
		email = None
	try:
		work = ClientContact.query.filter(ClientContact.client_id == clientid).filter(ClientContact.contact_type == 1).first()
	except:
		work = None
	rendered_form = render_template('universal_form_with_tables.html', 
						   client = client, address = address,
						   cell = cell, email = email, work = work)
	path = os.path.dirname(os.path.realpath(__file__))
	pdf = pdfkit.from_string(rendered_form, False, css = '{}\\static\\styles\\universal_form.css'.format(path))

	response = make_response(pdf)
	response.headers['Content-Type'] = 'application/pdf'
	response.headers['Content-Disposition'] = 'inline; output.pdf'

	return response


@app.route('/add_address_<clientid>', methods = ['GET','POST'])
def add_address(clientid):
	history = ClientAddress.query.filter(ClientAddress.client_id == clientid).all()
	prefill = {'client_id':clientid,'created_by':current_user.id}
	form = CreateClientAddress(data = prefill)
	if form.validate_on_submit():
		form.execute_transaction()
		return redirect(url_for('add_address', clientid=clientid))
	return render_template('add_address.html', title = form.form_title, form = form, data = history, cid = clientid)


@app.route('/add_assessment_<clientid>', methods = ['GET','POST'])
def add_assessment(clientid):
	prefill = {'client_id':clientid,'created_by':current_user.id}
	form = OMAssessment(data = prefill)
	if form.validate_on_submit():
		form.execute_transaction()
		return redirect(url_for('client_dashboard', clientid = clientid))
	return render_template('add_om_score.html', form = form, cid = clientid)


@app.route('/create_family', methods = ['GET','POST'])
def create_family():
	prefill = {'created_by':current_user.id}
	form = CreateFamily(data = prefill)
	if (request.method == 'GET') and request.args.get('client_ids'):
		ids = request.args.get('client_ids').split(',')
		print('ids: {}'.format(ids), file = sys.stderr)
		program = request.args.get('program')
		if len(ids) != 0:
			new_family = Family(program_id = program, 
							    created_date = datetime.utcnow(), 
							    created_by = current_user.id)
			db.session.add(new_family)
			db.session.flush()
			fam_id = new_family.id
			for cid in ids:
				new_mem = FamilyMember(family_id = fam_id, client_id = cid)
				db.session.add(new_mem)
			data = {'message': 'Family {} created at {}'.format(fam_id, new_family.created_date), 'code':'SUCCESS'}
			db.session.commit()
			return make_response(jsonify(data), 201)
		elif len(ids) == 0:
			print('this is an error', file = sys.stderr)
			data = {'message': 'Cannot create a family with no members', 'code':'ERROR'}
			return make_response(jsonify(data), 401)
	return render_template('create_family.html', form = form)
		

@app.route('/family_<familyid>_dashboard', methods = ['GET'])
def family_dashboard(familyid):
	family_members = FamilyMember.query.filter(FamilyMember.family_id == familyid).all()
	return render_template('family_dashboard.html', family_members = family_members, fid = familyid)