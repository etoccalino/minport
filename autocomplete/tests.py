import unittest
import autocomplete

#
# The fixture is a downloaded copy of:
# http://dx.com/p/0-25w-18k-47kr-resistor-assortment-kit-220-pcs-152206
#


class AutocompleteTestCase (unittest.TestCase):
    fixture = 'fixtures/dx.com.resistor'

    def setUp(self):
        page_buffer = open(self.fixture).read()
        self.completer = autocomplete.Completer(page=page_buffer)

    def test_can_find_thumbnail(self):
        url = "//img.dxcdn.com/productimages/sku_152206_1_small.jpg"
        thumbnail = self.completer.thumbnail()
        self.assertTrue(thumbnail.endswith(url))

    def test_can_find_name(self):
        expected = "0.25W 18K~47KR Resistor Assortment Kit (220 PCS)"
        name = self.completer.name()
        self.assertEqual(expected, name)


if __name__ == "__main__":
    unittest.main()
