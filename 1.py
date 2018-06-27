#!/usr/bin/python3


from paymaster_sdk_python.domain.protocols.common import Common


# Print necessary headers.
print("Content-Type: text/html")
print("")

print(Common.get_form('post'))
