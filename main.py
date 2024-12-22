from datetime import datetime
from collections import UserList
'''
Створити систему, яка буде працювати з повідомлення

Message(content: str, author: User, recepient: User, sending_time, receiving_time)
User(first_name, last_name, phone_number)

MessageSystem(messages):
    - додати метод, який буде діставати усі чати з нашої системи
'''

class User:
    def __init__(self, first_name: str, last_name: str, phone_number: str):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number

    def __str__(self):
        return f'{self.first_name} {self.last_name} | {self.phone_number}'
    
    def __repr__(self):
        return str(self)
        

class Message:
    def __init__(self, content: str, author: User, recepient: User):
        self.content = content
        self.author = author
        self.recepient = recepient
        self.sending_time = datetime.now()
        self.receiving_time = None

    def is_message_read(self) -> bool:
        return self.receiving_time is not None

    def mark_message_as_read(self):
        self.receiving_time = datetime.now()


class MessageSystem(UserList):
    def __init__(self, messages: list[Message] = []):
        super().__init__(messages)

    def get_all_chats(self, user: User) -> list[User]:
        user_set = set()
        # Перебрати усі повідомлення, які є в нашій системі
        for message in self:
            # В повідомленні потрібно дістати інформацію про відправника та отримувача
            author, recepient = message.author, message.recepient
            # Перевірити коли користувач є автором
            if user == author:
                user_set.add(recepient)
            # Перевірити коли користувач є отримувачем
            if user == recepient:
                user_set.add(author)

            # Перевірити коли користувач є автором та отримувачем
        return list(user_set)

user_john = User("John", "Doe", "1234567890")
user_jane = User("Jane", "Doe", "0987654321")

message_one = Message("Hello, Jane!", user_john, user_jane)
message_two = Message("Hello, John!", user_jane, user_john)
message_three = Message("How are you doing?", user_john, user_jane)

message_four = Message("Todo: finish homework", user_john, user_john)

messages = [message_one, message_two, message_three, message_four]

message_system = MessageSystem(messages)
print(message_system.get_all_chats(user_john))


# my_list = [1, 2, 3, 4]
# for i in my_list
# message_system = MessageSystem([1, 2, 3, 4])

# print(my_list)
# print(message_system)

# my_list.append(5)
# message_system.append(5)

# print(my_list)
# print(message_system)

# hello, world = [3, 4]
# print(hello)
# print(world)
