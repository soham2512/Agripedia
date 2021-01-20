from project import db
from project.com.vo.CropTypeVO import CropTypeVO
from project.com.vo.CropVO import CropVO
from project.com.vo.LoginVO import LoginVO


class ImageVO(db.Model):
    __tablename__ = 'imagemaster'
    imageID = db.Column('imageID', db.Integer, primary_key=True, autoincrement=True, nullable=False)
    inputImageName = db.Column('inputImageName', db.String(100))
    inputImagePath = db.Column('inputImagePath', db.String(100))
    outputImageName = db.Column('outputImageName', db.String(100))
    outputImagePath = db.Column('outputImagePath', db.String(100))
    imageUploadDate = db.Column('imageUploadDate', db.String(100))
    imageUploadTime = db.Column('imageUploadTime', db.String(100))
    image_CropTypeId = db.Column('image_CropTypeId', db.Integer, db.ForeignKey(CropTypeVO.cropTypeId))
    image_CropId = db.Column('image_CropId', db.Integer, db.ForeignKey(CropVO.cropId))
    imageFrom_LoginId = db.Column('imageFrom_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))
    cropDisease = db.Column('cropDisease', db.String(500))

    def as_dict(self):
        return {
            'imageID': self.imageID,
            'inputImageName': self.inputImageName,
            'inputImagePath': self.inputImagePath,
            'outputImageName': self.outputImageName,
            'outputImagePath': self.outputImagePath,
            'imageUploadDate': self.imageUploadDate,
            'imageUploadTime': self.imageUploadTime,
            'image_CropTypeId': self.image_CropTypeId,
            'image_CropId': self.image_CropId,
            'imageFrom_LoginId': self.imageFrom_LoginId,
            'cropDisease': self.cropDisease

        }


db.create_all()
