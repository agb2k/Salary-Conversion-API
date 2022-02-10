from unittest import TestCase

from main import convertFactorJSON, create_address


class Test(TestCase):
    def test_create_address(self):
        add_dict = {'street': 'Kattie Turnpike', 'suite': 'Suite 198', 'city': 'Lebsackbury', 'zipcode': '31428-2261', 'geo': {'lat': '-38.2386', 'lng': '57.2232'}}
        self.assertEqual(create_address(add_dict), 'Kattie Turnpike, Suite 198, Lebsackbury, 31428-2261')

    def test_create_usd(self):
        self.assertTrue(1.0, float(convertFactorJSON.get("IDR_USD")))
