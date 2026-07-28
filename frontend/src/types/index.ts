// API Response Types
export interface LunarDate {
     ngay_am: number
     thang_am: number
     nam_am: number
     thang_nhuan: boolean
}

export interface CanChi {
     can_nam: number
     chi_nam: number
     can_thang: number
     chi_thang?: number
     chi_gio?: number
     ten_can_nam: string
     ten_chi_nam: string
     ten_can_thang?: string
     ten_chi_thang?: string
     ten_chi_gio?: string
}

export interface Star {
     saoID: number
     saoTen: string
     saoNguHanh: string
     saoLoai: number
     saoPhuongVi: string
     saoAmDuong: number | string
     vongTrangSinh: number
     cssSao: string
     saoDacTinh: string | null
}

export interface Palace {
     cung_so: number
     cung_ten: string
     cung_chu: string
     hanh_cung: string
     cung_am_duong: number
     cung_sao: Star[]
     cung_dai_han: number
     cung_tieu_han: string
     cung_than: boolean
     tuan_trung: boolean
     triet_lo: boolean
}

export interface DiaBan {
     thang_sinh_am_lich: number
     gio_sinh_am_lich: number
     cung_menh: number
     cung_than: number
     cuc: number
     ten_cuc: string
     thap_nhi_cung: Palace[]
}

export interface BirthInfo {
     ngay: number
     thang: number
     nam: number
     gio: number
     gioi_tinh: 1 | -1 // 1 = Male, -1 = Female
     duong_lich: boolean
     timezone?: number
     ten?: string
}

export interface ChartResponse {
     birth_info: BirthInfo
     lunar_date: LunarDate
     can_chi: CanChi
     dia_ban: DiaBan
     generated_at: string
}

export interface PalaceAnalysis {
     palace_name: string
     palace_number: number
     stars: string[]
     strength: number
     characteristics: string[]
}

export interface ChartAnalysisResponse {
     birth_info: BirthInfo
     life_palace_analysis: PalaceAnalysis | null
     career_palace_analysis: PalaceAnalysis | null
     wealth_palace_analysis: PalaceAnalysis | null
     overall_strength: string
     lucky_elements: string[]
     unlucky_elements: string[]
     major_life_events: string[]
     generated_at: string
}

export interface BatchChartResponse {
     total: number
     successful: number
     failed: number
     results: ChartResponse[]
     generated_at: string
}

export interface Element {
     id: number
     key: string
     name: string
     cuc: number
     ten_cuc: string
}

export interface ElementsResponse {
     title: string
     description: string
     elements: Element[]
     cycle: {
          generation: string
          destruction: string
     }
}

export interface CanChiItem {
     id: number
     name: string
     element?: string
}

export interface ZodiacItem extends CanChiItem {
     zodiac?: string
}

export interface CanChiInfoResponse {
     title: string
     description: string
     thien_can: {
          count: number
          items: CanChiItem[]
     }
     dia_chi: {
          count: number
          items: ZodiacItem[]
     }
}

export interface APIStats {
     api_version: string
     status: string
     endpoints: {
          total: number
          chart_generation: number
          calendar: number
          analysis: number
          info: number
     }
     features: string[]
}

export interface ErrorResponse {
     error: string
     detail: string
}

// Form Types
export interface ChartFormData {
     ngay: string
     thang: string
     nam: string
     gio: string
     gioi_tinh: '1' | '-1'
     duong_lich: 'true' | 'false'
     timezone: string
     ten: string
}

// Utility Types
export type GioiTinh = 1 | -1
export type LichType = boolean

// Constants
export const GIOI_TINH_OPTIONS = [
     { value: '1', label: 'Nam' },
     { value: '-1', label: 'Nữ' },
] as const

export const LICH_OPTIONS = [
     { value: 'true', label: 'Dương lịch' },
     { value: 'false', label: 'Âm lịch' },
] as const

export const GIO_OPTIONS = [
     { value: '1', label: 'Tý (23:00 - 01:00)' },
     { value: '2', label: 'Sửu (01:00 - 03:00)' },
     { value: '3', label: 'Dần (03:00 - 05:00)' },
     { value: '4', label: 'Mão (05:00 - 07:00)' },
     { value: '5', label: 'Thìn (07:00 - 09:00)' },
     { value: '6', label: 'Tỵ (09:00 - 11:00)' },
     { value: '7', label: 'Ngọ (11:00 - 13:00)' },
     { value: '8', label: 'Mùi (13:00 - 15:00)' },
     { value: '9', label: 'Thân (15:00 - 17:00)' },
     { value: '10', label: 'Dậu (17:00 - 19:00)' },
     { value: '11', label: 'Tuất (19:00 - 21:00)' },
     { value: '12', label: 'Hợi (21:00 - 23:00)' },
] as const

export const TIMEZONE_OPTIONS = [
     { value: '7', label: 'GMT+7 (Việt Nam)' },
     { value: '8', label: 'GMT+8' },
     { value: '9', label: 'GMT+9' },
] as const

// Element Colors
export const ELEMENT_COLORS = {
     K: '#FFD700', // Kim - Gold
     M: '#10B981', // Mộc - Green
     T: '#3B82F6', // Thủy - Blue
     H: '#EF4444', // Hỏa - Red
     O: '#F59E0B', // Thổ - Orange
} as const

export const ELEMENT_NAMES = {
     K: 'Kim',
     M: 'Mộc',
     T: 'Thủy',
     H: 'Hỏa',
     O: 'Thổ',
} as const
