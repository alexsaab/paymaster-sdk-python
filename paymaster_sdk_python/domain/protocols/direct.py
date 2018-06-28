import requests
import urllib.parse
import time
import hashlib
import base64
from bs4 import BeautifulSoup


class Direct:
    # Словарь для хранения запроса
    request = dict()

    # Константа. Параметр всегда должен иметь значение "code"
    response_type = 'code'

    # Микровремя  iat
    iat = 0

    # Идентификатор Продавца в системе PayMaster
    client_id = ''

    # Идентификатор Проавца в системе PayMaster (тоже самое, что и client_id)
    merchant_id = ''

    # Идентификатор платежа в системе обязательный параметр, номер транзакции
    merchant_transaction_id = ''

    # Сумма платежа
    amount = 0.00

    # Валюта платежа
    currency = 'RUB'

    # Описание платежа
    description = ''

    # Номер транзации в системе Paymaster
    processor_transaction_id = ''

    # Номер платежа в системе
    payment_id = ''

    # URL для перенаправления клиента после успешной авторизации.  НЕ кодированная.
    redirect_uri = ''

    # Идентификатор платежной системы
    scope = '503'
    # 503 тест, рабочие режимы bankcard webmoney

    # Временный токен, присвоенный при запросе на авторизацию
    code = ''

    # Постоянный token доступа
    access_token = ''

    # Тип токена
    token_type = ''

    # Вермя действия (истечения)
    expires_in = 0

    # Идентификатор учетной записи
    account_identifier = ''

    # Константа. Всегда должен быть установлен на "authorization_code"
    grant_type = 'authorization_code'

    # Секретный ключ DIRECT от сайта
    secret = ''

    # тип запроса
    type = 'rest'

    #  подпись
    sign = ''

    # URLы список
    # Базовый URL
    urlBase = 'https://paymaster.ru'

    # URL для формы авторизации (первый шаг)
    urlGetAuthActionForm1 = ''

    # URL для формы авторизации (второй шаг)
    urlGetAuthActionForm2 = ''

    # Авторизация
    urlGetAuth = 'https://paymaster.ru/direct/security/auth'

    # Получение token
    urlGetToken = 'https://paymaster.ru/direct/security/token'

    # Отзыв токена
    urlRevoke = 'https://paymaster.ru/direct/security/revoke'

    # Инициализация платежа
    urlPaymentInit = 'https://paymaster.ru/direct/payment/init'

    # Проведение платежа
    urlPaymentComplete = 'https://paymaster.ru/direct/payment/complete'

    # Инлайн токенизация карт
    # Запрос авторизации
    urlAuthorizeCard = 'https://paymaster.ru/direct/authorize/card'

    # Подтверждение суммы списания
    urlAuthorizeConfirm = 'https://paymaster.ru/direct/authorize/confirm'

    # Проведение 3DSecure авторизации
    # Завершение 3DSecure авторизации
    urlAuthorizeComplete3ds = 'https://paymaster.ru/direct/authorize/complete3ds'

    # Инициализация конструктор
    def __init__(self):
        self.iat = int(round(time.time()))

    # Получение подписи к запросуё
    def get_sign(self, request_type=None):
        body = ''
        # ругается на предупреждение
        # Тело подписи
        # Тело подписи при запросе постоянного токена
        if request_type == 'token':
            body = 'client_id=' + self.client_id + '&' + 'code=' + self.code + '&' + 'grant_type=' + \
                   self.grant_type + '&' + 'redirect_uri=' + urllib.parse.quote(self.redirect_uri, safe='') + '&' + \
                   'type=' + self.type
        # TODO отзыв token узнать как делать подпись в этот раз    
        elif request_type == 'revoke':
            body = 'access_token=' + self.access_token + '&' + 'client_id=' + self.client_id + '&' + \
                   'code=' + self.code + '&' + 'grant_type=' + self.grant_type + '&' + 'redirect_uri=' + \
                   urllib.parse.quote(self.redirect_uri, safe='') + '&' + 'type=' + self.type
        # Тело подписи при инициализации платежа
        elif request_type == 'init':
            body = 'access_token=' + self.access_token + '&' + 'merchant_id=' + self.client_id + \
                   '&' + 'merchant_transaction_id=' + urllib.parse.quote(self.merchant_transaction_id, safe='') + '&' \
                   + 'amount=' + str(self.amount) + '&' + 'currency=' + self.currency + '&' + 'description=' + \
                   urllib.parse.quote(self.description, safe='') + '&' + 'type=' + self.type
        # Тело подписи при проведении платежа
        elif request_type == 'complete':
            body = 'access_token=' + self.access_token + '&' + 'merchant_id=' + self.merchant_id + '&' + \
                   'merchant_transaction_id=' + urllib.parse.quote(self.merchant_transaction_id, safe='') + '&' + \
                   'processor_transaction_id=' + str(self.processor_transaction_id) + '&' + 'type=' + self.type
        elif request_type == 'auth':
            body = 'response_type=' + self.response_type + '&' + 'client_id=' + self.client_id + '&' + \
                   'redirect_uri=' + urllib.parse.quote(self.redirect_uri, safe='') + '&' + 'scope=' + \
                   self.scope + '&' + 'type=' + self.type

        # строка подписи
        clear_sign = body + ';' + str(self.iat) + ';' + self.secret
        # вычисление подписи
        self.sign = base64.b64encode(hashlib.sha256(clear_sign.encode()).digest()).decode('utf-8')
        # Возвращаем подпись
        return self.sign

    # Авторизация
    def auth(self):
        fields = {
            'response_type': self.response_type,
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': self.scope,
            'type': self.type,
            'sign': self.get_sign('auth'),
            'iat': self.iat
        }

        try:
            respond = requests.post(self.urlGetAuth, fields)
        except Exception:
            print('Something went wrong!')

        try:
            self.urlGetAuthActionForm1 = self.urlBase + self._get_form_action(respond.text, 'mainForm')
            respond = requests.post(self.urlGetAuthActionForm1, {})
        except Exception:
            print('Problem in get token form #1!')

        card_form = {
            'values[card_pan]': "4100000000000010",
            'values[card_month]': "6",
            'values[card_year]': str((int(time.strftime("%Y")) + 5)),
            'values[card_cvv]': "111",
        }
        try:
            self.urlGetAuthActionForm2 = self.urlBase + self._get_form_action(respond.text, 'proceedForm')
            respond = requests.post(self.urlGetAuthActionForm2, card_form)
        except Exception:
            print('Problem in get token form #2!')

        self.token = self._get_token(respond.text)
        return self.token

    # Получение экшена формы
    # TODO Переделать на регулярки
    @staticmethod
    def _get_form_action(html, form_id):
        soup = BeautifulSoup(html, 'html.parser')
        action = soup.find('form', id=form_id).get('action')
        return action

    @staticmethod
    # Получение токена
    def _get_token(html):
        soup = BeautifulSoup(html, 'html.parser')
        url = soup.find('a', {'class': 'pp-button-ok pp-rounded-5px'}).get('href')
        code = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)['code'][0]
        return code
