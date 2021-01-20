from project import db


class CropTypeVO(db.Model):
    __tablename__ = 'croptypemaster'
    cropTypeId = db.Column('cropTypeId', db.Integer, primary_key=True, autoincrement=True)
    cropTypeName = db.Column('cropTypeName', db.String(100))
    cropTypeDescription = db.Column('cropTypeDescription', db.String(1000))

    def as_dict(self):
        return {
            'cropTypeId': self.cropTypeId,
            'cropTypeName': self.cropTypeName,
            'cropTypeDescription': self.cropTypeDescription
        }


db.create_all()
