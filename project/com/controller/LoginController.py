from flask import redirect, url_for, session
from flask import render_template, request

from project import app
from project.com.dao.LoginDAO import LoginDAO
from project.com.vo.LoginVO import LoginVO


@app.route('/admin/login', methods=['GET', 'POST'])
def adminLoadLogin():
    try:
        session.clear()
        return render_template('admin/login.html')
    except Exception as ex:
        print(ex)


@app.route("/admin/validateLogin", methods=['POST'])
def adminValidateLogin():
    try:
        loginUsername = request.form['loginUsername']
        loginPassword = request.form['loginPassword']
        loginVO = LoginVO()
        loginDAO = LoginDAO()
        loginVO.loginUsername = loginUsername
        loginVO.loginPassword = loginPassword

        loginVOList = loginDAO.validateLogin(loginVO)
        loginDictList = [i.as_dict() for i in loginVOList]
        print(loginDictList)
        lenLoginDictList = len(loginDictList)
        if lenLoginDictList == 0:
            msg = 'Username Or Password is Incorrect !'
            return render_template('admin/login.html', error=msg)
        elif loginDictList[0]['loginStatus'] == 'unactive':
            msg = 'You are BLOCKED.'
            return render_template('admin/login.html', error=msg)
        else:
            for row1 in loginDictList:
                loginId = row1['loginId']
                loginUsername = row1['loginUsername']
                loginRole = row1['loginRole']
                session['session_loginId'] = loginId
                session['session_loginUsername'] = loginUsername
                session['session_loginRole'] = loginRole
                session.permanent = True
                if loginRole == 'admin':
                    return redirect(url_for('adminLoadDashboard'))
                elif loginRole == 'user':
                    return redirect(url_for('userLoadDashboard'))
    except Exception as ex:
        print(ex)


@app.route('/admin/loadDashboard', methods=['GET'])
def adminLoadDashboard():
    try:
        if adminLoginSession() == 'admin':
            return render_template('admin/index.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/loadDashboard', methods=['GET'])
def userLoadDashboard():
    try:
        if adminLoginSession() == 'user':
            return render_template('user/index.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/loginSession')
def adminLoginSession():
    try:
        if 'session_loginId' and 'session_loginRole' in session:
            if session['session_loginRole'] == 'admin':
                return 'admin'
            elif session['session_loginRole'] == 'user':
                return 'user'
            print("<<<<<<<<<<<<<<<<True>>>>>>>>>>>>>>>>>>>>")
        else:
            print("<<<<<<<<<<<<<<<<False>>>>>>>>>>>>>>>>>>>>")
            return False
    except Exception as ex:
        print(ex)


@app.route('/admin/blockUser')
def adminBlockUser():
    try:
        if adminLoginSession() == 'admin':
            loginId = request.args.get('loginId')
            loginStatus = 'unactive'
            loginVO = LoginVO()
            loginDAO = LoginDAO()
            loginVO.loginId = loginId
            loginVO.loginStatus = loginStatus
            loginDAO.updateLogin(loginVO)
            return redirect(url_for('adminViewUser'))
        else:
            return redirect(url_for('adminLogoutSession'))
    except Exception as ex:
        print(ex)


@app.route('/admin/unblockUser')
def adminUnblockUser():
    try:
        if adminLoginSession() == 'admin':
            loginId = request.args.get('loginId')
            loginStatus = 'active'
            loginVO = LoginVO()
            loginDAO = LoginDAO()
            loginVO.loginId = loginId
            loginVO.loginStatus = loginStatus
            loginDAO.updateLogin(loginVO)
            return redirect(url_for('adminViewUser'))
        else:
            return redirect(url_for('adminLogoutSession'))
    except Exception as ex:
        print(ex)


@app.route("/admin/logoutSession", methods=['GET'])
def adminLogoutSession():
    try:
        session.clear()
        return redirect('/')
    # return redirect(url_for('adminLoadLogin'))
    except Exception as ex:
        print(ex)
