""" ДЗ12
"""
from collections import UserDict
from typing import List
from datetime import datetime
import re
import pickle
import json

class AdressBook(UserDict):

    def __init__(self):
        self.current_value = 0
        super().__init__()  # чтоб не потерять атрибут data родительского класса
                            # посокльку __init__ переопределит такой же метод у родителя
    def __iter__(self):
        return self

    def __next__(self):
        if self.current_value < len(self.data):
            self.current_value += 1
            l1 = []
            for i in self.data:
                l1.append(i)    # сделали нормальный список ключей, который индексируется
            return f'{self.current_value}: \
{l1[self.current_value-1]} - {self.data[l1[self.current_value-1]]}'
        raise StopIteration

    def first(self):
        self.current_value = 0  # возврат итератора в исходное состояние
        
    def iterator(self, items = 2):
        
        while True:
            print("Новая страница")
            j = 0
            for i in self:
                yield(i)
                j += 1
                if j == items:
                    break
            if self.current_value == len(self.data) :
                print("Конец книги")
                break

    def find_info(self, fs:'строка для поиска не менее 3 символов' = ''):

        if len(fs) >= 3:
            print("Результат вашего поиска")
            cnt = 0
            for key, rec in self.data.items():
                if fs in key:
                    cnt += 1
                    print(f'№{cnt}: ', key, rec)
                for it in rec.phones:
                    if fs in it.phone:
                        cnt += 1
                        print(f'№{cnt}: ', key, rec)
                        break
        else:
            print('Поиск по одному или двум символам - глупость. Задайте 3 и более!')
    
    def add_record(self,  rec):
        if isinstance(rec, Record):
            self.data.update({rec.name.value:rec})
        else:
            print("Добавить можно только объект класса Record")

    def del_record(self, rec):

            if isinstance(rec, Record):
                l1 = self.data.keys() # получили список ключей
                if rec.name.value in l1: # если такой есть то удаляем
                    self.data.pop(rec.name.value)
                else:
                    print("Нет записи с таким именем")
            else:
                print("Метод принимает только объект класса Record")
        
    def save_to_file(self, choise:'pickle - p json - j' = 'p',
                     filename = "rezerv.dat"):
        if (choise == 'p') or (choise == 'j'):
            if choise == 'j':
                filename = "reserv.json"           # json для обзора и тренировки
                with open(filename, "wb") as file:  # при попытке выкидывает ошибку объект не сериализуем через JSON
                    json.dump(self, file)         # потому что у нас ключи - оббъект Name, а должны быть строки
            else:
                with open(filename, "wb") as file:
                    pickle.dump(self, file)
        else:
            print("Выберите p для pickle или j для json")

    def restore_from_file(self, filename = "rezerv.dat"):

        with open(filename, "rb") as file:
            unpd = pickle.load(file)
            return unpd



class Field:  
                    #смысл инкапсулированой константы класса - просто показать что знаю как ее объявлять и ей пользоваться. а зачем нужна константа - как и в Си
    __VAL = ''      # если много переменных, то проще завести константу и менять ее значение, если надо, а не исправлять каждую переменную
                    # ну и последнее - показать что в курсе неформального правила константы всегда пишет КАПСЛОКОМ
    def __init__(self):
        self.__fvalue = Field.__VAL

    @property
    def fvalue(self):
        return self.__fvalue

    @fvalue.setter
    def fvalue(self, n_value):
        self.__fvalue = n_value


class Name(Field):

    def __init__(self, name):
        self.value = name


class Phone(Field):
    def __init__(self, phone):
        self.__phone = None
        self.phone = phone

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, phone):
        if re.search(r"^\+\([0-9]{3}\)[0-9]{9}$", phone) != None:
            self.__phone = phone
            print("Телефон корректен")
        else:
            self.__phone = ""
            print("Задайте телефон в виде строки  +(xxx)xxxxxxxxх   ")

    def __eq__(self, __o: object) -> bool:
        if self.phone == __o.phone:
            return True
        return False


