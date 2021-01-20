from project import db
from project.com.vo.CropTypeVO import CropTypeVO
from project.com.vo.CropVO import CropVO


class CropDAO:
    def insertCrop(self, cropVO):
        db.session.add(cropVO)
        db.session.commit()

    def viewCrop(self):
        cropList = db.session.query(CropTypeVO, CropVO) \
            .join(CropVO, CropTypeVO.cropTypeId == CropVO.crop_CropTypeId).all()
        return cropList

    def deleteCrop(self, cropVO):
        cropList = CropVO.query.get(cropVO.cropId)
        db.session.delete(cropList)
        db.session.commit()

    def editCrop(self, cropVO):
        cropList = CropVO.query.filter_by(cropId=cropVO.cropId).all()
        return cropList

    def updateCrop(self, cropVO):
        db.session.merge(cropVO)
        db.session.commit()

    def ajaxCropImage(self, cropVO):
        ajaxImageCropList = CropVO.query.filter_by(
            crop_CropTypeId=cropVO.crop_CropTypeId).all()

        return ajaxImageCropList
