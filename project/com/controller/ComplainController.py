import os
from datetime import datetime

from flask import request, render_template, redirect, url_for, session
from werkzeug.utils import secure_filename

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.ComplainDAO import ComplainDAO
from project.com.vo.ComplainVO import ComplainVO


@app.route('/user/loadComplain', methods=['GET'])
def userLoadComplain():
    try:
        if adminLoginSession() == 'user':
            return render_template('user/addComplain.html')
        elif adminLoginSession() == 'admin':
            pass
    except Exception as ex:
        print(ex)


@app.route('/user/insertComplain', methods=['POST', 'GET'])
def UserInsertComplain():
    try:
        if adminLoginSession() == 'user':
            UPLOAD_FOLDER = 'project/static/adminResources/complain/'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            complainSubject = request.form['complainSubject']
            complainDescription = request.form['complainDescription']
            file = request.files['complainFile']

            now = datetime.now()
            complainDate = now.strftime("%d/%m/%Y")
            complainTime = now.strftime("%H:%M:%S")
            complainStatus = 'Pending'

            complainDAO = ComplainDAO()
            complainVO = ComplainVO()

            print(file)

            complainFileName = secure_filename(file.filename)
            print(complainFileName)

            complainFilePath = os.path.join(app.config['UPLOAD_FOLDER'])
            print(complainFilePath)

            file.save(os.path.join(complainFilePath, complainFileName))

            complainVO.complainSubject = complainSubject
            complainVO.complainDescription = complainDescription
            complainVO.complainDate = complainDate
            complainVO.complainTime = complainTime
            complainVO.complainFileName = complainFileName
            complainVO.complainFilePath = complainFilePath.replace("project", "..")
            complainVO.complainStatus = complainStatus
            complainVO.complainFrom_LoginId = session['session_loginId']

            # print("just before insert")
            complainDAO.insertComplain(complainVO)

            return redirect(url_for('UserViewComplain'))

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/viewComplain', methods=['GET'])
def UserViewComplain():
    try:
        if adminLoginSession() == 'user':
            complainDAO = ComplainDAO()
            complainVO = ComplainVO()
            complainVO.complainFrom_LoginId = session['session_loginId']
            complainVOlist = complainDAO.userViewComplain(complainVO)
            return render_template('user/viewComplain.html', complainVOlist=complainVOlist)

        elif adminLoginSession() == 'admin':
            pass
    except Exception as ex:
        print(ex)


@app.route('/user/deleteComplain', methods=['GET'])
def adminDeleteComplain():
    try:
        if adminLoginSession() == 'user':
            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainId = request.args.get('complainId')

            complainVO.complainId = complainId
            complainList = complainDAO.deleteComplain(complainVO)
            print(complainList)

            complainFileName = complainList.complainFileName
            complainFilePath = complainList.complainFilePath
            complainFullPath = complainFilePath.replace('..', 'project') + complainFileName
            os.remove(complainFullPath)

            if complainList.complainStatus == "Replied":
                replyFilePath = complainList.replyFilePath
                replyFileName = complainList.replyFileName
                replyFullPath = replyFilePath.replace("..", "project") + replyFileName
                os.remove(replyFullPath)

            return redirect(url_for('UserViewComplain'))

        elif adminLoginSession() == 'admin':
            pass

    except Exception as ex:
        print(ex)


@app.route('/user/viewComplainReply', methods=['GET'])
def UserViewComplainReply():
    try:
        if adminLoginSession() == 'user':
            complainVO = ComplainVO()
            complainDAO = ComplainDAO()
            complainId = request.args.get('complainId')
            complainVO.complainId = complainId
            # complainVO.complainFrom_LoginId = session['session_loginId']
            replyVOList = complainDAO.viewComplainReply(complainVO)
            return render_template('user/viewComplainReply.html', replyVOList=replyVOList)
        elif adminLoginSession() == 'admin':
            pass
    except Exception as ex:
        print(ex)


@app.route('/admin/loadComplainReply', methods=['GET'])
def adminloadComplainReply():
    try:
        if adminLoginSession() == 'admin':
            complainId = request.args.get('complainId')
            return render_template('admin/addComplainReply.html', complainId=complainId)
        elif adminLoginSession() == 'user':
            pass

    except Exception as ex:
        print(ex)


@app.route('/admin/insertComplainReply', methods=['GET', 'POST'])
def adminInsertComplainReply():
    try:
        if adminLoginSession() == 'admin':
            UPLOAD_FOLDER = 'project/static/adminResources/complainReply/'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            complainId = request.form['complainId']
            replySubject = request.form['replySubject']
            replyMessage = request.form['replyMessage']
            file = request.files['replyFile']

            now = datetime.now()
            replyDate = now.strftime("%d/%m/%Y")
            replyTime = now.strftime("%H:%M:%S")

            complainDAO = ComplainDAO()
            complainVO = ComplainVO()
            print(file)

            replyFileName = secure_filename(file.filename)
            print(replyFileName)

            replyFilePath = os.path.join(app.config['UPLOAD_FOLDER'])
            print(replyFilePath)

            file.save(os.path.join(replyFilePath, replyFileName))

            complainVO.complainId = complainId
            complainVO.replySubject = replySubject
            complainVO.replyMessage = replyMessage
            complainVO.replyDate = replyDate
            complainVO.replyTime = replyTime
            complainVO.replyFileName = replyFileName
            complainVO.replyFilePath = replyFilePath.replace("project", "..")
            complainVO.complainStatus = "Replied"

            print("just before admin's complain reply insert")
            complainDAO.adminInsertComplain(complainVO)

            return redirect(url_for('adminViewComplain'))

        elif adminLoginSession() == 'user':
            pass
    except Exception as ex:
        print(ex)


@app.route('/admin/viewComplain', methods=['GET'])
def adminViewComplain():
    try:
        if adminLoginSession() == 'admin':
            complainVO = ComplainVO()
            complainDAO = ComplainDAO()
            complainVO.complainStatus = "pending"
            complainVOList = complainDAO.adminViewComplain(complainVO)
            return render_template('admin/viewComplain.html', complainVOList=complainVOList)

        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
