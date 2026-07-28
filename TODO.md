## Todo list ##

### 🧪 Testing (Modern Stack - 2025)
* [x] **Viết lại tests với pytest 8.x** ✅ PHASE 1 COMPLETE
  - [x] Setup pytest + pytest-cov + pytest-xdist
  - [x] Parametrize tests với nhiều test cases
  - [x] Integration tests cho các hàm chính (Lich module)
  - [ ] Coverage report (target: >80%) - Currently 14%, Lich_HND 86%
  - [x] Parallel testing với pytest-xdist (8x speedup!)
  - ~~[ ] Viết lại test, sử dụng hypothesis~~ (deprecated - overkill cho project này)
* [ ] ### Phase 2: Complete Test Coverage ✅ **COMPLETED**
- [x] Add tests for `AmDuong.py` functions (88% coverage, 88 tests)
- [x] Add tests for `DiaBan.py` calculations (100% coverage, 42 tests)
- [x] Add tests for `ThienBan.py` module (83% coverage via integration)
- [x] Add tests for `Sao.py` module (98% coverage via integration)
- [x] Create integration tests for full chart calculation
- [x] **Target: 80%+ overall coverage → ACHIEVED: 89%** 🎯
- [x] Fix all 12 failing tests (API expectation corrections)
- [x] Format code with black (15 files reformatted)
- [x] Check with ruff (48 issues fixed, 10 remaining non-critical)
- [x] Type check with pyright (documented legacy issues)

### 📅 Lịch pháp
* [ ] **Viết hàm chuyển đổi âm-dương lịch dựa trên dữ liệu của NASA**
  - [ ] Đánh giá thư viện skyfield (thay ephem)
  - [ ] Benchmark accuracy vs current implementation
* [ ] **Tích hợp lịch âm theo tiết khí**
  - [ ] Validate logic getSunLongitude với tiết khí
  - [ ] Test edge cases (tháng nhuận)

### 🌐 Web Application (Modern Stack) 
* [x] ~~Viết module cho django~~ (deprecated)
* [x] **Phase 3: Backend - FastAPI + Python 3.12** ✅ **COMPLETED**
  - [x] Tạo RESTful API với FastAPI (15 endpoints)
  - [x] Auto-generated OpenAPI/Swagger docs (/docs, /redoc)
  - [x] Pydantic v2 models cho validation (13 models)
  - [x] CORS middleware
  - [x] Request logging middleware with timing
  - [x] Global exception handler
  - [x] Health check endpoints
  - [x] Chart generation endpoints (basic + analysis + batch)
  - [x] Calendar conversion endpoints
  - [x] Info/reference endpoints (elements, can-chi, stats)
  - [x] 199/199 tests passing, 90% coverage 🎯
  - [x] API documentation (API_README.md)
  - [ ] Rate limiting (slowapi installed, needs config)
  - [ ] Response caching (Redis)
  - [ ] Docker containerization

### 📖 Interpretation Engine (Backend)
* [x] `EarthPlate.get_related_palaces` — san fang si zheng frame
* [x] `ChartAnalyzer` — detect formations + palace interpretations
* [x] Knowledge base `lasotuvi/data/interpretations.json` (English keys)
* [x] API fields: `formations`, `palaces[].interpretations`
* [ ] Expand KB: đủ 14 chính tinh × 12 cung + phụ tinh then từ Tailieuthamkhao
* [ ] Siết rule cách cục (miếu/hãm, đồng cung vs hội chiếu, Tài/Quan)

### 🔧 Code Quality & Type Safety ✅ **COMPLETED**
* [x] **Modern Python typing (thay mypy)**
  - [x] Upgrade lên Python 3.12+ ✅
  - [x] Sử dụng built-in type hints (PEP 695) ✅
  - [x] Setup pyright cho type checking ✅
  - [x] Setup ruff cho linting ✅ (All checks passed!)
  - [x] Setup black cho formatting ✅
  - [ ] Pre-commit hooks (optional - can add later)
* [ ] **Refactoring & Optimization**
  - [x] Fixed all bare except statements (8 instances) ✅
  - [x] Fixed exception chaining (raise from) ✅
  - [x] Removed unused variables (4 instances) ✅
  - [x] Fixed undefined function references ✅
  - [ ] Profile performance bottlenecks
  - [ ] Optimize calculation algorithms nếu cần
  - [ ] Add caching layer (functools.lru_cache)

### ✅ Completed
* [x] Tạo ảnh lá số bằng python
* [x] Xử lý thiên bàn cho chuẩn
* [x] Sửa lại trường hợp sinh năm 1983

### 📚 Documentation
* [ ] **Viết lại README với modern examples**
  - [ ] Hướng dẫn installation với pip/poetry
  - [ ] API usage examples
  - [ ] Thêm badges (tests, coverage, license)
  - [ ] Architecture diagram
* [ ] **Thêm các bước an sao chi tiết**
  - [ ] Documentation cho từng hàm tính toán
  - [ ] Flowcharts cho logic phức tạp
  - [ ] Reference đến tài liệu Tử Vi

### 🚀 DevOps & Deployment
* [ ] **CI/CD Pipeline**
  - [ ] GitHub Actions cho auto testing
  - [ ] Auto deployment (Railway/Render + Vercel)
  - [ ] Code quality checks on PR
  - [ ] Automated release notes
* [ ] **Monitoring & Analytics**
  - [ ] Error tracking (Sentry)
  - [ ] Usage analytics
  - [ ] Performance monitoring

---

## 📦 Dependencies Update Plan

**Current (2018):**
```
pytest==3.5.0
mypy==0.580
ephem==3.7.6.0
```

**Proposed (2025):**
```
# Core
python>=3.12
ephem>=4.1.5  # or skyfield>=1.49

# Testing
pytest>=8.3.0
pytest-cov>=5.0.0
pytest-xdist>=3.6.0
pytest-mock>=3.14.0
faker>=30.0.0

# Linting & Formatting
ruff>=0.7.0
black>=24.0.0
pyright>=1.1.380

# API (optional)
fastapi>=0.115.0
uvicorn[standard]>=0.32.0
pydantic>=2.9.0
```
