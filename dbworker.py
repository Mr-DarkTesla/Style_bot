from vedis import Vedis
import config


def get_current_state(user_id):
    with Vedis(config.db_file) as db:
        try:
            return db[user_id].decode()  # Если используете Vedis версии ниже, чем 0.7.1, то .decode() НЕ НУЖЕН
        except KeyError:
            return config.States.S_START.value


def set_state(user_id, value):
    with Vedis(config.db_file) as db:
        try:
            db[user_id] = value
            return True
        except:
            pass
            return False
