import attr
import requests

from musical_chairs import download, parse


@attr.s
class CourseFetcher:
    _parser = attr.ib(factory=parse.Parser)
    _downloader = attr.ib(factory=download.CoursePageDownloader)
    _last_open_seat_count = attr.ib()

    def fetch_name(self):
        course_page = self._downloader.download_course_page()
        return self._parser.parse_name(course_page)

    @_last_open_seat_count.default
    def fetch_open_seat_count(self):
        course_page = self._downloader.download_course_page()
        return self._parser.parse_open_seat_count(course_page)

    def get_last_open_seat_count(self):
        return self._last_open_seat_count

    def update_last_open_seat_count(self):
        self._last_open_seat_count = self.fetch_open_seat_count()

    def fetch_open_seat_count_changed(self):
        last_seat_count = self._last_open_seat_count
        seat_count = self.fetch_open_seat_count()
        return last_seat_count != seat_count
