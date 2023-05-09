import os

API_ID = os.environ.get("API_ID", None)
API_HASH = os.environ.get("API_HASH", None)
ALLOW_CHATS = os.environ.get("ALLOW_CHATS", True)
ALLOW_EXCL = os.environ.get("ALLOW_EXCL", False)
CASH_API_KEY = os.environ.get("CASH_API_KEY", None)
DB_URI = os.environ.get("DATABASE_URL")
DEL_CMDS = bool(os.environ.get("DEL_CMDS", False))
EVENT_LOGS = os.environ.get("EVENT_LOGS", None)
INFOPIC = bool(os.environ.get("INFOPIC", "True"))
LOAD = os.environ.get("LOAD", "").split()
MONGO_DB_URI = os.environ.get("MONGO_DB_URI", None)
NO_LOAD = os.environ.get("NO_LOAD", "").split()
START_IMG = os.environ.get( 
    "START_IMG", "https://telegra.ph/file/b84e865d639912ee28f73.jpg" 
)
STRICT_GBAN = bool(os.environ.get("STRICT_GBAN", True))
SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", "LegendBot_OP")
TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TEMP_DOWNLOAD_DIRECTORY", "./")
TOKEN = os.environ.get("TOKEN", None)
TIME_API_KEY = os.environ.get("TIME_API_KEY", None)
WORKERS = int(os.environ.get("WORKERS", 8))
  
try: 
    OWNER_ID = int(os.environ.get("OWNER_ID", None))
except ValueError:
    raise Exception("Your OWNER_ID env variable is not a valid integer.")
try:
    BL_CHATS = set(int(x) for x in os.environ.get("BL_CHATS", "").split())
except ValueError:
    raise Exception("Your blacklisted chats list does not contain valid integers.")
try:
    DRAGONS = set(int(x) for x in os.environ.get("DRAGONS", "").split())
    DEV_USERS = set(int(x) for x in os.environ.get("DEV_USERS", "").split())
except ValueError:
    raise Exception("Your sudo or dev users list does not contain valid integers.")
try:
    DEMONS = set(int(x) for x in os.environ.get("DEMONS", "").split())
except ValueError:
    raise Exception("Your support users list does not contain valid integers.")
try:
    TIGERS = set(int(x) for x in os.environ.get("TIGERS", "").split())
except ValueError: 
    raise Exception("Your tiger users list does not contain valid integers.")
try:
    WOLVES = set(int(x) for x in os.environ.get("WOLVES", "").split())
except ValueError:
    raise Exception("Your whitelisted users list does not contain valid integers.") 
 
