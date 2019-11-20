import attr
from loguru import logger
import schedule

from musical_chairs import settings


@attr.s
class Scheduler:
    _poll_interval = attr.ib(default=settings.POLL_INTERVAL)

    def schedule_repeating(self, callback):
        schedule.every(self._poll_interval).seconds.do(callback)

    def run_pending(self):
        schedule.run_pending()
