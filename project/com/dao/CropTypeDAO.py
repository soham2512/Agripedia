from project import db
from project.com.vo.CropTypeVO import CropTypeVO


class CropTypeDAO:
    def insertCropType(self, cropTypeVO):
        db.session.add(cropTypeVO)
        db.session.commit()

    def viewCropType(self):
        cropTypeVOList = CropTypeVO.query.all()
        return cropTypeVOList

    def deleteCropType(self, cropTypeVO):
        cropTypeList = CropTypeVO.query.get(cropTypeVO.cropTypeId)
        db.session.delete(cropTypeList)
        db.session.commit()

    def editCropType(self, cropTypeVO):
        cropTypeList = CropTypeVO.query.filter_by(cropTypeId=cropTypeVO.cropTypeId).all()
        return cropTypeList

    def updateCropType(self, cropTypeVO):
        db.session.merge(cropTypeVO)
        db.session.commit()
