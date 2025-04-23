import requests
import allure
import json

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
            response = requests.post(url, json=payload)
            allure.attach(response.text, name="API Response", attachment_type=allure.attachment_type.JSON)
            assert response.status_code == 200, f"Статус код не 200: {response.status_code}"

        with allure.step("Загрузка эталонного JSON"):
            with open("response.json", "r", encoding="utf-8") as file:
                expected_response = json.load(file)
            allure.attach(json.dumps(expected_response, indent=2, ensure_ascii=False), 
                          name="Expected Response", 
                          attachment_type=allure.attachment_type.JSON)

        with allure.step("Сравнение JSON-ответов"):
            actual_response = response.json()
            assert actual_response == expected_response, "JSON ответы не совпадают"