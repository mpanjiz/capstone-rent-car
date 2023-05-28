import getpass;
import uuid;
import bcrypt;
import model
from model import *
import dbconnect
from dbconnect import *
import pprint
from pprint import pprint

def auth() :
    init = True
    qOption = ''
    response = model.RespAuth;
    while init :
        qOption = input("Login/Daftar ke car rent Apps? (login/daftar) ")
        init = conditionQ1(qOption)
    
    if (qOption.lower() == 'login') :
        response = authLogin()
    elif (qOption.lower() == 'daftar') :
        response = authRegister()
    return response;

def conditionQ1(param) :
    if (param.lower() == 'daftar') :
        return False
    elif (param.lower() == 'login') :
        return False
    else :
        print('Maaf, input yang anda masukan di luar pilihan yang tersedia')
        return True

def authRegister() :
    print('Silahkan masukan username dan password akun baru anda')
    response= model.RespAuth;
    
    username = input("username : ")
    password = getpass.getpass("password:")
    userId = uuid.uuid4();

    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    user = model.User()

    user.id_user = str(userId)
    user.username = str(username)
    user.password = hash
    # user.password = str(password)
    user.user_role = 'consumer'

    sql = dbconnect.mysqlconnect();
    if sql.is_connected():
        # queryInsert = "INSERT INTO users (id_user, username, password, user_role) VALUES('{}', '{}', '{}', '{}')".format(user.id_user, user.username, user.password, user.user_role)
        queryInsert = "INSERT INTO users (id_user, username, password, user_role) VALUES(%s, %s, %s, %s)"
        data = (user.id_user, user.username, user.password, user.user_role)
        cursor = sql.cursor()
        cursor.execute(queryInsert, data)
        sql.commit()
        cursor.close()
        sql.close()
        response.rc = '00'
        response.message = 'Pendaftaran Akun berhasil'
        response.user = user
        return response;
    else :
        response.rc = '99'
        response.message = sql.msg


def authLogin() :
    print('login')
    response= model.RespAuth;
    user = model.User()

    username = input("username : ")
    password = getpass.getpass("password:")

    sql = dbconnect.mysqlconnect();
    if sql.is_connected():
        queryGetUser = "select * from users where username = '{}'".format(username)
        cursor = sql.cursor()
        cursor.execute(queryGetUser)
        result = cursor.fetchone()
        sql.commit()
        cursor.close()
        sql.close()

        if (result != None) :
            passCode = password.encode('utf-8')
            enc = result[2].encode('utf-8')
            checked = bcrypt.checkpw(passCode, enc)

            if (checked == True) :
                user.username = username
                user.user_role = result[3]
                response.rc = '01'
                response.message = 'Login Success'
                response.user = user
            else :
                response.rc = '99'
                response.message = 'Login Failed'
        else :
            response.rc = '99'
            response.message = 'Login Failed'
        
        # response.user = user
        return response;
    else :
        print('failed connect db : ' + str(sql.msg))
        response.rc = '99'
        response.message = sql.msg

