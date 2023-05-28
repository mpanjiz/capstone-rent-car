import authservice
from authservice import *

def main () :
    response = model.RespAuth;
    response = authservice.auth()

    if (response.rc == '00') :
        response = authservice.auth()
        print(response.message)
    elif (response.rc == '01') :
        print(response.message)
    else :
        print(response.message)

main();