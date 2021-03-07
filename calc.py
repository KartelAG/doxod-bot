import os
import datetime

import tinvest
import tinvest.schemas

TOKEN = os.getenv('TOKEN')
BROKER_ACCOUNT_STARTED_AT = datetime.datetime.strptime('01.08.2020', '%d.%m.%Y')
FIGI_USD = 'BBG0013HGFT4'
TICKER_USD = 'USD000UTSTOM'

FIGI_EUR = 'BBG0013HJJ31'
TICKER_EUR = 'EUR_RUB__TOM'

def get_currency_price(client: tinvest.SyncClient, figi: str, day: str):
    ''' gets price for a day (close candle)
        format of "day" is "2021-03-06"
    ''' 
    from_ = day+'T00:00:00.000000+03:00'
    to_ = day[:-2]+f'{int(day[-2:])+1:02}'+'T00:00:00.000000+03:00'
    return (client.get_market_candles(figi, from_, to_, tinvest.schemas.CandleResolution('day'))).payload.candles[0].c

client = tinvest.SyncClient(TOKEN)
oper_list = client.get_operations(BROKER_ACCOUNT_STARTED_AT, '2021-03-06T18:38:33.131642+03:00')

sum = 0
for operation in oper_list.payload.operations:
    if (operation.operation_type.value == "PayIn") or (operation.operation_type.value == "PayOut"):
        if (operation.currency == 'RUB'):
            value = operation.payment
        elif (operation.currency == 'USD'):
            value = operation.payment * get_currency_price(client, FIGI_USD, str(operation.date.date()))
        elif (operation.currency == 'EUR'):
            value = operation.payment * get_currency_price(client, FIGI_EUR, str(operation.date.date()))
        sum += value
        print(f'{operation.operation_type.value}:\t{str(operation.payment)} {operation.currency}\t{value}\t{operation.date.date()}')

print('=====================')
print(f'Overall:\t{str(sum)}')
#print(get_currency_price(client, FIGI_USD, '2021-03-04'))
