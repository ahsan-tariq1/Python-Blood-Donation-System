from flask import Flask, render_template, redirect, request, g, session, url_for
from DBHandler import AccountInfo,DonorBlood,DonorLocation,PeopleInfo,RequestBlood,RequestLocation
import os, smtplib

app = Flask(__name__)

app.secret_key='A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

account_info = AccountInfo()
donor_blood = DonorBlood()
donor_location = DonorLocation()
people_info = PeopleInfo()
request_blood = RequestBlood()
request_location = RequestLocation()


adminEmail = []
@app.route('/')
def index():
    return redirect(url_for('ind'))


@app.route('/BDMS')
def ind():
    if 'email' in session:
        email = session['email']
        return render_template('index.html', loggedin='true', email=email)
    return render_template('index.html')


@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=='POST':
        email=request.form['email']
        checkEmail=account_info.checkEmail(email)
        if checkEmail:
            return render_template('Donor-sign-up.html', email_check='true')
        else:
            email_passwd = os.getenv('Password')
            with smtplib.SMTP('smtp.gmail.com',587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login('mohsintariq132@gmail.com',email_passwd)
                subject = "BDMS Email Conformation"
                body = " Welcome To BDMS\n\n"
                body1 = " Link to Registration: http://127.0.0.1:5000/confirmed-signup\n\n\n\n\n\n\nRegards:BDMS Team"
                msg = f'Subject: {subject}\n\n{body} {body1}'
                smtp.sendmail('mohsintariq132@gmail.com',email,msg)
            return render_template('Donor-sign-up.html',email_check='false')
    return render_template('Donor-sign-up.html',email_check='get')

@app.route('/confirmed-signup',methods=['POST','GET'])
def confirmed_signup():
    try:
        if request.method=='POST':
            fname = request.form['first-name']
            lname = request.form['last-name']
            gender = request.form['Gender']
            birthdate = request.form['birthdate']
            phoneNo = request.form['phone-number']
            email = request.form['email']
            country = request.form['country']
            bloodGroup = request.form['blood-group']
            province = request.form['province']
            city = request.form['city']
            password = request.form['password']
            checkEmail=account_info.checkEmail(email)
            if checkEmail:
                return render_template('confirmed-signup.html',email_check='true')
            else:
                account_check=account_info.register(fname,lname,gender,birthdate,phoneNo,email,password)
                donor_bd_check=donor_blood.register(bloodGroup,email)
                donor_loca_check=donor_location.register(country.upper(),province.upper(),city.upper(),email)
                if account_check and donor_bd_check and donor_loca_check:
                    email_passwd = os.getenv('Password')
                    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                        smtp.ehlo()
                        smtp.starttls()
                        smtp.ehlo()
                        smtp.login('mohsintariq132@gmail.com', email_passwd)
                        subject = 'BDMS registration Successful'
                        body = " You are registered Successfully\n" \
                               "Note:Your default status is True(Means you can give blood)" \
                               "You can change it by signing in to your account accordingly" \
                               "\n\n\n\n\n\nRegards:BDMS Team"
                        msg = f'Subject: {subject}\n\n{body}'
                        smtp.sendmail('mohsintariq132@gmail.com', email, msg)
                    return redirect(url_for('signin'))
                else:
                    return redirect(url_for('failure'))
        return render_template("confirmed-signup.html")

    except Exception as e:
        print(e)
        error = str(e)
        return render_template('failure.html', error=error)



@app.before_request
def before_request():
    g.email=None
    if 'email' in session:
        g.email=session['email']


@app.route('/signin',methods=['POST','GET'])
def signin():
    try:
        if request.method=='POST':
            session.pop('email',None)
            session.pop('password',None)
            user_email = request.form['email']
            user_password = request.form['password']
            done=account_info.checksignin(user_email,user_password)
            if done:
                session['email'] = user_email
                session['password']=user_password
                return redirect(url_for('loggedin'))
            else:
                return render_template('signin.html',error = "invalid email or password")

    except Exception as e:
        print(e)
        error = str(e)
        return redirect(url_for('failure'))
    if g.email:
        return redirect(url_for('loggedin'))
    return render_template('signin.html')

@app.route('/my-account', methods=['GET'])
def loggedin():
    if g.email:
        email = session['email']
        if email == 'no.reply.bdms@gmail.com':
            return redirect(url_for('admin'))
        return render_template('my-account.html', email=email)
    else:
        return redirect(url_for('signin'))


@app.route('/admin-portal',methods=['GET'])
def admin():
    if g.email:
        email = session['email']
        if email == 'no.reply.bdms@gmail.com':
            rows=account_info.getRecords_Admin()
            return render_template('admin-portal.html', records = True , update=True, donors=rows, email=email)
        else:
            session.pop('email', None)
            session['email'] = 'no.reply.bdms@gmail.com'
            return redirect(url_for('loggedin'))
    else:
        return redirect(url_for('signin'))

@app.route('/adminUpdate',methods=['POST','GET'])
def adminupdate():
    if request.method=='POST':
        email_del_update = request.form['email']
        if email_del_update=='Choose email...':
            return redirect(url_for('admin'))
        session.pop('email', None)
        session['email'] = email_del_update
        if request.form.get('adminMani') == 'manipulate':
            adminEmail.insert(0,"no.reply.bdms@gmail.com")
            return redirect(url_for('updateData'))
        if request.form.get('adminDelete') == 'delete':
            return redirect(url_for('deleteRecord'))


@app.route('/delete-record',methods=['GET','POST'])
def deleteRecord():
    if request.method=='GET':
        email = session['email']
        if email == 'no.reply.bdms@gmail.com':
            session.pop('email', None)
            session['email'] = 'no.reply.bdms@gmail.com'
            return redirect(url_for('admin'))
        else:
            done=account_info.delete(email)
            if done:
                session.pop('email', None)
                session['email'] = 'no.reply.bdms@gmail.com'
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('failure'))

