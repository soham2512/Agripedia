from datetime import datetime

from flask import request, render_template, redirect, url_for, session

from project import app
from project.com.controller.LoginController import adminLogoutSession, adminLoginSession
from project.com.dao.FeedbackDAO import FeedbackDAO
from project.com.vo.FeedbackVO import FeedbackVO


@app.route('/user/loadFeedback')
def userLoadFeedback():
    try:
        if adminLoginSession() == 'user':
            return render_template('user/addFeedback.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/insertFeedback', methods=['POST'])
def userInsertFeedback():
    try:
        if adminLoginSession() == 'user':
            feedbackSubject = request.form['feedbackSubject']
            feedbackDescription = request.form['feedbackDescription']
            feedbackRating = request.form['feedbackRating']
            feedbackFrom_LoginId = session['session_loginId']

            now = datetime.now()
            feedbackDate = now.strftime("%d/%m/%Y")
            feedbackTime = now.strftime("%H:%M:%S")

            feedbackVO = FeedbackVO()
            feedbackDAO = FeedbackDAO()

            feedbackVO.feedbackSubject = feedbackSubject
            feedbackVO.feedbackDescription = feedbackDescription
            feedbackVO.feedbackDate = feedbackDate
            feedbackVO.feedbackTime = feedbackTime
            feedbackVO.feedbackRating = feedbackRating
            feedbackVO.feedbackFrom_LoginId = feedbackFrom_LoginId

            feedbackDAO.insertFeedback(feedbackVO)

            return redirect(url_for('userViewFeedback'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/deleteFeedback')
def userDeleteFeedback():
    try:
        if adminLoginSession() == 'user':

            feedbackVO = FeedbackVO()
            feedbackDAO = FeedbackDAO()
            feedbackId = request.args.get('feedbackId')
            feedbackVO.feedbackId = feedbackId
            feedbackDAO.deleteFeedback(feedbackVO)

            return redirect(url_for('userViewFeedback'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/viewFeedback')
def userViewFeedback():
    try:
        if adminLoginSession() == 'user':
            feedbackVO = FeedbackVO()
            feedbackDAO = FeedbackDAO()
            feedbackVO.feedbackFrom_LoginId = session['session_loginId']
            feedbackVOList = feedbackDAO.userViewFeedback(feedbackVO)

            return render_template('user/viewFeedback.html', feedbackVOList=feedbackVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/viewFeedback')
def adminViewFeedback():
    try:
        if adminLoginSession() == 'admin':
            feedbackDAO = FeedbackDAO()
            feedbackVO = FeedbackVO()
            feedbackVOList = feedbackDAO.adminViewFeedback()
            return render_template('admin/viewFeedback.html', feedbackVOList=feedbackVOList)
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/updateFeedback')
def adminUpdateFeedback():
    try:
        if adminLoginSession() == 'admin':
            feedbackId = request.args.get('feedbackId')
            feedbackTo_LoginId = session['session_loginId']

            feedbackVO = FeedbackVO()
            feedbackDAO = FeedbackDAO()

            feedbackVO.feedbackId = feedbackId
            feedbackVO.feedbackTo_LoginId = feedbackTo_LoginId

            feedbackDAO.adminUpdateFeedback(feedbackVO)
            return redirect(url_for('adminViewFeedback'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
