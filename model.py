import requests
from typing import Optional, NoReturn

class BaseAPI:
    response: requests.Response = None

    def check_status(self, status: int) -> NoReturn:
        """Проверить статус ответа"""
        assert self.response is not None, "Нет сохранённого response"
        assert self.response.status_code == status, f"Ожидался статус {status}, а пришёл {self.response.status_code}"

class ObjectAPI(BaseAPI):

    BASE_URL = "https://api.restful-api.dev/objects"

    def get_list_of_all_objects(self) -> requests.Response:

        self.response = requests.get(self.BASE_URL)
        return self.response

    def get_list_of_objects_by_id(self, ids: list[int]) -> requests.Response:

        params = [('id', i) for i in ids]
        self.response = requests.get(self.BASE_URL, params=params)
        return self.response

    def get_single_object(self, object_id: int) -> requests.Response:

        url = f"{self.BASE_URL}/{object_id}"
        self.response = requests.get(url)
        return self.response

    def add_object(self, name: str, data: dict) -> requests.Response:

        create_object = {'name': name, 'data': data}
        self.response = requests.post(url=self.BASE_URL, json=create_object)
        return self.response

    def update_object(self, object_id: int, name: str, data: dict) -> requests.Response:

        update_object = {'name': name, 'data': data}
        url = f"{self.BASE_URL}/{object_id}"
        self.response = requests.put(url=url, json=update_object)
        return self.response

    def partially_update_object(self, object_id: int, name: Optional[str] = None,
                                data: Optional[dict] = None) -> requests.Response:

        assert name is not None or data is not None, "Нужно передать хотя бы один параметр для обновления"
        update_object = {}
        if name is not None:
            update_object['name'] = name
        if data is not None:
            update_object['data'] = data
        url = f"{self.BASE_URL}/{object_id}"
        self.response = requests.patch(url=url, json=update_object)
        return self.response

    def delete_object(self, object_id: int) -> requests.Response:
        """Удаление объекта по id"""

        url = f"{self.BASE_URL}/{object_id}"
        self.response = requests.delete(url)
        return self.response

    def check_successful_deleted_message(self, object_id: int):
        """Проверить текст тела удаленного объекта"""

        successful_text = f'Object with id = {object_id} has been deleted.'
        assert self.response.json()['message'] == successful_text, 'Ответ успешно удаленного объекта не совпадает'

    def check_delete_error_message(self, object_id: int):
        """Проверить текст тела при удалении не существующего объекта"""

        error_message = f"Object with id = {object_id} doesn't exist."
        assert self.response.json()['error'] == error_message, 'Ответ не найденного объекта для удаления не совпадает'
