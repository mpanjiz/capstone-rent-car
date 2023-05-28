class User:  
        id_user:any
        username:any     
        password:any
        user_role:any;

class ExcecuteCursor:
        execute:any;

class Mysqldb:  
        connection:any
        cursor:ExcecuteCursor
        status:any    
        message:any;

class RespAuth:
        rc:any
        message:any
        user:User;
