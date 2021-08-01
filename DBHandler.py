import pymysql, os
DATABASE_IP = os.getenv("DATABASE_IP")
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DATABASE = os.getenv('DATABASE')


class AccountInfo:

    def register(self, fname, lname, gender, birthdate, phoneNo, email,password):
        db=None
        insert=False
        try:
            db=pymysql.connect(host=DATABASE_IP, port=3310, user=DB_USER, password=DB_PASSWORD, database=DATABASE)
            cur=db.cursor()
            sql = 'INSERT INTO account_info (fname,lname,gender,birthDate,phoneNo,email,password)' \
                  ' VALUES (%s,%s,%s,%s,%s,%s,%s)'
            args = (fname, lname, gender, birthdate, phoneNo, email,password)
            done=cur.execute(sql, args)
            if done:
                insert = True

        except Exception as e:
            print(e)
            print("some error")
        finally:
            if(db!=None):
                db.commit()
        return insert

    def checkEmail(self,email):
        db=None
        check=False
        try:
            db=pymysql.connect(host=DATABASE_IP,port=3310,user=DB_USER,password=DB_PASSWORD,database=DATABASE)
            cur=db.cursor()
            sql = 'Select email from account_info'
            value = cur.execute(sql)
            check_email = cur.fetchall()
            for i in range(0, value):
                if email == check_email[i][0]:
                    check=True
        except Exception as e:
            print(e)
            print("some error")
        finally:
            if db != None:
                db.commit()
        return check

    def checksignin(self,email,password):
        db=None
        check=False
        try:
            db=pymysql.connect(host=DATABASE_IP,port=3310,user=DB_USER,password=DB_PASSWORD,database=DATABASE)
            cur=db.cursor()
            sql = 'Select password from account_info where email=%s'
            args = email
            done=cur.execute(sql, args)
            tuple=cur.fetchone()
            password1=tuple[0]
            if done:
                if(password==password1):
                    check=True
        except Exception as e:
            print(e)
            print("some error")
        finally:
            if db != None:
                db.commit()
        return check

    def updateSuccess(self, email, data_update, data_check):
        db= None
        insert=False
        try:
            db = pymysql.connect(host=DATABASE_IP, port=3310, user=DB_USER, passwd=DB_PASSWORD, database=DATABASE)
            cur = db.cursor()
            if(data_check == 'phoneNo'):

                sql = 'Update account_info set phoneNo=%s where email=%s'
                args = (data_update,email)
                done = cur.execute(sql, args)
                if(done>0):
                    insert = True
            if (data_check == 'password'):
                sql = 'Update account_info set password=%s where email=%s'
                args = (data_update, email)
                done = cur.execute(sql, args)
                if(done>0):
                    insert = True
        except Exception as e:
            print(e)
            print("some error")
        finally:
            if (db != None):
                db.commit()
        return insert

    def delete(self,email):
        db = None
        insert=False
        try:
            db = pymysql.connect(host=DATABASE_IP, port=3310, user=DB_USER, passwd=DB_PASSWORD, database=DATABASE)
            cur = db.cursor()
            sql = 'delete from account_info where email=%s'
            args = email
            done=cur.execute(sql, args)
            if(done>0):
                insert = True
        except Exception as e:
            print(e)
            print("some error")
        finally:
            if (db != None):
                db.commit()
        return insert

    def showDonorsData(self,email):
        db = None
        try:
            db = pymysql.connect(host=DATABASE_IP, port=3310, user=DB_USER, password=DB_PASSWORD, database=DATABASE)
            cur = db.cursor()
            sql = 'Select fname,lname,birthDate,gender,phoneNo,email,bloodGroup,country,province,city,status ' \
                  'from account_info join donor_blood on donor_blood.AccountId = account_info.AccountId ' \
                  'join donor_location on donor_location.AccountId = account_info.AccountId where email=%s'
            args = email
            done=cur.execute(sql, args)
            if(done>0):
                row=cur.fetchall()
                print(row)
                donor = row[0][2]

                donorData=[row[0][0] +" " +row[0][1]+'&'+row[0][3]+'&'+ row[0][4]+'&'+ row[0][5]+'&'+ row[0][6]+'&'
                           + row[0][7]+'&'+ row[0][8]+'&'+ row[0][9]+'&'+ row[0][10]+'&'+donor.strftime('%m/%d/%Y')]
                return donorData

        except Exception as e:
            print(e)
            print("some error")
        finally:
            if(db!=None):
                db.commit()

    def getRecords_Admin(self):
        db = None
        try:
            db = pymysql.Connect(host=DATABASE_IP, port=3310, user=DB_USER, password=DB_PASSWORD, database=DATABASE)
            cur = db.cursor()
            sql = 'Select LocationId,fname,lname,birthDate,gender,phoneNo,email,' \
                  'bloodGroup,country,province,city,password,status ' \
                  'from account_info join donor_blood on donor_blood.AccountId = account_info.AccountId ' \
                  'join donor_location on donor_location.AccountId = account_info.AccountId'
            done = cur.execute(sql)
            if done > 0:
                data = cur.fetchall()
                return data
        except Exception as e:
            print(e)
        finally:
            if db != None:
                db.commit()


