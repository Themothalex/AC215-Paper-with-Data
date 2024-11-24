'use client';
import React from 'react';
import { useSearchParams } from 'next/navigation';
import { ArrowLeft, Users, Calendar, FileText, Database, Download, Link, BookOpen, GitBranch, Star, Eye } from 'lucide-react';
import { useRouter } from 'next/navigation';

export default function PaperDetails() {
    const router = useRouter();
    const searchParams = useSearchParams();
    const paperId = searchParams.get('id');

    // Replace with API fetched data
    const paperDetails = {
        title: "Depth Pro: Sharp Monocular Metric Depth in Less Than a Second",
        authors: [
            { name: "John Smith", affiliation: "Stanford University" },
            { name: "Alice Johnson", affiliation: "MIT" },
            { name: "Bob Williams", affiliation: "Google Research" }
        ],
        publication: {
            date: "2 Oct 2024",
            venue: "arXiv/cs",
            doi: "10.1234/5678.9012"
        },
        metrics: {
            stars: "2,408",
            views: "4.23 stars/hour",
            citations: "156"
        },
        abstract: "We present a foundation model for zero-shot metric monocular depth estimation. Our approach leverages recent advances in transformer architectures and self-supervised learning to achieve state-of-the-art results across multiple benchmarks. The model demonstrates robust performance in challenging real-world scenarios and operates in real-time on consumer hardware.",
        datasets: [
            {
                name: "KITTI Dataset",
                type: "Image Sequences",
                samples: "50,000 frames",
                description: "Real-world driving scenarios with depth ground truth"
            },
            {
                name: "NYU Depth V2",
                type: "RGB-D Images",
                samples: "120,000 frames",
                description: "Indoor scenes with accurate depth measurements"
            }
        ],
        methodology: [
            "Novel transformer-based architecture",
            "Self-supervised training pipeline",
            "Multi-scale feature fusion",
            "Adaptive depth range prediction"
        ],
        results: {
            metrics: [
                { name: "RMSE", value: "0.128", comparison: "15% improvement" },
                { name: "δ < 1.25", value: "0.956", comparison: "State-of-the-art" },
                { name: "Runtime", value: "45ms", comparison: "2x faster" }
            ],
            keyFindings: [
                "Superior performance in low-light conditions",
                "Robust depth estimation at varying scales",
                "Minimal domain gap between synthetic and real data"
            ]
        }
    };

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Top Navigation Bar */}
            <div className="bg-white border-b">
                <div className="max-w-7xl mx-auto px-4 py-4">
                    <button 
                        onClick={() => router.back()}
                        className="flex items-center text-gray-600 hover:text-gray-900"
                    >
                        <ArrowLeft className="w-5 h-5 mr-2" />
                        Back to Search
                    </button>
                </div>
            </div>

            {/* Main Content */}
            <div className="max-w-7xl mx-auto px-4 py-8">
                {/* Paper Title and Metrics */}
                <div className="bg-white rounded-lg shadow-sm p-8 mb-6">
                    <h1 className="text-3xl font-bold mb-4">{paperDetails.title}</h1>
                    
                    <div className="flex items-center gap-6 text-sm text-gray-600 mb-6">
                        <div className="flex items-center gap-1">
                            <Calendar className="w-4 h-4" />
                            {paperDetails.publication.date}
                        </div>
                        <div className="flex items-center gap-1">
                            <Star className="w-4 h-4" />
                            {paperDetails.metrics.stars} stars
                        </div>
                        <div className="flex items-center gap-1">
                            <Eye className="w-4 h-4" />
                            {paperDetails.metrics.views}
                        </div>
                        <div className="flex items-center gap-1">
                            <BookOpen className="w-4 h-4" />
                            {paperDetails.metrics.citations} citations
                        </div>
                    </div>

                    {/* Authors */}
                    <div className="flex items-center gap-2 mb-6">
                        <Users className="w-5 h-5 text-gray-600" />
                        <div className="flex flex-wrap gap-2">
                            {paperDetails.authors.map((author, index) => (
                                <span key={index} className="text-sm">
                                    <span className="font-medium">{author.name}</span>
                                    <span className="text-gray-600"> ({author.affiliation})</span>
                                    {index < paperDetails.authors.length - 1 && ", "}
                                </span>
                            ))}
                        </div>
                    </div>

                    {/* Action Buttons */}
                    <div className="flex gap-4">
                        <button className="flex items-center gap-2 px-4 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700">
                            <Download className="w-4 h-4" />
                            Download PDF
                        </button>
                        <button className="flex items-center gap-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600">
                            <GitBranch className="w-4 h-4" />
                            View Code
                        </button>
                        <button className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
                            <Link className="w-4 h-4" />
                            DOI: {paperDetails.publication.doi}
                        </button>
                    </div>
                </div>

                {/* Paper Details Grid */}
                <div className="grid grid-cols-3 gap-6">
                    {/* Abstract */}
                    <div className="col-span-2 space-y-6">
                        <div className="bg-white rounded-lg shadow-sm p-6">
                            <h2 className="text-xl font-semibold mb-4">Abstract</h2>
                            <p className="text-gray-700 leading-relaxed">
                                {paperDetails.abstract}
                            </p>
                        </div>

                        {/* Methodology */}
                        <div className="bg-white rounded-lg shadow-sm p-6">
                            <h2 className="text-xl font-semibold mb-4">Methodology</h2>
                            <ul className="list-disc list-inside space-y-2 text-gray-700">
                                {paperDetails.methodology.map((method, index) => (
                                    <li key={index}>{method}</li>
                                ))}
                            </ul>
                        </div>

                        {/* Results */}
                        <div className="bg-white rounded-lg shadow-sm p-6">
                            <h2 className="text-xl font-semibold mb-4">Results</h2>
                            <div className="grid grid-cols-3 gap-4 mb-6">
                                {paperDetails.results.metrics.map((metric, index) => (
                                    <div key={index} className="bg-gray-50 p-4 rounded-lg">
                                        <div className="text-sm text-gray-600">{metric.name}</div>
                                        <div className="text-lg font-semibold">{metric.value}</div>
                                        <div className="text-sm text-green-600">{metric.comparison}</div>
                                    </div>
                                ))}
                            </div>
                            <div>
                                <h3 className="font-medium mb-2">Key Findings</h3>
                                <ul className="list-disc list-inside space-y-1 text-gray-700">
                                    {paperDetails.results.keyFindings.map((finding, index) => (
                                        <li key={index}>{finding}</li>
                                    ))}
                                </ul>
                            </div>
                        </div>
                    </div>

                    {/* Datasets Sidebar */}
                    <div className="space-y-6">
                        <div className="bg-white rounded-lg shadow-sm p-6">
                            <h2 className="text-xl font-semibold mb-4">Datasets</h2>
                            <div className="space-y-4">
                                {paperDetails.datasets.map((dataset, index) => (
                                    <div key={index} className="border-b last:border-b-0 pb-4 last:pb-0">
                                        <h3 className="font-medium text-lg mb-2">{dataset.name}</h3>
                                        <div className="space-y-2 text-sm text-gray-600">
                                            <p><span className="font-medium">Type:</span> {dataset.type}</p>
                                            <p><span className="font-medium">Samples:</span> {dataset.samples}</p>
                                            <p>{dataset.description}</p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}