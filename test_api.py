import pytest
import requests
from model import ObjectAPI
import data

resp = requests.get(url='https://api.restful-api.dev/objects')


class TestObjectApi:
    """Тестирование объекта object"""

    object_model = ObjectAPI()
    check_data = data
    id = None

    def test_get_list_of_all_objects(self):
        """Получение списка object"""

        object_list = self.object_model.get_list_of_all_objects().json()
        print(object_list)

        self.object_model.check_status(200)

    def test_get_single_object_by_id(self):
        """Получение одного объекта по id"""
        single_object = self.object_model.get_single_object(1).json()
        assert single_object == self.check_data.single_object
        self.object_model.check_status(200)

    def test_create_object(self, delete_object):
        """Создание object"""
        name = self.check_data.create_object['name']
        data = self.check_data.create_object['data']
        created_object = self.object_model.add_object(name=name, data=data).json()
        self.id = created_object['id']
        assert created_object['name'] == name
        assert created_object['data'] == data
        self.object_model.check_status(200)

    @pytest.fixture
    def delete_object(self):
        """Удаление объекта"""

        yield
        self.object_model.delete_object(self.id).json()
        self.object_model.check_successful_deleted_message(self.id)
        self.object_model.delete_object(self.id).json()
        self.object_model.check_delete_error_message(self.id)
