from app.repositories.user_repository import UserRepository

class AuthService:

    @staticmethod
    def get_user_by_username(db, username: str):
        return UserRepository.get_by_username(db, username)

    @staticmethod
    def get_user_by_id(db, user_id: int):
        return UserRepository.get_by_user_id(db, user_id)
