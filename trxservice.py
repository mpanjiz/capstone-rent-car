import dbconnect
import model
# import apprm
import pandas as pd
import numpy as np

def menu () :
    response = model.RespData;
    sql = dbconnect.mysqlconnect();
    if sql.is_connected():
        queryGetInventory = "select car_name, type, release_year, stock, price from inventory"
        cursor = sql.cursor()
        cursor.execute(queryGetInventory)
        result = cursor.fetchall()
        sql.commit()
        cursor.close()
        sql.close()

        if (result != None) :
            headers=["Mobil", "Tipe", "Tahun Rilis", "Stok(Unit)", "Harga/hari(Rp)"]
            print(pd.DataFrame(result, columns = headers))

            response.rc = '00'
            response.message = 'Get Data'

        else :
            response.rc = '99'
            response.message = 'Get Data Failed'
        
        # response.user = user
        return response;
    else :
        print('failed connect db : ' + str(sql.msg))
        response.rc = '99'
        response.message = sql.msg;


def welcomeConsumer () :
    init = True
    while init :
        print('============== Selamat Datang di Rental mobil Juara ==============')
        print('1 : Pesan Rental Mobil')
        print('2 : Riwayat Pesanan')
        print('3 : lokasi operasional rental mobil')
        wOption = input("Pilih menu (1/2/3) ")
        if (wOption == '1' or 
            wOption == '2') :
            init = False
        else :
            print('Pilihan anda tida tersedia di daftar menu')
    
    if (wOption == '1') :
        order()
    elif (wOption == '2') :
        print('service riwayat pesanan')
    elif (wOption == '3') :
        print('servis lokasi operasional rental')
        lokasi =  getCityData()
        if (lokasi.rc == '00') :
            hLoc=["Kode", "Kota"]
            dataKota = pd.DataFrame(lokasi.data, columns = hLoc)
            print(dataKota)
            print('--------------------------------------------------')
            isLogout = input("Kembali ke menu utama? (yes/keluar)")
            noLogout = True
            while noLogout :
                if (isLogout == 'yes') :
                    noLogout = False
                    welcomeConsumer()
                elif (isLogout == 'keluar') :
                    noLogout = False
                    # apprm.main()
                else :
                    print('Maaf, input yang anda masukan di luar pilihan yang tersedia')

        else :
            print(lokasi.message)
            print('--------------------------------------------------')
            isLogout = input("Kembali ke menu utama? (yes/keluar)")
            noLogout = True
            while noLogout :
                if (isLogout == 'yes') :
                    noLogout = False
                    welcomeConsumer()
                elif (isLogout == 'keluar') :
                    noLogout = False
                    # apprm.main()
                else :
                    print('Maaf, input yang anda masukan di luar pilihan yang tersedia')
    else :
        print('opsi lain');

def order() :
    carOrdered = [];
    lokasi =  getCityData()
    if (lokasi.rc == '00') :
        hLoc=["Kode", "Kota"]
        dataKota = pd.DataFrame(lokasi.data, columns = hLoc)
        print(dataKota)
        loc = input("Lokasi rental : (ex: 1)")
        startDate = input("Tanggal Pengambilan : (dd-mm-yyyy)")
        endDate = input("Tanggal Pengembalian : (dd-mm-yyyy)")
        print(lokasi.data)
        for val in lokasi.data :
            print(val[0] == 'BD')
            if (val[0] == 'BD') :
                break

    else :
        print(lokasi.message)
        print('--------------------------------------------------')
        isLogout = input("Kembali ke menu utama? (yes/keluar)")
        noLogout = True
        while noLogout :
            if (isLogout == 'yes') :
                noLogout = False
                welcomeConsumer()
            elif (isLogout == 'keluar') :
                noLogout = False
                # apprm.main()
            else :
                print('Maaf, input yang anda masukan di luar pilihan yang tersedia')


def updateOrder() :
    print('update order');    

def orderChart() :
    print('order');

def getCityData () :
    sql = dbconnect.mysqlconnect();
    responseData = model.RespData;
    if sql.is_connected():
        queryGetCity = "select a.city_code, a.city from city a order by a.city asc"
        cursor = sql.cursor()
        cursor.execute(queryGetCity)
        result = cursor.fetchall()
        sql.commit()
        cursor.close()
        sql.close()

        if (result != None) :
            responseData.rc = '00'
            responseData.message = 'Success'
            responseData.data = result
        else :
            responseData.rc = '01'
            responseData.message = 'Daftar Kota Tidak Tersedia'
        
        return responseData
    else :
        responseData.rc = '99'
        responseData.message = 'Gagal, ' + sql.msg
        return responseData
