from dotenv import dotenv_values
import ast
env_dict = dotenv_values('.env')

TOKEN: str = str(env_dict["TOKEN"])
DB_USER: str = str(env_dict["DB_USER"])
DB_PASSWORD: str = str(env_dict["DB_PASSWORD"])
DB_HOST: str = str(env_dict["DB_HOST"])
DB_NAME: str = str(env_dict["DB_NAME"])

USERS_NAME_LIST: list = ast.literal_eval(str(env_dict["USERS_NAME_LIST"]))
USERS_ID_LIST: list = ast.literal_eval(str(env_dict["USERS_ID_LIST"]))
USER_MAILS_DICT: dict = ast.literal_eval(str(env_dict["USER_MAILS_DICT"]))

EMAIL_SENDER: str = str(env_dict["EMAIL_SENDER"])
EMAIL_PASSWORD: str = str(env_dict["EMAIL_PASSWORD"])
SMTP_SERVER: str = str(env_dict["SMTP_SERVER"])
