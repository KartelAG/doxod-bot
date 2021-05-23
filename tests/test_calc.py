import unittest, datetime, sys

from doxod import calc

FIGI_USD = 'BBG0013HGFT4'

class TestCalc(unittest.TestCase):

    def test_get_position_price(self):
        self.assertGreater(calc.get_position_price(FIGI_USD, datetime.datetime.now()), 0)
        self.assertRaises(ValueError, calc.get_position_price, FIGI_USD, datetime.datetime.now()+datetime.timedelta(days=1))
        self.assertRaises(ValueError, calc.get_position_price, FIGI_USD, datetime.datetime.now()+datetime.timedelta(days=3))
        self.assertRaises(ValueError, calc.get_position_price, FIGI_USD, datetime.datetime.now()+datetime.timedelta(days=7))
        self.assertGreater(calc.get_position_price(FIGI_USD, datetime.datetime.now()-datetime.timedelta(days=1)), 0)
        self.assertGreater(calc.get_position_price(FIGI_USD, datetime.datetime.now()-datetime.timedelta(days=3)), 0)
        self.assertGreater(calc.get_position_price(FIGI_USD, datetime.datetime.now()-datetime.timedelta(days=7)), 0)
        self.assertGreater(calc.get_position_price(FIGI_USD, datetime.datetime.strptime('2020-01-08', '%Y-%m-%d')), 0)
    
    def test_get_portfolio_price(self):
        self.assertGreater(calc.get_current_portfolio_price(), 0)

    def test_get_portfolio_price_dollat(self):
        self.assertGreater(calc.get_current_portfolio_price_dollar(), 0)

    def test_get_pays_in(self):
        self.assertGreater(calc.get_pays_in(), 0)
    
    def test_get_pays_in_dollar(self):
        self.assertGreater(calc.get_pays_in_dollar(), 0)

    def test_real_case(self):
        self.assertGreater(calc.get_current_portfolio_price() - calc.get_pays_in(), 0)

    

if __name__ == '__main__':
    unittest.main()