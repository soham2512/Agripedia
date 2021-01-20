from project import db
from project.com.vo.LoginVO import LoginVO


class ComplainVO(db.Model):
    __tablename__ = 'complainmaster'
    complainId = db.Column('complainId', db.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    complainSubject = db.Column('complainSubject', db.String(100), nullable=False)
    complainDescription = db.Column('complainDescription', db.String(1000), nullable=False)
    complainDate = db.Column('complainDate', db.String(100), nullable=False)
    complainTime = db.Column('complainTime', db.String(100), nullable=False)
    complainStatus = db.Column('complainStatus', db.String(100), nullable=False)
    complainFileName = db.Column('complainFileName', db.String(100), nullable=False)
    complainFilePath = db.Column('complainFilePath', db.String(100), nullable=False)
    complainFrom_LoginId = db.Column('complainFrom_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))
    complainTo_LoginId = db.Column('complainTo_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))
    replySubject = db.Column('replySubject', db.String(100), nullable=True)
    replyMessage = db.Column('replyMessage', db.String(1000), nullable=True)
    replyFileName = db.Column('replyFileName', db.String(100), nullable=True)
    replyFilePath = db.Column('replyFilePath', db.String(100), nullable=True)
    replyDate = db.Column('replyDate', db.String(100), nullable=True)
    replyTime = db.Column('replyTime', db.String(100), nullable=True)

    def as_dict(self):
        return {
            'complainId': self.complainId,
            'complainSubject': self.complainSubject,
            'complainDescription': self.complainDescription,
            'complainDate': self.complainDate,
            'complainTime': self.complainTime,
            'complainStatus': self.complainStatus,
            'complainFileName': self.complainFileName,
            'complainFilePath': self.complainFilePath,
            'complainFrom_LoginId': self.complainFrom_LoginId,
            'complainTo_LoginId': self.complainTo_LoginId,

            'replySubject': self.replySubject,
            'replyMessage': self.replyMessage,
            'replyFileName': self.replyFileName,
            'replyFilePath': self.replyFilePath,
            'replyDate': self.replyDate,
            'replyTime': self.replyTime,

        }


db.create_all()