class Birthday:

    def __init__(self):
        self.__value = ''

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if type(new_value) == str:  # защита от пустого поля
            try:
                brt = datetime.strptime(new_value, '%d.%m.%Y')
                self.__value = new_value
                print("Дата дня рождения корректна")
            except:
                print("Задайте дату ДР в виде строки dd.mm.YYYY")
        else:
            print("Дата ДР не задана")
            

class Record:
    def __init__(self, name: Name, phones: List[Phone] = [], birthday: Birthday = Birthday()):
        self.name = name
        self.phones = phones
        self.birthday = birthday

    def add_phone(self, p:Phone) -> bool:

        if isinstance(p, Phone) and (p.phone != None):
            self.phones.append(p)
            print("Объект с телефоном добавлен")
            return True
        else:
            print("Создайте номер как объект класса Phone(телефон)")

    def del_phone(self, p:Phone):

        if len(self.phones) >= 1:
            if isinstance(p, Phone) and (p.phone != None):
                for i in self.phones:
                    del_nmb = False           #флаг найденного совпадения
                    if i.phone == p.phone:
                        self.phones.remove(i)
                        del_nmb = True
                        break
                if del_nmb == True:
                    print("Номер удален")
                else:
                    print("Совпадений с заданным номером не найдено")
            else:
                print("Метод принимает объект класса Phone")

        else:
            print("Список номеров пуст")

    def change_phone(self, p:Phone, pn:Phone):

        if (isinstance(p, Phone) and isinstance(pn, Phone) and
           (p.phone != None) and (pn.phone != None)):
            for i in self.phones:
                if i.phone == p.phone:
                    i.phone = pn.phone
                    print("Требуемый номер изменен")
                    break
                else:
                    print("Исходного номера не найдено, добавьте номер через метод add_phone")
        else:
            print("Создайте номер как объект класса Phone")

    def days_to_birthday(self):

        if self.birthday.value != None:
            current_datetime = datetime.now()  # текущая дата
            current_year = current_datetime.year # текущий год
            brt = self.birthday.value[0:6]  # день и месяц ДР
            brt = brt + str(current_year)  # ДР в текущем году
            brt_this_year = datetime.strptime(brt, '%d.%m.%Y')
            dif_day = brt_this_year - current_datetime
            if dif_day.days > 0 :
                print(f"До дня рождения {self.name.value} осталось {dif_day.days} дней")
            else:
                print(f"ДР в этом году уже прошло {abs(dif_day.days)} дней назад")
        else:
            print("Задайте ДР")

    def __str__(self) -> str:
        return (
            f"{self.name.value} : {', '.join([phone.phone for phone in self.phones])}"
        )


def main():
    print("ДЗ12")
    Ivan = Record(Name("Ivan"))
    phone1 = Phone("+(380)987876545")
    phone2 = Phone("+(380)887876545")
    phone3 = Phone("+(380)787876546")
    Ivan.add_phone(phone1)
    Ivan.add_phone(phone2) 
    Ivan.add_phone(phone3)
    bd_Bill = Birthday()
    bd_Bill.value = "21.10.1999"
    Bill = Record(Name("Bill"), [Phone("+(380)456786767"), Phone("+(380)732345634")], bd_Bill)
    print(Ivan)
    print(Bill)
    Bill.days_to_birthday()
    Ivan1 = Record(Name("Ivan1"), [Phone("+(380)987876556")])
    Ivan2 = Record(Name("Ivan2"), [Phone("+(380)987876567")])
    Ivan3 = Record(Name("Ivan3"), [Phone("+(380)987876578")])
    tlf = AdressBook()
    tlf.add_record(Ivan)
    tlf.add_record(Bill)
    tlf.add_record(Ivan1)
    tlf.add_record(Ivan2)
    tlf.add_record(Ivan3)
    for page in tlf.iterator(2):
        print(page)
    tlf.save_to_file()
    rez_tlf = AdressBook()
    rez_tlf = rez_tlf.restore_from_file()
    print("Исходник - ", tlf)
    print("Восстановленый обьект - ", rez_tlf)
    
    print("Одинаковы ли они -  ", tlf == rez_tlf)
    tlf.find_info('0')
    tlf.find_info('Iva')
    tlf.find_info('732')


if __name__ == "__main__":
    main()
