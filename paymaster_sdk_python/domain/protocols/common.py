import cgi
import hashlib
import base64


class Common:
    # Где лежит файл шаблона для формы
    tempale_path = '../views/form.html'

    # Идентификатор продавца
    # Идентификатор сайта в системе PayMaster.Идентификатор можно увидеть в Личном Кабинете, на странице
    # "Список сайтов" в первой колонке
    LMI_MERCHANT_ID = ''

    # Сумма платежа
    # Сумма платежа, которую продавец желает получить от покупателя. Сумма должна быть больше нуля, дробная часть
    # отделяется точкой.
    LMI_PAYMENT_AMOUNT = 0.00

    # Валюта платежа
    # Идентификатор валюты платежа. Система PayMaster понимает как текстовый 3-буквенный код валюты (RUB),
    # так и ISO-код (643) (см. http:#www.currency-iso.org/en/home/tables/table-a1.html)
    LMI_CURRENCY = 'RUB'

    # Внутренний номер счета продавца
    # В этой переменной продавец задает номер счета (идентификатор покупки) в соответствии со своей системой учета.
    # Несмотря на то, что параметр не является обязательным, мы рекомендуем всегда задавать его. Идентификатор должен
    # представлять собой не пустую строку.
    LMI_PAYMENT_NO = ''

    # Назначение платежа
    # Описание товара или услуги. Формируется продавцом. Максимальная длина - 255 символов.
    LMI_PAYMENT_DESC = ''

    # Режим тестирования
    # Дополнительное поле, определяющее режим тестирования. Действует только в режиме тестирования и может
    # принимать одно из следующих значений:
    # 0 или отсутствует: Для всех тестовых платежей сервис будет имитировать успешное выполнение;
    # 1: Для всех тестовых платежей сервис будет имитировать выполнение с ошибкой (платеж не выполнен);
    # 2: Около 80% запросов на платеж будут выполнены успешно, а 20% - не выполнены.
    LMI_SIM_MODE = 0

    # Замена Invoice Confirmation URL
    # Если присутствует, то запрос Invoice Confirmation будет отправляться по указанному URL
    # (а не установленному в настройках). Этот параметр игнорируется, если в настройках сайта запрещена замена URL.
    LMI_INVOICE_CONFIRMATION_URL = ''

    # Замена Payment Notification URL
    # Если присутствует, то запрос Payment Notification будет отправляться по указанному URL
    # (а не установленному в настройках).
    # Этот параметр игнорируется, если в настройках сайта запрещена замена URL.
    LMI_PAYMENT_NOTIFICATION_URL = ''

    # Замена Success URL
    # Если присутствует, то при успешном платеже пользователь будет отправлен по указанному URL
    # (а не установленному в настройках).
    # Этот параметр игнорируется, если в настройках сайта запрещена замена URL.
    LMI_SUCCESS_URL = ''

    # Замена Failure URL
    # Если присутствует, то при отмене платежа пользователь будет отправлен по указанному
    # URL (а не установленному в настройках).
    # Этот параметр игнорируется, если в настройках сайта запрещена замена URL.
    LMI_FAILURE_URL = ''

    # Телефон покупателя
    # Номер телефона покупателя в международном формате без ведущих символов + (например, 79031234567).
    # Эти данные используются системой PayMaster для оповещения пользователя о статусе платежа. Кроме того,
    # некоторые платежные системы требуют указания номера телефона.
    LMI_PAYER_PHONE_NUMBER = ''

    # E-mail покупателя
    # E-mail покупателя. Эти данные используются системой PayMaster для оповещения пользователя о статусе платежа.
    # Кроме того, некоторые платежные системы требуют указания e-mail.
    LMI_PAYER_EMAIL = ''

    # Срок истечения счета
    # Дата и время, до которого действует выписанный счет. Формат YYYY-MM-DDThh:mm:ss, часовой пояс UTC.
    # Внимание: система PayMaster приложит все усилия, чтобы отклонить платеж при истечении срока, но не
    # может гарантировать этого.
    LMI_EXPIRES = ''

    # Идентификатор платежного метода
    # Идентификатор платежного метода, выбранный пользователем. Отсутствие означает, что пользователь будет
    # выбирать платежный метод на странице оплаты PayMaster.
    # Платежный метод указан в настройках сайта в квадратных скобках рядом с названием платежной системы
    # (Например: Webmoney [WebMoney]).
    # Рекомендуется поменять параметр LMI_PAYMENT_SYSTEM на LMI_PAYMENT_METHOD.
    # Но LMI_PAYMENT_SYSTEM по-прежнему принимается и обрабатывается системой.
    LMI_PAYMENT_METHOD = ''

    # Внешний идентификатор магазина в платежной системе
    # Внешний идентификатор магазина, передаваемый интегратором в платежную систему.
    # Указывается только при явном определении платежной системы (Указан параметр LMI_PAYMENT_SYSTEM).
    # Для каждой платежной системы формат согласовывается отдельно.
    # (Только для интеграторов!!!)
    LMI_SHOP_ID = ''

    # Ключ
    # Самое важно из этого всего ключевая фраза, которая испрользуется для формирования обоих хешей
    # (Подписи и самого хеша)
    KEYPASS = ''

    # Подпись запроса (SIGN)
    # Этого параметра нет в https:#paymaster.ru/Partners/ru/docs/protocol
    # Так он необходим только для идентификации платежа
    SIGN = ''

    # Как работаем с хешем, по какому алгоритму его шифруем для проверки подлинности запроса
    HASH_METHOD = 'md5'

    # Перечисляем обязательные параметры
    required = ('LMI_MERCHANT_ID', 'LMI_PAYMENT_AMOUNT', 'LMI_CURRENCY', 'LMI_PAYMENT_DESC', 'KEYPASS')

    # Начинаем работать с онлайн-кассой
    # Для начала забиваем корзину товара
    LMI_SHOPPINGCART = {}

    # Массив с обязательными параметрами для онлайн позиции (товара) онлайн кассы
    cart_required = ('NAME', 'QTY', 'PRICE', 'TAX')

    # URL для оплаты через форму
    # Очень важно
    url = 'https://paymaster.ru/Payment/Init'

    # ставки НДС
    # НДС 18%
    # НДС 10%
    # НДС по формуле 18/118
    # НДС по формуле 10/110
    # НДС 0%
    # НДС не облагается
    vatValues = ('vat18', 'vat10', 'vat118', 'vat110', 'vat0', 'no_vat')

    # Переменная для хранения запроса
    request = {}

    @classmethod
    def __init__(cls):
        setattr(cls, 'request', cgi.FieldStorage())

    @classmethod
    def set(cls, instance, value):
        getattr(cls, instance, value)

    @classmethod
    def get(cls, instance, default=None):
        if getattr(cls, instance, default) is not None:
            return getattr(cls, instance)
        else:
            return default

    @classmethod
    def test(cls):
        setattr(cls, 'request', cgi.FieldStorage())
        for i in cls.request.keys():
            print(i + ": " + cls.request[i].value + "<br/>")

    # Получаем подпись
    @classmethod
    def get_sign(cls):
        sign = cls.LMI_MERCHANT_ID + ':' + str(cls.LMI_PAYMENT_AMOUNT) + ':' + cls.LMI_PAYMENT_DESC + ':' + cls.KEYPASS
        cls.SIGN = hashlib.md5(sign.encode('utf-8')).hexdigest()
        return cls.SIGN

    # Получаем LMI_HASH
    @classmethod
    def get_lmi_hash(cls):
        # Подготавливаем строчку для хеша
        stringToHash = cls.LMI_MERCHANT_ID + ";" + str(cls.LMI_PAYMENT_NO) + ";" + str(
            cls.LMI_SYS_PAYMENT_ID) + ";" + str(cls.LMI_SYS_PAYMENT_DATE) + ";" + str(
            cls.LMI_PAYMENT_AMOUNT) + ";" + cls.LMI_CURRENCY + ";" + cls.LMI_PAID_AMOUNT + ";" \
                       + cls.LMI_PAID_CURRENCY + ";" + cls.LMI_PAYMENT_SYSTEM + ";" + str(
            cls.LMI_SIM_MODE) + ";" + cls.KEYPASS;
        # И кодируем хеш в соответствии с установленным алгоритмом для шифорования
        if cls.HASH_METHOD == 'md5':
            return base64.b64encode(hashlib.md5(stringToHash).digest())
        elif cls.HASH_METHOD == 'sha1':
            return base64.b64encode(hashlib.sha1(stringToHash).digest())
        elif cls.HASH_METHOD == 'sha256':
            return base64.b64encode(hashlib.sha256(stringToHash).digest())

    # Получаем форму для получения платежа
    @classmethod
    def get_form(cls, method):
        # Рассчитываем подпись
        cls.SIGN = cls.get_sign()
        # Переменная для начала формаы оплаты
        o = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Paymaster Payment</title>
