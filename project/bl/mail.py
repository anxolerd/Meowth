from flask import session
from project.bl.utils import BaseBL


class MailTemplateBL(BaseBL):

    def who_update(self):
        self.model.user_id = session['user_id']
