from datetime import datetime
from collections import UserList
import json
'''
Створити систему, яка буде працювати з повідомлення

Message(content: str, author: User, recepient: User, sending_time, receiving_time)
User(first_name, last_name, phone_number)

MessageSystem(messages):
    - додати метод, який буде діставати усі чати з нашої системи
    - додати метод, який буде виводити усі повідомлення між двома користувачами

При десеріалізації в нас буде проблема:
    що кожен користувач буде окремою сутністю

    Можна до кожного користувача додати унікальний ідентифікатор
'''
MESSAGES_JSON_FILE = "messages.json"

# user_id = 0
class User:
    id = 0

    def __init__(self, first_name: str, last_name: str, phone_number: str):
        User.id += 1
        self.id = User.id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number
        }

    def __str__(self):
        return f'{self.id} | {self.first_name} {self.last_name} | {self.phone_number}'
    
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

    def to_json(self) -> dict:
        return {
            "content": self.content,
            "sending_time": str(self.sending_time),
            "receiving_time": str(self.receiving_time),
            "author": self.author.to_json(),
            "recepient": self.recepient.to_json()
        }

    def __lt__(self, other) -> bool:
        return self.sending_time < other.sending_time

    def __str__(self):
        return f"Message from [{self.author}] to [{self.recepient}] \n '{self.content} {self.sending_time}'"
    
    def __repr__(self):
        return str(self)


class MessageSystem(UserList):
    def __init__(self, messages: list[Message] = []):
        super().__init__(messages)

    def get_messages_between_users(self, user_one: User, user_two: User) -> list[Message]:
        messages_set = set()
        # Перебрати усі повідомлення, які є в нашій системі
        for message in self:
            # В повідомленні потрібно дістати інформацію про відправника та отримувача
            author, recepient = message.author, message.recepient
            # Перевірити чи user_one є автором та user_two є отримувачем
            if author == user_one and recepient == user_two:
                messages_set.add(message)
            # Перевірити чи user_two є автором та user_one є отримувачем
            if author == user_two and recepient == user_one:
                messages_set.add(message)
        return sorted(list(messages_set))
    
    def save_to_file(self):
        with open(MESSAGES_JSON_FILE, 'w') as json_file:
            json.dump(self.data, json_file, default=lambda o: o.to_json(), indent=2)

    def read_from_json(self):
        # id_set = set() # {1, 2, 3, 4}
        # user_set = set() # {..., ..., ..., ...}
        # {1: User(...), 2: User(...)}
        users_dict = {}
        message_list = []
        # Прочитати json файл
        # Перебрати кожне повідомлення
            # Дістати автора та отримувача з повідомлення
            # Дістати їх id
            # Зробити перевірку чи такий користувач вже був:
                # Якщо був, то дістаємо з переліку
                # Якщо не був, то створюємо нового та додаємо до переліку
        with open(MESSAGES_JSON_FILE) as json_file:
            json_data = json.load(json_file)
            for message_dict in json_data:
                author = None
                recepient = None
                author_id, recepient_id = message_dict['author']['id'], message_dict['recepient']['id']
                if author_id in users_dict:
                    author = users_dict[author_id]
                else:
                    author_dict = message_dict['author']
                    author = User(author_dict['first_name'], author_dict['last_name'], author_dict['phone_number'])
                    author.id = author_dict['id']
                    users_dict[author.id] = author
                message_list.append(Message(message_dict['content'], author, None))
        return message_list


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
user_jack = User("Jack", "Doe", "0987654321")
# print(user_john.id)
# print(user_jane.id)
# print(user_jack.id)

# print(User.id)

# message_one = Message("Hello, Jane!", user_john, user_jane)
# message_two = Message("Hello, John!", user_jane, user_john)
message_one = Message("Hello, Jane!", user_john, user_jane)
message_two = Message("Hello, John!", user_jane, user_john)
message_three = Message("How are you doing?", user_john, user_jane)

message_four = Message("Todo: finish homework", user_john, user_john)
message_five = Message("Hello, I am Jack", user_jack, user_john)

# messages = [message_one, message_two, message_three, message_four, message_five]
# messages = [message_two, message_one, message_four, message_five, message_three, message_four]
# print(messages)
# messages.sort()
# print(messages)

message_system = MessageSystem()
# message_system.save_to_file()

print(message_system.read_from_json())
# print(message_system.get_all_chats(user_john))
# print(message_system.get_messages_between_users(user_john, user_jane))

# < > <= >= ==
#<

# message_four < message_five
# message_four.__lt__(message_five)

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

# print({"hello", "world", "people"})

# [1, 2, 3, 4]
# 1 < 2, 2 < 3, 3 < 4
