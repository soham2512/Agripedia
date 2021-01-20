from project import db
from project.com.vo.FeedbackVO import FeedbackVO
# from project.com.vo.LoginVO import LoginVO


class FeedbackDAO():
    def insertFeedback(self, feedbackVO):
        db.session.add(feedbackVO)
        db.session.commit()

    def userViewFeedback(self, feedbackVO):
        feedbackVOList = db.session.query(FeedbackVO) \
            .filter(FeedbackVO.feedbackFrom_LoginId == feedbackVO.feedbackFrom_LoginId).all()
        return feedbackVOList

    def deleteFeedback(self, feedbackVO):
        feedbackVOList = FeedbackVO.query.get(feedbackVO.feedbackId)
        db.session.delete(feedbackVOList)
        db.session.commit()

    # def adminViewFeedback(self,feedbackVO):
    #     feedbackVOList = db.session.query(LoginVO)\
    #         .join(LoginVO, FeedbackVO.feedbackFrom_LoginId == LoginVO.loginId).\
    #         filter(FeedbackVO.feedbackFrom_LoginId == feedbackVO.feedbackTo_LoginId).all()
    #
    #     return feedbackVOList

    def adminViewFeedback(self):
        feedbackVOList = FeedbackVO.query.all()
        return feedbackVOList

    def adminUpdateFeedback(self, feedbackVO):
        db.session.merge(feedbackVO)
        db.session.commit()
