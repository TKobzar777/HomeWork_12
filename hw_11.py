from collections import UserDict
from datetime import date, timedelta
import re
import pickle
import copy



class PhoneValueError(Exception):
    ...


class DateValueError(Exception):
    ...


class Field:
    def __init__(self, value:str)-> None:
        self.__value = None
        self.value = value
        #self.fl = None

    @property
    def value(self)->str:
        return self.__value
    
    @value.setter
    def value(self, value)-> None:
        self.__value = value
  
    def __str__(self) -> str:
        return self.value
        
    
class Name(Field):
    ...


class Birthday(Field):

    @property
    def value(self)->str:
        return self.__value
    
    @value.setter
    def value(self, value:str) -> None:
        str_date:None
        list_date = []
        str_date = re.search('\d\d/\d\d/\d{4}', value) 
        if  str_date:
            list_date = str(str_date.group()).split('/')
        else:
            str_date = re.search('\d\d.\d\d.\d{4}', value)
            if not str_date:
                raise DateValueError(f'{value} Format date wrong')
            list_date = str(str_date.group()).split('.')
        value = date(year= int(list_date[2]), month=int(list_date[1]), day=int(list_date[0]))
        self.__value = value

    def __str__(self) -> str:
        return self.value.strftime('%d %B %Y')


class Phone(Field):
    def __eq__(self, __value: object) -> bool:
        return self.value == __value.value
    
    @property
    def value(self)->str:
        return self.__value
    
    @value.setter
    def value(self, value:str) -> None:
        if not all((len(value) == 10, value.isdigit())):
            raise PhoneValueError('Phone number most be 10 didgit')
        self.__value = value


class Record:
    def __init__(self, name:Name, phone: Phone | None = None, birthday:Birthday | None = None)->None:
        self.name = name
        self.birthday = birthday 
        self.list_phones = [phone] if phone else []
        #self.idx = 0
    
    def __str__(self):
        return f'Name: {self.name} -- list phones: {" ,".join([str(pn) for pn in self.list_phones]) if self.list_phones else "no phone"} -- Birthday: {self.birthday if self.birthday else "No information"} -- {self.days_to_birthday()} days until birthday'

    def days_to_birthday(self)->int|str:
        if self.birthday==None:
            return 'No information'
        date_now = date.today() 
        delta_year=date(date_now.year+1,1,1)-date(date_now.year,1,1)
        bd_year = date(date_now.year,self.birthday.value.month,self.birthday.value.day)
        if bd_year < date_now:
            next_bd = bd_year + delta_year
        else:
            next_bd = bd_year
        delta_bd = next_bd - date_now
        return delta_bd.days
    
    def add_birthday(self, birthday:Birthday)->str:
        if not self.birthday:
            self.birthday = birthday
            return f'Date birthday {birthday}  added to the sonnact {self.name}'
        return f'Date birthday {birthday} already exists' 

    def add_phone(self, phone:Phone)->str:
        if phone not in self.list_phones:
            self.list_phones.append(phone)
            return f'Phone number {phone}  added to the sonnact {self.name}'
        return f'Phone number {phone} already exists' 
    
    def find_phone(self, phone:Phone)->str:
        for pn in self.list_phones:
            if pn == phone:
                return f'Phone number {phone} is in contact {self.name}'
        return None
    
    def edit_phone(self, phone: Phone, new_phone: Phone) -> str:
        if all((phone in self.list_phones, phone != new_phone)):
            self.list_phones[self.list_phones.index(phone)] = new_phone
            return f"Phone number {phone} change to {new_phone} for contact {self.name}"
        return f"Phone {phone} not in phones or {phone} = {new_phone}" 

    def delete_phone(self, phone:Phone)-> str:
        self.list_phones.remove(phone)
        return f'Phone number {phone} delete'

class AddressBook(UserDict):
   
    def iterator(self, n:int)-> None:
        s=0
        for _, record in self.data.items():
            if s<n:
                yield record
                s+=1
            else:
                input("For continue click 'Enter' <<<< ")
                yield record
                s=1            
    
    def add_record(self, record:Record)->str:
        self.data[record.name.value] = record
        return f'Add record {record} to Address Book'
 
    def delete_record(self, record:Record)->str:
        self.pop(record.name.value)
        return f'Delete {record} to Address Book'    
 
    def find_on_name(self, name:str) -> Record|None:
        record = self.get(name)
        return record if record else None 
    
    def find_on_phone(self, phone:Phone)-> Record|None:
        for _, record in self.items():
            if record.find_phone(phone):
                return record
        return None


    
    def save_address_book(self, file_name:str):
        with open(file_name, "wb") as file:
            pickle.dump(self, file)
            return f'Address book save to file {file_name}'
        
    def unpack_address_book(self, file_name:str):
        with open(file_name, "rb") as file:
            self = pickle.load(file)
            return self


if __name__ == "__main__":

    '''Checking Class Description'''
    book = AddressBook()

    # john_record = Record(Name("John"), Phone("5555555555"), Birthday('24.09.2012'))
    # print(john_record)
    # print(john_record.days_to_birthday())
    # john_record.add_phone(Phone("1234567890"))
    # john_record.add_phone(Phone("1234567890"))
    # john_record.add_phone(Phone("5555555555"))   

    # print('Додавання запису John до адресної книги\n')
    # book.add_record(john_record)
   
    # print('Створення та додавання нового запису для Jane\n')
    # jane_record = Record(Name("Jane"))
    # jane_record.add_phone(Phone("9876543210"))
    # book.add_record(jane_record)

    # print('Знаходження та редагування телефону для John\n')
    # john = book.find("John")
    # print(john)

    # print('Замінити номер телефону\n')
    # print(john.edit_phone(Phone("1234567890"), Phone("1112223333")))

    
    # print('Пошук конкретного телефону у записі John')
    # found_phone = john.find_phone(Phone("5555555555"))
    # print(found_phone)
    # print(book.delete_record(book.find("Jane")))

    
    book.add_record(Record(Name("Anna"), Phone("1111111111"), Birthday('24.07.2007')))
    book.add_record(Record(Name("Boris"), Phone("2222222222"), Birthday('01.12.1969')))
    book.add_record(Record(Name("Sidny"), Phone("3333333333"), Birthday('03.03.2003')))
    book.add_record(Record(Name("Duk"), Phone("4444444444"), Birthday('04.04.1993')))
    book.add_record(Record(Name("Richard"), Phone("6666666666"), Birthday('15.05.2015')))
    book.add_record(Record(Name("Teddy"), Phone("7777777777"), Birthday('27.07.2020')))
    book.add_record(Record(Name("Gregory"), Phone("8888888888"), Birthday('18.07.2018')))
    book.add_record(Record(Name("Sofia"), Phone("9999999999"), Birthday('06.03.2005')))
    book.add_record(Record(Name("Nik"), Phone("1234567890"), Birthday('09.08.2011')))
    book.add_record(Record(Name("Bob"), Phone("9078563412"), Birthday('28.02.2004')))  

    print('Виведення всіх записів у книзі')
    for i in book.iterator(12):
        print(i)
    
    print('Save dict\n')
    print(book.save_address_book('new_file.bin'))

    new_book= AddressBook()
    new_book = new_book.unpack_address_book('new_file.bin')

    for i in new_book.iterator(12):
        print(i)
    




