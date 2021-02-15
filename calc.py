import os
import datetime

import tinvest
import tinvest.schemas

TOKEN = os.getenv('TOKEN')
BROKER_ACCOUNT_STARTED_AT = datetime.datetime.strptime('01.08.2020', '%d.%m.%Y')


client = tinvest.SyncClient(TOKEN)
oper_list = client.get_operations(BROKER_ACCOUNT_STARTED_AT, '2021-02-15T18:38:33.131642+03:00')

for operation in oper_list.payload.operations:
    if (operation.operation_type.value == "PayIn") or (operation.operation_type.value == "PayOut"):
        print(f'{operation.operation_type.value}:          {str(operation.payment)} {operation.currency}         {operation.date}')
            