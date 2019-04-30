import sqlite3
from telebot import types

bot_state = 0
db = "rating.db"

def get_user_status(user_telegram_id=None):
    conn = sqlite3.connect(db)  # Подключаемся к БД
    cursor = conn.cursor()  # Создаём курсор для работы с ней. Он будет выполнять наши команды
    cursor.execute('SELECT status FROM users WHERE user_id=:userID',
                           {'userID': user_telegram_id})  # Ищем в БД пользователя с ID из телеграмма
    user_data = cursor.fetchone()  # Беррём найденную строку
    cursor.close()  # Отключаемся от БД
    conn.close()
    if user_data:
        return int(user_data[0])
    else:
        return 0

def names():
    conn = sqlite3.connect(db)  # Подключаемся к БД
    cursor = conn.cursor()  # Создаём курсор для работы с ней. Он будет выполнять наши команды
    cursor.execute('SELECT name FROM users WHERE user_id=0',)  # Ищем в БД пользователя ,без ID из телеграмма
    user_data = cursor.fetchall()  # Беррём найденную строку
    cursor.close()  # Отключаемся от БД
    conn.close()
    return [types.InlineKeyboardButton(text=str(x[0]), callback_data=str(x[0])) for x in user_data]

def save_id(user_telegram_id, name):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET user_id=:user_telegram_id WHERE name=:name',
                   {'name': name, 'user_telegram_id': user_telegram_id})
    conn.commit()
    cursor.close()
    conn.close()

def set_user_status(user_telegram_id, new_state):
    conn = sqlite3.connect(db)  # Подключаемся к БД
    cursor = conn.cursor()  # Создаём курсор для работы с ней. Он будет выполнять наши команды
    cursor.execute('UPDATE users SET status=:status WHERE user_id=:user_telegram_id',
                       {'status': new_state, 'user_telegram_id': user_telegram_id})
    conn.commit()
    cursor.close()
    conn.close()  # Отключаемся от БД

def buttons(user_telegram_id):
    conn = sqlite3.connect(db)  # Подключаемся к БД
    cursor = conn.cursor()  # Создаём курсор для работы с ней. Он будет выполнять наши команды
    cursor.execute('SELECT name FROM users WHERE team=(SELECT team FROM users WHERE user_id=:userID) AND user_id<>:userID AND student=0', {'userID': user_telegram_id})
    teams_data = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return [types.InlineKeyboardButton(text=str(x[0]), callback_data=str(x[0])) for x in teams_data ]

def get_student_status(name):
    conn = sqlite3.connect(db)  # Подключаемся к БД
    cursor = conn.cursor()  # Создаём курсор для работы с ней. Он будет выполнять наши команды
    cursor.execute(
        'SELECT student FROM users WHERE name=:name',
        {'name': name})
    student_data = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return int(student_data[0])

def save(user_telegram_id, c):
    conn = sqlite3.connect(db)  # Подключаемся к БД
    cursor = conn.cursor()  # Создаём курсор для работы с ней. Он будет выполнять наши команды
    cursor.execute('UPDATE users SET student=:userID WHERE name=:name',
                       {'name': c, 'userID': user_telegram_id})
    conn.commit()
    cursor.execute('SELECT id, quest FROM questions')
    teams_data = cursor.fetchall()
    cursor.close()
    conn.close()
    return [types.InlineKeyboardButton(text=str(x[1]), callback_data=int(x[0])) for x in teams_data]

def save_student(user_telegram_id, c):
    conn = sqlite3.connect(db)  # Подключаемся к БД
    cursor = conn.cursor()  # Создаём курсор для работы с ней. Он будет выполнять наши команды
    cursor.execute('SELECT id, quest, cost FROM questions')
    teams_data = cursor.fetchall()
    if int(c) < 0:
        cursor.close()
        conn.close()
        return [types.InlineKeyboardButton(text=str(x[1]), callback_data=int(x[0])) for x in teams_data]
    cursor.execute('SELECT q1, q2, q3, q4, q5 FROM users WHERE student=:userID', {'userID': user_telegram_id})
    result_data = cursor.fetchone()
    result_data = list(result_data)
    if result_data[int(c)-1] == 0:
        result_data[int(c)-1] = teams_data[int(c)-1][2]
    else:
        result_data[int(c) - 1] = 0
    cursor.execute('UPDATE users SET q1=:q1, q2=:q2, q3=:q3, q4=:q4, q5=:q5 WHERE student=:userID',
                   {'userID': user_telegram_id, 'q1': result_data[0], 'q2': result_data[1], 'q3': result_data[2],
                    'q4': result_data[3], 'q5': result_data[4]})
    conn.commit()
    cursor.close()
    conn.close()
    z = []
    for x in teams_data:
        if result_data[int(x[0])-1]:
            z.append(types.InlineKeyboardButton(text='👌 ' + str(x[1]), callback_data=int(x[0])))
        else:
            z.append(types.InlineKeyboardButton(text=str(x[1]), callback_data=int(x[0])))
    return z

