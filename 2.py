#!/usr/bin/python3


from paymaster_sdk_python.domain.protocols.direct import Direct
import random

# Print necessary headers.
# print("Content-Type: text/html")
# print("")

direct = Direct()

direct.client_id = 'e430408c-3213-4580-9c25-946677a01ea8'
direct.scope = '503'
direct.redirect_uri = 'http://test1.techpaymaster.ru'
direct.secret = '12345'

print('Token (временный), полученный при авторизации: %s' % (direct.auth()))
print('Постоянный токен, полученный при авторизации:' + direct.get_token())
print('Номер транзакции для проведения:' + str(direct.init(random.randint(100, 60000), 500, 'На подарок')))
print('Данные проведенной транзакции:')
dc = direct.complete()
for i in dc:
    print(str(i)+' => '+str(dc[i]))

print('----------------------------------------------------------------------')
