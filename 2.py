#!/usr/bin/python3


from paymaster_sdk_python.domain.protocols.direct import Direct


# Print necessary headers.
print("Content-Type: text/html")
print("")

Direct.clien_id = 'e430408c-3213-4580-9c25-946677a01ea8'
Direct.scope = '503'
Direct.redirect_uri = 'RUB'
Direct.secret = '12345'

Direct.auth()