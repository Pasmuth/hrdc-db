# HRDC Database

This is my project to create an alternative to CaseWorthy. I'm going to use Python Flask to build the forms and interface logic, and SQLAlchemy to build the database logic.

<<<<<<< HEAD
## Current Branch Projects

This branch is to merge into before merging into master

||||||| merged common ancestors
## Current Branch Projects

- Add outcome matrix functionality
  - Domains
  - Scores at time

=======
>>>>>>> jatesting
## Current Version: 0.3

The current 'stable' version has a few core features:


- Check-in Kiosk
  - Customers enter information to a Google Form on a laptop/iPad in the lobby
  - Google Form information is piped into the database
- Clients
  - Create and update
  - Search
  - Add contact information
  - Add relationships between clients
  - Add address informatoin
- Services
  - Create programs and service types
  - Add services to a client
- Assessments
  - Outcome Matrix
- Users
  - Manage user logins and password hashing


## Version 0.5 Goals

- Clients
  - All CRUD operations
- Services
  - All CRUD operations
  - Limit service types by program
    - e.g. only the warming center has the service type "emergency shelter"
- Users
  - Manage user roles (i.e. admin/regular)


## Version 1.0 Goals

- Generate CSBG All Characteristics report
  - Collect all relavent information about clients
- Generate other reports, similar to current CaseWorthy capabilities 
