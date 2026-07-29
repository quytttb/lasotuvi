# Zi Wei Dou Shu glossary

[Bản tiếng Việt](TERMINOLOGY.md)

This is the English reference for terminology used in `lasotuvi`. For the full Hán Việt ↔ Traditional Chinese comparison tables, see the Vietnamese-first document linked above. Identifier conventions are defined in [Naming conventions](NAMING.en.md).

## General system

| Term | Traditional Chinese | Meaning |
|---|---|---|
| Zi Wei Dou Shu | 紫微斗數 | Purple Star Astrology; a chart system based on twelve palaces and star placement |
| Natal chart | 命盤 | Twelve-palace chart calculated from birth date and time |
| Star placement | 安星 | Algorithm that places stars in palaces |
| Heaven plate | 天盤 | Chart metadata such as stem–branch and natal information |
| Earth plate | 地盤 | Twelve fixed branch palaces and their placed stars |
| Human plate | 人盤 | Luck-cycle layer for age or viewing year |

## Core concepts

- **Heavenly Stems** (天干) and **Earthly Branches** (地支) form the stem–branch calendar cycle.
- **Five Elements** (五行 / Wu Xing) are Metal, Wood, Water, Fire, and Earth. The Five-Element Bureau determines the starting age of major luck.
- The **Twelve Palaces** include Life, Parents, Spirit/Blessings, Property, Career, Friends, Travel, Health, Wealth, Children, Spouse, and Siblings.
- A **Body Palace** (身宮) is the secondary focal point after the Life Palace.
- **San Fang Si Zheng** is the four-palace frame: the palace under review, its opposite palace, and two trine palaces.

## Brightness and transformations

| Code | Pinyin | English meaning |
|---|---|---|
| M | Miao | Peak / temple |
| V | Wang | Prosperous |
| Đ | De | Favorable / attained |
| B | Ping | Neutral |
| H | Xian | Fallen / trapped |

The Four Transformations (四化 / Si Hua) are Hua Lu (prosperity), Hua Quan (authority), Hua Ke (recognition), and Hua Ji (obstruction). They are determined by the Heavenly Stem.

## Luck cycles

Major luck (Da Xian) is a roughly ten-year period; annual luck (Xiao Xian) is the annual cycle; monthly luck is the monthly layer. Flowing year refers to annual stars and transformations. Xun and Triet are void-span markers.

## Fourteen Major Stars

Zi Wei, Tian Ji, Tai Yang, Wu Qu, Tian Tong, Lian Zhen, Tian Fu, Tai Yin, Tan Lang, Ju Men, Tian Xiang, Tian Liang, Qi Sha, and Po Jun are the fourteen major stars. Use their Pinyin identifiers in code; do not introduce literal-English star identifiers.

## Common formations and interpretation

Formations (格局) are patterns evaluated in the four-palace frame. The engine detects formations through `ChartAnalyzer`; interpretation readings come from `lasotuvi/data/interpretations.json`. Common named formations include Zi Fu Wu Xiang, Sha Po Tan, Ji Yue Tong Liang, and Ju Ri.

## Code identifiers

Use `earth_plate`, `heaven_plate`, `life_palace`, and `body_palace` for chart structure. Use `wu_xing_ju`, `miao_wang`, `da_xian_age`, `xiao_xian_branch`, `yue_xian`, `ming_zhu`, `shen_zhu`, `nayin`, and `sheng_ke_status` for the domain concepts defined in [Naming conventions](NAMING.en.md).
