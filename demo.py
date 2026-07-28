#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Demo chương trình lập lá số tử vi
"""
from lasotuvi.DiaBan import diaBan
from lasotuvi.ThienBan import lapThienBan
from lasotuvi.App import lapDiaBan

# Thông tin người dùng
ngay_sinh = 15      # Ngày sinh
thang_sinh = 8      # Tháng sinh
nam_sinh = 1990     # Năm sinh
gio_sinh = 1        # Giờ sinh (1=Tý, 2=Sửu, 3=Dần, 4=Mão, 5=Thìn, 6=Tỵ, 7=Ngọ, 8=Mùi, 9=Thân, 10=Dậu, 11=Tuất, 12=Hợi)
gioi_tinh = 1       # 1: Nam, -1: Nữ
duong_lich = True   # True: Dương lịch, False: Âm lịch
time_zone = 7       # Múi giờ Việt Nam
ten = "Demo"        # Tên

print("="*60)
print("CHƯƠNG TRÌNH LẬP LÁ SỐ TỬ VI")
print("="*60)
print(f"\nThông tin:")
print(f"- Ngày sinh: {ngay_sinh}/{thang_sinh}/{nam_sinh}")
print(f"- Giờ sinh: {gio_sinh}")
print(f"- Giới tính: {'Nam' if gioi_tinh == 1 else 'Nữ'}")
print(f"- Lịch: {'Dương lịch' if duong_lich else 'Âm lịch'}")

# Tạo địa bàn
print("\n" + "="*60)
print("ĐANG LẬP ĐỊA BÀN...")
print("="*60)
dia_ban = lapDiaBan(diaBan, ngay_sinh, thang_sinh, nam_sinh, gio_sinh, 
                   gioi_tinh, duong_lich, time_zone)

# Tạo thiên bàn
print("\n" + "="*60)
print("ĐANG LẬP THIÊN BÀN...")
print("="*60)
thien_ban = lapThienBan(ngay_sinh, thang_sinh, nam_sinh, 
                       gio_sinh, gioi_tinh, ten, dia_ban, duong_lich, time_zone)

print("\n" + "="*60)
print("ĐỊA BÀN - THÔNG TIN CÁC CUNG")
print("="*60)

# In thông tin các cung trong địa bàn
cung_names = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

for i in range(1, 13):
    cung = dia_ban.thapNhiCung[i]
    print(f"\nCung {cung_names[i-1]}:")
    if hasattr(cung, 'cungChu'):
        print(f"  - Cung chủ: {cung.cungChu}")
    if hasattr(cung, 'cungSao') and cung.cungSao:
        ten_sao_list = []
        for s in cung.cungSao:
            if 'tenSao' in s:
                ten_sao_list.append(s['tenSao'])
        if ten_sao_list:
            print(f"  - Các sao: {', '.join(ten_sao_list)}")

print("\n" + "="*60)
print("THIÊN BÀN - THÔNG TIN")
print("="*60)
print(f"Tên: {thien_ban.ten}")
print(f"Ngày Dương: {thien_ban.ngayDuong}/{thien_ban.thangDuong}/{thien_ban.namDuong}")
print(f"Ngày Âm: {thien_ban.ngayAm}/{thien_ban.thangAm}/{thien_ban.namAm}")
print(f"Giờ sinh: {thien_ban.gioSinh}")
print(f"Giới tính: {thien_ban.namNu}")
print(f"Can năm: {thien_ban.canNamTen}")
print(f"Chi năm: {thien_ban.chiNamTen}")
print(f"Bản mệnh: {thien_ban.banMenh}")
print(f"Cục: {thien_ban.tenCuc}")
print(f"Âm dương: {thien_ban.amDuongNamSinh}")
print(f"Sinh khắc: {thien_ban.sinhKhac}")

print("\n" + "="*60)
print("HOÀN THÀNH!")
print("="*60)
