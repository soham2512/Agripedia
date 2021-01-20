from flask import request, render_template, redirect, url_for

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.CropTypeDAO import CropTypeDAO
from project.com.vo.CropTypeVO import CropTypeVO


@app.route('/admin/loadCropType')
def adminLoadCropType():
    try:
        if adminLoginSession() == 'admin':
            return render_template('admin/addCropType.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/insertCropType', methods=['POST'])
def adminInsertCropType():
    try:
        if adminLoginSession() == 'admin':
            cropTypeName = request.form['cropTypeName']
            cropTypeDescription = request.form['cropTypeDescription']

            cropTypeVO = CropTypeVO()
            cropTypeDAO = CropTypeDAO()

            cropTypeVO.cropTypeName = cropTypeName
            cropTypeVO.cropTypeDescription = cropTypeDescription
            cropTypeDAO.insertCropType(cropTypeVO)
            return redirect(url_for('adminViewCropType'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/viewCropType', methods=['GET'])
def adminViewCropType():
    try:
        if adminLoginSession() == 'admin':
            croptypeDAO = CropTypeDAO()
            croptypeVOList = croptypeDAO.viewCropType()
            print("__________________", croptypeVOList)
            return render_template('admin/viewCropType.html', croptypeVOList=croptypeVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/deleteCropType', methods=['GET'])
def adminDeleteCropType():
    try:
        if adminLoginSession() == 'admin':
            cropTypeVO = CropTypeVO()
            cropTypeDAO = CropTypeDAO()

            cropTypeId = request.args.get('cropTypeId')
            print(cropTypeId)
            cropTypeVO.cropTypeId = cropTypeId
            cropTypeDAO.deleteCropType(cropTypeVO)
            return redirect(url_for('adminViewCropType'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/editCropType', methods=['GET'])
def adminEditCropType():
    try:
        if adminLoginSession() == 'admin':
            cropTypeVO = CropTypeVO()
            cropTypeDAO = CropTypeDAO()

            cropTypeId = request.args.get('cropTypeId')
            print(cropTypeId)
            cropTypeVO.cropTypeId = cropTypeId
            cropTypeVOList = cropTypeDAO.editCropType(cropTypeVO)
            print("=======CropTypeVOList=======", cropTypeVOList)
            print("=======type of CropTypeVOList=======", type(cropTypeVOList))

            return render_template('admin/editCropType.html', cropTypeVOList=cropTypeVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/updateCropType', methods=['POST'])
def adminUpdateCropType():
    try:
        if adminLoginSession() == 'admin':
            cropTypeId = request.form['cropTypeId']
            cropTypeName = request.form['cropTypeName']
            cropTypeDescription = request.form['cropTypeDescription']

            cropTypeVO = CropTypeVO()
            cropTypeDAO = CropTypeDAO()

            cropTypeVO.cropTypeId = cropTypeId
            cropTypeVO.cropTypeName = cropTypeName
            cropTypeVO.cropTypeDescription = cropTypeDescription

            cropTypeDAO.updateCropType(cropTypeVO)

            return redirect(url_for('adminViewCropType'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
