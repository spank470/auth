import re
import requests
import allure

BASE_URL = "http://webtours.load-test.ru:1080"

@allure.step("Получение userSession из навигационной страницы")
def get_user_session():
    # Сначала отправляем запрос на выход
    requests.get(f"{BASE_URL}/cgi-bin/welcome.pl?signOff=true")

    # Затем открываем домашнюю страницу
    response = requests.get(f"{BASE_URL}/cgi-bin/nav.pl?in=home")
    assert response.status_code == 200, "Не удалось открыть домашнюю страницу"

    match = re.search(r'<input[^>]*name="userSession"[^>]*value="([^"]+)"', response.text)
    assert match, "userSession не найден в ответе"
    return match.group(1)

@allure.step("Аутентификация пользователя с userSession={user_session}")
def login(user_session, username="pank1", password="pank1"):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {
        "userSession": user_session,
        "username": username,
        "password": password
    }

    response = requests.post(f"{BASE_URL}/cgi-bin/login.pl", data=payload, headers=headers)
    return response

@allure.feature("Аутентификация")
@allure.story("Успешный логин с корректными данными")
def test_successful_login():
    user_session = get_user_session()
    response = login(user_session)

    assert response.status_code == 200, "Запрос логина не дал 200 OK"
    assert "<title>Web Tours</title>" in response.text, "HTML-страница логина не соответствует ожиданиям"