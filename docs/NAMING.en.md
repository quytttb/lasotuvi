# Naming conventions — Pinyin and structural English

[Bản tiếng Việt](NAMING.md)

Identifiers follow PEP 8: `snake_case`, `PascalCase`, and `UPPER_SNAKE_CASE`.

## Rules

1. Use **Pinyin** for stars, deities, Four Transformations, and other proper domain names: `ZI_WEI`, `TAI_YANG`, `WU_QU`, `hua_lu`, `zi_wei`, `find_tian_kui`.
2. Use stable **English** for chart structure: `life_palace`, `body_palace`, `earth_plate`, `stem_branch`, `palace`, `stars`.
3. Use **Pinyin**, not literal translations, for brightness, bureaux, and luck cycles: `miao_wang`, `wu_xing_ju`, `da_xian_age`, `xiao_xian_branch`, `yue_xian`.
4. Files use `snake_case.py`; classes use `PascalCase`, for example `EarthPlate`, `Palace`, `Star`, and `HeavenPlate`.
5. User-facing Vietnamese/Hán Việt strings remain separate from machine-facing identifiers.
6. Do not translate star names into literal English identifiers and do not use unaccented Vietnamese identifiers.

Pinyin preserves the terminology used internationally in Zi Wei Dou Shu, Feng Shui, and BaZi literature and avoids confusion with Western-astrology terms such as “Sun” and “Moon”.

## Canonical mappings

| Domain concept | Identifier |
|---|---|
| Miao/Wang/De/Ping/Xian brightness | `miao_wang` (`M`/`V`/`Đ`/`B`/`H`) |
| Five-Element Bureau | `wu_xing_ju`, `wu_xing_ju_name` |
| Major, annual, monthly luck | `da_xian_age`, `xiao_xian_branch`, `yue_xian` |
| Xun / Triet | `is_xun`, `is_triet` |
| Twelve Stages of Life | `is_chang_sheng` |
| Life ruler / body ruler | `ming_zhu`, `shen_zhu` |
| Natal element / Nayin | `ben_ming_name`, `nayin` |
| Generating and controlling relationship | `sheng_ke_status` |
| Life / Body Palace | `life_palace`, `body_palace` |

## Function renames

| Previous | Pinyin-aligned |
|---|---|
| `find_element_bureau` | `find_wu_xing_ju` |
| `apply_star_brightness` | `apply_star_miao_wang` |
| `set_brightness` | `set_miao_wang` |
| `assign_major_periods` | `assign_da_xian` |
| `assign_annual_luck` | `assign_xiao_xian` |
| `set_major_period` | `set_da_xian` |
| `set_annual_luck` | `set_xiao_xian` |
