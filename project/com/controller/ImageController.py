
import os
from datetime import datetime

import cv2
import numpy as np
import tensorflow as tf
from flask import render_template, redirect, url_for, request, session, jsonify
from keras.preprocessing import image
from tensorflow.python.keras.models import load_model
from tensorflow.python.keras.preprocessing import image
from werkzeug.utils import secure_filename

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.CropDAO import CropDAO
from project.com.dao.CropTypeDAO import CropTypeDAO
from project.com.dao.ImageDAO import ImageDAO
from project.com.vo.CropVO import CropVO
from project.com.vo.ImageVO import ImageVO

INPUT_IMAGE_FOLDER = 'project/static/adminResources/Input_Image/'
app.config['INPUT_IMAGE_FOLDER'] = INPUT_IMAGE_FOLDER

OUTPUT_IMAGE_FOLDER = 'project/static/adminResources/Output_Image/'
app.config['OUTPUT_IMAGE_FOLDER'] = OUTPUT_IMAGE_FOLDER

model = load_model('project/static/adminResources/Model/crop.h5')
graph = tf.get_default_graph()
Disease_Classes = [

    'Apple-:-Apple_scab',
    'Apple-:-Black_rot',
    'Apple-:-Cedar_apple_rust',
    '--No_Disease_Diagnosed--Healthy_Crop_Apple--',

    'Corn(maize)-:-Cercospora_leaf_spot',
    'Corn(maize)-:-Common_rust',
    'Corn(maize)-:-Northern_Leaf_Blight',
    '--No_Disease_Diagnosed--Healthy_Crop_Corn--',

    'Grape-:-Black_rot',
    'Grape-:-Esca_(Black_Measles)',
    'Grape-:-Leaf_blight_(Isariopsis_Leaf_Spot)',
    '--No_Disease_Diagnosed--Healthy_Crop_Grape--',

    'Potato-:-Early_blight',
    'Potato-:-Late_blight',
    '--No_Disease_Diagnosed--Healthy_Crop_Potato--',

    'Tomato-:-Bacterial_spot',
    'Tomato-:-Early_blight',
    'Tomato-:-Late_blight',
    'Tomato-:-Leaf_Mold',
    'Tomato-:-Septoria_leaf_spot',
    'Tomato-:-Spider_mites_Two_spotted_spider_mite',
    'Tomato-:-Target_Spot',
    'Tomato-:-Tomato_YellowLeaf__Curl_Virus',
    'Tomato-:-Tomato_mosaic_virus',
    '--No_Disease_Diagnosed--Healthy_Crop_Tomato--',

]


