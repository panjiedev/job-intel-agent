import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import Link from 'next/link'
import { Briefcase, FileText, BarChart3, UploadCloud } from 'lucide-react'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Job Intel AI RAG System',
  description: 'AI-Native Job Search & Resume Analysis',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-gray-50 flex h-screen overflow-hidden`}>
        {/* Sidebar */}
        <aside className="w-64 bg-white border-r border-gray-200 flex flex-col">
          <div className="h-16 flex items-center px-6 border-b border-gray-200">
            <span className="text-xl font-bold text-indigo-600 flex items-center gap-2">
              <Briefcase className="w-6 h-6" />
              Job Intel Agent
            </span>
          </div>
          <nav className="flex-1 overflow-y-auto py-4">
            <ul className="space-y-1 px-3">
              <li>
                <Link href="/" className="flex items-center gap-3 px-3 py-2 text-gray-700 rounded-md hover:bg-gray-100 font-medium">
                  <BarChart3 className="w-5 h-5" />
                  智能数据大盘
                </Link>
              </li>
              <li>
                <Link href="/jobs/import" className="flex items-center gap-3 px-3 py-2 text-gray-700 rounded-md hover:bg-gray-100 font-medium">
                  <UploadCloud className="w-5 h-5" />
                  岗位批量录入
                </Link>
              </li>
              <li>
                <Link href="/resume" className="flex items-center gap-3 px-3 py-2 text-gray-700 rounded-md hover:bg-gray-100 font-medium">
                  <FileText className="w-5 h-5" />
                  简历对标分析
                </Link>
              </li>
            </ul>
          </nav>
        </aside>

        {/* Main Content */}
        <main className="flex-1 flex flex-col h-screen overflow-hidden">
          <header className="h-16 bg-white border-b border-gray-200 flex justify-between items-center px-8 shrink-0">
            <h1 className="text-lg font-semibold text-gray-800">AI 工作台</h1>
            <div className="text-sm text-gray-500">FastAPI + Next.js + RAG 架构</div>
          </header>
          <div className="flex-1 overflow-auto p-8">
            {children}
          </div>
        </main>
      </body>
    </html>
  )
}
