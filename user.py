from __future__ import annotations
from pymongo import MongoClient
from dataclasses import dataclass
from typing import List, Optional
import os

MONGO_HOST = os.getenv("mongo_host")
MONGO_PORT = os.getenv("mongo_port")


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
        self.client = MongoClient(MONGO_HOST, MONGO_PORT)
        self.users = self.client.averager.users

    def get_by_id(self, user_id: str) -> UserModel:
        return UserModel.from_mongo(self.users.find_one({"user_id": user_id}))

    def get_by_username(self, username: str) -> UserModel:
        return UserModel.from_mongo(self.users.find_one({"username": username}))

    def get_all(self) -> List[UserModel]:
        return [UserModel.from_mongo(json=user) for user in self.users.find()]

    def post(self, user: UserModel) -> None:
        self.users.update_one({"user_id": user.user_id}, {"$set": vars(user)}, upsert=True)
