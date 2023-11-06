from collections import UserDict
import hw_12 
from hw_11 import Name, Phone, Record, Birthday, AddressBook


class BotCommands:
    def __init__(self, command_bot:str, function_bot:None, help_bot:str):
        self.command_bot = command_bot
        self.function_bot = function_bot
        self.help_bot = help_bot

    def __str__(self):
        return f'\t{self.command_bot} - {self.help_bot}'

    

class Commands(UserDict):
    def add_command(self, bot_conand:BotCommands)->str:
        self.data[bot_conand.command_bot] = bot_conand
        # return f'Add new record to Address Book'

    def print_halp(self):
        print('Command Line Interface\n'\
        'I will help you with your phone book\n'\
        'List of commands you can use:\n')
        for _, i in self.items():
            print(i)
        
def create_bot(bot_commands:Commands)->Commands:
    bot_commands.add_command(BotCommands(command_bot = 'HELLO', function_bot = hw_12.hello, help_bot ='greeting'))
    bot_commands.add_command(BotCommands(command_bot = 'ADD', function_bot = hw_12.add_contact, help_bot ='(name and phone) - add a phonebook entry'))
    bot_commands.add_command(BotCommands(command_bot = 'EDIT', function_bot = hw_12.edit_contact, help_bot ='(name or phone) - edit contact'))
    bot_commands.add_command(BotCommands(command_bot = 'SEARCH', function_bot = hw_12.search_oll_param, help_bot ='(name or phone) - search contact by name or phone number'))
    bot_commands.add_command(BotCommands(command_bot = 'FIND MATCHES', function_bot = hw_12.search_for_matches, help_bot ='(part of the name or phone) - find matches by part of the name or phone number'))
    bot_commands.add_command(BotCommands(command_bot = 'SHOW ALL', function_bot = hw_12.show_all, help_bot ='(part of the name or phone) - find matches by part of the name or phone number'))
    bot_commands.add_command(BotCommands(command_bot = 'EXIT', function_bot = hw_12.finish_work, help_bot =' finish work'))
    return bot_commands



def main():
    bot_commands = Commands()
    bot_commands = create_bot(bot_commands)
    bot_commands.print_halp()
    # address_book= AddressBook()
    hw_12.address_book = hw_12.start_work()

    while True:
        try:
            stp_user_input = input('<<<< ')
            list_user_input =stp_user_input.split()
            cw = list_user_input[0].upper()
            if cw == 'FIND' or cw == 'SHOW':
               cw= cw + ' ' +list_user_input[1].upper()
               list_user_input.pop(1)
               list_user_input[0]= cw
            if cw == 'FIND MATCHES':
                temp_book:AddressBook
                temp_book = bot_commands[cw].function_bot(*list_user_input)
                for i in temp_book.iterator(10):
                    print(i)
            else:
                print(bot_commands[cw].function_bot(*list_user_input))
            if cw == 'EXIT':
                break
        except KeyError:
            print('Wrong command. Try again')


if __name__ == "__main__":
    main()    



