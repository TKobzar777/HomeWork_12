from hw_11 import Name, Phone, Record, Birthday, AddressBook, DateValueError
import copy

class ChoiceError(Exception):
    pass

# import string
global file_name
file_name= 'new_file.bin'

global address_book
address_book = AddressBook()


def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except IndexError:
            return 'Not enough params. Try again'
        except ValueError:
            return 'Phon nomber is not correct. Try again'
        except KeyError:
            return 'There is no entry in the phone book that contains that parameter.'
        # except PhoneAlreadyExistsError:
        #     return 'Phone already exists'
        # except RecordError:
        #     return r'There is no corresponding entry in the phone book!'
        except DateValueError:
            return 'Format date wrong'
        except ChoiceError:
            return 'Wrong choice.Try again'
        
    return inner


def start_work()->str:    
    book = AddressBook()
    return book.unpack_address_book(file_name)  


def hello(*args)->str:
    return F'{args[0]} How can I help you?'


def finish_work(*args)->str:
    str_result = address_book.save_address_book(file_name)
    return args[0]+ ' - ' +str_result


@input_error
def add_contact(*args)->str:
    record = address_book.get(args[1])
    if not record:
        record = Record(Name(args[1]))
    record.add_phone(Phone(args[2]))
    len_args = len(args)
    if len_args > 3:
        record.add_birthday(Birthday(args[3]))
    return address_book.add_record(record)

    
def serch_on_param(str_param:str)-> Record|None:
    record = address_book.find_on_name(str_param)   
    if record:
        return record
    record = address_book.find_on_phone(Phone(str_param))
    if record:
        return record
    return None

def search_oll_param(*args) ->Record|None:
    if (len(args))<=1:
        raise IndexError
    i=1
    while i < len(args):
        record = serch_on_param(args[i])
        i+=1
        if record:
            return record      
    return None

def search_for_matches_by_name(part_name:str)->AddressBook|None:
    book_temp = AddressBook()
    for key, value in address_book.items():
        if str(key).lower().find(part_name.lower()) < 0:
            continue
        book_temp.add_record(value)
    if len(book_temp):
        return book_temp
    return None

def search_for_matches_by_phone(part_name:str)->AddressBook|None:
    book_temp = AddressBook()
    for _, value in address_book.items():
        for ph in value.list_phones:
            if str(ph).find(part_name) < 0:
                continue
            book_temp.add_record(value)
    if len(book_temp):
        return book_temp
    return None

def search_for_matches(*args)-> AddressBook|None:
    if args[1].isdigit():
        return search_for_matches_by_phone(args[1])
    else:
        return search_for_matches_by_name(args[1])
    

@input_error
def edit_contact(*args) -> str:

    record = search_oll_param(*args)
    if not record:
        return 'There is no entry in the phone book that contains that parameter'
    print(f'Entry for editing: \n {record}')
    print('Select a command from the list:\n'\
            '\tedit phone - 1\n'\
            '\tdelete phone -2\n'\
            '\tchange name - 3\n'\
            '\tdelete contact - 4\n'\
            '\texit - 5')
    while True:
        user_input= int(input('<<<< '))
        if user_input == 1:
            phone = Phone(input('<<<< input phone '))
            new_phone = Phone(input('<<<< input new phone '))
            return record.edit_phone(phone, new_phone)
        elif user_input == 2:
            phone = Phone(input('<<<< input phone '))
            return record.delete_phone(phone)
        elif user_input == 3:
            new_name = Name(input('<<<< input new name '))
            record_temp = copy.deepcopy(record)
            print(address_book.delete_record(record))
            record_temp.name.value = new_name.value
            print(address_book.add_record(record_temp))
            return 'Name is changed'
        elif user_input == 5:
            return 'Exiting edit mode'
        elif user_input == 4:
            return address_book.delete_record(record)
        else:
            raise ChoiceError
        
def show_all(*args) -> str:    
    print(f'args[0]:')
    for i in address_book.iterator(7):
        print(i)
    return('Thet ALL') 

  



        
