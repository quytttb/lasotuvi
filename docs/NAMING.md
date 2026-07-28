# Python naming conventions (English + PEP 8)

Mục tiêu: toàn bộ **tên file / module / class / function / biến** dùng tiếng Anh, `snake_case` (PEP 8).  
Chuỗi hiển thị (UI/API labels) có thể giữ Hán Việt; thuật ngữ đối chiếu xem [TERMINOLOGY.md](./TERMINOLOGY.md).

## Rules

1. **Modules / files:** `snake_case.py` (không `AmDuong.py`, không viết hoa giữa tên).
2. **Classes:** `PascalCase` English (`EarthPlate`, `Palace`, `Star`).
3. **Functions / methods / variables:** `snake_case` English (`build_chart`, `life_palace`).
4. **Constants:** `UPPER_SNAKE_CASE` (`HEAVENLY_STEMS`, `EARTHLY_BRANCHES`).
5. **Không** dùng camelCase kiểu Java (`cungMenh`, `lapDiaBan`).
6. **Không** nhét Hán Việt không dấu vào identifier (`menh`, `cuc` chỉ chấp nhận tạm khi là acronym đã định nghĩa trong glossary — ưu tiên `life_palace`, `element_bureau`).

## Proposed file rename map

| Hiện tại | Đề xuất | Vai trò |
|---|---|---|
| `lasotuvi/AmDuong.py` | `lasotuvi/yin_yang.py` hoặc `stem_branch.py` | Can Chi, âm dương, ngũ hành, cục |
| `lasotuvi/DiaBan.py` | `lasotuvi/earth_plate.py` | 12 cung địa bàn |
| `lasotuvi/ThienBan.py` | `lasotuvi/heaven_plate.py` | Meta thiên bàn |
| `lasotuvi/Sao.py` | `lasotuvi/stars.py` | Định nghĩa sao |
| `lasotuvi/App.py` | `lasotuvi/chart_builder.py` | An sao / lập địa bàn |
| `lasotuvi/Lich_HND.py` | `lasotuvi/lunar_calendar.py` | Đổi lịch HND |
| `lasotuvi/Lich_EPHEM.py` | `lasotuvi/ephemeris_calendar.py` | Đổi lịch ephem |
| `api/sao_catalog.py` | `api/star_catalog.py` | Catalog tham chiếu |

Package name `lasotuvi` có thể giữ (brand) hoặc đổi `ziwei` / `zwds` ở phase riêng (breaking cho PyPI).

## Proposed symbol rename samples

| Hiện tại (camel / HV) | English PEP 8 |
|---|---|
| `thienCan` | `HEAVENLY_STEMS` |
| `diaChi` | `EARTHLY_BRANCHES` |
| `ngayThangNam` | `to_lunar_ymd` |
| `canChiNgay` | `day_stem_branch` |
| `timCuc` | `find_element_bureau` |
| `timTuVi` | `find_zi_wei_position` |
| `lapDiaBan` | `build_earth_plate` |
| `cungDiaBan` | `Palace` |
| `diaBan` | `EarthPlate` |
| `lapThienBan` | `HeavenPlate` / `build_heaven_plate` |
| `cungMenh` | `life_palace` |
| `cungThan` | `body_palace` |
| `cungSao` | `stars` |
| `saoDacTinh` | `brightness` |
| `cungDaiHan` | `major_period_age` |
| `cungTieuHan` | `annual_luck_branch` |
| `cungNguyetHan` | `monthly_luck` |
| `tuanTrung` | `is_xun` |
| `trietLo` | `is_triet` |
| `banMenh` | `natal_element_name` |
| `menhChu` | `life_master_star` |
| `thanChu` | `body_master_star` |
| `cach_cuc` / `analyze_cach_cuc` | `formation` / `detect_formations` |
| `luan_doan` / `analyze_palace` (KB) | `interpretation` / `interpret_palace` |
| `luan_doan.json` | `interpretations.json` |
| `get_related_palaces` | giữ (opposite + trines = san fang si zheng) |

## API JSON field strategy

Hai hướng (chọn một trước khi refactor API):

**A. Breaking (khuyến nghị nếu API chưa public rộng):** đổi field sang English  
`cung_menh` → `life_palace`, `cung_sao` → `stars`, `dac_tinh` → `brightness`.

**B. Tương thích:** giữ field Hán Việt trong JSON một thời gian, thêm alias English, deprecate dần.

Hiện API đang dùng `snake_case` nhưng còn key Hán Việt (`cung_menh`, `thap_nhi_cung`). Nên chuyển sang English keys theo hướng A khi rename core.

## Migration plan (status)

1. Done — Glossary: `docs/TERMINOLOGY.md`
2. Done — Naming map: `docs/NAMING.md`
3. Done — Core modules renamed to English filenames
4. Done — Identifiers → English PEP 8
5. Done — API v2 English JSON keys (`api` version **2.0.0**)
6. Done — Tests + frontend types updated
7. Done — Interpretation engine: `analysis.py`, `data/interpretations.json`, API fields `formations` / `interpretations`

### Interpretation module map

| File / symbol | Role |
|---|---|
| `lasotuvi/analysis.py` | `ChartAnalyzer` — detect formations, attach palace readings |
| `lasotuvi/data/interpretations.json` | Knowledge base (`formations`, `palaces`) |
| `EarthPlate.get_related_palaces` | Opposite + trines for san fang si zheng |
| API `formations` | List of `{code, name, description}` on chart / earth plate |
| API `palaces[].interpretations` | List of `{star, interpretation}` per palace |

> Display strings for stars/palaces may remain Vietnamese; code identifiers and JSON keys are English.
