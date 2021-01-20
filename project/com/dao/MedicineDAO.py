from project import db
from project.com.vo.CropTypeVO import CropTypeVO
from project.com.vo.CropVO import CropVO
from project.com.vo.ImageVO import ImageVO
from project.com.vo.MedicineVO import MedicineVO


class MedicineDAO:
    def insertMedicine(self, MedicineVO):
        db.session.add(MedicineVO)
        db.session.commit()

    def viewMedicine(self):
        medicineList = db.session.query(MedicineVO, CropVO, CropTypeVO). \
            join(CropVO, MedicineVO.medicine_CropId == CropVO.cropId).\
            join(CropTypeVO, MedicineVO.medicine_CropTypeId == CropTypeVO.cropTypeId).all()
        return medicineList

    def userViewMedicine(self, imageVO):
        userMedicineList = db.session.query(MedicineVO, CropVO, CropTypeVO). \
            join(CropVO, MedicineVO.medicine_CropId == CropVO.cropId). \
            join(CropTypeVO, MedicineVO.medicine_CropTypeId == CropTypeVO.cropTypeId).\
            filter(MedicineVO.diseaseName == imageVO.cropDisease).all()
        return userMedicineList

    def deleteMedicine(self, medicineVO):
        medicineList = MedicineVO.query.get(medicineVO.medicineId)
        db.session.delete(medicineList)
        db.session.commit()

    def editMedicine(self, medicineVO):
        medicineList = MedicineVO.query.filter_by(medicineId=medicineVO.medicineId).all()
        return medicineList

    def updateMedicine(self, medicineVO):
        db.session.merge(medicineVO)
        db.session.commit()
