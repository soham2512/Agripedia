from project import db
from project.com.vo.LoginVO import LoginVO


class LoginDAO:
    def validateLogin(self, loginVO):
        loginList = LoginVO.query.filter_by(loginUsername=loginVO.loginUsername,
                                            loginPassword=loginVO.loginPassword)
        return loginList

    def insertLogin(self, loginVO):
        db.session.add(loginVO)
        db.session.commit()

    def updateLogin(self, loginVO):
        db.session.merge(loginVO)
        db.session.commit()

    def findUser(self, loginUsername):
        loginList = LoginVO.query.filter_by(loginUsername=loginUsername)

        return loginList


