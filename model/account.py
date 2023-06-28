class Account:
    def __init__(self, data):
        self._id = data["_id"]
        self.username = data["username"]
        self.password = data["password"]
        self.email = data["email"]
        self.followers = data["followers"]
        self.following = data["following"]
        self.posts = data["posts"]
        self.warmup_phase = data["warmup_phase"]
        self.warmup_configuration = []

        for config in data["warmup_configuration"]:
            self.warmup_configuration.append(WarmupConfiguration(config))

        self.last_login = data["last_login"]
        self.created_at = data["created_at"]
        self.daily_actions = []

        for action in data["daily_actions"]:
            self.daily_actions.append(DailyAction(action))

        self.__v = data["__v"]


class WarmupConfiguration:
    def __init__(self, data):
        self.day_of_week = data["day_of_week"]
        self.actions = []

        for action in data["actions"]:
            self.actions.append(Action(action))

        self._id = data["_id"]


class Action:
    def __init__(self, data):
        self.action_type = data["action_type"]
        self.count = data["count"]
        self.sessions = data["sessions"]
        self.start_time = data["start_time"]
        self._id = data["_id"]


class DailyAction:
    def __init__(self, data):
        self.date = data["date"]
        self.sessions = []

        for session in data["sessions"]:
            self.sessions.append(Session(session))

        self._id = data["_id"]


class Session:
    def __init__(self, data):
        self.session_id = data["session_id"]
        self.start_time = data["start_time"]
        self.end_time = data["end_time"]
        self.actions = []

        for action in data["actions"]:
            self.actions.append(Action(action))

        self._id = data["_id"]
