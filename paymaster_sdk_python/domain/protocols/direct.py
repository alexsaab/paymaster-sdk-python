# coding=<utf8>
# -*- coding: <utf8> -*-

import requests
import urllib.parse
import time
import hashlib
import base64
from bs4 import BeautifulSoup
import json


class Direct:
    # Словарь для хранения запроса
    request = dict()

    # Константа. Параметр всегда должен иметь значение "code"
    response_type = 'code'

    # Микровремя  iat
    iat = 0

    # Идентификатор Продавца в системе PayMaster
    client_id = None

    # Идентификатор Проавца в системе PayMaster (тоже самое, что и client_id)
    merchant_id = None

    # Идентификатор платежа в системе обязательный параметр, номер транзакции
    merchant_transaction_id = None

    # Сумма платежа
    amount = 0.00

    # Валюта платежа
    currency = 'RUB'

    # Описание платежа
    description = None

    # Номер транзации в системе Paymaster
    processor_transaction_id = None

    # Номер платежа в системе
    payment_id = None

    # URL для перенаправления клиента после успешной авторизации.  НЕ кодированная.
    redirect_uri = None

    # Идентификатор платежной системы
    scope = '503'
    # 503 тест, рабочие режимы bankcard webmoney

    # Временный токен, присвоенный при запросе на авторизацию
    code = None

    # Постоянный token доступа
    access_token = None

    # Тип токена
    token_type = None

    # Вермя действия (истечения)
    expires_in = 0

    # Идентификатор учетной записи
    account_identifier = None

    # Константа. Всегда должен быть установлен на "authorization_code"
    grant_type = 'authorization_code'

    # Секретный ключ DIRECT от сайта
    secret = None

    # тип запроса
    type = 'rest'

    # Подпись
    sign = None

    # Срок действия токена
    expires_in = None

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
            print(self.type)
            body = 'client_id=' + self.client_id + '&' + 'code=' + self.code + '&' + 'grant_type=' + \
                   self.grant_type + '&' + 'redirect_uri=' + urllib.parse.quote(self.redirect_uri, safe='') + '&' + \
                   'type=' + str(self.type)
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


    # Получение постоянного токена
    def get_token(self):
        fields = {
            'client_id': self.client_id,
            'code': self.code,
            'grant_type': self.grant_type,
            'redirect_uri': self.redirect_uri,
            'sign': self.get_sign('token'),
            'type': self.type,
            'iat': self.iat
        }

        try:
            respond = requests.post(self.urlGetToken, fields)
            respondObject = respond.text

            if respondObject.status is not None:
                if respondObject.status != 'failure':
                    self.access_token = respondObject.access_token
                    self.token_type = respondObject.token_type
                    self.expires_in = respondObject.expires_in
                    self.account_identifier = respondObject.account_identifier
                else:
                    raise Exception('I can\'t get token. Error is happen.')
            else:
                self.access_token = respondObject.access_token
                self.token_type = respondObject.token_type
                self.expires_in = respondObject.expires_in
                self.account_identifier = respondObject.account_identifier
        except Exception:
            print('I can\'t get token. Error is happen.')

        return respond.text

    # Отзыв токена
    # TODO необходимо узнать, как формируется подпись
    def refoke(self):
        fields = {
            'client_id': self.client_id,
            'access_token': self.access_token,
            'sign': self.get_sign('revoke'),
            'type': self.type,
            'iat': self.iat
        }
        respond = requests.post(self.urlRevoke, fields)
        return respond.text

    # Инициализация платежа
    def init(self, transaction_id=None, amount=None, desc=None):
        if transaction_id is None:
            raise Exception('Transaction id is not set!')
        if (amount is None) or (not float(amount)):
            raise Exception('Transaction amount is not set right!')
        if desc is None:
            raise Exception('Transaction description is not set!')

        if (self.access_token is None) or (self.access_token == ''):
            raise Exception("Access token is must set! " +
                            "Please make auth at first and get constant token!")

        self.merchant_transaction_id = transaction_id
        self.amount = round(amount, 2)
        self.description = desc

        field = {
            'access_token': self.access_token,
            'merchant_id': self.merchant_id,
            'merchant_transaction_id': self.merchant_transaction_id,
            'amount': self.amount,
            'currency': self.currency,
            'description': self.description,
            'sign': self.get_sign('init'),
            'type': self.type,
            'iat': self.iat
        }

        try:
            respond = requests.post(self.urlPaymentInit, field)
        except Exception:
            print('Can\'t connect with site ' + self.urlPaymentInit + '! Aborted.')
            exit(1)



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
