from app import app, db
from app.models import *
from app.forms import CreateClient

@app.shell_context_processor
def make_shell_context():
	return {'db':db,
			'User':User, 
			'Client':Client,
			'ClientRelationship': ClientRelationship,
			'Relationship': Relationship,
			'ClientContact': ClientContact,
			'ContactType': ContactType,
			'ClientAddress': ClientAddress,
			'Gender': Gender,
			'Ethnicity': Ethnicity,
			'Race': Race,
			'ClientRace': ClientRace,
			'ServiceType': ServiceType,
			'Program': Program,
			'ProgramServiceType': ProgramServiceType,
			'Kiosk': Kiosk,
			'Assessment':Assessment,
			'OutcomeMatrix':OutcomeMatrix,
			'OutcomeDomainLevels':OutcomeDomainLevels,
			'HousingAssessment':HousingAssessment,
			'HousingStatus':HousingStatus,
			'AssessmentType':AssessmentType,
			'Family':Family,
			'FamilyMember':FamilyMember}