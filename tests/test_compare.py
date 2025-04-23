import requests
import allure
import json
import os
from deepdiff import DeepDiff  # Убедись, что он установлен: pip install deepdiff

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

        with allure.step("Отправленный запрос"):
            response = requests.post(url, data=payload)
            allure.attach(f"Статус код ответа: {response.status_code}", name="Статус код", attachment_type=allure.attachment_type.TEXT)
            assert response.status_code == 200, f"Статус код не 200: {response.status_code}"

        with allure.step("Загрузка эталонного JSON"):
            test_dir = os.path.dirname(os.path.abspath(__file__))  # исправлено с file на file
            response_path = os.path.join(test_dir, "response.json")

            assert os.path.exists(response_path), f"Файл не найден: {response_path}"

            with open(response_path, "r", encoding="utf-8") as f:
                expected_response = json.load(f)

        with allure.step("Сравнение ответа отправленного запроса с эталоном"):
            actual_response = response.json()
            diff = DeepDiff(expected_response, actual_response, ignore_order=True)

            if diff:
                
                differences = json.dumps(diff, indent=4, ensure_ascii=False)
                allure.attach(differences, name="Различия JSON", attachment_type=allure.attachment_type.TEXT)
                assert False, "Ответы не совпадают, см. различия во вложении"