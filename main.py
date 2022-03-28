# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 18:51:47 2022

@author: musta
"""

#---------------KÜTÜPHANE--------------#
#--------------------------------------#
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from projeUI import *
from hakkindaUI import *
#---------------UYGULAMA OLUŞTUR--------------#
#---------------------------------------------#
Uygulama=QApplication(sys.argv)
penAna=QMainWindow()
ui=Ui_MainWindow()
ui.setupUi(penAna)
penAna.show()

"""penHakkinda=QDialog()
ui2=Ui_Dialog()
ui.setupUi(penHakkinda)"""

#---------------VERİTABANI OLUŞTUR--------------#
#-----------------------------------------------#

import sqlite3
global curs
global conn

conn=sqlite3.connect('veritabanı.db')
curs=conn.cursor()
sorguCreTbl=("CREATE TABLE IF NOT EXISTS mezar(   \
             Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, \
             AD TEXT NOT NULL,                          \
             SOYAD TEXT NOT NULL,           \
             MEZARLIK TEXT NOT NULL,    \
             FIYAT INTEGER NOT NULL,    \
             OLUM_TARIHI TEXT NOT NULL, \
             SON_ODEME TEXT NOT NULL )"
    )
curs.execute(sorguCreTbl)
conn.commit()

#---------------KAYDET--------------------------#
#-----------------------------------------------#
def EKLE():
    lneAd_=ui.lneAd.text()
    lneSoyad_=ui.lnesoyad.text()
    fiyat_=ui.fiyat.value()
    cmbmezarlik_=ui.cmbmezarlik.currentText()
    cw_tarih_=ui.cw_tarih.selectedDate().toString(QtCore.Qt.ISODate)
    cw_odeme_=ui.cw_odeme.selectedDate().toString(QtCore.Qt.ISODate)
    
    curs.execute("INSERT INTO mezar \
                 (AD,SOYAD,MEZARLIK,FIYAT,OLUM_TARIHI,SON_ODEME)\
                  VALUES(?,?,?,?,?,?)",\
                     (lneAd_,lneSoyad_,cmbmezarlik_,fiyat_,cw_tarih_,cw_odeme_))
    conn.commit()
    LISTELE()
#---------------LİSTELE--------------------------#
#------------------------------------------------#
def LISTELE():
    ui.tw_bilgiler.clear()
    ui.tw_bilgiler.setHorizontalHeaderLabels(('ID','AD','SOYAD','MEZARLIK','FIYAT','OLUM_TARIHI','SON_ODEME'))
    ui.tw_bilgiler.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    curs.execute("SELECT *FROM mezar")
    for satirIndex, satirVeri in enumerate(curs):
        for sutunIndex, sutunVeri in enumerate(satirVeri):
            ui.tw_bilgiler.setItem(satirIndex,sutunIndex,QTableWidgetItem(str(sutunVeri)))
    
    ui.lneAd.clear()
    ui.lnesoyad.clear()
    ui.cmbmezarlik.setCurrentIndex(-1)
    ui.fiyat.setValue(0)
    
    curs.execute("SELECT COUNT(*)FROM mezar")
    cnt=curs.fetchone()
    ui.lbl_kaysays.setText(str(cnt[0]))
    
    curs.execute("SELECT SUM(FIYAT) FROM mezar")
    total=curs.fetchone()
    ui.total.setText(str(total[0]))
LISTELE()
#---------------ÇIKIŞ---------------------------#
#-----------------------------------------------#
def CIKIS():
    cevap=QMessageBox.question(penAna,"ÇIKIŞ","Programdan çıkmak istediğinize emin misiniz?",\
                         QMessageBox.Yes|QMessageBox.No)
      
    if cevap==QMessageBox.Yes:
        conn.close()
        sys.exit(Uygulama.exec_())
    else:
        penAna.show()

#---------------SİL----------------------------------#
#----------------------------------------------------#
def SIL():
    cevap=QMessageBox.question(penAna,"KAYIT SİL","Kayıt silmek istediğinize emin misiniz?",\
                         QMessageBox.Yes|QMessageBox.No)
    if cevap==QMessageBox.Yes:
        secili=ui.tw_bilgiler.selectedItems()
        silinecek=secili[0].text()
        try:
            curs.execute("DELETE FROM mezar WHERE ID='%s'"%(silinecek))
            conn.commit()
            LISTELE()
            ui.statusbar.showMessage("Kayıt silme işlemi başarıyla gerçekleşti...",3000)
        except Exception as Hata:
            ui.statusbar.showMessage("Kayıt silme işlemi başarısız."+str(Hata))
    else:
        ui.statusbar.showMessage("Kayıt silme işlemi iptal edildi.",3000)
#---------------ARA----------------------------------#
#----------------------------------------------------#
def ARA():
    aranan1=ui.lneAd.text()
    aranan2=ui.lnesoyad.text()
    aranan3=ui.cmbmezarlik.currentText()
    curs.execute("SELECT* FROM mezar WHERE AD=? OR SOYAD=? OR MEZARLIK=? OR (AD=? AND SOYAD=?)",\
                 (aranan1,aranan2,aranan3,aranan1,aranan2))
    conn.commit()
    ui.tw_bilgiler.clear()
    for satirIndex, satirVeri in enumerate(curs):
        for sutunIndex, sutunVeri in enumerate(satirVeri):
            ui.tw_bilgiler.setItem(satirIndex,sutunIndex,QTableWidgetItem(str(sutunVeri)))
#---------------DOLDUR----------------------------------#
#-------------------------------------------------------#            
"""def DOLDUR():
    secili=ui.tw_bilgiler.selectedItems()
    ui.lneAd.setText(secili[1].text())
    ui.lnesoyad.setText(secili[2].text())
    ui.cmbmezarlik.setCurrentText(secili[3].text())
    ui.fiyat.setValue(int(secili[4].text()))
    yil=int(secili[5].text()[0:4])
    ay=int(secili[5].text()[5:7])
    gun=int(secili[5].text()[8:10])
    ui.cw_tarih.setSelectedDate(QtCore.QDate(yil,ay,gun))    
    
    yil1=int(secili[6].text()[0:4])
    ay1=int(secili[6].text()[5:7])
    gun1=int(secili[6].text()[8:10])
    ui.cw_tarih.setSelectedDate(QtCore.QDate(yil1,ay1,gun1))   """

#---------------GUNCELLE----------------------------------#
#---------------------------------------------------------# 
def GUNCELLE():
    cevap=QMessageBox.question(penAna,"Kayıt Güncelle","Kayıt güncellemek istediğinize emin misiniz ?",\
                               QMessageBox.Yes|QMessageBox.No)
    if cevap==QMessageBox.Yes:
        try:
            secili=ui.tw_bilgiler.selectedItems()
            _Id=int(secili[0].text())
            lneAd_=ui.lneAd.text()
            lneSoyad_=ui.lnesoyad.text()
            fiyat_=ui.fiyat.value()
            cmbmezarlik_=ui.cmbmezarlik.currentText()
            cw_tarih_=ui.cw_tarih.selectedDate().toString(QtCore.Qt.ISODate)
            cw_odeme_=ui.cw_odeme.selectedDate().toString(QtCore.Qt.ISODate)
            
            curs.execute("UPDATE mezar SET AD=?, SOYAD=?, MEZARLIK=?, FIYAT=?,SON_ODEME=?,OLUM_TARIHI=?,WHERE Id=?",\
                             (lneAd_,lneSoyad_,cmbmezarlik_,fiyat_,cw_odeme_,cw_tarih_,_Id))
            conn.commit()
            LISTELE()
        except Exception as Hata:
                ui.statusbar.showMessage("Şöyle bir hata meydana geldi "+str(Hata))
    else:
        ui.statusbar.showMessage("Güncelleme iptal edildi. ",3000)
        
#---------------HAKKINDA------------------------#
#-----------------------------------------------#
def HAKKINDA():
    penHakkinda.show()
    
            
#---------------SİNYAL-SLOT--------------------------#
#----------------------------------------------------#
ui.btn_ekle.clicked.connect(EKLE)
ui.btn_liste.clicked.connect(LISTELE)
ui.btn_cikis.clicked.connect(CIKIS)
ui.btn_sil.clicked.connect(SIL)
ui.btn_ara.clicked.connect(ARA)
#ui.tw_bilgiler.itemSelectionChanged.connect(DOLDUR)
ui.btn_guncelle.clicked.connect(GUNCELLE)
#ui.menuhakkinda.triggered.connect(HAKKINDA)
sys.exit(Uygulama.exec_())