from Models.MemoModel import Memo
from Models.UserModel import User
from .DA import DataBaseAccess

class MemoService:
    def __init__(self):
        self.da = DataBaseAccess()

    def get_memo(self):
        models = [Memo, User.name]

        inner_join_list = [
            (User, User.user_id == Memo.user_id)
        ]

        memo = self.da.data_select(models, inner_join_list=inner_join_list)

        return memo