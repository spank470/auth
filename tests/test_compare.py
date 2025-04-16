import allure
import requests

LOGIN_URL = "https://authenticationtest.com//login/?mode=simpleFormAuth"

@allure.step("Отправка POST-запроса на вход")
def send_login_request(email, password):
    payload = {
        "email": email,
        "password": password
    }
    response = requests.post(LOGIN_URL, data=payload)
    return response

@allure.feature("Аутентификация")
@allure.story("Успешный логин с корректными данными")
def test_successful_login():
    email = "simpleForm@authenticationtest.com"
    password = "pa$$w0rd"
    
    response = send_login_request(email, password)
    
    assert response.status_code == 200, f"Ожидался статус 200, но получен {response.status_code}"
    assert "<h1>Login Success</h1>" in response.text, "Ответ не содержит ожидаемого сообщения о успешном логине"