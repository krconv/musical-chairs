import re

import attr
import bs4


@attr.s
class Parser:
    def parse_name(self, course_page):
        parsed_page = self._parse_page(course_page)
        try:
            return self._find_name(parsed_page)
        except AttributeError as error:
            raise ParseError() from error

    def _find_name(self, parsed_page):
        results = parsed_page.find(class_="title")
        name = results.text.strip()
        return name

    def parse_open_seat_count(self, course_page):
        parsed_page = self._parse_page(course_page)
        try:
            return self._find_open_seat_count(parsed_page)
        except AttributeError as error:
            raise ParseError() from error

    def _find_open_seat_count(self, parsed_page):
        results = parsed_page.find(text="Enrolled/Seats:")
        seats_value = str(results.parent.next_sibling).strip()
        taken_seats, total_seats = [int(seats) for seats in seats_value.split("/")]
        return total_seats - taken_seats

    def _parse_page(self, page):
        return bs4.BeautifulSoup(page, "html.parser")


class ParseError(Exception):
    pass
