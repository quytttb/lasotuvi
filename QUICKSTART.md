# 🚀 Lá Số Tử Vi - Quick Start Guide

## Current Status: Phase 4 Complete ✅

**Project Progress: ~80% Complete**
- ✅ Phase 1: Testing Modernization (199 tests passing)
- ✅ Phase 2: Test Coverage (90% achieved)
- ✅ Phase 3: FastAPI Backend (15 endpoints)
- ✅ Phase 4: Next.js Frontend Setup
- 🚀 Phase 4.5-4.8: Frontend Development (NEXT)

---

## Part 1: Backend (FastAPI)

### Start Backend API Server

```bash
cd /home/haiquy/PycharmProjects/lasotuvi

# Start API (already running if you followed Phase 3)
./run_api.sh

# Or manually:
source venv/bin/activate
PYTHONPATH=/home/haiquy/PycharmProjects/lasotuvi:$PYTHONPATH uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### Verify Backend

```bash
# Health check
curl http://localhost:8000/health

# API stats
curl http://localhost:8000/stats

# API documentation
open http://localhost:8000/docs
```

**Backend Endpoints**: 15 total
- 4 Chart generation endpoints
- 2 Calendar conversion endpoints
- 1 Analysis endpoint
- 5 Info/reference endpoints
- 3 Meta endpoints

---

## Part 2: Frontend (Next.js 15)

### Install Frontend Dependencies

```bash
cd /home/haiquy/PycharmProjects/lasotuvi/frontend

# Option 1: Use setup script
./setup.sh

# Option 2: Manual install
npm install
```

**This will install**:
- Next.js 15
- React 19 (RC)
- TypeScript 5.6
- Tailwind CSS
- TanStack Query
- Axios
- And 20+ more packages (~300MB)

### Start Frontend Dev Server

```bash
# Make sure you're in /frontend directory
cd /home/haiquy/PycharmProjects/lasotuvi/frontend

# Start development server
npm run dev
```

**Open**: http://localhost:3000

### Available Frontend Commands

```bash
# Development
npm run dev          # Start dev server (port 3000)

# Production
npm run build        # Build for production
npm start            # Start production server

# Code Quality
npm run lint         # ESLint
npm run type-check   # TypeScript check
npm run format       # Prettier format

# Testing
npm test             # Run Jest tests
npm test:watch       # Watch mode
```

---

## Part 3: Full Stack Development

### Running Both Servers

**Terminal 1 - Backend**:
```bash
cd /home/haiquy/PycharmProjects/lasotuvi
./run_api.sh
# API running on http://localhost:8000
```

**Terminal 2 - Frontend**:
```bash
cd /home/haiquy/PycharmProjects/lasotuvi/frontend
npm run dev
# Frontend running on http://localhost:3000
```

### Verify Integration

1. **Frontend**: http://localhost:3000
2. **Backend API**: http://localhost:8000
3. **API Docs**: http://localhost:8000/docs
4. **API Health**: http://localhost:8000/health

### Test API Connection

```bash
# From frontend directory
curl http://localhost:8000/health

# Should return:
# {"status": "healthy", "version": "1.0.0"}
```

---

## Part 4: Next Development Steps

### 4.1 Install shadcn/ui Components

```bash
cd frontend

# Install Button
npx shadcn-ui@latest add button

# Install Form components
npx shadcn-ui@latest add form input label select

# Install Card components
npx shadcn-ui@latest add card

# Install Layout components
npx shadcn-ui@latest add tabs dialog

# Install Feedback components
npx shadcn-ui@latest add toast alert
```

### 4.2 Create Chart Form Page

```bash
# Create directory
mkdir -p src/app/chart

# Create page file
touch src/app/chart/page.tsx
```

**File structure**:
```
src/app/chart/
├── page.tsx              # Chart form page
├── [id]/
│   └── page.tsx          # Chart display page
└── analyze/
    └── page.tsx          # Chart analysis page
```

### 4.3 Create Chart Components

```bash
# Create components directory
mkdir -p src/components/chart

# Create component files
touch src/components/chart/chart-form.tsx
touch src/components/chart/chart-display.tsx
touch src/components/chart/palace-card.tsx
touch src/components/chart/star-badge.tsx
touch src/components/chart/analysis-panel.tsx
```

### 4.4 Create Custom Hooks

```bash
# Create hooks directory (if not exists)
mkdir -p src/hooks

# Create hook files
touch src/hooks/use-chart.ts
touch src/hooks/use-analyze-chart.ts
touch src/hooks/use-batch-charts.ts
```

---

## Part 5: Testing

### Backend Tests

```bash
cd /home/haiquy/PycharmProjects/lasotuvi

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=lasotuvi --cov-report=html

# Run specific test file
pytest tests/test_api.py -v
pytest tests/test_api_advanced.py -v

# View coverage report
open htmlcov/index.html
```

**Test Results**: 199/199 passing ✅, 90% coverage

### Frontend Tests (TODO)

```bash
cd frontend

# Run tests
npm test

# Watch mode
npm test:watch

