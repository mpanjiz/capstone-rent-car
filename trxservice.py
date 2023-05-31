import dbconnect
import model
# import apprm
import pandas as pd
import numpy as np
import datetime as dt

carOrdered = [];

def carsMenu (cityId, rentalDate, today) :
    response = model.RespData;
    sql = dbconnect.mysqlconnect();
    if sql.is_connected():
        result = None
        if (cityId == '') :
            queryGetInventory = "select car_name, type, release_year, stock, price from inventory"
            cursor = sql.cursor()
            cursor.execute(queryGetInventory)
            result = cursor.fetchall()
            sql.commit()
            cursor.close()
            sql.close()
        else :
            param = [today, today, rentalDate, cityId]
            queryGetInventory = """with x as (select 
                i.city_id as city_id,
                i.inventory_id as inventory_id,
                sum(t.numbers_of_cars) as total_unit
                from inventory i 
                right join `transaction` t on i.inventory_id = t.inventory_id 
                where 
                %s >= date(t.rental_date) and %s <= date(t.return_date)
                and %s > t.return_date
                group by t.inventory_id )
                select 
                i2.car_name,
                i2.`type`,
                i2.release_year,
                CASE
                    WHEN i2.stock + x.total_unit is null THEN i2.stock
                    ELSE i2.stock + x.total_unit
                END as total_unit,
                i2.price 
                from inventory i2 
                left join x on i2.city_id = x.city_id and i2.inventory_id = x.inventory_id 
                where i2.city_id = %s
                group by i2.inventory_id"""
            cursor = sql.cursor()
            cursor.execute(queryGetInventory, param)
            result = cursor.fetchall()
            sql.commit()
            cursor.close()
            sql.close()

        if (len(result) != 0) :
            headers=["Mobil", "Tipe", "Tahun Rilis", "Stok(Unit)", "Harga/hari(Rp)"]
            data = pd.DataFrame(result, columns = headers)

            response.rc = '00'
            response.message = 'Get Data Success'
            response.data = data

        else :
            response.rc = '01'
            response.message = 'Kendaraan Tidak Tersedia'
        
        return response;
    else :
        response.rc = '99'
        response.message = sql.msg;


def welcomeConsumer () :
    init = True
    while init :
        print('============== Selamat Datang di Rental mobil Juara ==============')
        print('1 : Pesan Rental Mobil')
        print('2 : Riwayat Pesanan')
        print('3 : lokasi operasional rental mobil')
        wOption = input("Pilih menu (1/2/3) : ")
        if (wOption == '1' or 
            wOption == '2' or 
            wOption == '3') :
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
            isLogoutCs()

        else :
            isLogoutCs()
    else :
        print('opsi lain');

def order() :
    responseData = model.RespData;
    lokasi =  getCityData()
    if (lokasi.rc == '00') :
        hLoc=["Kode", "Kota"]
        dataKota = pd.DataFrame(lokasi.data, columns = hLoc)
        print(dataKota)
        loc = input("Lokasi rental (ex: BD) : ")
        startDate = input("Tanggal Pengambilan (yyyy-mm-dd) : ")
        endDate = input("Tanggal Pengembalian (yyyy-mm-dd) : ")

        valid = False
        namaKota = ''
        locOrderAvailable = False
        for val in lokasi.data :
            if (val[0] == loc) :
                locOrderAvailable = True
                valid = True
                namaKota = val[1]
                break
        
        dateFormat = "%Y-%m-%d"
        dateValidation = False
        startDateObject:any
        endDateObject:any
        try:
            startDateObject = dt.datetime.strptime(startDate, dateFormat)
            endDateObject = dt.datetime.strptime(endDate, dateFormat)
            dateValidation = True
            valid = True
        except ValueError:
            valid = False
            dateValidation = False
        
        if (valid) :
            if (endDateObject < startDateObject) :
                print('Data input tanggal tidak sesuai, tanggal pengembalian kendaraan tidak bisa sebelum tanggal pengambilan kendaraan')
                isLogoutCs()
            else :
                today = dt.datetime.now().strftime("%Y-%m-%d")
                responseData = carsMenu(loc, startDate, today)
                if (responseData.rc == '00') :
                    print(responseData.data)
                    init = True
                    car:any
                    dataUnit = responseData.data.to_numpy()
                    while init :
                        car = input("Pilih kendaraan (nomor urut, ex: 0) : ")
                        unit = input("jumlah kendaraan yang akan disewa? (ex: 1) : ")
                        if(car.isnumeric() and unit.isnumeric()) :
                            car = int(car)
                            unit = int(unit)
                            if (car <= (len(dataUnit) - 1)) :
                                if (unit <= dataUnit[car][3]) :
                                    init = False
                                else :
                                    print('jumlah unit yang dipesan melebihi stok kendaraan yang tersedia')
                            else :
                                print('nomor urut tidak ada dalam daftar')    
                        else :
                            print('inputan harus berupa angka')
                    
                    lengthRent = endDateObject - startDateObject
                    totalCost = lengthRent.days * dataUnit[car][4]
                    ordered = [namaKota, dataUnit[car][0], dataUnit[car][1], unit, startDate, endDate, lengthRent.days, totalCost]
                    carOrdered.append(ordered)
                    print('-----------------------------------------------------------------------------------')
                    headerOrder = ["Lokasi", "Mobil", "Tipe", "Jumlah(Unit)","tanggal awal", "tanggal akhir", "Lama Sewa(hari)", "Total Biaya"]
                    dfOrder = pd.DataFrame(carOrdered, columns = headerOrder)
                    print(dfOrder)
                    print('-----------------------------------------------------------------------------------')
                    init3 = True
                    while init3 :
                        print('1 : Bayar')
                        print('2 : Ubah Pesanan')
                        print('3 : Batal')
                        lastOption = input("(1/2/3) : ")
                        if (lastOption == '1') :
                            payment()
                            print('Pemesanan dan Pembayaran Sewa Kendaraan Berhasil')
                            init3 = False
                        elif (lastOption == '2') :
                            print('update')
                        elif (lastOption == '3') :
                            carOrdered.clear()
                            init3 = False
                    
                    isLogoutCs()
                else :
                    print(responseData.message)
                    isLogoutCs()
        else :
            if (locOrderAvailable == False) :
                print('lokasi yang di pilih tidak tersedia')
                isLogoutCs()
            elif (dateValidation == False) :
                print("Format tanggal tidak sesuai, seharusnya dengan format YYYY-MM-DD")
                isLogoutCs()

    else :
        print(lokasi.message)
        isLogoutCs()


def updateOrder() :
    print('Field apa yang akan anda ubah?')
    print('1 : Lokasi')
    print('2 : Tanggal Rental')
    print('3 : Kendaraan')
    print('4 : Jumlah unit')


def payment() :
    print('proses insert transaction')
    carOrdered.clear()

def getCityData () :
    sql = dbconnect.mysqlconnect();
    responseData = model.RespData;
    if sql.is_connected():
        queryGetCity = "select a.city_id, a.city from city a order by a.city asc"
        cursor = sql.cursor()
        cursor.execute(queryGetCity)
        result = cursor.fetchall()
        sql.commit()
        cursor.close()
        sql.close()

        if (len(result) != 0) :
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

def isLogoutCs() :
    print('--------------------------------------------------')
    isLogout = input("Kembali ke menu utama? (yes/keluar) : ")
    noLogout = True
    while noLogout :
        if (isLogout == 'yes') :
            noLogout = False
            welcomeConsumer()
        elif (isLogout == 'keluar') :
            noLogout = False
        else :
            print('Maaf, input yang anda masukan di luar pilihan yang tersedia')