'use client';
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function ResearchPage() {
    const [variables, setVariables] = useState([]);
    const [independentVar, setIndependentVar] = useState('');
    const [dependentVar, setDependentVar] = useState('');
    const [selectedResult, setSelectedResult] = useState(null);
    const [selectedVariable, setSelectedVariable] = useState(null);
    const [variableFeatures, setVariableFeatures] = useState([]);
    const [newFeature, setNewFeature] = useState({ feature: '', value: '' });
    const [hasSearched, setHasSearched] = useState(false);
    const [searchResults, setSearchResults] = useState([]);

    const independentVariables = [  ];
    const dependentVariables = [   ];

    const router = useRouter();

    const addVariable = (type) => {
        if (type === 'independent' && independentVar) {
            setVariables([...variables, { type: 'independent', name: independentVar }]);
            setIndependentVar('');
        } else if (type === 'dependent' && dependentVar) {
            setVariables([...variables, { type: 'dependent', name: dependentVar }]);
            setDependentVar('');
        }
    };

    // Filter variables by type
    const addedIndependentVars = variables.filter(v => v.type === 'independent');
    const addedDependentVars = variables.filter(v => v.type === 'dependent');


    // Handle variable selection
    const handleVariableSelect = (variable) => {
        // Store features in the variables array when switching variables
        if (selectedVariable) {
            setVariables(variables.map(v =>
                v.name === selectedVariable.name
                    ? { ...v, features: variableFeatures }
                    : v
            ));
        }

        // Set new selected variable and load its features
        setSelectedVariable(variable);
        setVariableFeatures(variable.features || []);
    };

    // Add new feature
    const addFeature = () => {
        if (newFeature.feature && newFeature.value) {
            const updatedFeatures = [...variableFeatures, { ...newFeature }];
            setVariableFeatures(updatedFeatures);
            setNewFeature({ feature: '', value: '' });

            // Update the features in the variables array
            setVariables(variables.map(v =>
                v.name === selectedVariable.name
                    ? { ...v, features: updatedFeatures }
                    : v
            ));
        }
    };
       // Remove feature
    const removeFeature = (index) => {
        const updatedFeatures = variableFeatures.filter((_, i) => i !== index);
        setVariableFeatures(updatedFeatures);

        // Update the features in the variables array
        setVariables(variables.map(v =>
            v.name === selectedVariable.name
                ? { ...v, features: updatedFeatures }
                : v
        ));
    };

       // Handle search
       const handleSearch2 = () => {
        const searchData = {
            variables: variables.map(variable => ({
                name: variable.name,
                type: variable.type,
                features: variable.features || []
            }))
        };

        console.log('Search data:', searchData);
        setHasSearched(true);
        // Make API call here
        // apiCall(searchData);
    };


        const handleSearch = async () => {
        const searchData = {
            independent_variable: addedIndependentVars.map(v => v.name).join(', '),
            dependent_variable: addedDependentVars.map(v => v.name).join(', ')
        };

        try {
            const response = await fetch('http://34.27.230.188:9000/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(searchData)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log('API response:', data);

            // Transform the API response to match your UI structure
            const formattedResults = data.results.map(result => ({
                id: Math.random().toString(), // Or use a proper ID from your backend
                title: result.study_title,
                authors: Array.isArray(result.authors) ? result.authors.join(', ') : result.authors,
                description: result.summary,
                topic: "Research Paper", // Add appropriate topic from your backend
                stars: result.similarity_score ? `${(result.similarity_score * 100).toFixed(1)}%` : "N/A",
                views: result.publication_year || "N/A",
                thumbnail: "/api/placeholder/120/80"
                }));

            setSearchResults(formattedResults);
            setHasSearched(true);
        } catch (error) {
            console.error('Error fetching search results:', error);
        }
    };

    // const searchResults = Array(6).fill({
    //     id: 1,
    //     title: "Depth Pro: Sharp Monocular Metric Depth in Less Than a Second",
    //     authors: "applehit depth-pro • arXiv/cs • 2 Oct 2024",
    //     description: "We present a foundation model for zero-shot metric monocular depth estimation.",
    //     topic: "Monocular Depth Estimation",
    //     stars: "2,408",
    //     views: "4.23 stars / hour",
    //     thumbnail: "/api/placeholder/120/80"
    // });


    return (
            <div className="min-h-screen bg-gray-100">
                <div className="flex">
                {/* Left Column - Variables */}
                <div className="w-90 bg-gray-100 min-h-screen p-4">
                        <h2 className="text-xl font-bold mb-4 md:text-2xl text-center">Add Variables</h2>

                        <div className="grid grid-cols-2 gap-4">
                            {/* Independent Variables Column */}
                            <div className="space-y-2">
                                <div className="bg-red-50 p-4 rounded-lg">
                                    <h3 className="font-semibold mb-2">Independent Variable</h3>
                                    <div className="flex gap-2">
                                        <input
                                            type="text"
                                            value={independentVar}
                                            onChange={(e) => setIndependentVar(e.target.value)}
                                            className="flex-1 p-2 border rounded bg-white"
                                            placeholder="Enter variable"
                                        />
                                        <button
                                            onClick={() => addVariable('independent')}
                                            className="text-red-500 text-xl font-bold"
                                        >
                                            +
                                        </button>
                                    </div>
                                </div>
                                {/* Variables list - only show once */}
                                {variables.filter(v => v.type === 'independent').map((variable, index) => (
                                    <div
                                        key={index}
                                        className={`p-2 rounded-lg bg-red-100 cursor-pointer ${
                                            selectedVariable?.name === variable.name ? 'ring-2 ring-red-500' : ''
                                        }`}
                                        onClick={() => handleVariableSelect(variable)}
                                    >
                                        {variable.name}
                                    </div>
                                ))}
                                {/* Predefined Independent Variables */}
                                {independentVariables.map((variable, index) => (
                                    <div
                                        key={`predefined-${index}`}
                                        className="p-2 rounded-lg cursor-pointer bg-red-100"
                                    >
                                        {variable}
                                    </div>
                                ))}
                            </div>

                            {/* Dependent Variables Column */}
                            <div className="space-y-2">
                                <div className="bg-blue-50 p-4 rounded-lg">
                                    <h3 className="font-semibold mb-2">Dependent Variable</h3>
                                    <div className="flex gap-2">
                                        <input
                                            type="text"
                                            value={dependentVar}
                                            onChange={(e) => setDependentVar(e.target.value)}
                                            className="flex-1 p-2 border rounded bg-white"
                                            placeholder="Enter variable"
                                        />
                                        <button
                                            onClick={() => addVariable('dependent')}
                                            className="text-blue-500 text-xl font-bold"
                                        >
                                            +
                                        </button>
                                    </div>
                                </div>
                                {/* Variables list - only show once */}
                                {variables.filter(v => v.type === 'dependent').map((variable, index) => (
                <div
                                        key={index}
                                        className={`p-2 rounded-lg bg-blue-100 cursor-pointer ${
                                            selectedVariable?.name === variable.name ? 'ring-2 ring-blue-500' : ''
                                        }`}
                                        onClick={() => handleVariableSelect(variable)}
                                    >
                                        {variable.name}
                                    </div>
                                ))}
                                {/* Predefined Dependent Variables */}
                                {dependentVariables.map((variable, index) => (
                                    <div
                                        key={`predefined-${index}`}
                                        className="p-2 rounded-lg cursor-pointer bg-blue-100"
                                    >
                                        {variable}
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* Variable Details */}
                        <div className="mt-8">
                        <h3 className="text-lg font-semibold mb-4">Variable Details:</h3>
                         <div className="bg-white p-4 rounded-lg shadow">
                    {selectedVariable ? (
                        <div className="space-y-4">
                            <div className="text-lg font-medium mb-4">
                                Selected: {selectedVariable.name}
                            </div>
                            <div className="flex items-center justify-between">
                                <span className="font-medium">Variable Feature</span>
                                <span className="font-medium">Feature Value</span>
                            </div>

                            {/* Show added features */}
                            {variableFeatures.map((feature, index) => (
                                <div key={index} className="flex items-center justify-between">
                                    <input
                                        type="text"
                                        value={feature.feature}
                                        className="w-32 p-2 border rounded"
                                        readOnly
                                    />
                                    <div className="flex items-center gap-2">
                                        <input
                                            type="text"
                                            value={feature.value}
                                            className="w-32 p-2 border rounded"
                                            readOnly
                                        />
                                        <button
                                            onClick={() => removeFeature(index)}
                                            className="text-red-500 text-xl font-bold"
                                        >
                                            -
                                        </button>
                                    </div>
                                </div>
                            ))}
                            {/* New feature input */}
                            <div className="flex items-center justify-between">
                                <input
                                    type="text"
                                    value={newFeature.feature}
                                    onChange={(e) => setNewFeature({...newFeature, feature: e.target.value})}
                                    className="w-32 p-2 border rounded"
                                    placeholder="New feature"
                                />
                                <div className="flex items-center gap-2">
                                    <input
                                        type="text"
                                        value={newFeature.value}
                                        onChange={(e) => setNewFeature({...newFeature, value: e.target.value})}
                                        className="w-32 p-2 border rounded"
                                        placeholder="New value"
                                    />
                                    <button
                                        onClick={addFeature}
                                        className="text-red-500 text-xl font-bold"
                                    >
                                        +
                                    </button>
                                </div>
                            </div>
                        </div>
                    ) : (
                        <div className="text-gray-500 text-center">
                            Select a variable to add details
                        </div>
                    )}
                         </div>
                            
                         {/* Search Button */}

                         <div className="fixed bottom-8 ml-24"> {/* Position fixed at bottom with margin */}
                        <button
                            onClick={handleSearch}
                            className="bg-blue-500 text-white px-8 py-3 rounded-lg flex items-center gap-2 hover:bg-blue-600 shadow-lg w-64"
                        >
                            <svg
                                className="w-5 h-5"
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                            >
                                <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth={2}
                                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                                />
                            </svg>
                            Search Papers
                        </button>
                    </div>


            </div>
                </div>


                 {/* Middle Column - Search Results */}
                    
                <div className="flex-1 p-4">
                    <h2 className="text-xl font-bold mb-4 text-center">Paper Results</h2>
                        <div className="bg-white rounded-lg shadow min-h-screen">
                            {hasSearched ? (
                                <div className="p-4 space-y-4">
                                        {searchResults.map((result, index) => (
                                <div
                        key={index}
                        className="p-4 bg-white border rounded-lg hover:shadow-md transition-shadow cursor-pointer"
                        onClick={() => setSelectedResult(result)}
                    >
                        {/* Basic Info Section */}
                        <div className="flex gap-4">
                            <div className="flex-shrink-0">
                                <img
                                    src={result.thumbnail}
                                    alt="Preview"
                                    className="w-32 h-24 object-cover rounded"
                                />
                            </div>
                            {/* <div className="flex-1">
                                <h3 className="font-semibold text-lg">{result.title}</h3>
                                <p className="text-sm text-gray-600">{result.authors}</p>
                                <p className="text-sm mt-1">{result.description}</p>
                                <div className="flex items-center justify-between mt-2">
                                    <div className="flex items-center gap-2">
                                        <span className="text-sm bg-purple-100 text-purple-800 px-2 py-1 rounded">
                                            {result.topic}
                                        </span>
                                        <span className="text-sm text-gray-600">
                                    ★ {result.stars} • {result.views}
                                        </span>
                                    </div>
                                    <div className="flex gap-2">
                                    <button 
                                            onClick={(e) => {
                                                e.stopPropagation();
                                                router.push(`/paperdetails?id=${result.id}`);
                                            }}
                                            className="px-4 py-1 bg-teal-600 text-white rounded hover:bg-teal-700"
                                        >
                                            Paper
                                        </button>
                                    </div>
                                </div>
                            </div> */}
                                <div className="flex-1">
    <h3 className="font-semibold text-lg">{result.title}</h3>
    <p className="text-sm text-gray-600">Authors: {result.authors}</p>
    <p className="text-sm mt-1">{result.description}</p>
    <div className="flex items-center justify-between mt-2">
        <div className="flex items-center gap-2">
            <span className="text-sm bg-purple-100 text-purple-800 px-2 py-1 rounded">
                Match Score: {result.stars}
            </span>
            <span className="text-sm text-gray-600">
                Year: {result.views}
            </span>
        </div>
        <div className="flex gap-2">
            <button
                onClick={(e) => {
                    e.stopPropagation();
                    router.push(`/paperdetails?id=${result.id}`);
                }}
                className="px-4 py-1 bg-teal-600 text-white rounded hover:bg-teal-700"
            >
                Paper
            </button>
        </div>
    </div>
</div>

                        </div>
                    </div>
                ))}
            </div>
        ) : (
            <div className="flex items-center justify-center h-full text-gray-500">
                Add variables and click search to find relevant papersss
            </div>
        )}
    </div>
                </div>

                {/* Right Column - Dataset Details */}

                {selectedResult && (
                    <div className="w-80 bg-gray-100 min-h-screen p-4">
                     <h2 className="text-xl font-bold mb-4">Dataset Details:</h2>
                        <div className="space-y-4">
                         <div className="bg-white p-4 rounded-lg shadow">
                                <p className="text-sm space-y-1">
                                    <span className="font-semibold">Title:</span> {selectedResult.title}<br/>
                                    <span className="font-semibold">Authors:</span> {selectedResult.authors}<br/>
                                    <span className="font-semibold">Publication Year:</span> {selectedResult.views}<br/>
                                    <span className="font-semibold">Similarity Score:</span> {selectedResult.stars}<br/>
                                    <span className="font-semibold">Summary:</span><br/>
                                    <span className="text-gray-600">{selectedResult.description}</span>
                </p>
            </div>
        </div>
    </div>
)}
            </div>
        </div>
    );
}
