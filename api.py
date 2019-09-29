from app import app
from user import UserService


@app.route('/average')
def get_average():
    user_service = UserService()
    users = user_service.get_all()
    return "".join([f"{user.username} {user.calculate_average()} \n" for user in users])


@app.route('/average/<username>')
def get_average_by_username(username):
    user_service = UserService()
    user = user_service.get_by_username(username=username)
    return f"{user.username} {user.calculate_average()}"
