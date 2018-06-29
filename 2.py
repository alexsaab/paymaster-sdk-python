#!/usr/bin/python3


from paymaster_sdk_python.domain.protocols.direct import Direct

# Print necessary headers.
# print("Content-Type: text/html")
# print("")

direct = Direct()

direct.client_id = 'e430408c-3213-4580-9c25-946677a01ea8'
direct.scope = '503'
direct.redirect_uri = 'http://test1.techpaymaster.ru'
direct.secret = '12345'

print('Token (временный), полученный при авторизации: %s' % (direct.auth()))
print('Постоянный объект токена, полученный при авторизации:' + direct.get_token())
