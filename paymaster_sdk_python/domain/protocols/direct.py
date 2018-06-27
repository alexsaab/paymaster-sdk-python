import cgi
import requests
import time


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
    urlBase = 'https://paymaster.ru/'

    # URL для формы авторизации (первый шаг)
    urlGetAuthActionForm1  = ''

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
        self.iat = time.time()

    # Получение подписи к запросу
    def getSign(type = None):
        # Получение какая функция вызвала getSign
        if (!$type):
            $backtrace = debug_backtrace();
            $type = $backtrace[1]['function'];
        }

        // Тело подписи
        switch ($type) {
            case "token": // Тело подписи при запросе постоянного токена
                $body = 'client_id=' . $this->client_id . '&' . 'code=' . $this->code . '&' . 'grant_type=' .
                    $this->grant_type . '&' . 'redirect_uri=' . urlencode($this->redirect_uri) . '&' . 'type=' .
                    $this->type;
                break;
            case "revoke": // TODO отзыв token узнать как делать подпись в этот раз
                $body = 'access_token=' . $this->access_token . '&' . 'client_id=' . $this->client_id . '&' .
                    'code=' . $this->code . '&' . 'grant_type=' . $this->grant_type . '&' . 'redirect_uri=' .
                    urlencode($this->redirect_uri) . '&' . 'type=' . $this->type;
                break;
            case "init": // Тело подписи при инициализации платежа
                $body = 'access_token=' . $this->access_token . '&' . 'merchant_id=' . $this->client_id .
                    '&' . 'merchant_transaction_id=' . urlencode($this->merchant_transaction_id) . '&' . 'amount=' .
                    $this->amount . '&' . 'currency=' . $this->currency . '&' . 'description='
                    . urlencode($this->description) . '&' . 'type=' . $this->type;
                break;
            case "complete": // Тело подписи при проведении платежа
                $body = 'access_token=' . $this->access_token . '&' . 'merchant_id=' . $this->merchant_id . '&' .
                    'merchant_transaction_id=' . urlencode($this->merchant_transaction_id) . '&' .
                    'processor_transaction_id=' . $this->processor_transaction_id . '&' . 'type=' . $this->type;
                var_dump($body);
                break;
            default:   // По умолчанию и при инийциализации
            case "auth":
                $body = 'response_type=' . $this->response_type . '&' . 'client_id=' . $this->client_id . '&' .
                    'redirect_uri=' . urlencode($this->redirect_uri) . '&' . 'scope=' . $this->scope . '&' .
                    'type=' . $this->type;
                break;
        }

        // строка подписи
        $clear_sign = $body . ';' . $this->iat . ';' . $this->secret;
        // вычисление подписи
        $this->sign = base64_encode(hash('sha256', $clear_sign, true));

        var_dump($this->sign);

        // Возвращаем подпись
        return $this->sign;
    }

