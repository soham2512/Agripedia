from flask import render_template

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.ImageDAO import ImageDAO


@app.route('/admin/viewDetection', methods=['GET', 'POST'])
def adminViewDetection():
    try:
        if adminLoginSession() == 'admin':
            imageDAO = ImageDAO()
            imageVOList = imageDAO.adminViewImage()
            return render_template('admin/viewDetection.html', imageVOList=imageVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
