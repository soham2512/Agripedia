from project import db
from project.com.vo.LoginVO import LoginVO
from project.com.vo.RegisterVO import RegisterVO


class RegisterDAO:
    def insertRegister(self, RegisterVO):
        db.session.add(RegisterVO)
        db.session.commit()

    def viewUser(self):
        registerList = db.session.query(RegisterVO, LoginVO) \
            .join(LoginVO, LoginVO.loginId == RegisterVO.register_LoginId).all()
        return registerList
