from cryptography.fernet import Fernet
import mysql.connector as sql

key = 'D9QRguYyat5TWlIyfg9AFWizc91muAGD-UlpWHxT0Y8='

db = sql.connect(
    host = 'localhost',
    username = 'root',
    password = 'stooby',
    database = 'notTalabat'
)
cursor = db.cursor()
f=Fernet(key)

def login(username, password):
    cursor.execute(f'select password from userdata where username = \'{username}\'')
    encpassword = cursor.fetchall()[0][0]
    output = f.decrypt(encpassword.encode())
    if password == output.decode():
        return True

def register(username, password, name):
    password = f.encrypt(password.encode())
    cursor.execute(f'insert into userdata values (\'{password.decode()}\', \'{username}\', \'{name}\')')
    db.commit()
    return True

def check(username):
    cursor.execute(f'select * from userdata where username = \'{username}\'')
    output = cursor.fetchall()
    if output != []:
        output = output[0]
        return True, output[2]
    else:
        return False, None

def retrieve(username):
    cursor.execute(f'select * from data where username = \'{username}\'')
    output = cursor.fetchall()
    return output[0]

def getRestaurants():
    cursor.execute('select * from restaurants')
    output = cursor.fetchall()
    return output


cursor.execute('insert into restaurants values(\'B\', "{\'Veggie Exotica\': 69.00, \'Chicken BBQ\': 73.00, \'Margerita\': 55.00}", "{\'Location\': \'Lulu Hypermarket, Maysaloon\', \'Phone\': \'+971 4 4444 444\', \'Website\': \'www.restaurant.com\', \'Opening Hours\': \'9:00 - 21:00\', \'Cuisine\': \'Italian\', \'Rating\': \"4.5\"}")')