from __future__ import annotations
from pymongo import MongoClient
from dataclasses import dataclass
from typing import List, Optional


@dataclass()
class UserModel:
    total_numbers: int = 0
    sum_numbers: float = 0.0
    username: str = None
    user_id: str = None

    @classmethod
    def from_mongo(cls, json) -> Optional[UserModel]:
        if json:
            return UserModel(username=json["username"],
                             user_id=json["user_id"],
                             sum_numbers=json["sum_numbers"],
                             total_numbers=json["total_numbers"])
        return None

    def calculate_average(self) -> float:
        return round(self.sum_numbers / self.total_numbers, 2)


class UserService:
    def __init__(self):
        self.model = None
        self.not_found_exception = None
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.averager
        self.users = self.db.users

    def get_by_id(self, user_id: str) -> UserModel:
        return UserModel.from_mongo(self.users.find_one({"user_id": user_id}))

    def get_by_username(self, username: str) -> UserModel:
        return UserModel.from_mongo(self.users.find_one({"username": username}))

    def get_all(self) -> List[UserModel]:
        return [UserModel.from_mongo(json=user) for user in self.users.find()]

    def post(self, user: UserModel) -> None:
        self.users.update_one({"user_id": user.user_id}, {"$set": vars(user)}, upsert=True)
