from project import db
from project.com.vo.LoginVO import LoginVO


class RegisterVO(db.Model):
    __tablename__ = 'registermaster'
    registerId = db.Column('registerId', db.Integer, primary_key=True, autoincrement=True, nullable=False)
    registerFirstName = db.Column('registerFirstName', db.String(100), nullable=False)
    registerLastName = db.Column('registerLastName', db.String(100), nullable=False)
    registerMobileNumber = db.Column('registerMobileNumber', db.String(100), nullable=False)
    registerGender = db.Column('registerGender', db.String(100), nullable=False)
    register_LoginId = db.Column('register_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))

    def as_dict(self):
        return {
            'registerId': self.registerId,
            'registerFirstName': self.registerFirstName,
            'registerLastName': self.registerLastName,
            'registerMobileNumber': self.registerMobileNumber,
            'registerGender': self.registerGender,
            'register_LoginId': self.register_LoginId
        }


db.create_all()
