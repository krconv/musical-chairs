import operator
import urllib3

import attr
import cachetools
import requests

from musical_chairs import settings


@attr.s
class CoursePageDownloader:
    _url = attr.ib(default=settings.COURSE_URL)
    _cache = attr.ib(
        default=cachetools.TTLCache(maxsize=1, ttl=settings.COURSE_CACHE_TTL)
    )

    @cachetools.cachedmethod(operator.attrgetter("_cache"))
    def download_course_page(self):
        try:
            response = requests.get(self._url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as error:
            raise DownloadError() from error
        except urllib3.exceptions.ProtocolError as error:
            raise DownloadError() from error


class DownloadError(Exception):
    pass
