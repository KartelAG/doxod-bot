#!/usr/bin/env python

import os
from datetime import datetime, timedelta

import tinvest
import tinvest.schemas
from utils import get_now, localize

TOKEN = os.getenv('TOKEN')
BROKER_ACCOUNT_STARTED_AT = datetime.strptime('01.08.2020', '%d.%m.%Y')
FIGI_USD = 'BBG0013HGFT4'
TICKER_USD = 'USD000UTSTOM'

FIGI_EUR = 'BBG0013HJJ31'
TICKER_EUR = 'EUR_RUB__TOM'

def get_currency_price(client: tinvest.SyncClient, figi: str, day: datetime):
    ''' gets price for a day - from [day - 1] to [day] (close candle)''' 
    return (client.get_market_candles(figi, day - timedelta(days=1), day, tinvest.schemas.CandleResolution('day'))).payload.candles[0].c

client = tinvest.SyncClient(TOKEN)

oper_list = client.get_operations(BROKER_ACCOUNT_STARTED_AT, datetime.now())

sum = 0
for operation in oper_list.payload.operations:
    if (operation.operation_type.value == "PayIn") or (operation.operation_type.value == "PayOut"):
        if (operation.currency == 'RUB'):
            value = operation.payment
        elif (operation.currency == 'USD'):
            value = operation.payment * get_currency_price(client, FIGI_USD, operation.date)
        elif (operation.currency == 'EUR'):
            value = operation.payment * get_currency_price(client, FIGI_EUR, operation.date)
        sum += value
        print(f'{operation.operation_type.value}:\t{str(operation.payment)} {operation.currency}\t{value}\t{operation.date.date()}')

print('=====================')
print(f'Overall:\t{str(sum)}')
#print(get_currency_price(client, FIGI_USD, '2021-03-04'))
