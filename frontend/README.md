# Lá Số Tử Vi - Frontend

🌟 **Modern Vietnamese Astrology Web Application**

Built with Next.js 15, React 19, TypeScript, and Tailwind CSS.

## 🚀 Quick Start

### Prerequisites
- Node.js 18.18.0 or higher
- npm 9.0.0 or higher
- Backend API running on http://localhost:8000

### Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## 📦 Tech Stack

### Core
- **Next.js 15** - React framework with App Router
- **React 19** - UI library (Release Candidate)
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first CSS

### State & Data
- **TanStack Query (React Query)** - Server state management
- **React Hook Form** - Form handling
- **Zod** - Schema validation
- **Axios** - HTTP client

### UI Components
- **shadcn/ui** - Re-usable component library
- **Radix UI** - Headless UI primitives
- **Lucide React** - Icon library
- **Tailwind CSS** - Styling

### Utilities
- **date-fns** - Date manipulation
- **jsPDF** - PDF generation
- **html2canvas** - Chart to image conversion
- **clsx** + **tailwind-merge** - Class name utilities

## 📁 Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── layout.tsx          # Root layout
│   │   ├── page.tsx            # Home page
│   │   ├── globals.css         # Global styles
│   │   ├── chart/              # Chart pages
│   │   ├── batch/              # Batch pages
│   │   └── about/              # About pages
│   │
│   ├── components/             # React components
│   │   ├── ui/                 # shadcn/ui components
│   │   ├── chart/              # Chart-specific components
│   │   ├── forms/              # Form components
│   │   └── providers.tsx       # Context providers
│   │
│   ├── lib/                    # Utility functions
│   │   ├── api-client.ts       # API client
│   │   ├── utils.ts            # Helper functions
│   │   └── validators.ts       # Zod schemas
│   │
│   ├── hooks/                  # Custom React hooks
│   │   ├── use-chart.ts        # Chart hooks
│   │   └── use-api.ts          # API hooks
│   │
│   └── types/                  # TypeScript types
│       └── index.ts            # Type definitions
│
├── public/                     # Static assets
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── next.config.js
└── README.md
```

## 🎨 Features

### Implemented
- ✅ Responsive landing page
- ✅ TypeScript type definitions
- ✅ API client with error handling
- ✅ TanStack Query integration
- ✅ Tailwind CSS styling
- ✅ Form validation with Zod

### To Implement
- [ ] Chart generation form
- [ ] Chart visualization (12 palaces)
- [ ] Chart analysis display
- [ ] Batch chart generation
- [ ] PDF export
- [ ] Element reference pages
- [ ] Can Chi reference pages
- [ ] Mobile responsive design
- [ ] Dark mode support

## 🔧 Development

### Available Scripts

```bash
# Development server (http://localhost:3000)
npm run dev

# Production build
npm run build

# Start production server
npm start

# Linting
npm run lint

# Type checking
npm run type-check

# Format code
npm run format

# Run tests
npm test
```

### Environment Variables

Create `.env.local` file:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME="Lá Số Tử Vi"
NEXT_PUBLIC_APP_VERSION=1.0.0
NODE_ENV=development
```

## 📝 API Integration

### API Client Usage

```typescript
import { apiClient } from '@/lib/api-client'

// Generate chart
const chart = await apiClient.generateChart({
  ngay: 15,
  thang: 8,
  nam: 1990,
  gio: 7,
  gioi_tinh: 1,
  duong_lich: true,
  ten: 'Nguyễn Văn A'
})

// Analyze chart
const analysis = await apiClient.analyzeChart(birthInfo)

// Batch generation
const batch = await apiClient.generateBatchCharts([
  birthInfo1,
  birthInfo2
])
```

### React Query Usage

```typescript
import { useQuery } from '@tanstack/react-query'
import { apiClient } from '@/lib/api-client'

function ChartPage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['chart', birthInfo],
    queryFn: () => apiClient.generateChart(birthInfo),
  })

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>

  return <ChartDisplay chart={data} />
}
```