</head>
<body>
        """
        # Переменная для футера формы оплаты
        o_footer = """
        </form>
<script>
    window.onload = function(){
        document.forms['paymentForm'].submit();
    }
</script>
</body>
</html>
        """
        o += '<form method="' + method + '" action="' + cls.url + '" name="paymentForm">\n'
        o += '<input type="hidden" name="LMI_MERCHANT_ID" value="' + cls.LMI_MERCHANT_ID + '"/>\n'
        o += '<input type="hidden" name="LMI_PAYMENT_AMOUNT" value="' + str('%.2f' % cls.LMI_PAYMENT_AMOUNT) + '"/>\n'
        o += '<input type="hidden" name="LMI_CURRENCY" value="' + cls.LMI_CURRENCY + '"/>\n'
        o += '<input type="hidden" name="LMI_PAYMENT_DESC" value="' + cls.LMI_PAYMENT_DESC + '"/>\n'
        if cls.LMI_PAYMENT_NO != "":
            o += '<input type="hidden" name="LMI_PAYMENT_NO" value="' + str(cls.LMI_PAYMENT_NO) + '"/>\n'
        if cls.LMI_SIM_MODE != "":
            o += '<input type="hidden" name="LMI_SIM_MODE" value="' + str(cls.LMI_SIM_MODE) + '"/>\n'
        if cls.LMI_INVOICE_CONFIRMATION_URL != "":
            o += '<input type="hidden" name="LMI_INVOICE_CONFIRMATION_URL" value="' + str(
                cls.LMI_INVOICE_CONFIRMATION_URL) + '"/>\n'
        if cls.LMI_PAYMENT_NOTIFICATION_URL != "":
            o += '<input type="hidden" name="LMI_PAYMENT_NOTIFICATION_URL" value="' + cls.LMI_PAYMENT_NOTIFICATION_URL + '"/>\n'
        if cls.LMI_SUCCESS_URL != "":
            o += '<input type="hidden" name="LMI_SUCCESS_URL" value="' + cls.LMI_SUCCESS_URL + '"/>\n'
        if cls.LMI_FAILURE_URL != "":
            o += '<input type="hidden" name="LMI_INVOICE_CONFIRMATION_URL" value="' + cls.LMI_FAILURE_URL + '"/>\n'
        if cls.LMI_PAYER_PHONE_NUMBER != "":
            o += '<input type="hidden" name="LMI_PAYER_PHONE_NUMBER" value="' + str(
                cls.LMI_PAYER_PHONE_NUMBER) + '"/>\n'
        if cls.LMI_PAYER_EMAIL != "":
            o += '<input type="hidden" name="LMI_PAYER_EMAIL" value="' + cls.LMI_PAYER_EMAIL + '"/>\n'
        if cls.LMI_EXPIRES != "":
            o += '<input type="hidden" name="LMI_EXPIRES" value="' + str(cls.LMI_EXPIRES) + '"/>\n'
        if cls.LMI_SHOP_ID != "":
            o += '<input type="hidden" name="LMI_SHOP_ID" value="' + str(cls.LMI_SHOP_ID) + '"/>\n'
        if cls.SIGN != "":
            o += '<input type="hidden" name="LMI_SHOP_ID" value="' + cls.SIGN + '"/>\n'
        for key, item in cls.LMI_SHOPPINGCART:
            o += '<input type="hidden" name="LMI_SHOPPINGCART.ITEM[' + key + '].NAME" value="' + item.NAME + '"/>\n'
            o += '<input type="hidden" name="LMI_SHOPPINGCART.ITEM[' + key + '].QTY" value="' + item.QTY + '"/>\n'
            o += '<input type="hidden" name="LMI_SHOPPINGCART.ITEM[' + key + '].PRICE" value="' + str(
                '%.2f' % item.PRICE) + '"/>\n'
            o += '<input type="hidden" name="LMI_SHOPPINGCART.ITEM[' + key + '].TAX" value="' + item.TAX + '"/>\n'
        o += o_footer
        return o
