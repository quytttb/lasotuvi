# Naming conventions — Pinyin + structural English (option 2)

Mục tiêu: identifier **PEP 8** (`snake_case` / `PascalCase` / `UPPER_SNAKE`), theo **chuẩn quốc tế Zi Wei Dou Shu**.

## Rules

1. **Sao, thần sát, tứ hóa, tên riêng domain** → **Pinyin**  
   `ZI_WEI`, `TAI_YANG`, `WU_QU`, `hua_lu`, `zi_wei`, `find_tian_kui`
2. **Khái niệm cấu trúc lá số** → **English ổn định**  
   `life_palace`, `body_palace`, `earth_plate`, `stem_branch`, `palace`, `stars`
3. **Độ sáng / cục / hạn** → **Pinyin** (không dịch literal)  
   `miao_wang`, `wu_xing_ju`, `da_xian_age`, `xiao_xian_branch`, `yue_xian`
4. **Modules / files:** `snake_case.py`
5. **Classes:** `PascalCase` (`EarthPlate`, `Palace`, `Star`, `HeavenPlate`)
6. **Display strings (UI):** có thể giữ Hán Việt cho user VN
7. **Không** dịch sao ra literal English (`emperor_star`, `sun_star`, …)
8. **Không** dùng Vietnamese không dấu cho tên sao (`tu_vi`, `thai_duong` làm identifier)

## Why Pinyin for stars

International ZWDS / Feng Shui / BaZi literature keeps Pinyin (Zi Wei, Tian Fu, Qi Sha) to preserve meaning, stay interoperable, and avoid confusion with Western astrology “Sun/Moon”.

## Module map (current)

| File | Role |
|------|------|
| `stem_branch.py` | Gan–Zhi, Wu Xing, Wu Xing Ju |
| `earth_plate.py` | 地盤 — 12 palaces |
| `heaven_plate.py` | Chart meta / 天盤 info |
| `stars.py` | Star definitions (Pinyin constants) |
| `chart_builder.py` | Place stars / build plate |
| `lunar_calendar.py` / `ephemeris_calendar.py` | Calendar |

## Domain field map (Pinyin)

| Concept (Hán Việt) | Identifier |
|--------------------|------------|
| Miếu/Vượng/Đắc/Bình/Hãm | `miao_wang` (values `M`/`V`/`Đ`/`B`/`H`) |
| Ngũ hành cục | `wu_xing_ju`, `wu_xing_ju_name` |
| Đại hạn | `da_xian_age` |
| Tiểu hạn | `xiao_xian_branch` |
| Nguyệt hạn | `yue_xian` |
| Tuần / Triệt | `is_xun`, `is_triet` |
| Trường sinh vòng | `is_chang_sheng` |
| Mệnh chủ / Thân chủ | `ming_zhu`, `shen_zhu` |
| Bản mệnh / Nạp âm | `ben_ming_name`, `nayin` |
| Sinh khắc | `sheng_ke_status` |
| Cung Mệnh / Thân | `life_palace`, `body_palace` (structural EN) |

## Function rename map

| Previous | Pinyin-aligned |
|----------|----------------|
| `find_element_bureau` | `find_wu_xing_ju` |
| `apply_star_brightness` | `apply_star_miao_wang` |
| `set_brightness` | `set_miao_wang` |
| `assign_major_periods` | `assign_da_xian` |
| `assign_annual_luck` | `assign_xiao_xian` |
| `set_major_period` | `set_da_xian` |
| `set_annual_luck` | `set_xiao_xian` |

## API

JSON keys follow the same map (breaking). Version remains **2.x**; document as Pinyin alignment pass.

See also [TERMINOLOGY.md](./TERMINOLOGY.md).
