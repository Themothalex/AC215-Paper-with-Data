'use client';

import Link from 'next/link';

export default function Home() {
    return (
        <div className="page-wrapper">
            {/* Hero Section */}
            <section className="hero-section relative min-h-screen flex items-center justify-center bg-blue-50">
                <div className="hero-content relative">
                    <div className="relative">
                        {/* PAPER squares */}
                        <div className="absolute -left-12 top-4 w-8 h-8 bg-blue-500 rounded-md" />
                        <div className="absolute -right-12 top-4 w-8 h-8 bg-blue-500 rounded-md" />
                        
                        {/* DATA squares */}
                        <div className="absolute -left-12 bottom-4 w-8 h-8 bg-blue-500 rounded-md" />
                        <div className="absolute -right-12 bottom-4 w-8 h-8 bg-blue-500 rounded-md" />
                        
                        <h1 className="text-7xl font-bold text-center text-blue-500 leading-relaxed">
                            PAPER<br />
                            <span className="text-5xl">with</span><br />
                            DATA
                        </h1>
                    </div>

                    <div className="text-center py-8 max-w-4xl mx-auto px-4">
    <h2 className="text-3xl font-bold text-blue-600 mb-4">
        We help you to find the most relevant papers to your research
    </h2>
    <div className="space-y-4">
        <p className="text-blue-800 text-lg">
            Define your variables of interest and discover research papers perfectly aligned with your study
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
            <div className="p-4 bg-blue-50 rounded-lg border border-blue-100">
                <div className="text-blue-600 font-semibold mb-2">Smart Search</div>
                <p className="text-blue-700 text-sm">
                    Our algorithm matches your research variables with thousands of academic papers
                </p>
            </div>
            <div className="p-4 bg-blue-50 rounded-lg border border-blue-100">
                <div className="text-blue-600 font-semibold mb-2">Precise Matching</div>
                <p className="text-blue-700 text-sm">
                    Get match scores to identify the most relevant papers for your research
                </p>
            </div>
            <div className="p-4 bg-blue-50 rounded-lg border border-blue-100">
                <div className="text-blue-600 font-semibold mb-2">Detailed Analysis</div>
                <p className="text-blue-700 text-sm">
                    Explore comprehensive paper summaries and dataset details
                </p>
            </div>
        </div>
    </div>
</div>

                    <div className="flex justify-center gap-4 mt-12">
                      <Link href="/search" className="block">
                        <button className="px-8 py-3 bg-blue-500 text-white text-xl rounded-md hover:bg-blue-600 transition-colors">
                            Get Started
                        </button>
                        </Link>
                        <button className="px-8 py-3 border-2 border-blue-500 text-blue-500 text-xl rounded-md hover:bg-blue-50 transition-colors">
                            Learn More
                        </button>
                    </div>
                </div>
            </section>

            {/* Content Section */}
            <section className="content-section">
                <div className="content-grid">
                    <Link href="/image" className="block">
                        <div className="feature-card">
                            <h3 className="feature-card-title">Enhanced Precision in Academia Searches</h3>
                            <p className="feature-card-description">
                              Unlike traditional keyword-based academic search engines, this platform offers fine-grained dataset categorization and relationship-based filtering. Researchers can specify dataset variables and relationships, quickly isolating relevant papers and reducing time spent filtering irrelevant results
                            </p>
                        </div>
                    </Link>

                    <Link href="/audio" className="block">
                        <div className="feature-card">
                            <h3 className="feature-card-title">Integration of Comprehensive Data Sources </h3>
                            <p className="feature-card-description">
                            Leveraging structured metadata from academic journals and popular datasets, this system provides an integrated search experience. With consistent data quality and full access to both metadata and article content, researchers benefit from a robust and reliable resource for literature discovery.
                            </p>
                        </div>
                    </Link>
                </div>
            </section>
        </div>
    );
}