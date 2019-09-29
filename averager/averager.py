from rtmbot.core import Plugin, Job
from typing import List
from user import UserService, UserModel


class AveragerJob(Job):
    def __init__(self, interval):
        super().__init__(interval)
        self._channels = None
        self.new_messages = False
        self.user_service = UserService()


    @property
    def channels(self):
        if self._channels is None:
            self._channels = []
        return self._channels

    @channels.setter
    def channels(self, value: list):
        self._channels = value

    def run(self, slack_client):
        if self.new_messages:
            messages = []
            users = self.user_service.get_all()
            self.new_messages = False
            text = ""

            for user in users:
                text = text + f"from {user.username} {user.calculate_average()} \n"

            for channel_id in self.channels:
                messages.append([channel_id, "------ This is a scheduled message ------"])
                messages.append([channel_id, text])
            self.channels = []
            return messages

    def toggle_job(self):
        self.new_messages = True

    def add_channel(self, channel_id: str):
        self.channels.append(channel_id)


class AveragerPlugin(Plugin):

    def process_message(self, data: dict):
        try:
            self.averager_job.toggle_job()
            self.averager_job.channels.append(data["channel"])
            user_service = UserService()
            user = user_service.get_by_id(data["user"])
            # get user's  username(not DISPLAY NAME) if he doesn't exist in the db
            if not user:
                username = self.slack_client.api_call(method="users.info", user=data["user"])["user"]["name"]
                user = UserModel(username=username, user_id=data["user"])
            numbers = self.parse_numbers(data["text"])
            if numbers:
                for number in numbers:
                    user.total_numbers += 1
                    user.sum_numbers = user.sum_numbers + number

                self.outputs.append(
                    [data['channel'], f"from {user.username} {user.calculate_average()}"])

                user_service.post(user)
        except Exception as e:
            # Added this so exceptions could be seen in the terminal where the bot is running
            import traceback
            traceback.print_exc()
            print(str(e))

    def register_jobs(self):
        self.averager_job = AveragerJob(60)
        self.jobs.append(self.averager_job)

    def parse_numbers(self, message: str) -> List[int]:
        return [int(s) for s in message.split() if s.isdigit()]
