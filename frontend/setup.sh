#!/bin/bash
# Frontend Setup Script for Lá Số Tử Vi

echo "🚀 Setting up Lá Số Tử Vi Frontend..."
echo ""

# Check Node.js version
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js 18+ required. Current version: $(node -v)"
    echo "Please install Node.js 18 or higher from https://nodejs.org/"
    exit 1
fi

echo "✅ Node.js version: $(node -v)"
echo "✅ npm version: $(npm -v)"
echo ""

# Navigate to frontend directory
cd "$(dirname "$0")"

# Install dependencies
echo "📦 Installing dependencies..."
npm install

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "✅ Dependencies installed successfully!"
echo ""

# Create .env.local if it doesn't exist
if [ ! -f .env.local ]; then
    echo "📝 Creating .env.local file..."
    cat > .env.local << EOF
# Environment Variables
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME="Lá Số Tử Vi"
NEXT_PUBLIC_APP_VERSION=1.0.0

# Development
NODE_ENV=development
EOF
    echo "✅ .env.local created"
fi

echo ""
echo "🎉 Frontend setup complete!"
echo ""
echo "Next steps:"
echo "  1. Make sure the backend API is running on http://localhost:8000"
echo "  2. Run 'npm run dev' to start the development server"
echo "  3. Open http://localhost:3000 in your browser"
echo ""
echo "Available commands:"
echo "  npm run dev       - Start development server"
echo "  npm run build     - Build for production"
echo "  npm start         - Start production server"
echo "  npm run lint      - Run ESLint"
echo "  npm run format    - Format code with Prettier"
echo ""