# Coverage
npm test -- --coverage
```

---

## Part 6: Project Structure

```
lasotuvi/
├── api/                          # FastAPI Backend
│   ├── main.py                   # 15 endpoints (540+ lines)
│   ├── models.py                 # 13 Pydantic models
│   ├── services.py               # 7 service methods
│   └── __init__.py
│
├── frontend/                     # Next.js 15 Frontend
│   ├── src/
│   │   ├── app/                  # App Router pages
│   │   ├── components/           # React components
│   │   ├── lib/                  # Utilities (API client)
│   │   ├── types/                # TypeScript types
│   │   └── hooks/                # Custom hooks
│   ├── public/                   # Static assets
│   ├── package.json              # Dependencies
│   └── README.md                 # Frontend docs
│
├── lasotuvi/                     # Core Library
│   ├── AmDuong.py               # 90% coverage
│   ├── App.py                   # 90% coverage
│   ├── DiaBan.py                # 100% coverage
│   ├── Lich_HND.py              # 86% coverage
│   ├── Lich_EPHEM.py            # 71% coverage
│   ├── Sao.py                   # 98% coverage
│   └── ThienBan.py              # 83% coverage
│
├── tests/                        # Test Suite
│   ├── test_api.py              # 15 API tests
│   ├── test_api_advanced.py    # 18 advanced tests
│   └── ... (20+ test files)
│
├── docs/                         # Documentation
├── run_api.sh                    # Backend start script
├── requirements.txt              # Python dependencies
├── requirements-api.txt          # API dependencies
└── README.md                     # Main documentation
```

---

## Part 7: Common Tasks

### Task 1: Generate a Chart via API

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
    "ten": "Test User"
  }'
```

### Task 2: Analyze a Chart

```bash
curl -X POST "http://localhost:8000/chart/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "ngay": 15,
    "thang": 8,
    "nam": 1990,
    "gio": 7,
    "gioi_tinh": 1,
    "duong_lich": true
  }' | jq '.'
```

### Task 3: Batch Generation

```bash
curl -X POST "http://localhost:8000/chart/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "charts": [
      {"ngay": 15, "thang": 8, "nam": 1990, "gio": 7, "gioi_tinh": 1, "duong_lich": true},
      {"ngay": 20, "thang": 12, "nam": 1995, "gio": 3, "gioi_tinh": -1, "duong_lich": true}
    ]
  }' | jq '.total, .successful'
```

### Task 4: Get Reference Data

```bash
# Five Elements
curl http://localhost:8000/info/elements | jq '.elements[].name'

# Can Chi
curl http://localhost:8000/info/can-chi | jq '.thien_can.count'

# API Stats
curl http://localhost:8000/stats | jq '.endpoints'
```

---

## Part 8: Troubleshooting

### Backend Issues

**Problem**: Port 8000 already in use
```bash
# Kill existing process
pkill -f uvicorn

# Or find and kill specific PID
lsof -ti:8000 | xargs kill -9
```

**Problem**: Module not found
```bash
# Activate venv and set PYTHONPATH
source venv/bin/activate
export PYTHONPATH=/home/haiquy/PycharmProjects/lasotuvi:$PYTHONPATH
```

**Problem**: Tests failing
```bash
# Re-run with verbose output
pytest tests/ -v --tb=short

# Check coverage
pytest tests/ --cov=lasotuvi --cov-report=term-missing
```

### Frontend Issues

**Problem**: Dependencies not installed
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Problem**: Port 3000 in use
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9

# Or use different port
PORT=3001 npm run dev
```

**Problem**: Type errors
```bash
# Reinstall @types packages
npm install --save-dev @types/node @types/react @types/react-dom

# Type check
npm run type-check
```

**Problem**: Cannot connect to API
```bash
# Check backend is running
curl http://localhost:8000/health

# Check environment variable
cat frontend/.env.local | grep API_URL
# Should show: NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Part 9: Documentation

### Available Documentation

1. **Main README**: `/README.md`
2. **API Documentation**: `/API_README.md`
3. **API Improvements**: `/API_IMPROVEMENTS_SUMMARY.md`
4. **Frontend README**: `/frontend/README.md`
5. **Phase 4 Summary**: `/PHASE_4_SUMMARY.md`
6. **This Quick Start**: `/QUICKSTART.md`
7. **TODO List**: `/TODO.md`

### Online Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

---

## Part 10: Quick Reference

### Environment Variables

**Backend** (already configured):
```bash
# In venv activation or run_api.sh
PYTHONPATH=/home/haiquy/PycharmProjects/lasotuvi:$PYTHONPATH
```

**Frontend** (`frontend/.env.local`):
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME="Lá Số Tử Vi"
NEXT_PUBLIC_APP_VERSION=1.0.0
NODE_ENV=development
```

### Port Map

- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Key Commands Cheat Sheet

```bash
# Backend
./run_api.sh                    # Start API
pytest tests/ -v                # Run tests
pytest --cov=lasotuvi          # Coverage

# Frontend
npm run dev                     # Dev server
npm run build                   # Production build
npm run lint                    # Lint
npm test                        # Tests

# Both
git status                      # Check changes
git add .                       # Stage all
git commit -m "message"         # Commit
git push                        # Push to remote
```

---

## 🎯 What's Next?

### Immediate Next Steps:

1. **Install frontend dependencies**:
   ```bash
   cd frontend && npm install
   ```

2. **Start both servers**:
   - Terminal 1: `./run_api.sh`
   - Terminal 2: `cd frontend && npm run dev`

3. **Verify both are running**:
   - http://localhost:8000/health
   - http://localhost:3000

4. **Start development**:
   - Create chart form page
   - Implement chart visualization
   - Add analysis display

### Development Priorities:

1. **Chart Form** (Phase 4.5)
   - React Hook Form setup
   - Zod validation
   - Submit to API

2. **Chart Display** (Phase 4.6)
   - 12 palaces layout
   - Star badges
   - Responsive design

3. **Features** (Phase 4.7)
   - Analysis panel
   - Batch generation
   - PDF export

4. **Polish** (Phase 4.8)
   - Dark mode
   - Mobile optimization
   - Performance tuning

---

**Status**: ✅ Ready for full-stack development!

**Current**: Frontend setup complete, dependencies defined, API integrated
**Next**: Install dependencies and start building UI components

Good luck! 🚀
