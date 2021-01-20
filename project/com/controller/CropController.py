from flask import request, render_template, redirect, url_for

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.CropDAO import CropDAO
from project.com.dao.CropTypeDAO import CropTypeDAO
from project.com.vo.CropVO import CropVO


@app.route('/admin/loadCrop')
def adminLoadCrop():
    try:
        if adminLoginSession() == 'admin':
            cropTypeDAO = CropTypeDAO()
            cropTypeVOList = cropTypeDAO.viewCropType()
            return render_template('admin/addcrop.html', cropTypeVOList=cropTypeVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/insertCrop', methods=['POST'])
def adminInsertCrop():
    try:
        if adminLoginSession() == 'admin':
            cropName = request.form['cropName']
            cropDescription = request.form['cropDescription']
            crop_CropTypeId = request.form['crop_CropTypeId']
            cropVO = CropVO()
            cropDAO = CropDAO()
            cropVO.cropName = cropName
            cropVO.cropDescription = cropDescription
            cropVO.crop_CropTypeId = crop_CropTypeId
            cropDAO.insertCrop(cropVO)
            return redirect(url_for('adminViewCrop'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/viewCrop', methods=['GET'])
def adminViewCrop():
    try:
        if adminLoginSession() == 'admin':
            cropDAO = CropDAO()
            cropVOList = cropDAO.viewCrop()
            print("__________________", cropVOList)
            return render_template('admin/viewCrop.html', cropVOList=cropVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/deleteCrop', methods=['GET'])
def adminDeleteCrop():
    try:
        if adminLoginSession() == 'admin':
            cropVO = CropVO()
            cropDAO = CropDAO()
            cropId = request.args.get('cropId')
            print(cropId)
            cropVO.cropId = cropId
            print(cropVO.cropId)
            print("just before delete query...........!!!!!!!!")
            cropDAO.deleteCrop(cropVO)
            print("just after delete query...........!!!!!!!!")
            return redirect(url_for('adminViewCrop'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/editCrop', methods=['GET'])
def adminEditCrop():
    try:
        if adminLoginSession() == 'admin':
            cropVO = CropVO()
            cropDAO = CropDAO()
            cropTypeDAO = CropTypeDAO()
            cropId = request.args.get('cropId')
            cropVO.cropId = cropId
            cropVOList = cropDAO.editCrop(cropVO)
            cropTypeVOList = cropTypeDAO.viewCropType()
            print("=======CropVOList=======", cropVOList)
            print("=======type of CropVOList=======", type(cropVOList))
            return render_template('admin/editCrop.html', cropTypeVOList=cropTypeVOList, cropVOList=cropVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/updateCrop', methods=['POST'])
def adminUpdateCrop():
    try:
        if adminLoginSession() == 'admin':
            cropId = request.form['cropId']
            cropName = request.form['cropName']
            cropDescription = request.form['cropDescription']
            crop_CropTypeId = request.form['crop_CropTypeId']
            cropVO = CropVO()
            cropDAO = CropDAO()
            cropVO.cropId = cropId
            cropVO.cropName = cropName
            cropVO.cropDescription = cropDescription
            cropVO.crop_CropTypeId = crop_CropTypeId
            cropDAO.updateCrop(cropVO)
            return redirect(url_for('adminViewCrop'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
