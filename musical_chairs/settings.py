import os

import dotenv

dotenv.load_dotenv()

COURSE_URL = os.getenv("COURSE_URL")
COURSE_CACHE_TTL = int(os.getenv("COURSE_CACHE_TTL"))

POLL_INTERVAL = int(os.getenv("POLL_INTERVAL"))

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION_NAME = os.getenv("AWS_REGION_NAME")
AWS_SNS_TOPIC_ARN = os.getenv("AWS_SNS_TOPIC_ARN")
AWS_SNS_LIMIT = int(os.getenv("AWS_SNS_LIMIT"))
AWS_SNS_COOLDOWN = int(os.getenv("AWS_SNS_COOLDOWN"))
