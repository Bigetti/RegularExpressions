from pprint import pprint 
import csv
import re

# Функция для извлечения и обновления ФИО
def fio_change(contact_list):
    new_contact_list = []
    for contact in contact_list:
        # Используем модифицированное регулярное выражение для поиска ФИО
        match = re.search(r'(\b\w+\b)(?:\s+(\b\w+\b)(?:\s+(\b\w+\b))?)?', contact[0])
        
        if match:
            # Если найдено, извлекаем Фамилию, Имя и Отчество
            last_name = match.group(1)
            first_name = match.group(2) if match.group(2) else ''
            middle_name = match.group(3) if match.group(3) else ''
            
            # Создаем новый контакт с обновленными данными
            new_contact = [last_name, first_name, middle_name] + contact[3:]
            
            # Добавляем новый контакт в новый список
            new_contact_list.append(new_contact)

    return new_contact_list

def format_phone_number(phone):
    # Поиск номера телефона с возможным добавочным номером
    pattern = r'(\+\d{1,2})?\s*(\(\d{3}\))?\s*(\d{3})[-\s]?(\d{2})[-\s]?(\d{2})\s*(доб\.\s*\d{1,5})?'

    match = re.search(pattern, phone)
    if match:
        # Извлечение соответствующих групп из регулярного выражения
        country_code = match.group(1) if match.group(1) else '+7'
        area_code = match.group(2) if match.group(2) else '(000)'
        first_part = match.group(3)
        second_part = match.group(4)
        third_part = match.group(5)
        extension = match.group(6) if match.group(6) else ''

        # Форматирование номера в заданный формат
        formatted_phone = f"{country_code}{area_code}{first_part}-{second_part}-{third_part} {extension}"

        return formatted_phone
    else:
        return None
    

if __name__ == '__main__':
    # Читаем адресную книгу в формате CSV в список contacts_list:
    with open("phonebook_raw.csv", encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contact_list = list(rows)
    

# Сохраняем названия столбцов
    column_names = contact_list[0]

    print("----trying to put FIO into correct place-----")
    # Вызываем функцию для обновления ФИО и создания нового списка
    new_contact_list = fio_change(contact_list)

    # Выводим обновленный список
   # pprint(new_contact_list)

    print("----next Func-----")
    print("----trying to get phone numbers to global format-----") 


    # Пройдемся по вашему списку и отформатируем номера
    for contact in new_contact_list:
        phone = contact[5]  # Номер телефона находится в пятой позиции
        formatted_phone = format_phone_number(phone)
        if formatted_phone:
            contact[5] = formatted_phone

    # Выведем отформатированный список контактов
    for contact in new_contact_list:
        print(contact)

    print("----next Func-----")
    print("----trying to merge same contacts-----")

    # Создаем словарь для хранения контактов с уникальными ключами (фамилия, имя)
    unique_contacts = {}

    # Проходим по каждому контакту в исходном списке
    for contact in new_contact_list:
        # Получаем фамилию и имя из текущего контакта
        last_name, first_name = contact[0], contact[1]

        # Создаем уникальный ключ на основе фамилии и имени
        key = (last_name, first_name)

        # Проверяем, есть ли такой ключ в словаре
        if key not in unique_contacts:
            # Если ключа нет в словаре, добавляем текущий контакт в словарь с этим ключом
            unique_contacts[key] = contact
        else:
            # Если ключ уже существует, объединяем контакты
            existing_contact = unique_contacts[key]
            for i in range(len(existing_contact)):
                if not existing_contact[i]:
                    existing_contact[i] = contact[i]

    # Преобразуем словарь обратно в список уникальных контактов
    merged_contact_list = list(unique_contacts.values())

    

    # Выводим объединенный список контактов
    for contact in merged_contact_list:
        print(contact)

    # # 2. Сохраните получившиеся данные в другой файл.
    with open("phonebook.csv", "w") as f:
       datawriter = csv.writer(f, delimiter=',')
       datawriter.writerows(merged_contact_list)

    print("----data was added to phonebool.csv-----")