def save_self(user_telegram_id, c):
    conn = sqlite3.connect(db)  # Подключаемся к БД
    cursor = conn.cursor()  # Создаём курсор для работы с ней. Он будет выполнять наши команды
    cursor.execute('SELECT id, quest, cost FROM questions')
    teams_data = cursor.fetchall()
    cursor.execute('SELECT s1, s2, s3, s4, s5 FROM users WHERE user_id=:userID', {'userID': user_telegram_id})
    result_data = cursor.fetchone()
    result_data = list(result_data)
    print(result_data)
    if result_data[int(c)-1] == 0:
        result_data[int(c)-1] = teams_data[int(c)-1][2]
    else:
        result_data[int(c) - 1] = 0
    cursor.execute('UPDATE users SET s1=:q1, s2=:q2, s3=:q3, s4=:q4, s5=:q5 WHERE user_id=:userID',
                   {'userID': user_telegram_id, 'q1': result_data[0], 'q2': result_data[1], 'q3': result_data[2],
                    'q4': result_data[3], 'q5': result_data[4]})
    conn.commit()
    cursor.close()
    conn.close()
    z = []
    for x in teams_data:
        if result_data[int(x[0])-1]:
            z.append(types.InlineKeyboardButton(text='👌 ' + str(x[1]), callback_data=int(x[0])))
        else:
            z.append(types.InlineKeyboardButton(text=str(x[1]), callback_data=int(x[0])))
    return z

def save_delete_message(user_telegram_id, message_id):
    conn = sqlite3.connect(db)  # Подключаемся к БД
    cursor = conn.cursor()  # Создаём курсор для работы с ней. Он будет выполнять наши команды
    cursor.execute(
        'SELECT message FROM delete_t WHERE user_id=:userID',
        {'userID': user_telegram_id})
    student_data = cursor.fetchone()
    if student_data:
        cursor.execute('UPDATE delete_t SET message=:message WHERE user_id=:userID',
                       {'userID': user_telegram_id, 'message': message_id})
    else:
        cursor.execute('INSERT INTO delete_t (user_id, message) VALUES (?, ?)', (user_telegram_id, message_id))
    conn.commit()
    cursor.close()
    conn.close()

def get_delete_message(user_telegram_id):
    conn = sqlite3.connect(db)  # Подключаемся к БД
    cursor = conn.cursor()  # Создаём курсор для работы с ней. Он будет выполнять наши команды
    cursor.execute(
        'SELECT message FROM delete_t WHERE user_id=:userID',
        {'userID': user_telegram_id})
    student_data = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return int(student_data[0])

def names_and_marks(name):
    conn = sqlite3.connect(db)  # Подключаемся к БД
    cursor = conn.cursor()  # Создаём курсор для работы с ней. Он будет выполнять наши команды
    cursor.execute('UPDATE users SET teacher=teacher+1 WHERE name=:name', {'name': name})
    conn.commit()
    cursor.execute('SELECT name, teacher FROM users WHERE user_id=0',)  # Ищем в БД пользователя ,без ID из телеграмма
    user_data = cursor.fetchall()  # Беррём найденную строку
    cursor.close()  # Отключаемся от БД
    conn.close()
    return [types.InlineKeyboardButton(text=str(x[0])+' +'+str(x[1]), callback_data=str(x[0])) for x in user_data]

def result():
    conn = sqlite3.connect(db)  # Подключаемся к БД
    cursor = conn.cursor()  # Создаём курсор для работы с ней. Он будет выполнять наши команды
    cursor.execute('SELECT name, q1+q2+q3+q4+q5+s1+s2+s3+s4+s5, teacher FROM users ',)  # Ищем в БД пользователя ,без ID из телеграмма
    user_data = cursor.fetchall()  # Беррём найденную строку
    cursor.close()  # Отключаемся от БД
    conn.close()
    return '\n'.join([x[0] + '   ' + str(x[1] // 2 + x[2]) for x in user_data])
