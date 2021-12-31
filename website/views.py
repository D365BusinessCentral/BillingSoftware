from datetime import date
from flask import Blueprint, render_template, request, flash, jsonify
from flask.helpers import url_for
from flask_login import login_required, current_user
from sqlalchemy.sql.functions import user
from werkzeug.utils import redirect
from .models import Employees, Note, Reference, ReportingPersons, Testtypes, Tests
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/References', methods=['GET', 'POST'])
@login_required
def references():
    page=request.args.get('page',1,type=int)
    reference=Reference.query.filter_by(CompanyID=current_user.id).paginate(page=page,per_page=7)
    return render_template("ReferenceList.html", user=current_user,ReferencesPerPage=reference)
    
@views.route('/Reporters', methods=['GET', 'POST'])
@login_required
def reporters():
    page=request.args.get('page',1,type=int)
    Reporters=ReportingPersons.query.filter_by(CompanyID=current_user.id).paginate(page=page,per_page=7)
    return render_template("ReportersList.html", user=current_user,Reporters=Reporters)

@views.route('/Tests', methods=['GET', 'POST'])
@login_required
def tests():
    page=request.args.get('page',1,type=int)
    testList=Tests.query.filter_by(CompanyID=current_user.id).paginate(page=page,per_page=7)
    return render_template("TestList.html", user=current_user,TestsList=testList)

@views.route('/Employees', methods=['GET', 'POST'])
@login_required
def employees():
    page=request.args.get('page',1,type=int)
    employeeList=Employees.query.filter_by(CompanyID=current_user.id).paginate(page=page,per_page=7)
    return render_template("EmployeeList.html", user=current_user,employeeList=employeeList)

@views.route('/AddReference', methods=['GET', 'POST'])
@login_required
def addReference():
    if request.method == 'POST':
        RefName = request.form.get('RefName')
        RefDegree = request.form.get('RefDegree')
        RefMobile = request.form.get('RefMobileNumber')
        RefSpeciality = request.form.get('RefSpeciality')
        VisitPRO = request.form.get('VisitPRO')
        RefAddress = request.form.get('RefAddress')
        RefLocality = request.form.get('RefLocality')
        
        if len(RefName) < 2:
            flash('Reference Name is too short!', category='error')
        elif len(RefMobile)>0 and len(RefMobile)<10:
            flash('Mobile Number must be 10 digits.', category='error')
        else:
            new_Ref = Reference(Name=RefName, Degree=RefDegree,MobileNumber=RefMobile,Speciality=RefSpeciality,VisitPRO=VisitPRO,Address=RefAddress,Locality=RefLocality,CompanyID=current_user.id)
            db.session.add(new_Ref)
            db.session.commit()
            flash('Reference added!', category='success')
            return redirect(url_for('views.references',page=1))
    return render_template("AddReference.html", user=current_user)    

@views.route('/AddReporters', methods=['GET', 'POST'])
@login_required
def addReporters():
    if request.method == 'POST':
        RepName = request.form.get('RepName')
        RepQualification = request.form.get('RepQualification')
        RepMobile = request.form.get('RepMobileNumber')
        RepSpeciality = request.form.get('RepSpeciality')
        RepAddress = request.form.get('RepAddress')
        RepLocality = request.form.get('RepLocality')
        
        if len(RepName) < 2:
            flash('Reporting Person Name is too short!', category='error')
        elif len(RepMobile)>0 and len(RepMobile)<10:
            flash('Mobile Number must be 10 digits.', category='error')
        else:
            new_Rep = ReportingPersons(Name=RepName, Qualifications=RepQualification,MobileNumber=RepMobile,Speciality=RepSpeciality,Address=RepAddress,Locality=RepLocality,CompanyID=current_user.id)
            db.session.add(new_Rep)
            db.session.commit()
            flash('Reference added!', category='success')
            return redirect(url_for('views.reporters',page=1))
    return render_template("AddReporters.html", user=current_user)   

