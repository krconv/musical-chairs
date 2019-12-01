import attr
import boto3
from loguru import logger
import ratelimit

from musical_chairs import settings


@attr.s
class Alerter:
    _sns_topic = attr.ib(default=settings.AWS_SNS_TOPIC_ARN)
    _sns_client = attr.ib()

    @_sns_client.default
    def _create_sns_client(self):
        return boto3.client(
            "sns",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION_NAME,
        )

    def alert_that_open_seat_count_changed(self, course_fetcher):
        message = self._build_alert_message_for_open_seat_count_changed(course_fetcher)
        try:
            self._send_message(message)
            logger.info("Sent an alert about the open seat count change.")
        except ratelimit.RateLimitException:
            logger.warning("An alert was not sent due to a configured rate limit!")

    def _build_alert_message_for_open_seat_count_changed(self, course_fetcher):
        return (
            f'"{course_fetcher.get_name()}" now has '
            f"{course_fetcher.get_open_seat_count()} open seats "
            f"(was {course_fetcher.get_old_open_seat_count()} seats)"
        )

    @ratelimit.limits(calls=settings.AWS_SNS_LIMIT, period=settings.AWS_SNS_COOLDOWN)
    def _send_message(self, message):
        self._sns_client.publish(
            TopicArn=self._sns_topic, Message=message,
        )
