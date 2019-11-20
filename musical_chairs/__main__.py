import time

from musical_chairs import alert, course, schedule


def main():
    alerter = alert.Alerter()
    course_fetcher = course.CourseFetcher()
    scheduler = schedule.Scheduler()

    scheduler.schedule_repeating(
        lambda: _alert_if_course_seats_changed(course_fetcher, alerter)
    )

    _run_forever(scheduler)


def _alert_if_course_seats_changed(course_fetcher, alerter):
    seats_changed = course_fetcher.fetch_open_seat_count_changed()
    if seats_changed:
        alerter.alert_that_open_seat_count_changed(course_fetcher)
    course_fetcher.update_last_open_seat_count()


def _run_forever(scheduler):
    while True:
        scheduler.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