@views.route('/UpdateReference/<int:Id>', methods=['GET', 'POST'])
@login_required
def updateReference(Id):
    reference = Reference.query.get_or_404(int(Id))
    if request.method == 'POST':
        RefName = request.form.get('RefName')
        reference.Degree = request.form.get('RefDegree')
        RefMobile = request.form.get('RefMobileNumber')
        reference.Speciality = request.form.get('RefSpeciality')
        reference.VisitPRO = request.form.get('VisitPRO')
        reference.Address = request.form.get('RefAddress')
        reference.Locality = request.form.get('RefLocality')
        
        if len(RefName) < 2:
            flash('Reference Name is too short!', category='error')
        elif len(RefMobile)>0 and len(RefMobile)<10:
            flash('Mobile Number must be 10 digits.', category='error')
        else:
            reference.Name = RefName
            reference.MobileNumber = RefMobile
            try:
                db.session.commit()
                flash('Reference updated!', category='success')
                return redirect(url_for('views.references',page=1))
            except:
                flash('Something went wrong while updating Reference!', category='error')
    return render_template("UpdateReference.html", user=current_user,reference=reference)  

@views.route('/UpdateReporter/<int:Id>', methods=['GET', 'POST'])
@login_required
def updateReporter(Id):
    reporter = ReportingPersons.query.get_or_404(int(Id))
    if request.method == 'POST':
        RepName = request.form.get('RepName')
        reporter.Qualifications = request.form.get('RepQualification')
        RepMobile = request.form.get('RepMobileNumber')
        reporter.Speciality = request.form.get('RepSpeciality')
        reporter.Address = request.form.get('RepAddress')
        reporter.Locality = request.form.get('RepLocality')
        
        if len(RepName) < 2:
            flash('Reporting Person Name is too short!', category='error')
        elif len(RepMobile)>0 and len(RepMobile)<10:
            flash('Mobile Number must be 10 digits.', category='error')
        else:
            reporter.Name = RepName
            reporter.MobileNumber = RepMobile
            try:
                db.session.commit()
                flash('Reference updated!', category='success')
                return redirect(url_for('views.reporters',page=1))
            except:
                flash('Something went wrong while updating Reporting Person!', category='error')
    return render_template("UpdateReporter.html", user=current_user,reporter=reporter) 

@views.route('/UpdateTest/<int:Id>', methods=['GET', 'POST'])
@login_required
def updateTest(Id):
    Test = Tests.query.get_or_404(int(Id))
    if request.method == 'POST':
        TestName = request.form.get('TestName')
        TestTypeId = request.form.get('TestType')
        TestAmount = request.form.get('TestAmount')
        DCPAmount = request.form.get('DCPAmount')
        ACPAmount = request.form.get('ACPAmount')
        ReportingAmount = request.form.get('ReportingAmount')
        FilmQuantity = request.form.get('FilmQuantity')
        Contrast = request.form.get('Contrast')
        
        if len(TestName) < 2:
            flash('Test Name is too short!', category='error')
        elif len(TestTypeId)<1:
            flash('You must select a test type.', category='error')
        elif len(TestAmount)<1:
            flash('You must enter Test Amount.', category='error')
        elif len(DCPAmount)<1:
            flash('You must enter DCP Amount.', category='error')
        elif len(ReportingAmount)<1:
            flash('You must enter Reporting Amount.', category='error')
        elif len(FilmQuantity)<1:
            flash('You must enter Film Quantity.', category='error')
        else:
            testType = Testtypes.query.get_or_404(int(TestTypeId))
            if testType:
                testTypeName=testType.Name
            else:
               flash('Please select a valid Test Type.', category='error')
            Net_Amount=float(TestAmount)-float(DCPAmount)-float(ACPAmount)-float(ReportingAmount)
            Test.Name=TestName
            Test.Test_Type_Id=TestTypeId
            Test.Test_Type_Name=testTypeName
            Test.Fee_Amount=TestAmount
            Test.DCP_Amount=DCPAmount
            Test.ACP_Amount=ACPAmount
            Test.Reporting_Amount=ReportingAmount
            Test.Net_Amount=Net_Amount
            Test.Film_Quantity=FilmQuantity
            Test.Contrast=Contrast
            try:
                db.session.commit()
                flash('Test details updated!', category='success')
                return redirect(url_for('views.tests',page=1))
            except:
                flash('Something went wrong while updating test!', category='error')
    return render_template("UpdateTest.html", user=current_user,TestData=Test)    

