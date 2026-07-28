import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { Providers } from '@/components/providers'

const inter = Inter({ subsets: ['latin', 'vietnamese'] })

export const metadata: Metadata = {
     title: 'Lá Số Tử Vi - Vietnamese Purple Star Astrology',
     description: 'Calculate and analyze Vietnamese Tử Vi astrology charts online',
     keywords: ['tử vi', 'lá số', 'astrology', 'vietnamese', 'purple star'],
}

export default function RootLayout({
     children,
}: {
     children: React.ReactNode
}) {
     return (
          <html lang="vi" suppressHydrationWarning>
               <body className={inter.className}>
                    <Providers>{children}</Providers>
               </body>
          </html>
     )
}
