from project import db
from project.com.vo.CropTypeVO import CropTypeVO


class CropVO(db.Model):
    __tablename__ = 'cropmaster'
    cropId = db.Column('cropId', db.Integer, primary_key=True, autoincrement=True)
    cropName = db.Column('cropName', db.String(100), nullable=False)
    cropDescription = db.Column('cropTypeDescription', db.String(1000), nullable=False)
    crop_CropTypeId = db.Column('crop_CropTypeId', db.Integer, db.ForeignKey(CropTypeVO.cropTypeId))

    def as_dict(self):
        return {
            'cropId': self.cropId,
            'cropName': self.cropName,
            'cropDescription': self.cropDescription,
            'crop_CropTypeId': self.crop_CropTypeId,
        }


db.create_all()
