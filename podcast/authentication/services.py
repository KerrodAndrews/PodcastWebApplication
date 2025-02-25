from flask import session
from podcast.domainmodel.model import User
from podcast.adapters.abstract_repository import AbstractRepository

class Services:
    def get_user(self, username: str, repo: AbstractRepository) -> User:
        return repo.get_user(username)

    def get_current_username(self):
        try:
            return session['username']
        except KeyError:
            return ""

    def user_registered(self, username:str, repo: AbstractRepository):
        user = repo.get_user(username)
        if user is None:
            return False
        else:
            return True

    def authenticate_user(self, username: str, password: str, repo: AbstractRepository):
        user = self.get_user(username, repo)
        if user is None:
            return False
        elif user.password == password:
            return True
        else:
            return False

    def register_user(self, username: str, password: str, repo: AbstractRepository):
        if not self.user_registered(username, repo):
            user_num = len(repo.get_users())
            repo.add_user(User(user_num + 1, username, password))


auth_services = Services()
