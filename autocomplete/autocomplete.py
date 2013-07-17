from pyquery.pyquery import PyQuery
import requests

__all__ = ['Complete']


def sanitize_url(url):
    # TODO: enforce correct protocol in URL.
    return url


class Complete (object):
    "All of its methods return strings, or raises LookupError."

    def __init__(self, url='', page=None):
        if page is None:
            page = requests.get(sanitize_url(url)).text
        self.document = PyQuery(page)

    def _complete_url(self, url=''):
        "Compensate for partial and relative URLs"
        return "http:" + url

    def thumbnail(self):
        imgs = self.document('.product_photo ul.product-small-images img')
        if not imgs:
            raise LookupError("No thumbnail found")
        return self._complete_url(imgs[0].get('src'))

    def name(self):
        try:
            return self.document('#headline')[0].get('title')
        except IndexError:
            raise LookupError("No name found")

    def price(self):
        try:
            return self.document('#price')[0].text
        except IndexError:
            raise LookupError("No name found")
