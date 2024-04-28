import sender_stand_request
import data


def get_kit_body(name):
    return {
        "name": name,
    }


def get_new_user_token():
    return sender_stand_request.post_new_user(data.user_body).json()["authToken"]


def positive_assert(kit_body):
    # В переменную ket_response сохраняется результат запроса на создание kit:
    kit_response = sender_stand_request.post_new_client_kit(kit_body, get_new_user_token())

    # Проверяется, что код ответа равен 201
    assert kit_response.status_code == 201
    # В ответе поле name совпадает с полем name в запросе
    assert kit_response.json()["name"] == kit_body["name"]


def negative_assert_code_400(kit_body):
    # В переменную ket_response сохраняется результат запроса на создание kit:
    kit_response = sender_stand_request.post_new_client_kit(kit_body, get_new_user_token())

    # Проверяется, что код ответа равен 400
    assert kit_response.status_code == 400


def test_create_kit_1_letter_in_name_get_success_response():
    """
    Допустимое количество символов (1):
        kit_body = {
            "name": "a"
        }
    """
    positive_assert(get_kit_body("a"))


def test_create_kit_511_letters_in_name_get_success_response():
    """
    Допустимое количество символов (511):
        kit_body = {
        "name": "<511 символов>"
        }
    """
    positive_assert(get_kit_body(data.kit_name_511_letters))


def test_create_kit_0_letters_in_name_get_error_response():
    """
    Количество символов меньше допустимого (0):
        kit_body = {
        "name": ""
        }
    """
    negative_assert_code_400(get_kit_body(""))


def test_create_kit_512_letters_in_name_get_error_response():
    """
    Количество символов больше допустимого (512):
        kit_body = {
        "name": "<512 символов>"
        }
    """
    negative_assert_code_400(get_kit_body(data.kit_name_512_letters))


def test_create_kit_english_letters_in_name_get_success_response():
    """
    Разрешены английские буквы:
        kit_body = {
        "name": "QWErty"
        }
    """
    positive_assert(get_kit_body("QWErty"))


def test_create_kit_russian_letters_in_name_get_success_response():
    """
    Разрешены русские буквы:
        kit_body = {
        "name": "Мария"
        }
    """
    positive_assert(get_kit_body("Мария"))


def test_create_kit_special_characters_in_name_get_success_response():
    """
    Разрешены спецсимволы:
        kit_body = {
        "name": '"№%@",'
        }
    """
    positive_assert(get_kit_body('"№%@",'))


def test_create_kit_spaces_in_name_get_success_response():
    """
    Разрешены пробелы:
        kit_body = {
        "name": " Человек и КО "
        }
    """
    positive_assert(get_kit_body(" Человек и КО "))


def test_create_kit_numbers_in_name_get_success_response():
    """
    Разрешены цифры:
        kit_body = {
        "name": "123"
        }
    """
    positive_assert(get_kit_body("123"))


def test_create_kit_without_name_get_error_response():
    """
    Параметр не передан в запросе:
        kit_body = {
        }
    """
    negative_assert_code_400({})


def test_create_kit_wrong_name_format_get_error_response():
    """
    Передан другой тип параметра (число):
        kit_body = {
        "name": 123
        }
    """
    negative_assert_code_400(get_kit_body(123))
