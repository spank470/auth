import allure
import requests

LOGIN_URL = "https://authenticationtest.com//login/?mode=simpleFormAuth"

@allure.step("Отправка POST-запроса на вход")
def send_login_request(email, password):
    session = requests.Session()

    payload = {
        "email": email,
        "password": password
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = session.post(LOGIN_URL, data=payload, headers=headers)

    # Прикрепляем тело запроса вручную, так как request.body может быть None
    encoded_payload = requests.models.RequestEncodingMixin._encode_params(payload)

    allure.attach(
        name="Запрос",
        body=f"URL: {LOGIN_URL}\n"
             f"Метод: POST\n"
             f"Заголовки: {headers}\n"
             f"Тело: {encoded_payload}",
        attachment_type=allure.attachment_type.TEXT
    )

    allure.attach(
        name="Ответ",
        body=f"Статус: {response.status_code}\n"
             f"Заголовки: {dict(response.headers)}\n"
             f"Тело: {response.text[:1000]}...",  # Ограничим длину
        attachment_type=allure.attachment_type.TEXT
    )

    return response

@allure.feature("Аутентификация")
@allure.story("Успешный логин с корректными данными")
def test_successful_login():
    email = "simpleForm@authenticationtest.com"
    password = "pa$$w0rd"

    response = send_login_request(email, password)

    assert response.status_code == 200, f"Ожидался статус 200, но получен {response.status_code}"
    assert "<h1>Login Success</h1>" in response.text, "Ответ не содержит ожидаемого сообщения о успешном логине"