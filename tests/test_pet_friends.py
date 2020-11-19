from api import PetFriends
from settings import valid_email, valid_password, not_valid_email, not_valid_password
import os

pf = PetFriends()


def test_get_api_key_for_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Барик', animal_type='кот',
                                     age='2', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_get_all_pets_with_valid_key_wrong_filter(filter='my'):
    """ Проверяем что при запросе всех питомцев если передать в значение фильтра
     недопустимы параметр, будет возращен стстус код ошибки.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев  """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 500

def test_get_api_key_for_not_valid_user(email=not_valid_email, password=not_valid_password):
    """ Проверяем что запрос api ключа для не зарегестрированного пользователя возвращает
    статус 403 """

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403

def test_add_new_pet_without_photo(name='Барик', animal_type='кот',
                                     age='2'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
def test_add_new_pet_without_photo_noncorrect(name='Барик', animal_type='кот',
                                     age='два'):
    """Проверяем можно ли добавить питомца с некорректными данными"""

       # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    result['age'] = age.isdigit()
    assert age.isdigit() == False
def test_add_new_pet_without_parrametrs(name='', animal_type='',
                                     age=''):
    """Проверяем можно ли добавить питомца с пустыми параметрами"""

       # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
def test_add_new_pet_with_large_parametr_name(name='ea738145d14ea738145d1413877f3691a3731380e733e877b0aea738148a1f19838e1c5d1413877f3691a3731380e733e877b0ae729e729ea738148a1f19838e1c5d14138777b0aea738148a1f19838e1c5d1413877f3691a3731380e733e877b0ae729e729ea738148a1f19838e1c5d14138713877f3691a3731380e733e877b0aea738148a1f19838e1c5d1413877f3691a3731380e733e877b0ae729e729ea738148a1f19838e1c5d14138777b0aea738148a1f19838e1c5d1413877f3691a3731380e733e877b0ae729e729ea738148a1f19838e1c5d141387'
                                     , animal_type='',age=''):
    """Проверяем можно ли добавить питомца c большим значением в параметре name"""

       # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
def test_add_new_pet_with_large_parametr_type(name=''
                                     , animal_type='ea738145d14ea738145d1413877f3691a3731380e733e877b0aea738148a1f19838e1c5d1413877f3691a3731380e733e877b0ae729e729ea738148a1f19838e1c5d14138777b0aea738148a1f19838e1c5d1413877f3691a3731380e733e877b0ae729e729ea738148a1f19838e1c5d14138713877f3691a3731380e733e877b0aea738148a1f19838e1c5d1413877f3691a3731380e733e877b0ae729e729ea738148a1f19838e1c5d14138777b0aea738148a1f19838e1c5d1413877f3691a3731380e733e877b0ae729e729ea738148a1f19838e1c5d141387'
                                     ,age=''):
    """Проверяем можно ли добавить питомца c большим значением в параметре animal_type"""

       # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
def test_add_new_pet_with_large_parametr_age(name=''
                                     , animal_type=''
                                     ,age='14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706791415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679'):
    """Проверяем можно ли добавить питомца c большим значением в параметре age"""

       # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    result['age'] = age.isdigit()
    assert age.isdigit() == True
