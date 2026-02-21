"use client"

import Link from "next/link"
import { BarChart3, UploadCloud, FileText, Database, CodeSquare } from "lucide-react"

export default function Home() {
  return (
    <div className="flex flex-col gap-8 flex-grow">
      {/* 头部欢迎 */}
      <div className="bg-gradient-to-r from-indigo-500 to-purple-600 rounded-2xl p-8 text-white shadow-md">
        <h1 className="text-3xl font-bold mb-4">欢迎来到 Job Intel RAG 分析系统</h1>
        <p className="text-indigo-100 max-w-2xl leading-relaxed">
          本项目依托 DashScope (Qwen/Embeddings) 与 PostgreSQL pgvector 构建，为您提供岗位分析、AI 原生简历向量检索和能力提升分析闭环服务。
        </p>
      </div>

      {/* 核心板块 */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

        <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition">
          <div className="w-12 h-12 bg-indigo-50 rounded-xl flex items-center justify-center text-indigo-600 mb-4">
            <UploadCloud className="w-6 h-6" />
          </div>
          <h3 className="text-xl font-bold text-gray-800 mb-2">职位矩阵落库</h3>
          <p className="text-gray-500 text-sm mb-6">
            动态映射不同表头的 Excel，批量生成文本向量（Embeddings）并存入关系型库。
          </p>
          <Link href="/jobs/import" className="text-indigo-600 font-medium hover:text-indigo-800 flex items-center gap-1">
            Go to Import <span aria-hidden="true">&rarr;</span>
          </Link>
        </div>

        <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition">
          <div className="w-12 h-12 bg-emerald-50 rounded-xl flex items-center justify-center text-emerald-600 mb-4">
            <FileText className="w-6 h-6" />
          </div>
          <h3 className="text-xl font-bold text-gray-800 mb-2">简历 RAG 验证</h3>
          <p className="text-gray-500 text-sm mb-6">
            采用 text-embedding-v3 技术，在海量岗位中进行简历相似度余弦检测匹配。
          </p>
          <Link href="/resume" className="text-emerald-600 font-medium hover:text-emerald-800 flex items-center gap-1">
            Start Analysis <span aria-hidden="true">&rarr;</span>
          </Link>
        </div>

        <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition">
          <div className="w-12 h-12 bg-orange-50 rounded-xl flex items-center justify-center text-orange-600 mb-4">
            <BarChart3 className="w-6 h-6" />
          </div>
          <h3 className="text-xl font-bold text-gray-800 mb-2">大盘与职业规划 (WIP)</h3>
          <p className="text-gray-500 text-sm mb-6">
            由大语言模型反推提炼指定岗群落的技能共性，帮助候选人绘制缺口雷达。
          </p>
          <span className="text-gray-400 font-medium cursor-not-allowed">Coming Next</span>
        </div>

      </div>

      <div className="mt-6 flex items-center gap-4 text-sm text-gray-500 border-t border-gray-200 pt-6">
        <span className="flex items-center gap-2"><Database className="w-4 h-4" /> PostgreSQL (pgvector)</span>
        <span className="flex items-center gap-2"><CodeSquare className="w-4 h-4" /> FastAPI</span>
        <span className="flex items-center gap-2"><CodeSquare className="w-4 h-4" /> Next.js 14 (App)</span>
      </div>
    </div>
  )
}
