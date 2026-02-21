"use client"

import { useState } from 'react'
import axios from 'axios'

export default function ImportJobsPage() {
    const [file, setFile] = useState<File | null>(null)

    // 简化的字段映射 (这里为了演示写死了几个默认映射关系，实际可做UI自由下拉选)
    const defaultMapping = {
        "职位名称": "job_name",
        "薪资": "salary_desc",
        "岗位描述": "post_description",
        "工作地点": "work_address",
        "要求技能": "show_skills",
        "经验要求": "experience_name",
        "学历": "degree_name",
        "职位分类": "position_name"
    }

    const [mappingStr, setMappingStr] = useState(JSON.stringify(defaultMapping, null, 2))
    const [loading, setLoading] = useState(false)
    const [result, setResult] = useState<any>(null)

    const handleImport = async () => {
        if (!file) return alert("请选择Excel文件")

        try {
            setLoading(true)
            const formData = new FormData()
            formData.append("file", file)
            formData.append("mapping_str", mappingStr)

            const { data } = await axios.post("http://localhost:8000/api/jobs/import", formData, {
                headers: { "Content-Type": "multipart/form-data" }
            })

            setResult(data)
        } catch (e: any) {
            alert("导入失败: " + e.message)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="max-w-4xl bg-white p-8 rounded-xl shadow-sm border border-gray-100">
            <h2 className="text-2xl font-bold mb-6 text-gray-800">职位批量分析与入库 (Excel -&gt; PGVector)</h2>

            <div className="space-y-6">
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">1. 选择文件 (.xlsx)</label>
                    <input
                        type="file"
                        accept=".xlsx"
                        onChange={(e) => setFile(e.target.files?.[0] || null)}
                        className="block w-full text-sm text-gray-500
              file:mr-4 file:py-2 file:px-4
              file:rounded-md file:border-0
              file:text-sm file:font-semibold
              file:bg-indigo-50 file:text-indigo-700
              hover:file:bg-indigo-100"
                    />
                </div>

                <div>
                    <label className="flex items-center text-sm font-medium text-gray-700 mb-2">
                        2. 表头映射关系 (JSON)
                    </label>
                    <textarea
                        className="w-full h-48 p-4 bg-gray-50 border border-gray-200 rounded-lg text-sm font-mono focus:ring-2 focus:ring-indigo-500 focus:outline-none"
                        value={mappingStr}
                        onChange={(e) => setMappingStr(e.target.value)}
                    />
                    <p className="mt-1 text-xs text-gray-500">
                        Key 为 Excel 表头名称，Value 为数据库字段名。请确保包含 `job_name` 和 `post_description` 以便生成向量。
                    </p>
                </div>

                <button
                    onClick={handleImport}
                    disabled={!file || loading}
                    className="bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2.5 px-6 rounded-lg shadow-sm disabled:opacity-50 transition w-full md:w-auto"
                >
                    {loading ? "处理中 (生成 Embeddings 需要时间)..." : "确认导入 & 生成向量"}
                </button>

                {result && (
                    <div className="mt-6 p-4 bg-green-50 text-green-700 rounded-lg border border-green-200">
                        <h4 className="font-semibold flex items-center gap-2">
                            🎉 导入成功
                        </h4>
                        <p className="mt-1 text-sm">成功将 {result.inserted} 条岗位存入 PostgreSQL，并自动构建向量特征引擎。</p>
                    </div>
                )}
            </div>
        </div>
    )
}