@views.route('/TestTypes', methods=['GET', 'POST'])
@login_required
def testTypes():
    if request.method == 'POST':
        testTypeName = request.form.get('testTypeName')

        if len(testTypeName) < 2:
            flash('Test Type Name is too short!', category='error')
        else:
            newTestType = Testtypes(Name=testTypeName, CompanyID=current_user.id)
            db.session.add(newTestType)
            db.session.commit()
            flash('Test Type added!', category='success')

    return render_template("TestTypes.html", user=current_user)


@views.route('/AddTest', methods=['GET', 'POST'])
@login_required
def addTest():
    if request.method == 'POST':
        TestName = request.form.get('TestName')
        TestTypeId = request.form.get('TestType')
        TestAmount = request.form.get('TestAmount')
        DCPAmount = request.form.get('DCPAmount')
        ACPAmount = request.form.get('ACPAmount')
        ReportingAmount = request.form.get('ReportingAmount')
        FilmQuantity = request.form.get('FilmQuantity')
        Contrast = request.form.get('Contrast')
        
        if len(TestName) < 2:
            flash('Test Name is too short!', category='error')
        elif len(TestTypeId)<1:
            flash('You must select a test type.', category='error')
        elif len(TestAmount)<1:
            flash('You must enter Test Amount.', category='error')
        elif len(DCPAmount)<1:
            flash('You must enter DCP Amount.', category='error')
        elif len(ReportingAmount)<1:
            flash('You must enter Reporting Amount.', category='error')
        elif len(FilmQuantity)<1:
            flash('You must enter Film Quantity.', category='error')
        else:
            testType = Testtypes.query.get_or_404(int(TestTypeId))
            if testType:
                testTypeName=testType.Name
            else:
               flash('Please select a valid Test Type.', category='error')
            Net_Amount=float(TestAmount)-float(DCPAmount)-float(ACPAmount)-float(ReportingAmount)
            new_Test = Tests(Name=TestName, Test_Type_Id=TestTypeId,Test_Type_Name=testTypeName,Fee_Amount=TestAmount,DCP_Amount=DCPAmount,ACP_Amount=ACPAmount,Reporting_Amount=ReportingAmount,Net_Amount=Net_Amount,Film_Quantity=FilmQuantity,Contrast=Contrast,CompanyID=current_user.id)
            try:
                db.session.add(new_Test)
                db.session.commit()
                flash('Test added!', category='success')
                return redirect(url_for('views.tests',page=1))
            except:
                flash('Something went wrong while adding test!', category='error')
    return render_template("AddTest.html", user=current_user)    

@views.route('/AddEmployee', methods=['GET', 'POST'])
@login_required
def addEmployee():
    if request.method == 'POST':
        Name = request.form.get('EmpName')
        email = request.form.get('EmpEmail')
        mobile_number = request.form.get('EmpMobile')
        isActiveStatus = request.form.get('IsActive')
        Designation = request.form.get('EmpDesignation')
        Location = request.form.get('EmpLocation')
        PAN_Number = request.form.get('EmpPAN')
        UIDAI_Number = request.form.get('EmpUIDAI')
        DOJoining = request.form.get('DOJ')
        DOResign = request.form.get('DOR')
        WagesPerMonth = request.form.get('EmpWages')
        DailyAllowance = request.form.get('EmpDA')
        
        if len(Name) < 2:
            flash('Employee Name is too short!', category='error')
        elif len(Designation)<1:
            flash('You must enter employee\'s designation.', category='error')
        elif len(DOJoining)<1:
            flash('You must select employee\'s Date of Joining.', category='error')
        elif len(WagesPerMonth)<1:
            flash('You must enter employee\'s wages per month.', category='error')            
        elif isActiveStatus=="1" and len(DOResign)<1:
            flash('You must select employee\'s Date of Resignation.', category='error')
        else:
            if isActiveStatus=="0":
                isActive=True
            else:
                isActive=False
            if DailyAllowance=="":
                DailyAllowance=0
            new_Emp = Employees(Name=Name, email=email,mobile_number=mobile_number,isActive=isActive,Designation=Designation,Location=Location,PAN_Number=PAN_Number,UIDAI_Number=UIDAI_Number,DOJ=DOJoining,DOR=DOResign,WagesPerMonth=float(WagesPerMonth),DailyAllowance=float(DailyAllowance),CompanyID=current_user.id)
            try:
                db.session.add(new_Emp)
                db.session.commit()
                flash('Employee added!', category='success')
                return redirect(url_for('views.employees',page=1))
            except:
                flash('Something went wrong while adding employee!', category='error')
    return render_template("AddEmployee.html", user=current_user)  

