import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import request, render_template

from project import app
from project.com.controller.LoginController import adminLoginSession
from project.com.dao.LoginDAO import LoginDAO
from project.com.dao.RegisterDAO import RegisterDAO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.RegisterVO import RegisterVO


@app.route('/user/loadRegister', methods=['GET'])
def UserRegister():
    try:
        return render_template('user/register.html')
    except Exception as ex:
        print(ex)


@app.route('/user/insertRegister', methods=['POST'])
def userInsertRegister():
    try:
        loginVO = LoginVO()
        loginDAO = LoginDAO()
        registerVO = RegisterVO()
        registerDAO = RegisterDAO()


        loginUsername = request.form["loginUsername"]
        loginVOList = loginDAO.findUser(loginUsername)
        print("check-----",loginVOList)
        loginDictList = [i.as_dict() for i in loginVOList]

        print(loginDictList)
        lenLoginDictList = len(loginDictList)
        if lenLoginDictList != 0:
            msg = "This Username Already Exist."
            return render_template('user/register.html', error=msg)

        else:
            loginPassword = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))

            registerFirstName = request.form['registerFirstName']
            registerLastName = request.form['registerLastName']
            registerMobileNumber = request.form['registerMobileNumber']
            registerGender = request.form['registerGender']

            print("loginPassword=" + loginPassword)

            sender = "aimfs.health@gmail.com"

            receiver = loginUsername

            msg = MIMEMultipart()

            msg['From'] = sender

            msg['To'] = receiver

            msg['Subject'] = "YOUR AGRI-PEDIA PASSWORD"

            msg.attach(MIMEText("Welcome To AGRI-PEDIA Family. ------------------ "
                                + registerFirstName + " " + registerLastName + "\n \n ", 'plain'))

            msg.attach(MIMEText("Your Username is " + loginUsername + "\n", 'plain'))

            msg.attach(MIMEText("Your Password is " + loginPassword + "\n \n \n ", 'plain'))

            msg.attach(
                MIMEText("Please Login to Website. Enter Username & Password And enjoy AGRI-PEDIA \n \n \n \n",
                         'plain'))

            msg.attach(MIMEText(" ~ ADMIN AGRI-PEDIA"))

            server = smtplib.SMTP('smtp.gmail.com', 587)

            server.starttls()

            server.login(sender, "aimfs@12345")

            text = msg.as_string()

            server.sendmail(sender, receiver, text)

            loginVO.loginUsername = loginUsername
            loginVO.loginPassword = loginPassword
            loginVO.loginRole = "user"
            loginVO.loginStatus = "active"

            loginDAO.insertLogin(loginVO)

            registerVO.registerFirstName = registerFirstName
            registerVO.registerLastName = registerLastName
            registerVO.registerMobileNumber = registerMobileNumber
            registerVO.registerGender = registerGender
            registerVO.register_LoginId = loginVO.loginId

            registerDAO.insertRegister(registerVO)

            server.quit()

            return render_template("admin/Login.html")





    except Exception as ex:
        print(ex)


@app.route('/admin/viewUser', methods=['GET'])
def adminViewUser():
    try:
        if adminLoginSession() == 'admin':
            registerDAO = RegisterDAO()
            registerVOList = registerDAO.viewUser()
            print(registerVOList)
            return render_template('admin/viewUser.html', registerVOList=registerVOList)
    except Exception as ex:
        print(ex)
