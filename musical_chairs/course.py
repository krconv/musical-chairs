import attr
import requests

from musical_chairs import download, parse


@attr.s
class CourseFetcher:
    _parser = attr.ib(factory=parse.Parser)
    _downloader = attr.ib(factory=download.CoursePageDownloader)
    _details = attr.ib(default=None)
    _old_details = attr.ib(default=None)

    def fetch_updates(self):
        try:
            course_page = self._downloader.download_course_page()
            details = CourseDetails(
                name=self._parser.parse_name(course_page),
                open_seats=self._parser.parse_open_seat_count(course_page),
            )
            self._old_details = self._details
            self._details = details
        except download.DownloadError as error:
            raise FetchError() from error
        except parse.ParseError as error:
            raise FetchError() from error

    def get_name(self):
        return self._details.name

    def get_open_seat_count(self):
        return self._details.open_seats

    def get_old_open_seat_count(self):
        return self._old_details.open_seats

    def is_open_seat_count_changed(self):
        if not (self._old_details and self._details):
            return False

        return self._old_details.open_seats != self._details.open_seats


@attr.s
class CourseDetails:
    name = attr.ib()
    open_seats = attr.ib()


class FetchError(Exception):
    pass
