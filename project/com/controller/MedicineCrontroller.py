from flask import request, render_template, redirect, url_for, jsonify

from project import app
from project.com.controller.LoginController import adminLogoutSession, adminLoginSession
from project.com.dao.CropDAO import CropDAO
from project.com.dao.CropTypeDAO import CropTypeDAO
from project.com.dao.MedicineDAO import MedicineDAO
from project.com.vo.CropVO import CropVO
from project.com.vo.ImageVO import ImageVO
from project.com.vo.MedicineVO import MedicineVO


@app.route('/admin/loadMedicine')
def adminLoadMedicine():
    try:
        if adminLoginSession() == 'admin':
            cropTypeDAO = CropTypeDAO()
            cropTypeVOList = cropTypeDAO.viewCropType()
            return render_template('admin/addMedicine.html', cropTypeVOList=cropTypeVOList)
        elif adminLoginSession() == 'user':
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/ajaxCropMedicine', methods=['GET'])
def adminAjaxCropMedicine():
    try:
        if adminLoginSession() == 'admin':
            cropVO = CropVO()
            cropDAO = CropDAO()

            medicine_CropTypeId = request.args.get('medicine_CropTypeId')
            cropVO.crop_CropTypeId = medicine_CropTypeId

            ajaxMedicineCropList = cropDAO.ajaxCropImage(cropVO)
            print('ajaxMedicineCropList>>>>>', ajaxMedicineCropList)

            ajaxMedicineCropJson = [i.as_dict() for i in ajaxMedicineCropList]

            return jsonify(ajaxMedicineCropJson)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/insertMedicine', methods=['POST'])
def adminInsertMedicine():
    try:
        if adminLoginSession() == 'admin':
            diseaseName = request.form['diseaseName']
            diseaseCause = request.form['diseaseCause']
            medicineName = request.form['medicineName']
            medicine_CropTypeId = request.form['medicine_CropTypeId']
            medicine_CropId = request.form['medicine_CropId']


            medicineVO = MedicineVO()
            medicineDAO = MedicineDAO()

            medicineVO.diseaseName = diseaseName
            medicineVO.diseaseCause = diseaseCause
            medicineVO.medicineName = medicineName
            medicineVO.medicine_CropTypeId = medicine_CropTypeId
            medicineVO.medicine_CropId = medicine_CropId


            medicineDAO.insertMedicine(medicineVO)

            return redirect(url_for('adminViewMedicine'))
        elif adminLoginSession() == 'user':
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/viewMedicine', methods=['GET'])
def adminViewMedicine():
    try:
        if adminLoginSession() == 'admin':
            medicineDAO = MedicineDAO()
            medicineVOList = medicineDAO.viewMedicine()
            print("__________________", medicineVOList)
            return render_template('admin/viewMedicine.html', medicineVOList=medicineVOList)
        elif adminLoginSession() == 'user':
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/deleteMedicine', methods=['GET'])
def adminDeleteMedicine():
    try:
        if adminLoginSession() == 'admin':
            medicineVO = MedicineVO()
            medicineDAO = MedicineDAO()
            medicineId = request.args.get('medicineId')
            print(medicineId)
            medicineVO.medicineId = medicineId
            print(medicineVO.medicineId)
            print("just before delete query...........!!!!!!!!")
            medicineDAO.deleteMedicine(medicineVO)
            print("just after delete query...........!!!!!!!!")
            return redirect(url_for('adminViewMedicine'))
        elif adminLoginSession() == 'user':
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/editMedicine', methods=['GET'])
def adminEditMedicine():
    try:
        if adminLoginSession() == 'admin':
            medicineVO = MedicineVO()
            medicineDAO = MedicineDAO()
            cropTypeDAO = CropTypeDAO()
            cropDAO = CropDAO()
            medicineId = request.args.get('medicineId')
            medicineVO.medicineId = medicineId
            medicineVOList = medicineDAO.editMedicine(medicineVO)
            cropTypeVOList = cropTypeDAO.viewCropType()
            cropVOList = cropDAO.viewCrop()
            print("=======MedicineVOList=======", medicineVOList)
            print("=======type of MedicineVOList=======", type(medicineVOList))
            return render_template('admin/editMedicine.html', cropTypeVOList=cropTypeVOList,
                                   cropVOList=cropVOList, medicineVOList=medicineVOList)
        elif adminLoginSession() == 'user':
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/updateMedicine', methods=['POST','GET'])
def adminUpdateMedicine():
    try:
        if adminLoginSession() == 'admin':
            medicineId = request.form['medicineId']
            diseaseName = request.form['diseaseName']
            diseaseCause = request.form['diseaseCause']
            medicine_CropTypeId = request.form['medicine_CropTypeId']
            medicine_CropId = request.form['medicine_CropId']
            medicineName = request.form['medicineName']

            medicineVO = MedicineVO()
            medicineDAO = MedicineDAO()

            medicineVO.medicineId = medicineId
            medicineVO.diseaseName = diseaseName
            medicineVO.diseaseCause = diseaseCause
            medicineVO.medicine_CropTypeId = medicine_CropTypeId
            medicineVO.medicine_CropId = medicine_CropId
            medicineVO.medicineName = medicineName

            medicineDAO.updateMedicine(medicineVO)

            return redirect(url_for('adminViewMedicine'))
        elif adminLoginSession() == 'user':
            return adminLogoutSession()
    except Exception as ex:
        print(ex)




@app.route('/user/viewDiseaseMedicine', methods=['GET'])
def userViewDiseaseMedicine():
    try:
        if adminLoginSession() == 'user':

            medicineDAO = MedicineDAO()

            cropTypeDAO = CropTypeDAO()
            cropDAO = CropDAO()

            imageVO = ImageVO()

            diseaseName = request.args.get('cropDisease')

            imageVO.cropDisease = diseaseName

            medicineVOList = medicineDAO.userViewMedicine(imageVO)

            cropTypeVOList = cropTypeDAO.viewCropType()
            cropVOList = cropDAO.viewCrop()
            print("=======MedicineVOList=======", medicineVOList)
            print("=======type of MedicineVOList=======", type(medicineVOList))
            return render_template('user/viewDiseaseMedicine.html', cropTypeVOList=cropTypeVOList,
                                   cropVOList=cropVOList, medicineVOList=medicineVOList)
        elif adminLoginSession() == 'admin':
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


