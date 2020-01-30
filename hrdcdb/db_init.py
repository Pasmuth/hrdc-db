import pandas as pd
from app import app, db
from app.models import *


race_list = ['White','Another Race','Black or African American','Asian',
			 'Native Hawaiian or Pacific Islander',
			 'American Indian or Alaska Native', 'Unknown']

ethnicity_list = ['Hispanic or Latino','Not Hispanic or Latino','Unknown']

gender_list = ['Male','Female','Nonbinary','Unknown']

contact_types = ['Work','Home','Cell','Fax','Email']

relationships = ['Spouse/Partner','Parent',
				 'Grandparent','Grandchild',
				 'Child','Sibling','Friend',
				 'Other Relative', 'Other Non-Relative']

programs = ['Housing','Energy','Food Bank','Galavan']

service_types = [['Case Management','Hours'],['Intake', None],['Food Box','People'],['Emergency Shelter', None],
				 ['Energy Assistance','Dollars'],['Weatherization','Hours'],['Medical Ride', None],['Social Ride', None]]

assess_types = ['Outcome Matrix','Housing']

housing_statuses = ['Homeless', 'Not Homeless']

domain_levels = {'housing':{0:'Homeless',
							1:'Unsafe Housing',
							2:'Living with Friends',
							3:'Unaffordable Housing',
							4:'Transitional Housing',
							6:'Subsidized Housing',
							8:'Non-subsidized Rental',
							10:'Home/Condo Owner'
							},
				 'transportation':{0:'No access to transportation',
				 				   3:'Limited access to transportation',
				 				   6:'Some access to transportation',
				 				   8:'Good access to transportation',
				 				   10:'Perfect access to transportation',
				 				   },
				 'education':{0:'No reading, writing, or math skills',
				 			  4:'Has reading, writing and math skills; no diploma',
				 			  6:'Highschool Graduate or GED/HI-SET',
				 			  8:'Vocational school, or some college',
				 			  9:'Bachelors or Associates Degree',
				 			  10:'Master\'s or Doctorate'
				 			  },
				 'employment':{0:'Unemployed, no history or skills',
				 			   2:'Unemployed with history or skills',
				 			   3:'Part-time, no benefits',
				 			   4:'Part-time, benefits',
				 			   5:'Full-time, minimum wage, no benefits',
				 			   6:'Full-time, minimum wage, benefits',
				 			   8:'Full-time, living wage, no benefits',
				 			   10:'Full-time, living wage, benefits'},
				 'childcare':{0:'Unlicenced/Unregulated childcare',
				 			  2:'Not enrolled in childcare',
				 			  3:'Wait-listed for childcare',
				 			  6:'Childcare provided by family or friend',
				 			  7:'Enrolled in subsidized care, limited choices',
				 			  8:'Enrolled in subsidized care, own choice',
				 			  10:'Enrolled in licenced, unsubsidized care'},
				 'income':{0:'Below 50% of poverty',
				 		   2:'51%-100% of poverty',
				 		   4:'101%-125% of poverty',
				 		   6:'126%-175% of poverty',
				 		   8:'176%-200% of poverty',
				 		   10:'>200% of poverty',}
				 }

OutcomeDomainLevels.query.delete()

for key in domain_levels.keys():
	for k in domain_levels[key].keys():
		row = [key, k, domain_levels[key][k]]
		cur = OutcomeDomainLevels(domain = key, score = k, score_description = domain_levels[key][k])
		db.session.add(cur)



Ethnicity.query.delete()
Race.query.delete()
Gender.query.delete()
ContactType.query.delete()
Relationship.query.delete()
ServiceType.query.delete()
Program.query.delete()
ProgramServiceType.query.delete()
Service.query.delete()
AssessmentType.query.delete()
Assessment.query.delete()
OutcomeMatrix.query.delete()
HousingStatus.query.delete()
HousingAssessment.query.delete()


# Uncomment this section to drop all client data
# Client.query.delete()
# ClientRelationship.query.delete()
# ClientAddress.query.delete()
# ClientContact.query.delete()
# ClientRace.query.delete()
# Kiosk.query.delete()

db.session.commit()

for r in race_list:
	cur = Race(race = r)
	db.session.add(cur)

for e in ethnicity_list:
	cur = Ethnicity(ethnicity = e)
	db.session.add(cur)

for g in gender_list:
	cur = Gender(gender = g)
	db.session.add(cur)

for c in contact_types:
	cur = ContactType(contact_type = c)
	db.session.add(cur)

for r in relationships:
	cur = Relationship(relationship = r)
	db.session.add(cur)

for s in service_types:
	cur = ServiceType(name = s[0], units = s[1])
	db.session.add(cur)

for p in programs:
	cur = Program(name = p)
	db.session.add(cur)

for a in assess_types:
	cur = AssessmentType(assess_type = a)
	db.session.add(cur)

for hs in housing_statuses:
	cur = HousingStatus(status = hs)
	db.session.add(cur)


db.session.commit()