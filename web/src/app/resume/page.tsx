"use client"

import { useState } from 'react'
import axios from 'axios'
import { CheckCircle, AlertCircle, RefreshCw } from 'lucide-react'

export default function ResumePage() {
    const [file, setFile] = useState<File | null>(null)
    const [loading, setLoading] = useState(false)
    const [resumeExtract, setResumeExtract] = useState<any>(null)

    const [matchLoading, setMatchLoading] = useState(false)
    const [matchedJobs, setMatchedJobs] = useState<any[]>([])

    const handleUploadResume = async () => {
        if (!file) return alert("请先选择以.txt或.md结尾的简历文件")
        setLoading(true)
        try {
            const formData = new FormData()
            formData.append("file", file)

            const { data } = await axios.post("http://localhost:8000/api/resume/upload", formData, {
                headers: { "Content-Type": "multipart/form-data" }
            })
            alert("上传与标签化成功")
            setResumeExtract({ id: data.resume_id, content: data.extracted })

        } catch (e: any) {
            alert("解析失败: " + e.message)
        } finally {
            setLoading(false)
        }
    }

    const handleMatch = async () => {
        if (!resumeExtract) return alert("请先上传简历提取特征")
        setMatchLoading(true)
        try {
            const res = await axios.get(`http://localhost:8000/api/resume/match/${resumeExtract.id}?top_k=5`)
            setMatchedJobs(res.data)
        } catch (e: any) {
            alert("匹配错误: " + e.message)
        } finally {
            setMatchLoading(false)
        }
    }

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 flex-grow gap-8">
            {/* 操作面板 */}
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex flex-col">
                <h2 className="text-xl font-bold mb-6 text-gray-800 flex items-center gap-2">
                    <FileText className="w-5 h-5 text-indigo-500" />
                    Upload Resume (MD/TXT)
                </h2>

                <input
                    type="file"
                    accept=".txt,.md"
                    onChange={(e) => setFile(e.target.files?.[0] || null)}
                    className="mb-4 block w-full text-sm text-gray-500
            file:mr-4 file:py-2 file:px-4
            file:rounded-md file:border-0
            file:text-sm file:font-semibold
            file:bg-indigo-50 file:text-indigo-700
            hover:file:bg-indigo-100"
                />

                <button
                    onClick={handleUploadResume}
                    disabled={!file || loading}
                    className="bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2.5 px-6 rounded-lg w-full transition disabled:opacity-50"
                >
                    {loading ? "RAG Vector Extracting..." : "Upload & Analyze Resume"}
                </button>

                {resumeExtract && (
                    <div className="mt-8 p-4 bg-gray-50 border border-indigo-100 rounded-lg">
                        <h4 className="font-semibold text-gray-700 text-sm flex items-center gap-1"><CheckCircle className="w-4 h-4 text-green-500" /> 核心特征提取</h4>
                        <p className="whitespace-pre-wrap mt-2 text-sm text-gray-600 font-mono bg-white p-3 rounded">
                            {resumeExtract.content}
                        </p>

                        <button
                            onClick={handleMatch}
                            disabled={matchLoading}
                            className="mt-4 flex justify-center items-center gap-2 bg-gray-900 text-white w-full rounded py-2 hover:bg-gray-800 transition"
                        >
                            {matchLoading ? <RefreshCw className="w-4 h-4 animate-spin" /> : "开始从职位库 (Job Library) RAG 匹配"}
                        </button>
                    </div>
                )}
            </div>

            {/* 匹配结果展示板 */}
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 overflow-auto">
                <h2 className="text-xl font-bold mb-6 text-gray-800">Job RAG Matches Top 5</h2>

                {matchedJobs.length > 0 ? (
                    <div className="space-y-4">
                        {matchedJobs.map((job, i) => (
                            <div key={job.id} className="p-4 rounded-xl border border-gray-200 shadow-sm hover:border-indigo-300 transition-colors">
                                <h3 className="font-bold flex justify-between">
                                    <span className="text-gray-800">{i + 1}. {job.job_name}</span>
                                    <span className="text-xs font-mono bg-indigo-50 text-indigo-700 px-2 py-1 rounded">Score: 匹配度极高</span>
                                </h3>
                                <div className="text-sm mt-2 text-gray-600">
                                    <strong>核心技能: </strong> {job.skills || "未提取"}
                                </div>
                                <button className="mt-3 text-sm text-indigo-600 hover:text-indigo-800 font-medium w-full text-right">
                                    获取 3 个月强化学习计划 →
                                </button>
                            </div>
                        ))}
                    </div>
                ) : (
                    <div className="flex flex-col items-center justify-center h-48 text-gray-400">
                        <AlertCircle className="w-10 h-10 mb-2 opacity-50" />
                        <span className="text-sm">暂无匹配数据，等待指令</span>
                    </div>
                )}
            </div>
        </div >
    )
}

function FileText(props: any) {
    return <svg {...props} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
    </svg>
}
