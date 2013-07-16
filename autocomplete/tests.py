import unittest
import autocomplete

#
# The fixture is a downloaded copy of:
# http://dx.com/p/0-25w-18k-47kr-resistor-assortment-kit-220-pcs-152206
#


class AutocompleteFixedTestCase (unittest.TestCase):
    fixture = 'fixtures/dx.com.resistors'

    def setUp(self):
        page_buffer = open(self.fixture).read()
        self.complete = autocomplete.Complete(page=page_buffer)

    def test_can_find_thumbnail(self):
        url = "//img.dxcdn.com/productimages/sku_152206_1_small.jpg"
        thumbnail = self.complete.thumbnail()
        self.assertTrue(thumbnail.endswith(url))

    def test_can_find_name(self):
        expected = "0.25W 18K~47KR Resistor Assortment Kit (220 PCS)"
        name = self.complete.name()
        self.assertEqual(expected, name)

    def test_can_find_price(self):
        expected = "5.50"
        price = self.complete.price()
        self.assertEqual(expected, price)


if __name__ == "__main__":
    unittest.main()
