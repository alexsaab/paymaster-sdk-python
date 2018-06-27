import requests

from paymaster_sdk_python.domain.protocols.common import Common
from paymaster_sdk_python.domain.protocols.direct import Direct


class ApiClient:

    def __init__(self, request_type):
        if request_type == 'direct':
            request = Direct()
        else:
            request = Common()