class DonorBlood:

    def register(self,bloodGroup,email):
        db=None
        insert=False
        try:

            db=pymysql.connect(host=DATABASE_IP, port=3310, user=DB_USER, password=DB_PASSWORD, database=DATABASE)
            cur=db.cursor()
            sql1= 'Select AccountId from account_info where email=%s'
            args1= (email)
            done1=cur.execute(sql1, args1)
            if done1:
                result=cur.fetchone()
                id=result[0]
                sql2 = 'INSERT INTO donor_blood (bloodGroup,AccountId) VALUES (%s,%s)'
                args2 = (bloodGroup,id)
                done2=cur.execute(sql2, args2)
                if done2:
                    insert = True

        except Exception as e:
            print(e)
            print("some error")
        finally:
            if(db!=None):
                db.commit()
        return insert

    def checkrequestblood(self,bloodGroup,country,province,city):
        db=None
        try:
            db=pymysql.connect(host=DATABASE_IP,port=3310,user=DB_USER,password=DB_PASSWORD,database=DATABASE)
            cur=db.cursor()
            status='True'
            sql = 'Select email from account_info join donor_location on donor_location.AccountId = account_info.AccountId ' \
                  'join donor_blood on donor_blood.AccountId = account_info.AccountId ' \
                  'where bloodGroup=%s and country=%s and province=%s and city=%s and status=%s'
            args = (bloodGroup,country,province,city,status)
            done=cur.execute(sql, args)
            if done:
                email = cur.fetchall()
                data=[email,done]
                return data
        except Exception as e:
            print(e)
            print("some error")
        finally:
            if db != None:
                db.commit()


class DonorLocation:

    def register(self,country,province,city,email):
        db=None
        insert=False
        try:
            db=pymysql.connect(host=DATABASE_IP, port=3310, user=DB_USER, password=DB_PASSWORD, database=DATABASE)
            cur=db.cursor()
            sql1= 'Select AccountId from account_info where email=%s'
            args1= (email)
            done1=cur.execute(sql1, args1)
            if done1:
                result=cur.fetchone()
                id=result[0]
                sql = 'INSERT INTO donor_location (country,province,city,AccountId) VALUES (%s,%s,%s,%s)'
                args = (country,province,city,id)
                done=cur.execute(sql, args)
                if done:
                    insert = True

        except Exception as e:
            print(e)
            print("some error")
        finally:
            if(db!=None):
                db.commit()
        return insert


    def statusUpdate(self,email,status):
        db=None
        insert=False
        try:
            db = pymysql.connect(host=DATABASE_IP, port=3310, user=DB_USER, password=DB_PASSWORD, database=DATABASE)
            cur = db.cursor()
            sql = 'Update donor_location join account_info on ' \
                  'donor_location.AccountId= account_info.AccountId set status=%s where email=%s'
            args = (status,email)
            done=cur.execute(sql, args)
            if done:
                insert = True
        except Exception as e:
            print(e)
            print("some error")
        finally:
            if db != None:
                db.commit()
        return insert

    def updateSuccess(self,email,data_update,data_check):
        db= None
        insert=False
        try:
            db = pymysql.connect(host=DATABASE_IP, port=3310, user=DB_USER, passwd=DB_PASSWORD, database=DATABASE)
            cur = db.cursor()
            if(data_check == 'country'):
                sql = 'Update donor_location join account_info on' \
                      ' donor_location.AccountId= account_info.AccountId set country=%s where email=%s'
                args = (data_update,email)
                done = cur.execute(sql, args)
                if(done>0):
                    insert = True
            if(data_check=='province'):
                sql = 'Update donor_location join account_info on' \
                      ' donor_location.AccountId= account_info.AccountId set province=%s where email=%s'

                args = (data_update,email)
                done = cur.execute(sql, args)
                if(done>0):
                    insert = True
            if(data_check=='city'):
                sql = 'Update donor_location join account_info on' \
                      ' donor_location.AccountId= account_info.AccountId set city=%s where email=%s'

                args = (data_update,email)
                done = cur.execute(sql, args)
                if(done>0):
                    insert = True

        except Exception as e:
            print(e)
            print("some error")
        finally:
            if (db != None):
                db.commit()
        return insert


