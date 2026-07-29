# Quy ước đặt tên — Pinyin và tiếng Anh cấu trúc

## Tiếng Việt

Mục tiêu: identifier tuân theo PEP 8 (`snake_case`, `PascalCase`, `UPPER_SNAKE_CASE`) và dùng thuật ngữ quốc tế của Zi Wei Dou Shu một cách nhất quán.

### Quy tắc

1. **Sao, thần sát, tứ hóa và tên riêng domain** dùng **Pinyin**: `ZI_WEI`, `TAI_YANG`, `WU_QU`, `hua_lu`, `zi_wei`, `find_tian_kui`.
2. **Khái niệm cấu trúc lá số** dùng **tiếng Anh ổn định**: `life_palace`, `body_palace`, `earth_plate`, `stem_branch`, `palace`, `stars`.
3. **Độ sáng, cục và hạn** dùng **Pinyin**, không dịch sát nghĩa: `miao_wang`, `wu_xing_ju`, `da_xian_age`, `xiao_xian_branch`, `yue_xian`.
4. Module và tệp dùng `snake_case.py`; class dùng `PascalCase`, ví dụ `EarthPlate`, `Palace`, `Star`, `HeavenPlate`.
5. Chuỗi hiển thị có thể dùng Hán Việt cho người dùng Việt Nam; phải tách biệt với identifier máy đọc.
6. Không dịch sao thành English literal, ví dụ `emperor_star` hoặc `sun_star`; không dùng tên sao tiếng Việt không dấu, ví dụ `tu_vi`, `thai_duong`.

### Vì sao dùng Pinyin cho tên sao

Tài liệu Zi Wei Dou Shu, Phong Thủy và Bát Tự quốc tế thường giữ Pinyin (Zi Wei, Tian Fu, Qi Sha). Cách này bảo toàn nghĩa, tăng khả năng tương tác và tránh nhầm với thuật ngữ chiêm tinh phương Tây như “Sun” hoặc “Moon”.

### Ánh xạ module hiện tại

| Tệp | Vai trò |
|---|---|
| `stem_branch.py` | Gan–Zhi, Wu Xing, Wu Xing Ju |
| `earth_plate.py` | 地盤 — 12 cung |
| `heaven_plate.py` | Thông tin thiên bàn / meta lá số |
| `stars.py` | Định nghĩa sao, hằng Pinyin |
| `chart_builder.py` | An sao và dựng bàn |
| `lunar_calendar.py` / `ephemeris_calendar.py` | Lịch |

### Ánh xạ trường domain

| Khái niệm Hán Việt | Identifier |
|---|---|
| Miếu/Vượng/Đắc/Bình/Hãm | `miao_wang` (giá trị `M`/`V`/`Đ`/`B`/`H`) |
| Ngũ hành cục | `wu_xing_ju`, `wu_xing_ju_name` |
| Đại hạn / Tiểu hạn / Nguyệt hạn | `da_xian_age`, `xiao_xian_branch`, `yue_xian` |
| Tuần / Triệt | `is_xun`, `is_triet` |
| Vòng Trường Sinh | `is_chang_sheng` |
| Mệnh chủ / Thân chủ | `ming_zhu`, `shen_zhu` |
| Bản mệnh / Nạp âm | `ben_ming_name`, `nayin` |
| Sinh khắc | `sheng_ke_status` |
| Cung Mệnh / Thân | `life_palace`, `body_palace` |

### Đổi tên hàm

| Tên cũ | Tên theo quy ước |
|---|---|
| `find_element_bureau` | `find_wu_xing_ju` |
| `apply_star_brightness` | `apply_star_miao_wang` |
| `set_brightness` | `set_miao_wang` |
| `assign_major_periods` | `assign_da_xian` |
| `assign_annual_luck` | `assign_xiao_xian` |
| `set_major_period` | `set_da_xian` |
| `set_annual_luck` | `set_xiao_xian` |

Khóa JSON API tuân theo cùng ánh xạ này. API vẫn thuộc dòng phiên bản **2.x**; mọi thay đổi khóa phải được ghi rõ là thay đổi không tương thích. Xem thêm [Thuật ngữ](TERMINOLOGY.md).

---

## English

Identifiers follow PEP 8: `snake_case`, `PascalCase`, and `UPPER_SNAKE_CASE`.

1. Use **Pinyin** for stars, deities, Four Transformations, and other proper domain names: `ZI_WEI`, `TAI_YANG`, `WU_QU`, `hua_lu`, `zi_wei`, `find_tian_kui`.
2. Use stable **English** for chart structure: `life_palace`, `body_palace`, `earth_plate`, `stem_branch`, `palace`, `stars`.
3. Use **Pinyin**, not literal translations, for brightness, bureaux, and luck cycles: `miao_wang`, `wu_xing_ju`, `da_xian_age`, `xiao_xian_branch`, `yue_xian`.
4. Files use `snake_case.py`; classes use `PascalCase`, for example `EarthPlate`, `Palace`, `Star`, and `HeavenPlate`.
5. User-facing Vietnamese/Hán Việt strings remain separate from machine-facing identifiers.

Do not translate star names into literal English identifiers and do not use unaccented Vietnamese identifiers. The tables above are the canonical mapping for the current codebase and API JSON keys. Pinyin preserves the terminology used internationally in Zi Wei Dou Shu, Feng Shui, and BaZi literature and avoids confusion with Western-astrology terms such as “Sun” and “Moon”.
