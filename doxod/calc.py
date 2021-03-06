import os
from decimal import Decimal
from datetime import datetime, timedelta

import tinvest
import tinvest.schemas
from .utils import get_now, localize

TOKEN = os.getenv('TOKEN')
BROKER_ACCOUNT_STARTED_AT = datetime.strptime(os.getenv('BROKER_ACCOUNT_START'), '%d.%m.%Y')

FIGI_USD = 'BBG0013HGFT4'
TICKER_USD = 'USD000UTSTOM'
FIGI_EUR = 'BBG0013HJJ31'
TICKER_EUR = 'EUR_RUB__TOM'

if (TOKEN == None):
    print('[ERROR] TOKEN variable is empty!')
    exit()
if (BROKER_ACCOUNT_STARTED_AT == None):
    print('[ERROR] BROKER_ACCOUNT_START variable is empty!')
    exit()

client = tinvest.SyncClient(TOKEN)

def get_position_price(figi: str, day: datetime) -> Decimal:
    ''' gets price for a day - from [day - 1] to [day] (close candle)''' 
    if datetime.now().timestamp() < day.timestamp():
        print('==== someone came from the future? ====')
        raise ValueError
    position_canldes = []
    days_delta = 1
    while (len(position_canldes) == 0):
        if days_delta > 14:
            raise ValueError
        position_canldes = client.get_market_candles(figi, day - timedelta(days=days_delta), day, tinvest.schemas.CandleResolution('day')).payload.candles
        days_delta += 1
    return position_canldes[0].c

def get_current_portfolio_price() -> Decimal:
    sum = 0
    for position in client.get_portfolio().payload.positions:
        try:
            candles = client.get_market_candles(position.figi, localize(datetime.now() - timedelta(days=1)), get_now(), tinvest.schemas.CandleResolution('hour')).payload.candles
            if (len(candles) == 0):
                position_price = get_position_price(position.figi, get_now())
            else:
                position_price = candles[-1].c
        except ValueError:
            return -1
        value = position.balance * position_price
        if position.expected_yield.currency == 'USD':
            value = value * get_position_price(FIGI_USD, datetime.now())
        if position.expected_yield.currency == 'EUR':
            value = value * get_position_price(FIGI_EUR, datetime.now())
        #print(f'{position.name} \t {str(value)}')
        sum += value
    return sum
        
def get_pays_in() -> Decimal:
    sum = 0
    oper_list = client.get_operations(BROKER_ACCOUNT_STARTED_AT, datetime.now())
    for operation in oper_list.payload.operations:
        if (operation.operation_type.value == "PayIn") or (operation.operation_type.value == "PayOut"):
            if (operation.currency == 'RUB'):
                value = operation.payment
            elif (operation.currency == 'USD'):
                value = operation.payment * get_position_price(FIGI_USD, operation.date)
            elif (operation.currency == 'EUR'):
                value = operation.payment * get_position_price(FIGI_EUR, operation.date)
            sum += value
    return sum


if ( __name__ == "__main__" ):
    portfolio = get_current_portfolio_price()
    print('=====================')
    if portfolio > 0:
        print(f'Overall income:\t{str(round(portfolio - get_pays_in(), 2))} RUB')
    else:
        print(f'Oops! Something went wrong')
