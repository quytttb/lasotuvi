# Thuật ngữ Tử Vi Đẩu Số

[English version](TERMINOLOGY.en.md)

Tài liệu đối chiếu **Hán Việt ↔ 繁體中文 ↔ English** dùng trong dự án `lasotuvi`. Tiếng Việt là ngôn ngữ chính; cột tiếng Anh hỗ trợ đối chiếu thuật ngữ, API và mã nguồn.

Nguồn tham chiếu chính (tra cứu năm 2026):

- [sǹg-miā — ZWDS Glossary (EN)](https://sng-mia.com/en/articles/learn/glossary)
- [sǹg-miā — Brightness 廟旺平陷](https://sng-mia.com/articles/learn/brightness-system)
- [Yueliang — Palaces & 14 Major Stars](https://yueliangapp.com/zwds)
- [PurpleStarAstro — EN–CN terminology](https://www.purplestarastro.com/blog/purple-star-astrology-terminology-reference)
- [Fortune Cloud — Four Transformations](https://fortunecloud.co/en/learn/four-transformations)
- [starnum — Si Hua / brightness (TW)](https://starnum.com.tw/blog/en/zwds-four-transformations-complete-guide)

> **Quy ước trong code:** tên biến, hàm, class và tệp tuân theo [Quy ước đặt tên](NAMING.md). Chuỗi hiển thị cho người dùng Việt Nam có thể giữ Hán Việt và luôn tách biệt với identifier.

## 1. Hệ thống tổng quát

| Hán Việt | 繁體中文 | English (chuẩn phổ biến) | Diễn giải ngắn |
|---|---|---|---|
| Tử Vi Đẩu Số | 紫微斗數 | Zi Wei Dou Shu / Purple Star Astrology | Hệ thống an sao theo 12 cung + hàng trăm sao, lấy Tử Vi làm chủ |
| Lá số / Mệnh bàn | 命盤 | Natal chart / Zi Wei chart | Bản đồ 12 cung lập từ ngày giờ sinh |
| An sao | 安星 | Star placement | Thuật toán đặt sao vào cung |
| Thiên bàn | 天盤 | Heaven plate | Phần “thiên” (can chi, bản mệnh, chủ…); trong code hay gắn meta lá số |
| Địa bàn | 地盤 | Earth plate | 12 cung cố định theo địa chi + sao đã an |
| Nhân bàn | 人盤 | Human plate | Lớp hạn theo tuổi / năm xem (đại hạn, tiểu hạn…) |

---

## 2. Thiên Can — Địa Chi

### Thiên Can (天干 / Heavenly Stems)

| # | Hán Việt | 繁體 | Pinyin | English |
|---|---|---|---|---|
| 1 | Giáp | 甲 | Jiǎ | Jia |
| 2 | Ất | 乙 | Yǐ | Yi |
| 3 | Bính | 丙 | Bǐng | Bing |
| 4 | Đinh | 丁 | Dīng | Ding |
| 5 | Mậu | 戊 | Wù | Wu |
| 6 | Kỷ | 己 | Jǐ | Ji |
| 7 | Canh | 庚 | Gēng | Geng |
| 8 | Tân | 辛 | Xīn | Xin |
| 9 | Nhâm | 壬 | Rén | Ren |
| 10 | Quý | 癸 | Guǐ | Gui |

### Địa Chi (地支 / Earthly Branches)

| # | Hán Việt | 繁體 | Pinyin | English | Giờ (VN) |
|---|---|---|---|---|---|
| 1 | Tý | 子 | Zǐ | Zi | 23h–1h |
| 2 | Sửu | 丑 | Chǒu | Chou | 1h–3h |
| 3 | Dần | 寅 | Yín | Yin | 3h–5h |
| 4 | Mão | 卯 | Mǎo | Mao | 5h–7h |
| 5 | Thìn | 辰 | Chén | Chen | 7h–9h |
| 6 | Tỵ | 巳 | Sì | Si | 9h–11h |
| 7 | Ngọ | 午 | Wǔ | Wu | 11h–13h |
| 8 | Mùi | 未 | Wèi | Wei | 13h–15h |
| 9 | Thân | 申 | Shēn | Shen | 15h–17h |
| 10 | Dậu | 酉 | Yǒu | You | 17h–19h |
| 11 | Tuất | 戌 | Xū | Xu | 19h–21h |
| 12 | Hợi | 亥 | Hài | Hai | 21h–23h |

**Can Chi** = 干支 / Stem–Branch — hệ đếm thời gian truyền thống; Can năm quyết định **Tứ Hóa**, Chi quyết định vị trí cung và hạn.

---

## 3. Âm Dương — Ngũ Hành — Cục

| Hán Việt | 繁體 | English | Ghi chú |
|---|---|---|---|
| Âm / Dương | 陰 / 陽 | Yin / Yang | |
| Ngũ Hành | 五行 | Five Elements / Wu Xing | Kim Mộc Thủy Hỏa Thổ |
| Kim | 金 | Metal | Cục số 4 — Metal Bureau |
| Mộc | 木 | Wood | Cục số 3 |
| Thủy | 水 | Water | Cục số 2 |
| Hỏa | 火 | Fire | Cục số 6 |
| Thổ | 土 | Earth | Cục số 5 |
| Ngũ Hành Cục | 五行局 | Five-Element Bureau | Quyết định tuổi khởi đại hạn |
| Thủy nhị cục | 水二局 | Water 2 Bureau | Đại hạn bắt đầu tuổi 2 |
| Mộc tam cục | 木三局 | Wood 3 Bureau | Tuổi 3 |
| Kim tứ cục | 金四局 | Metal 4 Bureau | Tuổi 4 |
| Thổ ngũ cục | 土五局 | Earth 5 Bureau | Tuổi 5 |
| Hỏa lục cục | 火六局 | Fire 6 Bureau | Tuổi 6 |
| Nạp âm | 納音 | Nayin (stem–branch element name) | Tên ngũ hành gắn cặp can–chi năm |
| Bản mệnh | 本命 | Natal self / natal element theme | Thường lấy nạp âm năm sinh |
| Sinh / Khắc | 生 / 剋 | Generating / Controlling | Quan hệ sinh khắc giữa bản mệnh và cục |

---

## 4. Thập nhị cung (十二宮)

Thứ tự trong engine `lasotuvi` (từ cung Mệnh theo chiều an cung):

| Hán Việt (repo) | 繁體 | English (chuẩn dùng trong code) | Ý nghĩa chính |
|---|---|---|---|
| Mệnh | 命宮 | Life Palace | Tính cách, hướng đời, cách người khác nhìn |
| Phụ mẫu | 父母宮 | Parents Palace | Cha mẹ, thầy cô, nền tảng học vấn |
| Phúc đức | 福德宮 | Spirit / Blessings Palace | Nội tâm, hưởng thụ, phúc báo |
| Điền trạch | 田宅宮 | Property Palace | Nhà đất, môi trường sống, tài sản cố định |
| Quan lộc | 官祿宮 | Career Palace | Sự nghiệp, công danh |
| Nô bộc | 交友宮 / 僕役宮 | Friends / Servants Palace | Bạn bè, cấp dưới, quan hệ ngang |
| Thiên di | 遷移宮 | Travel Palace | Bên ngoài, di chuyển, hình ảnh xã hội |
| Tật ách | 疾厄宮 | Health Palace | Sức khỏe, tai ách |
| Tài bạch | 財帛宮 | Wealth Palace | Kiếm tiền, thái độ với tiền |
| Tử tức | 子女宮 | Children Palace | Con cái, thế hệ sau, sáng tạo |
| Phu thê | 夫妻宮 | Spouse Palace | Hôn nhân, tình cảm đôi lứa |
| Huynh đệ | 兄弟宮 | Siblings Palace | Anh chị em, bạn đồng trang lứa |

**Cung Thân** (身宮 / Body Palace): điểm thứ hai sau Mệnh — hành vi thực tế, phát triển về sau.

**Tam phương tứ chính** (三方四正 / San Fang Si Zheng): khung 4 cung (cung đang xét + đối cung + hai cung hợp) khi luận một cung.

| Hán Việt | 繁體 | English (code) | Ý nghĩa |
|---|---|---|---|
| Xung chiếu / Đối cung | 對宮 | Opposite palace (`opposite`) | Cung cách 6 vị (+6) |
| Tam hợp | 三合 | Trine palaces (`trine_1`, `trine_2`) | Hai cung hợp (+4, +8) |
| Tam phương tứ chính | 三方四正 | San fang si zheng / four-palace frame | Cung gốc + opposite + 2 trines |

Trong code: `EarthPlate.get_related_palaces(index)`.

---

## 5. Độ sáng sao — Đặc tính (廟旺平陷)

Trường phái Việt trong repo dùng 5 mức: **M / V / Đ / B / H**.

| Code | Hán Việt | 繁體 | English | Mức năng lượng |
|---|---|---|---|---|
| M | Miếu | 廟 | Miao (Temple / Peak) | Mạnh nhất |
| V | Vượng | 旺 | Wang (Prosperous) | Rất mạnh |
| Đ | Đắc | 得 | De (Attained / Favorable) | Khá / thuận |
| B | Bình | 平 | Ping (Average / Neutral) | Trung bình |
| H | Hãm | 陷 | Xian (Fallen / Trapped) | Yếu nhất |

Một số sách Đài/Hoa lục còn chia nhỏ thêm **利 (Li)** giữa Đắc và Bình; repo hiện không dùng mức riêng đó.

---

## 6. Tứ Hóa (四化)

| Hán Việt | 繁體 | English | Ý chính |
|---|---|---|---|
| Tứ Hóa | 四化 | Four Transformations (Si Hua) | Cơ chế động theo Thiên Can |
| Hóa Lộc | 化祿 | Hua Lu — Prosperity | Thuận, nguồn lực, cơ hội, tiền chảy |
| Hóa Quyền | 化權 | Hua Quan — Authority | Quyền lực, chủ động, áp lực nỗ lực |
| Hóa Khoa | 化科 | Hua Ke — Fame / Recognition | Danh tiếng, học thuật, quý nhân |
| Hóa Kỵ | 化忌 | Hua Ji — Obstruction | Tắc nghẽn, cố chấp, bài học cần xử lý |

---

## 7. Hệ hạn và thời vận

| Hán Việt | 繁體 | English | Diễn giải |
|---|---|---|---|
| Đại hạn | 大限 | Major period / Da Xian (decade luck) | Chu kỳ ~10 năm theo cục |
| Tiểu hạn | 小限 | Annual / minor luck (Xiao Xian) | Hạn theo năm tuổi / chi năm |
| Nguyệt hạn | 月限 | Monthly luck | Lớp tháng trong năm xem |
| Lưu niên | 流年 | Annual (flowing year) | Sao / hóa theo năm xem |
| Thái Tuế | 太歲 | Tai Sui (Year Branch) | Chi của năm; cung có Thái Tuế hay “động” |
| Tuần Trung | 旬中 | Xun (Empty span marker) | Cặp cung “tuần không” |
| Triệt Lộ | 截路 / 空亡相關 | Triet / Void-road | Cặp cung triệt theo can năm |

> Tên English cho code: `major_period`, `annual_luck`, `monthly_luck`, `flowing_year`.

---

## 8. Mười bốn chính tinh (十四主星)

| Hán Việt (repo) | 繁體 | Pinyin | English (phổ biến) |
|---|---|---|---|
| Tử vi | 紫微 | Zǐwēi | Emperor Star / Zi Wei |
| Thiên cơ | 天機 | Tiānjī | Advisor / Strategist Star |
| Thái Dương | 太陽 | Tàiyáng | Sun Star |
| Vũ khúc | 武曲 | Wǔqǔ | Military / Wealth General Star |
| Thiên đồng | 天同 | Tiāntóng | Harmony / Blessing Star |
| Liêm trinh | 廉貞 | Liánzhēn | Integrity / Politician Star |
| Thiên phủ | 天府 | Tiānfǔ | Treasury Star |
| Thái âm | 太陰 | Tàiyīn | Moon Star |
| Tham lang | 貪狼 | Tānláng | Ambition / Desire Star |
| Cự môn | 巨門 | Jùmén | Gate / Great Door Star |
| Thiên tướng | 天相 | Tiānxiàng | Minister / Seal Star |
| Thiên lương | 天梁 | Tiānliáng | Elder / Bridge Star |
| Thất sát | 七殺 | Qīshā | Seven Killings |
| Phá quân | 破軍 | Pòjūn | Breaker / Defeat Star |

Nhóm Bắc Đẩu / Nam Đẩu: xem [sǹg-miā glossary](https://sng-mia.com/en/articles/learn/glossary).

---

## 9. Một số phụ tinh và sát tinh thường gặp

| Hán Việt | 繁體 | English (gợi ý code / docs) |
|---|---|---|
| Lộc tồn | 祿存 | Lu Cun (Wealth Store) |
| Kình dương | 擎羊 | Qing Yang / Blade |
| Đà la | 陀羅 | Tuo Luo / Spinner |
| Hỏa tinh | 火星 | Huo Xing / Fire Star |
| Linh tinh | 鈴星 | Ling Xing / Bell Star |
| Địa không | 地空 | Di Kong / Earth Void |
| Địa kiếp | 地劫 | Di Jie / Earth Calamity |
| Tả phù | 左輔 | Zuo Fu / Left Assistant |
| Hữu bật | 右弼 | You Bi / Right Assistant |
| Văn xương | 文昌 | Wen Chang / Literary Staff |
| Văn khúc | 文曲 | Wen Qu / Literary Music |
| Thiên khôi | 天魁 | Tian Kui / Heavenly Leader |
| Thiên việt | 天鉞 | Tian Yue / Heavenly Halberd |
| Hồng loan | 紅鸞 | Hong Luan / Red Phoenix |
| Thiên hỷ | 天喜 | Tian Xi / Heavenly Joy |
| Thiên mã | 天馬 | Tian Ma / Heavenly Horse |
| Đào hoa | 桃花 | Peach Blossom |
| Thái tuế | 太歲 | Tai Sui |
| Tràng sinh (vòng) | 長生十二神 | Twelve Stages of Life cycle |

**Lục cát** thường kể: Tả Phù, Hữu Bật, Văn Xương, Văn Khúc, Thiên Khôi, Thiên Việt.  
**Lục sát** thường kể: Kình Dương, Đà La, Hỏa, Linh, Địa Không, Địa Kiếp.

---

## 10. Vòng Trường Sinh (長生十二神)

| Hán Việt | 繁體 | English |
|---|---|---|
| Tràng sinh | 長生 | Birth / Growth |
| Mộc dục | 沐浴 | Bath |
| Quan đới | 冠帶 | Cap and Belt |
| Lâm quan | 臨官 | Coming of Age / Official Arrival |
| Đế vượng | 帝旺 | Peak Prosperity |
| Suy | 衰 | Decline |
| Bệnh | 病 | Illness |
| Tử | 死 | Death |
| Mộ | 墓 | Grave |
| Tuyệt | 絕 | Extinction |
| Thai | 胎 | Conception |
| Dưỡng | 養 | Nurture |

---

## 11. Lịch

| Hán Việt | 繁體 | English |
|---|---|---|
| Dương lịch | 陽曆 / 公曆 | Solar / Gregorian calendar |
| Âm lịch | 陰曆 / 農曆 | Lunar / Chinese calendar |
| Tháng nhuận | 閏月 | Leap month |
| Tiết khí / Trung khí | 節氣 / 中氣 | Solar terms / Major solar terms |
| Sóc (ngày sóc) | 朔 | New moon day |

---

## 12. Cách cục và luận đoán (格局)

| Hán Việt | 繁體 | English (code) | Ghi chú |
|---|---|---|---|
| Cách cục / Cách cục tinh hệ | 格局 | Chart formation / pattern (`formation`) | Tổ hợp chính tinh hội ở khung tam phương tứ chính |
| Luận đoán | 論斷 | Interpretation | Diễn giải sao tại cung từ knowledge base |
| Vô Chính Diệu | 無主星 / 空宮主星 | Empty life major stars | Cung Mệnh không có chính tinh (ID 1–14) |
| Tử Phủ Vũ Tướng | 紫府武相 | `emperor_treasury_military_minister` | Tử Vi + Thiên Phủ + Vũ Khúc + Thiên Tướng |
| Sát Phá Tham | 殺破貪 | `killings_breaker_ambition` | Thất Sát + Phá Quân + Tham Lang |
| Cơ Nguyệt Đồng Lương | 機月同梁 | `advisor_moon_harmony_elder` | Thiên Cơ + Thái Âm + Thiên Đồng + Thiên Lương |
| Cự Nhật | 巨日 | `gate_sun` | Cự Môn + Thái Dương |

Engine: `lasotuvi/analysis.py` → `ChartAnalyzer`.  
Dữ liệu: `lasotuvi/data/interpretations.json` (`formations`, `palaces`).  
API: `formations` trên chart / earth plate; `interpretations[]` trên mỗi palace.

---

## 13. Ánh xạ sang tên code

| Khái niệm domain | Identifier |
|---|---|
| Cung | `palace` |
| Sao | `star` / constants `ZI_WEI`, `TAI_YANG`, … |
| Địa bàn / Thiên bàn | `earth_plate` / `heaven_plate` / `chart_meta` |
| Cung Mệnh / Thân | `life_palace` / `body_palace` |
| Ngũ hành cục | `wu_xing_ju` / `wu_xing_ju_name` |
| Đại / tiểu / nguyệt hạn | `da_xian_age` / `xiao_xian_branch` / `yue_xian` |
| Miếu Vượng Đắc Bình Hãm | `miao_wang` |
| Mệnh chủ / Thân chủ | `ming_zhu` / `shen_zhu` |
| Bản mệnh / Nạp âm | `ben_ming_name` / `nayin` |
| Sinh khắc | `sheng_ke_status` |
| Trường sinh | `is_chang_sheng` |
| Can Chi | `stem_branch` / `HEAVENLY_STEMS` / `EARTHLY_BRANCHES` |
| Âm dương / Ngũ hành | `yin_yang` / `five_element` |

Đây là ánh xạ chuẩn của dự án; không dùng các tên English literal cũ như `brightness`, `element_bureau` hoặc `major_period` cho domain Pinyin. Chi tiết: [Quy ước đặt tên](NAMING.md).
