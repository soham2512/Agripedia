import os
from datetime import datetime

from flask import render_template, redirect, url_for, request
from werkzeug.utils import secure_filename

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.DatasetDAO import DatasetDAO
from project.com.vo.DatasetVO import DatasetVO

UPLOAD_FOLDER = 'project/static/adminResources/dataset/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/admin/loadDataset')
def adminLoadDataset():
    try:
        if adminLoginSession() == 'admin':
            return render_template('admin/addDataset.html')
        elif adminLoginSession() == 'user':
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/insertDataset', methods=['post'])
def adminInsertDataset():
    try:
        if adminLoginSession() == 'admin':
            datasetVO = DatasetVO()
            datasetDAO = DatasetDAO()

            file = request.files['file']
            print(file)

            datasetFileName = secure_filename(file.filename)
            print(datasetFileName)

            datasetFilePath = os.path.join(app.config['UPLOAD_FOLDER'])
            print(datasetFilePath)

            file.save(os.path.join(datasetFilePath, datasetFileName))

            now = datetime.now()
            datasetUploadDate = now.strftime("%d/%m/%Y")
            datasetUploadTime = now.strftime("%H:%M:%S")

            datasetVO.datasetFileName = datasetFileName

            datasetVO.datasetFilePath = datasetFilePath.replace("project", "..")

            datasetVO.datasetUploadDate = datasetUploadDate
            datasetVO.datasetUploadTime = datasetUploadTime

            datasetDAO.insertDataset(datasetVO)

            return redirect(url_for('adminViewDataset'))
        elif adminLoginSession() == 'user':
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/viewDataset')
def adminViewDataset():
    try:
        if adminLoginSession() == 'admin':
            datasetDAO = DatasetDAO()

            datasetVOList = datasetDAO.viewDataset()

            return render_template('admin/viewDataset.html', datasetVOList=datasetVOList)
        elif adminLoginSession() == 'user':
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/deleteDataset', methods=['GET'])
def adminDeleteDataset():
    try:
        if adminLoginSession() == 'admin':
            datasetVO = DatasetVO()

            datasetDAO = DatasetDAO()

            datasetId = request.args.get('datasetId')

            datasetVO.datasetId = datasetId
            datasetList = datasetDAO.deleteDataset(datasetVO)

            print(datasetList)

            datasetFileName = datasetList.datasetFileName
            datasetFilePath = datasetList.datasetFilePath

            fullPath = datasetFilePath.replace('..', 'project') + datasetFileName
            os.remove(fullPath)

            return redirect(url_for('adminViewDataset'))
        elif adminLoginSession() == 'user':
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