## 🎯 Component Development

### Using shadcn/ui Components

```bash
# Add button component
npx shadcn-ui@latest add button

# Add card component
npx shadcn-ui@latest add card

# Add form components
npx shadcn-ui@latest add form
npx shadcn-ui@latest add input
npx shadcn-ui@latest add select
```

### Custom Hook Example

```typescript
// src/hooks/use-chart.ts
import { useMutation } from '@tanstack/react-query'
import { apiClient } from '@/lib/api-client'
import type { BirthInfo } from '@/types'

export function useGenerateChart() {
  return useMutation({
    mutationFn: (birthInfo: BirthInfo) => 
      apiClient.generateChart(birthInfo),
    onSuccess: (data) => {
      console.log('Chart generated:', data)
    },
    onError: (error) => {
      console.error('Chart generation failed:', error)
    },
  })
}
```

## 🎨 Styling Guide

### Tailwind CSS Classes

```tsx
// Typography
<h1 className="text-4xl font-bold text-purple-600">

// Layout
<div className="container mx-auto px-4 py-8">

// Grid
<div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">

// Element colors
<div className="bg-kim text-white">  // Gold (Kim)
<div className="bg-moc text-white">  // Green (Mộc)
<div className="bg-thuy text-white"> // Blue (Thủy)
<div className="bg-hoa text-white">  // Red (Hỏa)
<div className="bg-tho text-white">  // Orange (Thổ)
```

### Custom CSS

Add to `globals.css`:

```css
@layer components {
  .chart-palace {
    @apply border-2 border-gray-300 rounded-lg p-4;
  }
  
  .star-badge {
    @apply inline-block px-2 py-1 text-sm rounded;
  }
}
```

## 📱 Responsive Design

### Breakpoints

- **sm**: 640px
- **md**: 768px  
- **lg**: 1024px
- **xl**: 1280px
- **2xl**: 1536px

### Usage

```tsx
<div className="
  text-sm md:text-base lg:text-lg
  p-2 md:p-4 lg:p-6
  grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3
">
```

## 🚀 Deployment

### Build for Production

```bash
npm run build
npm start
```

### Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Deploy to Netlify

```bash
# Install Netlify CLI
npm i -g netlify-cli

# Build
npm run build

# Deploy
netlify deploy --prod
```

### Environment Variables (Production)

```env
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NODE_ENV=production
```

## 🧪 Testing

### Setup Jest (TODO)

```bash
npm install --save-dev jest @testing-library/react @testing-library/jest-dom
```

### Example Test

```typescript
import { render, screen } from '@testing-library/react'
import HomePage from '@/app/page'

describe('HomePage', () => {
  it('renders heading', () => {
    render(<HomePage />)
    expect(screen.getByText('Tính Lá Số Tử Vi Online')).toBeInTheDocument()
  })
})
```

## 📚 Resources

### Documentation
- [Next.js Docs](https://nextjs.org/docs)
- [React Docs](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [shadcn/ui](https://ui.shadcn.com/)
- [TanStack Query](https://tanstack.com/query/latest)

### Vietnamese Astrology
- See backend API documentation for calculation methods
- Traditional Tử Vi calculation based on birth date and time
- 12 palaces (Thập nhị cung) analysis
- Star positions and qualities

## 🤝 Contributing

1. Create feature branch: `git checkout -b feature/amazing-feature`
2. Commit changes: `git commit -m 'Add amazing feature'`
3. Push to branch: `git push origin feature/amazing-feature`
4. Open Pull Request

## 📄 License

See LICENSE file in repository root.

## 🙏 Acknowledgments

- Built with modern React and Next.js ecosystem
- UI components from shadcn/ui
- Integrates with FastAPI backend
- Vietnamese astrology calculation methods

---

**Status**: Phase 4 - Frontend setup complete. Ready for component development.

**Next Steps**: 
1. Install dependencies: `npm install`
2. Start dev server: `npm run dev`
3. Implement chart form and visualization
4. Add batch processing UI
5. Implement PDF export
