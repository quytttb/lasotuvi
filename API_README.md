# LasoTuVi REST API

🌟 **Vietnamese Tử Vi (Purple Star Astrology) REST API**

Modern FastAPI-based REST API for generating and analyzing Vietnamese astrological charts.

## 🚀 Quick Start

### Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-api.txt
```

### Run API Server

```bash
# Method 1: Using the script
./run_api.sh

# Method 2: Direct uvicorn
source venv/bin/activate
PYTHONPATH=/path/to/lasotuvi:$PYTHONPATH uvicorn api.main:app --reload
```

API will be available at: `http://localhost:8000`

## 📚 Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## 🎯 Features

### Core Features
- ✅ Solar to Lunar calendar conversion
- ✅ Can Chi (Heavenly Stems & Earthly Branches) calculation
- ✅ Complete Tử Vi chart generation
- ✅ Dia Ban (地盤) with 12 palaces
- ✅ Star positions and qualities
- ✅ Chart analysis with interpretations
- ✅ Batch chart generation (up to 10 charts)

### API Features
- ✅ RESTful API design
- ✅ Pydantic v2 validation
- ✅ Comprehensive error handling
- ✅ CORS support
- ✅ Request logging
- ✅ Process time tracking
- ✅ Auto-generated OpenAPI docs

## 📡 API Endpoints

### Chart Generation

#### Generate Complete Chart
```http
POST /chart/generate
Content-Type: application/json

{
  "ngay": 15,
  "thang": 8,
  "nam": 1990,
  "gio": 7,
  "gioi_tinh": 1,
  "duong_lich": true,
  "timezone": 7,
  "ten": "Nguyễn Văn A"
}
```

**Response**: Complete chart with birth info, lunar date, Can Chi, and Dia Ban (12 palaces with stars).

#### Analyze Chart
```http
POST /chart/analyze
Content-Type: application/json

{
  "ngay": 15,
  "thang": 8,
  "nam": 1990,
  "gio": 7,
  "gioi_tinh": 1,
  "duong_lich": true,
  "timezone": 7,
  "ten": "Nguyễn Văn A"
}
```

**Response**: Detailed analysis including:
- Life Palace (Cung Mệnh) analysis
- Career Palace (Quan Lộc) analysis
- Wealth Palace (Tài Bạch) analysis
- Overall strength
- Lucky/Unlucky elements
- Major life events

#### Generate Dia Ban
```http
POST /chart/dia-ban
Content-Type: application/json

{
  "ngay": 15,
  "thang": 8,
  "nam": 1990,
  "gio": 7,
  "gioi_tinh": 1,
  "duong_lich": true,
  "timezone": 7
}
```

**Response**: Dia Ban (地盤) with 12 palaces.

#### Batch Chart Generation
```http
POST /chart/batch
Content-Type: application/json

{
  "charts": [
    {
      "ngay": 15,
      "thang": 8,
      "nam": 1990,
      "gio": 7,
      "gioi_tinh": 1,
      "duong_lich": true,
      "ten": "Person 1"
    },
    {
      "ngay": 20,
      "thang": 12,
      "nam": 1995,
      "gio": 3,
      "gioi_tinh": -1,
      "duong_lich": true,
      "ten": "Person 2"
    }
  ]
}
```

**Response**: Array of chart results (max 10 charts per request).

### Calendar Operations

#### Solar to Lunar Conversion
```http
POST /calendar/solar-to-lunar?ngay=15&thang=8&nam=1990&timezone=7
```

**Response**: 
```json
{
  "ngay_am": 25,
  "thang_am": 6,
  "nam_am": 1990,
  "thang_nhuan": false
}
```

#### Can Chi Calculation
```http
POST /calendar/can-chi?ngay=15&thang=8&nam=1990&duong_lich=true&timezone=7
```

**Response**: Can Chi for year, month, day with Vietnamese names.

### Information Endpoints

#### Get Zodiac Hours
```http
GET /info/gio-chi
```

**Response**: List of 12 Vietnamese zodiac hours with time ranges.

#### Get Five Elements
```http
GET /info/elements
```

**Response**: Information about Wu Xing (Five Elements) including generation and destruction cycles.

#### Get Can Chi Reference
```http
GET /info/can-chi
```

**Response**: Complete list of Heavenly Stems (Thiên Can) and Earthly Branches (Địa Chi).

#### API Statistics
```http
GET /stats
```

**Response**: API version, status, and feature list.

### Health Check

```http
GET /health
```

**Response**: API health status and version.

## 🔧 Configuration

### Parameters

