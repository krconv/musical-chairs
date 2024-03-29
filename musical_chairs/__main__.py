import time

from loguru import logger

from musical_chairs import alert, course, schedule


def main():
    logger.info("Starting up...")
    alerter = alert.Alerter()
    course_fetcher = course.CourseFetcher()
    scheduler = schedule.Scheduler()

    scheduler.schedule_repeating(
        lambda: _alert_if_course_seats_changed(course_fetcher, alerter)
    )

    logger.info("Finished starting up.")
    _run_forever(scheduler)


def _alert_if_course_seats_changed(course_fetcher, alerter):
    try:
        course_fetcher.fetch_updates()
        if course_fetcher.is_open_seat_count_changed():
            logger.info(
                "Detected a change in the open seat count from "
                f"{course_fetcher.get_old_open_seat_count()} to "
                f"{course_fetcher.get_open_seat_count()}.",
            )
            alerter.alert_that_open_seat_count_changed(course_fetcher)
    except course.FetchError as error:
        logger.opt(depth=0).error("Couldn't check open seats due to an error.")


def _run_forever(scheduler):
    scheduler.run_all()
    while True:
        scheduler.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
