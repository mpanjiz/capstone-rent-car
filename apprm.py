import authservice
import model
import trxservice
import pandas

def main () :
    responseAuth = model.RespAuth;
    responseData = model.RespData;
    responseAuth = authservice.auth()


    if (responseAuth.rc == '00') :
        responseAuth = authservice.auth()
        print(responseAuth.message)
    elif (responseAuth.rc == '01') :
        print(responseAuth.message)
        print('======================================================================')
        if (responseAuth.user.user_role == 'consumer') :
            aa = trxservice.welcomeConsumer()
        elif (responseAuth.user.user_role == 'admin') :
            print('as admin')
        else :
            print('role is not identified')        
    else :
        print(responseAuth.message)

main();