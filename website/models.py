from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('companies.id'))


class Companies(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    company_name = db.Column(db.String(150))
    mobile_number = db.Column(db.Integer())
    createdOn = db.Column(db.DateTime(timezone=True), default=func.now())
    References = db.relationship('Reference')
    notes = db.relationship('Note')
    Test_Types = db.relationship('Testtypes')
    Tests = db.relationship('Tests')
    Invoices = db.relationship('Invoices')
    ReportingPersons = db.relationship('ReportingPersons')
    Employees = db.relationship('Employees')

class Reference(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    Name = db.Column(db.String(150))
    Degree = db.Column(db.String(50))
    MobileNumber = db.Column(db.Integer)
    Speciality = db.Column(db.String(50))
    VisitPRO = db.Column(db.String(50))
    Address = db.Column(db.String(250))
    Locality = db.Column(db.String(50))
    CreatedOn = db.Column(db.DateTime(timezone=True), default=func.now())
    CompanyID = db.Column(db.Integer, db.ForeignKey('companies.id')) 

class Testtypes(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    Name = db.Column(db.String(50))
    CreatedOn = db.Column(db.DateTime(timezone=True), default=func.now())
    CompanyID = db.Column(db.Integer, db.ForeignKey('companies.id')) 
    Tests = db.relationship('Tests')    
    Invoices = db.relationship('Invoices')

class Tests(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    Test_Type_Id = db.Column(db.Integer, db.ForeignKey('testtypes.id'))
    Test_Type_Name = db.Column(db.String(50))
    Name = db.Column(db.String(80))
    Fee_Amount = db.Column(db.Numeric(10,2))
    DCP_Amount = db.Column(db.Numeric(10,2))
    ACP_Amount = db.Column(db.Numeric(10,2))
    Reporting_Amount = db.Column(db.Numeric(10,2))
    Net_Amount = db.Column(db.Numeric(10,2))
    Film_Quantity = db.Column(db.Integer)
    Contrast = db.Column(db.Integer)
    CreatedOn = db.Column(db.DateTime(timezone=True), default=func.now())
    CompanyID = db.Column(db.Integer, db.ForeignKey('companies.id')) 

class ReportingPersons(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    Name = db.Column(db.String(80))
    MobileNumber = db.Column(db.Integer)
    Qualifications = db.Column(db.String(50))
    Speciality = db.Column(db.String(50))
    Address = db.Column(db.String(150))
    Locality = db.Column(db.String(50))
    CreatedOn = db.Column(db.DateTime(timezone=True), default=func.now())
    CompanyID = db.Column(db.Integer, db.ForeignKey('companies.id'))     

class Invoices(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    PatientName = db.Column(db.String(100))
    PatientAddress = db.Column(db.String(100))
    PatientMobile = db.Column(db.Integer)
    Test_Type_Id = db.Column(db.Integer, db.ForeignKey('testtypes.id'))
    Test_Type_Name = db.Column(db.String(50))
    Test_Id = db.Column(db.Integer, db.ForeignKey('tests.id'))
    Test_Name = db.Column(db.String(80))
    Fee_Amount = db.Column(db.Numeric(10,2))
    DCP_Amount = db.Column(db.Numeric(10,2))
    ACP_Amount = db.Column(db.Numeric(10,2))
    Additional_Amount = db.Column(db.Numeric(10,2))
    Net_Amount = db.Column(db.Numeric(10,2))
    Film_Quantity = db.Column(db.Integer)
    Contrast = db.Column(db.Integer)
    Remarks = db.Column(db.String(250))
    CreatedOn = db.Column(db.DateTime(timezone=True), default=func.now())
    CompanyID = db.Column(db.Integer, db.ForeignKey('companies.id'))    

class Employees(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    Name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    mobile_number = db.Column(db.Integer())
    isActive = db.Column(db.Boolean)
    Designation = db.Column(db.String(50))
    Location = db.Column(db.String(50))
    PAN_Number = db.Column(db.String(15))
    UIDAI_Number = db.Column(db.String(20))
    DOJ = db.Column(db.String(20))
    DOR = db.Column(db.String(20))
    WagesPerMonth = db.Column(db.Numeric(10,2))
    DailyAllowance  =   db.Column(db.Numeric(10,2))
    createdOn = db.Column(db.DateTime(timezone=True), default=func.now())
    CompanyID = db.Column(db.Integer, db.ForeignKey('companies.id')) 

class Incentives(db.Model):
    Employee_Id = db.Column(db.Integer,db.ForeignKey('employees.id'),primary_key=True)
    Test_Type_Id = db.Column(db.Integer,db.ForeignKey('testtypes.id'),primary_key=True)
    Number_Of_cases = db.Column(db.Integer,primary_key=True)
    Incentive_Amount = db.Column(db.Numeric(10,2))
    createdOn = db.Column(db.DateTime(timezone=True), default=func.now())
    CompanyID = db.Column(db.Integer, db.ForeignKey('companies.id'))