class PeopleInfo:

    def register(self, fname, lname, phoneNo):
        db=None
        insert=False
        try:
            db=pymysql.connect(host=DATABASE_IP, port=3310, user=DB_USER, password=DB_PASSWORD, database=DATABASE)
            cur=db.cursor()
            sql = 'INSERT INTO people_info (fname ,lname, phoneNo) VALUES (%s,%s,%s)'
            args = (fname, lname,phoneNo)
            done=cur.execute(sql, args)
            if done:
                insert = True

        except Exception as e:
            print(e)
            print("some error")
        finally:
            if(db!=None):
                db.commit()
        return insert


class RequestBlood:

    def register(self, bloodGroup,hospitalAddress,phoneNo):
        db=None
        insert=False
        try:
            db=pymysql.connect(host=DATABASE_IP, port=3310, user=DB_USER, password=DB_PASSWORD, database=DATABASE)
            cur=db.cursor()
            sql1= 'Select PeopleId from people_info where phoneNo=%s'
            args1= (phoneNo)
            done1=cur.execute(sql1, args1)
            if done1:
                result=cur.fetchone()
                id=result[0]
                sql = 'INSERT INTO request_blood (bloodGroup,hospitalAddress,PeopleId)' \
                      ' VALUES (%s,%s,%s)'
                args = (bloodGroup,hospitalAddress,id)
                done=cur.execute(sql, args)
                if done:
                    insert = True

        except Exception as e:
            print(e)
            print("some error")
        finally:
            if(db!=None):
                db.commit()
        return insert


class RequestLocation:

    def register(self, country, province,city,phoneNo):
        db = None
        insert = False
        try:
            db = pymysql.connect(host=DATABASE_IP, port=3310, user=DB_USER, password=DB_PASSWORD, database=DATABASE)
            cur = db.cursor()
            sql1= 'Select PeopleId from people_info where phoneNo=%s'
            args1= (phoneNo)
            done1=cur.execute(sql1, args1)
            if done1:
                result=cur.fetchone()
                id=result[0]
                sql = 'INSERT INTO request_location (country, province,city,PeopleId) VALUES (%s,%s,%s,%s)'
                args = (country, province,city,id)
                done = cur.execute(sql, args)
                if done:
                    insert = True

        except Exception as e:
            print(e)
            print("some error")
        finally:
            if (db != None):
                db.commit()
        return insert




def Test():
    # db = DBHandler("localhost", "root", "1732544","project")
    ac = AccountInfo()
    db = DonorBlood()
    dl = DonorLocation()
    # pi=PeopleInfo()
    # rb=RequestBlood()
    # rl=RequestLocation()
    # print(DATABASE_IP)
    # print(DB_USER,DB_PASSWORD,DATABASE)
    # check=pi.register('mohsin','tariq','03244153398')
    # if check:
    #     print('ok1')
    # chec=rb.register('A+','Jinnah Hospital Lahore')
    # if chec:
    #     print('ok2')
    # che=rl.register('Pakistan','Punjab','Lahore')
    # if che:
    #     print('ok3')
    # mylist = db.showDonorsData("mohsintariq132@gmail.com")
    # for i in mylist:
    #     print(i)
    # che=ac.register('mohsin','tariq','male','1998-9-1','03244155398','mohsintariq132@gmail.com','1732544mO')
    # if che:
    #     print('ok1')
    # chec=db.register('A+','mohsintariq132@gmail.com')
    # if chec:
    #     print('ok2')
    # check=dl.register('Pakistan','Punjab','Lahore','mohsintariq132@gmail.com')
    # if check:
    #     print('ok3')
    #
    # chee=ac.register('mohsin','tariq','male','1998-9-1','03244155398','mohsintariq132@gmail.com','1732544mO')
    # if chee:
    #     print('ok1')
    # checc=db.register('A+')
    # if checc:
    #     print('ok2')
    # checkk=dl.register('Pakistan','Punjab','Lahore')
    # if checkk:
    #     print('ok3')
    # status=dl.statusUpdate('mohsintariq132@gmail.com','False')
    # if status:
    #     print("ok status")
    # check=ac.checkEmail('mohsintariq132@gmail.com')
    # if check:
    #     print('yes mail present')
    # passW=ac.checksignin('mohsintariq132@gmail.com','1732544mO')
    # if passW:
    #     print('password present')
    # bloodCheck=db.checkrequestblood('A+','Pakistan','Lahore')
    # if bloodCheck: CVB
    #     print(bloodCheck[1])
    # data = ac.getRecords_Admin()
    # if data:
    #     print(data)
    # dele=ac.delete('ahsantariq132@gmail.com')
    # if dele:
    #     print('deleted')

if __name__ == '__main__':
    Test()
