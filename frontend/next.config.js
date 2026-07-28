/** @type {import('next').NextConfig} */
const nextConfig = {
     reactStrictMode: true,
     swcMinify: true,

     // Environment variables
     env: {
          NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
     },

     // Image optimization
     images: {
          domains: ['localhost'],
          formats: ['image/avif', 'image/webp'],
     },

     // Experimental features
     experimental: {
          // Enable React 19 features
          reactCompiler: true,
     },

     // Headers for security
     async headers() {
          return [
               {
                    source: '/:path*',
                    headers: [
                         {
                              key: 'X-Frame-Options',
                              value: 'DENY',
                         },
                         {
                              key: 'X-Content-Type-Options',
                              value: 'nosniff',
                         },
                         {
                              key: 'Referrer-Policy',
                              value: 'origin-when-cross-origin',
                         },
                    ],
               },
          ];
     },
};

module.exports = nextConfig;
