from project import db
from project.com.vo.ComplainVO import ComplainVO


class ComplainDAO:
    def insertComplain(self, complainVO):
        db.session.add(complainVO)
        db.session.commit()

    def userViewComplain(self, complainVO):
        complainVOList = db.session.query(ComplainVO).filter(
            ComplainVO.complainFrom_LoginId == complainVO.complainFrom_LoginId).all()
        return complainVOList

    def viewComplainReply(self, complainVO):
        complainVOList = db.session.query(ComplainVO).filter(
            ComplainVO.complainId == complainVO.complainId).all()
        return complainVOList

    def deleteComplain(self, complainVO):
        complainList = ComplainVO.query.get(complainVO.complainId)
        db.session.delete(complainList)
        db.session.commit()
        return complainList

    def adminViewComplain(self, complainVO):
        complainVOList = ComplainVO.query.filter(ComplainVO.complainStatus == complainVO.complainStatus).all()
        return complainVOList

    def adminInsertComplain(self, complainVO):
        db.session.merge(complainVO)
        db.session.commit()