@app.route('/failure')
def failure():
    return render_template('failure.html')

@app.route('/dropsession')
def drop_session():
    session.pop('email', None)
    session.pop('password',None)
    return redirect(url_for('signin'))


@app.route('/requestblood', methods=['POST','GET'])
def requestblood():
    try:
        if request.method == 'POST':
            firstname = request.form['first-name']
            lastname = request.form['last-name']
            phoneNo = request.form['phone-number']
            bloodGroup = request.form['blood-group']
            hospital = request.form['hospital-address']
            country = request.form['country']
            province=request.form['province']
            city = request.form['city']
            people_check=people_info.register(firstname,lastname,phoneNo)
            request_check=request_blood.register(bloodGroup,hospital,phoneNo)
            location_check=request_location.register(country,province,city,phoneNo)
            data=donor_blood.checkrequestblood(bloodGroup, country.upper(),province.upper(),city.upper())
            if data and people_check and request_check and location_check:
                email_passwd = os.getenv('Password')
                with smtplib.SMTP('mymailserver.com', 465) as smtp:
                    smtp.starttls()
                    smtp.login('mohsintariq132@gmail.com', email_passwd)
                    subject = bloodGroup + " Blood Required!"
                    body0= 'Blood Request Information.'
                    body = "Name:" + firstname + " " + lastname + "\nPhone No:" + phoneNo + \
                           "\nHospital Address:" + hospital +\
                           "\nBlood Group:" + bloodGroup + "\nCountry:" + country +\
                           "\nProvince:" + province + "\nCity:" + city
                    body1 = "\n\n\n\nNOTE!Save life, be a Hero!\n\n\n\nRegards:BDMS Team"
                    msg = f'Subject: {subject}\n\n{body0}\n {body} {body1}'
                    for i in range(0, data[1]):
                        smtp.sendmail('mohsintariq132@gmail.com', data[0][i][0], msg)
                return render_template('I-need-Blood.html', requestSuccess='requestSuccess')
            else:
                return render_template('I-need-Blood.html', requestFailure='requestFailure')

    except Exception as e:
        print(e)
        error = str(e)
        return render_template('failure.html', error=error)
    return render_template('I-need-Blood.html')



