import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Calendar, Users, BarChart3, FileText } from 'lucide-react'

export default function HomePage() {
     return (
          <div className="min-h-screen bg-gradient-to-b from-purple-50 to-white dark:from-gray-900 dark:to-gray-800">
               {/* Header */}
               <header className="border-b">
                    <div className="container mx-auto px-4 py-4">
                         <div className="flex items-center justify-between">
                              <h1 className="text-2xl font-bold text-purple-600">Lá Số Tử Vi</h1>
                              <nav className="flex gap-4">
                                   <Link href="/chart">
                                        <Button variant="ghost">Tính Lá Số</Button>
                                   </Link>
                                   <Link href="/batch">
                                        <Button variant="ghost">Tính Nhiều</Button>
                                   </Link>
                                   <Link href="/about">
                                        <Button variant="ghost">Giới Thiệu</Button>
                                   </Link>
                              </nav>
                         </div>
                    </div>
               </header>

               {/* Hero Section */}
               <section className="container mx-auto px-4 py-16 text-center">
                    <h2 className="text-4xl font-bold mb-4">
                         Tính Lá Số Tử Vi Online
                    </h2>
                    <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
                         Ứng dụng tính toán và phân tích lá số Tử Vi theo phương pháp truyền thống Việt Nam.
                         Nhanh chóng, chính xác và miễn phí.
                    </p>
                    <div className="flex gap-4 justify-center">
                         <Link href="/chart">
                              <Button size="lg" className="bg-purple-600 hover:bg-purple-700">
                                   <Calendar className="mr-2 h-5 w-5" />
                                   Tính Lá Số Ngay
                              </Button>
                         </Link>
                         <Link href="/batch">
                              <Button size="lg" variant="outline">
                                   <Users className="mr-2 h-5 w-5" />
                                   Tính Nhiều Lá Số
                              </Button>
                         </Link>
                    </div>
               </section>

               {/* Features */}
               <section className="container mx-auto px-4 py-16">
                    <h3 className="text-3xl font-bold text-center mb-12">
                         Tính Năng Nổi Bật
                    </h3>
                    <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                         <Card>
                              <CardHeader>
                                   <Calendar className="h-10 w-10 text-purple-600 mb-2" />
                                   <CardTitle>Chuyển Đổi Lịch</CardTitle>
                                   <CardDescription>
                                        Chuyển đổi chính xác giữa dương lịch và âm lịch
                                   </CardDescription>
                              </CardHeader>
                         </Card>

                         <Card>
                              <CardHeader>
                                   <BarChart3 className="h-10 w-10 text-purple-600 mb-2" />
                                   <CardTitle>Phân Tích Chi Tiết</CardTitle>
                                   <CardDescription>
                                        Phân tích 12 cung, sao chiếu mệnh và vận hạn
                                   </CardDescription>
                              </CardHeader>
                         </Card>

                         <Card>
                              <CardHeader>
                                   <Users className="h-10 w-10 text-purple-600 mb-2" />
                                   <CardTitle>Tính Nhiều Lá Số</CardTitle>
                                   <CardDescription>
                                        Tính toán và so sánh nhiều lá số cùng lúc
                                   </CardDescription>
                              </CardHeader>
                         </Card>

                         <Card>
                              <CardHeader>
                                   <FileText className="h-10 w-10 text-purple-600 mb-2" />
                                   <CardTitle>Xuất File PDF</CardTitle>
                                   <CardDescription>
                                        Lưu và in lá số dưới dạng file PDF
                                   </CardDescription>
                              </CardHeader>
                         </Card>
                    </div>
               </section>

               {/* Call to Action */}
               <section className="bg-purple-600 text-white py-16">
                    <div className="container mx-auto px-4 text-center">
                         <h3 className="text-3xl font-bold mb-4">
                              Sẵn Sàng Tính Lá Số?
                         </h3>
                         <p className="text-xl mb-8 opacity-90">
                              Chỉ cần vài phút để có lá số Tử Vi chi tiết và chính xác
                         </p>
                         <Link href="/chart">
                              <Button size="lg" variant="secondary">
                                   Bắt Đầu Ngay
                              </Button>
                         </Link>
                    </div>
               </section>

               {/* Footer */}
               <footer className="border-t py-8">
                    <div className="container mx-auto px-4 text-center text-muted-foreground">
                         <p>© 2025 Lá Số Tử Vi. Phát triển bởi Next.js 15 + FastAPI.</p>
                         <p className="text-sm mt-2">
                              Chỉ mang tính chất tham khảo. Không dùng cho mục đích mê tín dị đoan.
                         </p>
                    </div>
               </footer>
          </div>
     )
}