#### Birth Info Parameters
- **ngay** (int, 1-31): Birth day
- **thang** (int, 1-12): Birth month
- **nam** (int, 1900-2100): Birth year
- **gio** (int, 1-12): Birth hour (1=Tý, 2=Sửu, ..., 12=Hợi)
- **gioi_tinh** (int, 1 or -1): Gender (1=Male, -1=Female)
- **duong_lich** (bool): Calendar type (true=Solar, false=Lunar)
- **timezone** (int, -12 to 14): Timezone offset (default: 7 for Vietnam)
- **ten** (string, optional): Person's name

## 📊 Response Structure

### Chart Response
```json
{
  "birth_info": {
    "ngay": 15,
    "thang": 8,
    "nam": 1990,
    "gio": 7,
    "gioi_tinh": 1,
    "duong_lich": true,
    "timezone": 7,
    "ten": "Nguyễn Văn A"
  },
  "lunar_date": {
    "ngay_am": 25,
    "thang_am": 6,
    "nam_am": 1990,
    "thang_nhuan": false
  },
  "can_chi": {
    "can_nam": 7,
    "chi_nam": 7,
    "can_thang": 10,
    "ten_can_nam": "Canh",
    "ten_chi_nam": "Ngọ"
  },
  "dia_ban": {
    "cung_menh": 2,
    "cung_than": 2,
    "cuc": 6,
    "ten_cuc": "Hỏa lục Cục",
    "thap_nhi_cung": [
      {
        "cung_so": 1,
        "cung_ten": "Tý",
        "cung_chu": "Huynh đệ",
        "hanh_cung": "Thủy",
        "cung_sao": [...]
      }
      // ... 11 more palaces
    ]
  },
  "generated_at": "2025-10-08T12:00:00"
}
```

## 🛠️ Development

### Run Tests
```bash
pytest tests/test_api.py -v
```

### Code Quality
```bash
# Format code
black api/

# Lint code
ruff check api/

# Type check
pyright api/
```

### Coverage
```bash
pytest tests/ --cov=lasotuvi --cov-report=html
```

## 🚦 Rate Limiting

API includes built-in rate limiting middleware (using slowapi). Default limits:
- 100 requests per minute per IP
- Configurable per endpoint

## 🔒 Security

### Production Considerations
1. **CORS**: Update `allow_origins` in production
2. **HTTPS**: Use reverse proxy (nginx) with SSL
3. **Authentication**: Add JWT tokens if needed
4. **Rate Limiting**: Adjust limits based on usage
5. **Input Validation**: Already handled by Pydantic

## 📈 Performance

- **Average Response Time**: ~50-200ms
- **Batch Processing**: Up to 10 charts per request
- **Caching**: Consider Redis for frequently accessed data
- **Async**: All endpoints are async for better concurrency

## 🐳 Docker (Coming Soon)

```dockerfile
# Dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt requirements-api.txt ./
RUN pip install -r requirements.txt -r requirements-api.txt
COPY . .
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📝 Examples

### Python Client Example
```python
import requests

# Generate chart
response = requests.post(
    "http://localhost:8000/chart/generate",
    json={
        "ngay": 15,
        "thang": 8,
        "nam": 1990,
        "gio": 7,
        "gioi_tinh": 1,
        "duong_lich": True,
        "timezone": 7,
        "ten": "Test User"
    }
)

chart = response.json()
print(f"Cung Mệnh: {chart['dia_ban']['cung_menh']}")
print(f"Cục: {chart['dia_ban']['ten_cuc']}")
```

### JavaScript/TypeScript Example
```typescript
// Using fetch
const response = await fetch('http://localhost:8000/chart/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    ngay: 15,
    thang: 8,
    nam: 1990,
    gio: 7,
    gioi_tinh: 1,
    duong_lich: true,
    timezone: 7,
    ten: 'Test User'
  })
});

const chart = await response.json();
console.log('Cung Mệnh:', chart.dia_ban.cung_menh);
```

### cURL Example
```bash
curl -X POST "http://localhost:8000/chart/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "ngay": 15,
    "thang": 8,
    "nam": 1990,
    "gio": 7,
    "gioi_tinh": 1,
    "duong_lich": true,
    "timezone": 7,
    "ten": "Test User"
  }'
```

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

See LICENSE file in repository root.

## 🙏 Acknowledgments

- Based on traditional Vietnamese Tử Vi (Purple Star Astrology) calculation methods
- Built with FastAPI, Pydantic v2, and modern Python practices
- Calculation-only library - no interpretation or fortune-telling

## 📞 Support

- **Documentation**: http://localhost:8000/docs
- **Issues**: GitHub Issues
- **API Version**: 1.0.0

---

**Note**: This API provides astrological calculations based on traditional methods. Results are for reference and entertainment purposes only.