@views.route('/UpdateEmployee/<int:Id>', methods=['GET', 'POST'])
@login_required
def updateEmployee(Id):
    employee = Employees.query.get_or_404(int(Id))
    if request.method == 'POST':
        Name = request.form.get('EmpName')
        employee.email = request.form.get('EmpEmail')
        employee.mobile_number = request.form.get('EmpMobile')
        isActiveStatus = request.form.get('IsActive')
        Designation = request.form.get('EmpDesignation')
        employee.Location = request.form.get('EmpLocation')
        employee.PAN_Number = request.form.get('EmpPAN')
        employee.UIDAI_Number = request.form.get('EmpUIDAI')
        DOJ = request.form.get('DOJ')
        DOR = request.form.get('DOR')
        WagesPerMonth = request.form.get('EmpWages')
        employee.DailyAllowance = float(request.form.get('EmpDA'))
        
        if len(Name) < 2:
            flash('Employee Name is too short!', category='error')
        elif len(Designation)<1:
            flash('You must enter employee\'s designation.', category='error')
        elif len(DOJ)<1:
            flash('You must select employee\'s Date of Joining.', category='error')
        elif len(WagesPerMonth)<1:
            flash('You must enter employee\'s wages per month.', category='error')
        elif isActiveStatus=="1" and len(DOR)<1:
            flash('You must select employee\'s Date of Resignation.', category='error')
        else:
            if isActiveStatus=="0":
                employee.isActive=True
            else:
                employee.isActive=False
 
            employee.Name=Name
            employee.Designation=Designation
            employee.WagesPerMonth=float(WagesPerMonth)
            employee.DOJ=DOJ
            employee.DOR=DOR
            try:
                db.session.commit()
                flash('Employee details updated!', category='success')
                return redirect(url_for('views.employees',page=1))
            except:
                flash('Something went wrong while updating Employee!', category='error')
    return render_template("UpdateEmployee.html", user=current_user,employee=employee)    

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/delete-reference', methods=['POST'])
def delete_reference():
    reference = json.loads(request.data)
    referenceId = reference['referenceId']
    reference = Reference.query.get(referenceId)
    if reference:
        if reference.CompanyID == current_user.id:
            db.session.delete(reference)
            db.session.commit()

    return jsonify({})

@views.route('/delete-testType', methods=['POST'])
def delete_testType():
    testType = json.loads(request.data)
    testTypeId = testType['testTypeId']
    tests = Tests.query.filter_by(Test_Type_Id=testTypeId,CompanyID=current_user.id).first()
    if tests:
        flash('This Test Type is linked with one or more Tests. You cannot delete this.', category='error')
    else:
        testType = Testtypes.query.get(testTypeId)
        if testType:
            if testType.CompanyID == current_user.id:
                db.session.delete(testType)
                db.session.commit()

    return jsonify({})    

@views.route('/delete-test', methods=['POST'])
def delete_test():
    test = json.loads(request.data)
    testId = test['testId']
    tests = Tests.query.get(testId)
    if tests:
        if tests.CompanyID == current_user.id:
            db.session.delete(tests)
            db.session.commit()

    return jsonify({})  

@views.route('/delete-reporter', methods=['POST'])
def delete_reporter():
    reporter = json.loads(request.data)
    reporterId = reporter['reporterId']
    reporter = ReportingPersons.query.get(reporterId)
    if reporter:
        if reporter.CompanyID == current_user.id:
            db.session.delete(reporter)
            db.session.commit()

    return jsonify({})  

@views.route('/delete-employee', methods=['POST'])
def delete_employees():
    employee = json.loads(request.data)
    empId = employee['empId']
    employee = Employees.query.get(empId)
    if employee:
        if employee.CompanyID == current_user.id:
            db.session.delete(employee)
            db.session.commit()

    return jsonify({})    