@app.route('/user/loadImage', methods=['GET'])
def userLoadImage():
    try:
        if adminLoginSession() == 'user':

            cropTypeDAO = CropTypeDAO()

            cropTypeVOList = cropTypeDAO.viewCropType()
            print(cropTypeVOList)

            return render_template('user/addImage.html', cropTypeVOList=cropTypeVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/ajaxCropImage', methods=['GET'])
def userAjaxCropImage():
    try:
        if adminLoginSession() == 'user':
            cropVO = CropVO()
            cropDAO = CropDAO()

            image_CropTypeId = request.args.get('image_CropTypeId')
            cropVO.crop_CropTypeId = image_CropTypeId

            ajaxImageCropList = cropDAO.ajaxCropImage(cropVO)
            print('ajaxImageCropList>>>>>', ajaxImageCropList)

            ajaxImageCropJson = [i.as_dict() for i in ajaxImageCropList]

            return jsonify(ajaxImageCropJson)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/insertImage', methods=['POST', 'GET'])
def userInsertImage():
    global graph
    with graph.as_default():
        try:
            if adminLoginSession() == 'user':

                imageVO = ImageVO()
                imageDAO = ImageDAO()

                imageFrom_LoginId = session['session_loginId']
                image_CropTypeId = request.form['image_CropTypeId']
                image_CropId = request.form['image_CropId']
                file = request.files['file']

                now = datetime.now()
                imageUploadDate = now.strftime("%d/%m/%Y")
                imageUploadTime = now.strftime("%H:%M:%S")

                inputImageName = secure_filename(file.filename)
                print(inputImageName)

                inputImagePath = os.path.join(app.config['INPUT_IMAGE_FOLDER'])
                print(inputImagePath)

                inputImage = os.path.join(inputImagePath, inputImageName)
                print(inputImage)
                file.save(inputImage)
                print("--------> Input Image Saved to location")


                # Detection Of disease
                # Pre-Processing function for test data and input the image to moddel.

                def prepare(inputImage):
                    print("---------> image Preprocessing Starts")
                    img = image.load_img(inputImage, target_size=(256, 256))
                    x = image.img_to_array(img)
                    x = x / 255
                    print(img, inputImage)
                    preprocessed_img = np.expand_dims(x, axis=0)
                    print("--------->image Preprocessing done")
                    return preprocessed_img

                # image feeded to the model
                print("---------> Leaf verification start")

                opt = tf.keras.optimizers.Adam(lr=0.001)
                model.compile(optimizer=opt, loss='mse')

                preprocessed_img = prepare(inputImage)

                model_prediction = model.predict(preprocessed_img)
                model_prediction = np.linalg.norm(model_prediction)
                print(model_prediction)

                print("---------> Leaf verification done")

                if model_prediction > 0.98:

                    print("---------> prediction start")

                    result = model.predict_classes([prepare(inputImage)])

                    print("---------> prediction done")

                    # Disease prediction Output
                    cropDisease = Disease_Classes[int(result)]
                    print("---------> Detection done")

                    print(cropDisease)
                    print(result)

                    img = cv2.imread(inputImage)

                    scale_percent = 200  # percent of original size
                    width = int(img.shape[1] * scale_percent / 100)
                    height = int(img.shape[0] * scale_percent / 100)
                    dim = (width, height)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    org = (20, 45)
                    fontScale = 1
                    color = (255, 0, 0)
                    thickness = 1

                    img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
                    # cv2.imshow("inputImage", img)

                    outputImage = cv2.putText(img, str(cropDisease), org, font, fontScale, color, thickness,
                                              cv2.LINE_AA)

                    # cv2.imshow("outputImage", outputImage)
                    # cv2.waitKey(0)


                    outputImageName = secure_filename(file.filename)
                    print('outputImageName>>>>>>>>>>', outputImageName)

                    outputImagePath = os.path.join(app.config['OUTPUT_IMAGE_FOLDER'])
                    print('outputImagePath>>>>>', outputImagePath)

                    cv2.imwrite(outputImagePath + outputImageName, outputImage)

                    # outputImage = os.path.join(outputImagePath, outputImageName)
                    # print(outputImage)
                    # file.save(outputImage)
                    # print("------------> Output Image Saved to location")

                    imageVO.inputImageName = inputImageName
                    imageVO.inputImagePath = inputImagePath.replace("project", "..")
                    imageVO.outputImageName = outputImageName
                    imageVO.outputImagePath = outputImagePath.replace("project", "..")
                    imageVO.imageUploadDate = imageUploadDate
                    imageVO.imageUploadTime = imageUploadTime
                    imageVO.imageFrom_LoginId = imageFrom_LoginId
                    imageVO.image_CropTypeId = image_CropTypeId
                    imageVO.image_CropId = image_CropId
                    imageVO.cropDisease = cropDisease
                    imageDAO.insertImage(imageVO)
                    return redirect(url_for('userViewImage'))

                else:
                    cropTypeDAO = CropTypeDAO()

                    cropTypeVOList = cropTypeDAO.viewCropType()
                    print(cropTypeVOList)

                    os.remove(inputImage)
                    message = "Please upload proper image of the crop leaf"
                    return render_template('user/addImage.html', error = message, cropTypeVOList=cropTypeVOList)

            else:
                return adminLogoutSession()
        except Exception as ex:
            print(ex)


@app.route('/user/viewImage', methods=['GET'])
def userViewImage():
    try:
        if adminLoginSession() == 'user':
            imageVO = ImageVO()
            imageDAO = ImageDAO()
            imageVO.imageFrom_LoginId = session['session_loginId']
            imageVOList = imageDAO.viewImage(imageVO)
            return render_template('user/viewImage.html', imageVOList=imageVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/deleteImage', methods=['GET'])
def userDeleteImage():
    try:
        if adminLoginSession() == 'user':
            imageVO = ImageVO()
            imageDAO = ImageDAO()
            imageID = request.args.get('imageID')

            imageVO.imageID = imageID
            imageList = imageDAO.deleteImage(imageVO)

            print(imageList)
            inputImageName = imageList.inputImageName
            inputImagePath = imageList.inputImagePath
            inputImagePath = inputImagePath.replace('..', 'project') + inputImageName

            outputImageName = imageList.outputImageName
            outputImagePath = imageList.outputImagePath
            outputImagePath = outputImagePath.replace('..', 'project') + outputImageName

            os.remove(inputImagePath)
            os.remove(outputImagePath)

            return redirect(url_for('userViewImage'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/viewImage', methods=['GET'])
def adminViewImage():
    try:
        if adminLoginSession() == 'admin':
            imageDAO = ImageDAO()
            imageVOList = imageDAO.adminViewImage()
            return render_template('admin/viewImage.html', imageVOList=imageVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)