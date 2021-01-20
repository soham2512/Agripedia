from project import db
from project.com.vo.CropTypeVO import CropTypeVO
from project.com.vo.CropVO import CropVO
from project.com.vo.ImageVO import ImageVO
from sqlalchemy.dialects.mysql import LONGTEXT



class MedicineVO(db.Model):
    __tablename__ = 'medicinemaster'
    medicineId = db.Column('medicineId', db.Integer, primary_key=True, autoincrement=True)
    diseaseName = db.Column('diseaseName', db.String(100), nullable=False)
    diseaseCause = db.Column('diseaseCause', db.String(100), nullable=False)
    medicineName = db.Column('medicineName', db.String(5000), nullable=False)
    medicine_CropTypeId = db.Column('medicine_CropTypeId', db.Integer, db.ForeignKey(CropTypeVO.cropTypeId))
    medicine_CropId = db.Column('medicine_CropId', db.Integer, db.ForeignKey(CropVO.cropId))
    medicine_ImageId = db.Column('medicine_ImageId',db.Integer, db.ForeignKey(ImageVO.imageID))

    def as_dict(self):
        return {
            'medicineId': self.medicineId,
            'diseaseName': self.diseaseName,
            'diseaseCause': self.diseaseCause,
            'medicineName': self.medicineName,
            'medicine_CropTypeId': self.medicine_CropTypeId,
            'medicine_CropId': self.medicine_CropId,
            'medicine_ImageId': self.medicine_ImageId
        }


db.create_all()
