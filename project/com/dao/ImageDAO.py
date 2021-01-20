from project import db
from project.com.vo.CropTypeVO import CropTypeVO
from project.com.vo.CropVO import CropVO
from project.com.vo.ImageVO import ImageVO
from project.com.vo.LoginVO import LoginVO


class ImageDAO:
    def insertImage(self, ImageVO):
        db.session.add(ImageVO)
        db.session.commit()

    def viewImage(self, imageVO):
        imageList = db.session.query(ImageVO, CropVO, CropTypeVO, LoginVO) \
            .join(CropVO, ImageVO.image_CropId == CropVO.cropId) \
            .join(CropTypeVO, ImageVO.image_CropTypeId == CropTypeVO.cropTypeId) \
            .join(LoginVO, ImageVO.imageFrom_LoginId == LoginVO.loginId) \
            .filter(ImageVO.imageFrom_LoginId == imageVO.imageFrom_LoginId).all()
        return imageList

    def deleteImage(self, imageVO):
        imageList = ImageVO.query.get(imageVO.imageID)
        db.session.delete(imageList)
        db.session.commit()
        return imageList

    def adminViewImage(self):
        imageList = db.session.query(ImageVO, CropVO, CropTypeVO, LoginVO) \
            .join(CropVO, ImageVO.image_CropId == CropVO.cropId) \
            .join(CropTypeVO, ImageVO.image_CropTypeId == CropTypeVO.cropTypeId) \
            .join(LoginVO, ImageVO.imageFrom_LoginId == LoginVO.loginId).all()
        return imageList