@app.route('/update', methods=['POST','GET'])
def updateData():
    try:
        if request.method == 'POST':
            if g.email:
                email = session['email']
                data_update = request.form['new_info']
                data_check = request.form['check']
                if data_check == 'phoneNo':
                    count=0
                    for i in data_update:
                        count=count+1
                    if count>11 or count<11 or int(data_update)<int('03000000000') or int(data_update)>int('03499999999'):
                        return render_template('update.html',phoneFailure='phoneFailure',email=email)

                if data_check == 'country' or data_check == 'city' or data_check=='province':
                    data_update=data_update.upper()
                    done1=donor_location.updateSuccess(email, data_update, data_check)
                    if (done1):
                        aEmailCheck = []
                        aEmailCheck.insert(0, "no.reply.bdms@gmail.com")
                        if adminEmail == aEmailCheck:
                            aEmailCheck.pop(0)
                            adminEmail.pop(0)
                            return redirect(url_for('admin'))
                        return redirect(url_for('showdata'))
                    else:
                        return render_template('update.html',cannotUpdate='cannotUpdate',email=email)
                if data_check == 'phoneNo':
                    done=account_info.updateSuccess(email, data_update, data_check)
                    if (done):
                        aEmailCheck = []
                        aEmailCheck.insert(0, "no.reply.bdms@gmail.com")
                        if adminEmail == aEmailCheck:
                            aEmailCheck.pop(0)
                            adminEmail.pop(0)
                            return redirect(url_for('admin'))
                        return redirect(url_for('showdata'))
                    else:
                        return render_template('update.html',cannotUpdate='cannotUpdate',email=email)
    except Exception as e:
        print(e)
        error = str(e)
        return render_template('failure.html', error=error)
    adminEmailCheck=[]
    adminEmailCheck.insert(0,"no.reply.bdms@gmail.com")
    if adminEmail == adminEmailCheck:
        adminEmailCheck.pop(0)
        user_email=adminEmail[0]
        return render_template('update.html', email=user_email,updateadmin=True)
    user_email = session['email']
    return render_template('update.html',email = user_email,updateuser=True)


@app.route('/updatePassword',methods=['POST','GET'])
def updatePassword():
    try:
        if request.method=='POST':
            email=session['email']
            previous_password=session['password']
            check_password=request.form['pre-password']
            if previous_password!=check_password:
                return render_template('update.html', pre_password='pre_password',email=email)
            else:
                new_password = request.form['password']
                done=account_info.updateSuccess(email, new_password, 'password')
                if done:
                    return redirect(url_for('drop_session'))
                else:
                    return render_template('update.html', passwordFail='passwordFail',email=email)

    except Exception as e:
        print(e)
        error = str(e)
        return render_template('failure.html', error=error)


@app.route('/message')
def message():
    donorData = request.args.get('donorData', None)
    email = session['email']
    return render_template('donorData.html', donorData = donorData, email= email)


@app.route('/showDonorsData',methods=['POST','GET'])
def showdata():
    try:
        if request.method=='POST':
            email = session['email']
            donorData=account_info.showDonorsData(email)
            if (donorData):
                return redirect(url_for('message', donorData=donorData))
            else:
                error = None
                return render_template('failure.html', error=error)
        else:
            email = session['email']
            donorData=account_info.showDonorsData(email)
            if (donorData):
                return redirect(url_for('message', donorData=donorData))
            else:
                error = None
                return render_template('failure.html', error=error)

    except Exception as e:
        print(e)
        error = str(e)
        return render_template('failure.html', error=error)


@app.route('/deleteDonorData',methods=['POST','GET'])
def delete():
    try:
        if g.email:
            email = session['email']
            done=account_info.delete(email)
            if (done):
                email_passwd = os.getenv('Password')
                with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                    smtp.starttls()
                    smtp.login('mohsintariq132@gmail.com', email_passwd)
                    subject = "Account Termination Successful"
                    body = "Your account has been terminated.\n\n\n\n\n\n\nRegards:BDMS Team"
                    msg = f'Subject: {subject}\n\n{body}'
                    smtp.sendmail('mohsintariq132@gmail.com', email, msg)
                session.pop('email',None)
                return redirect(url_for('signin'))

    except Exception as e:
        print(e)
        error = str(e)
        return render_template('failure.html', error=error)

@app.route('/status',methods=['POST','GET'])
def statusUpdate():
    try:
        if request.method=='POST':
            email=session['email']
            status=request.form['status']
            done=donor_location.statusUpdate(email,status)
            if done:
                return redirect(url_for('showdata'))
            else:
                return render_template('update.html',statusFailure='statusFailure',email=email)

    except Exception as e:
        error = str(e)
        return render_template('failure.html', error=error)


if __name__ == '__main__':
    app.run(debug=True)
