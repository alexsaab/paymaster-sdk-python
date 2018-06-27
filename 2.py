#!/usr/bin/python3


from paymaster_sdk_python.domain.protocols.common import Common


# Print necessary headers.
print("Content-Type: text/html")
print("")

Common.LMI_MERCHANT_ID = 'e430408c-3213-4580-9c25-946677a01ea8'
Common.LMI_PAYMENT_AMOUNT = 500
Common.LMI_CURRENCY = 'RUB'
Common.LMI_PAYMENT_DESC = 'Тестовая транзакция'
Common.KEYPASS = '12345'

print(Common.get_form('post'))
