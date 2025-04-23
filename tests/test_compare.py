import requests
import allure
import json
import os

@allure.suite("Сравнение JSON-ответа с эталонным")
class TestCompareJSON:

    @allure.title("Сравнение ответа API с эталонным JSON")
    @allure.description("Отправляем POST-запрос и сравниваем JSON-ответ с локальным файлом response.json")
    def test_compare_json_response(self):
        url = "https://k3s-sier.evolenta.tech/authorize"
        payload = {
            "login": "pankratov",
            "password": "0pFAYSGJ0"
        }

        with allure.step("POST-запрос к API"):
            # Отправляем данные как форму
            response = requests.post(url, data=payload)
            allure.attach(response.text, name="API Response", attachment_type=allure.attachment_type.TEXT)
            assert response.status_code == 200, f"Статус код не 200: {response.status_code}"

        with allure.step("Загрузка эталонного JSON"):
            # Относительный путь: ищем response.json рядом с этим тестом
            test_dir = os.path.dirname(os.path.abspath(__file__))
            response_path = os.path.join(test_dir, "response.json")

            # Проверим, что файл существует, иначе бросим понятную ошибку
            assert os.path.exists(response_path), f"Файл не найден: {response_path}"

            with open(response_path, "r", encoding="utf-8") as f:
                expected_response = json.load(f)

        with allure.step("Сравнение JSON-ответов"):
            actual_response = response.json()
            assert actual_response == expected_response, "JSON ответы не совпадают"