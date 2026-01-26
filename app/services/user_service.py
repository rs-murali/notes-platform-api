from app.core.models import UserCreate, UserUpdate


class UserService:
    def __init__(self, user_repo):
        self.user_repo = user_repo
        
    def get_users(self):
        return self.user_repo.list_users()
        
    def get_user(self, user_id: int):
        return self.user_repo.get_user_by_id(user_id)

    def create_user(self, user: UserCreate):
        return self.user_repo.create_user(user)
    
    def update_user(self, user_id: int, user: UserUpdate):
        existing_user = self.user_repo.get_user_by_id(user_id)
        if not existing_user:
            return False
        return self.user_repo.update_user(user)
    
    def delete_user(self, user_id: int):
        return self.user_repo.delete_user(user_id)