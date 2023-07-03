from flask_login import UserMixin

class UserLogin(UserMixin):
    def fromDB(self, user_id, db):
        self.__user = db.getUser(user_id)
        return self


    def create(self, user):
        self.__user = user
        return self

    """def is_authenticated(self):
        return True


    def is_active(self):
        return True


    def is_anonymous(self):
        return False"""


    def get_id(self):
        return str(self.__user['id']) 


    def getEmail(self):
        return self.__user['email'] if self.__user else 'Not email'
        

    def getRank(self):
        return self.__user['rank'] if self.__user else 'Not rank'