import pytest
import requests
from model import ObjectAPI
import data
import allure

resp = requests.get(url='https://api.restful-api.dev/objects')


@allure.suite('Тестирование объекта object')
class TestObjectApi:
    """Тестирование объекта object"""

    object_model = ObjectAPI()
    check_data = data
    id = None

    @allure.description("Получение списка object")
    def test_01_get_list_of_all_objects(self):
        """Получение списка object"""

        with allure.step("Получаем список объектов"):
            object_list = self.object_model.get_list_of_all_objects().json()

        with allure.step("Проверяем, что список объектов не пуст"):
            assert len(object_list) > 0, f"Нет объектов в списке {len(object_list)}"

        self.object_model.check_status(200)

    @allure.description("Получение одного объекта по id")
    def test_02_get_single_object_by_id(self):
        """Получение одного объекта по id"""

        with allure.step("Получаем объект"):
            single_object = self.object_model.get_single_object(1).json()

        with allure.step("Проверяем полученный объект"):
            assert single_object == self.check_data.single_object

        with allure.step("Проверяем статус"):
            self.object_model.check_status(200)

    @allure.description("Создание object")
    def test_03_create_object(self, delete_object):
        """Создание object"""

        name = self.check_data.create_object['name']
        data = self.check_data.create_object['data']

        with allure.step("Создаем объект"):
            created_object = self.object_model.add_object(name=name, data=data).json()
            self.id = created_object['id']

        with allure.step("Проверяем созданный объект"):
            assert created_object['name'] == name
            assert created_object['data'] == data

        with allure.step("Проверяем статус"):
            self.object_model.check_status(200)

    @pytest.fixture
    def delete_object(self):
        """Удаление объекта"""

        yield
        self.object_model.delete_object(self.id).json()
        self.object_model.check_successful_deleted_message(self.id)
        self.object_model.delete_object(self.id).json()
        self.object_model.check_delete_error_message(self.id)
