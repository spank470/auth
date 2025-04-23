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
            # Загружаем эталонный JSON
            current_dir = os.path.dirname(file)
            file_path = os.path.join(current_dir, "response.json")

            with open(file_path, "r", encoding="utf-8") as file:
                expected_response = json.load(file)

        with allure.step("Сравнение JSON-ответов"):
            # Сравниваем ответ с эталоном
            actual_response = response.json()
            assert actual_response == expected_response, "JSON ответы не совпадают"