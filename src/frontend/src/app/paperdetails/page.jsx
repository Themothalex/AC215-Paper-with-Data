'use client';
import React, { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { ArrowLeft, Users, Calendar, FileText, Database, Download, Link, BookOpen, GitBranch, Star, Eye } from 'lucide-react';
import { useRouter } from 'next/navigation';

export default function PaperDetails() {
    const router = useRouter();
    const searchParams = useSearchParams();
    const paperId = searchParams.get('id');
    const [paperDetails, setPaperDetails] = useState(null);

    useEffect(() => {
        // Retrieve paper details from localStorage
        const searchResults = JSON.parse(localStorage.getItem('searchResults') || '[]');
        const paper = searchResults.find(result => result.id === paperId);
        if (paper) {
            // Transform the paper data to match our UI structure
            setPaperDetails({
                title: paper.title,
                authors: paper.authors.split(', ').map(author => ({
                    name: author,
                    affiliation: '' // API doesn't provide affiliation
                })),
                publication: {
                    date: paper.views, // Using year as the date
                    venue: "Research Paper",
                    doi: "N/A" // API doesn't provide DOI
                },
                metrics: {
                    stars: paper.stars,
                    views: paper.views,
                    citations: "N/A" // API doesn't provide citations
                },
                abstract: paper.description,
                datasets: [],  // Could be populated if API provides dataset info
                methodology: [], // Could be populated if API provides methodology info
                results: {
                    metrics: [
                        { name: "Match Score", value: paper.stars, comparison: "" }
                    ],
                    keyFindings: [] // Could be populated if API provides key findings
                }
            });
        }
    }, [paperId]);

    if (!paperDetails) {
        return (
            <div className="min-h-screen bg-gray-50 flex items-center justify-center">
                <div className="text-gray-600">Loading paper details...</div>
            </div>
        );
    }

    const DatasetTable = ({ data, index }) => (
        <div className="bg-white rounded-lg shadow-sm overflow-hidden mb-6">
            <h3 className="text-lg font-semibold p-4 bg-blue-50 text-blue-800 border-b">
                Dataset {index + 1}: {data.formal_name}
            </h3>
            <div className="overflow-x-auto">
                <table className="w-full">
                    <tbody className="divide-y divide-gray-200">
                        {Object.entries(data)
                            .filter(([key]) => key !== 'usage_in_paper' && key !== 'formal_name')
                            .map(([key, value]) => (
                                <tr key={key}>
                                    <td className="px-4 py-3 bg-gray-50 font-medium text-gray-600 w-1/4">
                                        {key.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
                                    </td>
                                    <td className="px-4 py-3">{value}</td>
                                </tr>
                            ))}
                        {Object.entries(data.usage_in_paper).map(([key, value]) => (
                            <tr key={key}>
                                <td className="px-4 py-3 bg-gray-50 font-medium text-gray-600 w-1/4">
                                    {key.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
                                </td>
                                <td className="px-4 py-3">{value}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );

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
                            Year: {paperDetails.publication.date}
                        </div>
                        <div className="flex items-center gap-1">
                            <Star className="w-4 h-4" />
                            Match Score: {paperDetails.metrics.stars}
                        </div>
                    </div>

                    {/* Authors */}
                    <div className="flex items-center gap-2 mb-6">
                        <Users className="w-5 h-5 text-gray-600" />
                        <div className="flex flex-wrap gap-2">
                            {paperDetails.authors.map((author, index) => (
                                <span key={index} className="text-sm">
                                    <span className="font-medium">{author.name}</span>
                                    {index < paperDetails.authors.length - 1 && ", "}
                                </span>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Paper Details Grid */}
                <div className="grid grid-cols-1 gap-6">
                    {/* Abstract */}
                    <div>
                        <h2 className="text-xl font-semibold mb-4">Datasets Summary</h2>
                        {JSON.parse(paperDetails.abstract).map((dataset, index) => (
                            <DatasetTable key={index} data={dataset} index={index} />
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}