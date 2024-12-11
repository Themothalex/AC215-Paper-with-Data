'use client';
import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Search } from 'lucide-react';


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
        // Find the complete variable object with its features from the variables array
        const selectedVarWithFeatures = variables.find(v => v.name === variable.name);
        
        // Set the new selected variable
        setSelectedVariable(selectedVarWithFeatures);
        
        // Set the features from the found variable
        if (selectedVarWithFeatures) {
            setVariableFeatures(selectedVarWithFeatures.features || []);
        } else {
            setVariableFeatures([]);
        }
    };

    // Add new feature
    const addFeature = () => {
        if (newFeature.feature && newFeature.value) {
            const updatedFeatures = [...variableFeatures, { ...newFeature }];
            setVariableFeatures(updatedFeatures);
            setNewFeature({ feature: '', value: '' });

            // Update the features in the variables array immediately
            setVariables(prevVariables => prevVariables.map(v =>
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

        // Update the features in the variables array immediately
        setVariables(prevVariables => prevVariables.map(v =>
            v.name === selectedVariable.name
                ? { ...v, features: updatedFeatures }
                : v
        ));
    };

    const deleteVariable = (variableName) => {
        // Remove the variable from the variables array
        const updatedVariables = variables.filter(v => v.name !== variableName);
        setVariables(updatedVariables);
        
        // If the deleted variable was selected, clear the selection
        if (selectedVariable?.name === variableName) {
            setSelectedVariable(null);
            setVariableFeatures([]);
        }
    };

    useEffect(() => {
        const storedResults = localStorage.getItem('searchResults');
        const searchedBefore = localStorage.getItem('hasSearched');
        const storedVariables = localStorage.getItem('variables');
        const storedSelectedVariable = localStorage.getItem('selectedVariable');
        const storedVariableFeatures = localStorage.getItem('variableFeatures');

        if (storedResults) {
            setSearchResults(JSON.parse(storedResults));
        }
        if (searchedBefore === 'true') {
            setHasSearched(true);
        }
        if (storedVariables) {
            setVariables(JSON.parse(storedVariables));
        }
        if (storedSelectedVariable) {
            setSelectedVariable(JSON.parse(storedSelectedVariable));
        }
        if (storedVariableFeatures) {
            setVariableFeatures(JSON.parse(storedVariableFeatures));
        }
    }, []);


    // Save variables state whenever it changes
    useEffect(() => {
        localStorage.setItem('variables', JSON.stringify(variables));
    }, [variables]);

    // Save selected variable state whenever it changes
    useEffect(() => {
        localStorage.setItem('selectedVariable', JSON.stringify(selectedVariable));
    }, [selectedVariable]);

    // Save variable features whenever they change
    useEffect(() => {
        localStorage.setItem('variableFeatures', JSON.stringify(variableFeatures));
    }, [variableFeatures]);

     // Add useEffect to save variables state whenever it changes
     useEffect(() => {
        if (variables.length > 0) {
            localStorage.setItem('variables', JSON.stringify(variables));
        }
    }, [variables]);


    // Handle search
    const handleSearch2 = async () => {
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

    const handleSearch = async () => {
        const addedIndependentVars = variables.filter(v => v.type === 'independent');
        const addedDependentVars = variables.filter(v => v.type === 'dependent');
    
        const searchData = {
            independent_variable: addedIndependentVars.map(v => v.name).join(', '),
            dependent_variable: addedDependentVars.map(v => v.name).join(', '),
            variables: variables.map(variable => ({
                name: variable.name,
                type: variable.type,
                features: variable.features || []
            }))
        };
    
        try {
            const response = await fetch('http://34.27.230.188:9000/search', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(searchData)
            });
    
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
    
            const data = await response.json();
    
            const formattedResults = data.results.map(result => ({
                id: Math.random().toString(),
                title: result.study_title,
                authors: Array.isArray(result.authors) ? result.authors.join(', ') : result.authors,
                description: result.summary,
                topic: "Research Paper",
                stars: result.similarity_score ? `${(result.similarity_score * 100).toFixed(1)}%` : "N/A",
                views: result.publication_year || "N/A",
                thumbnail: "/api/placeholder/120/80"
            }));
    
            setSearchResults(formattedResults);
            setHasSearched(true);
    
            localStorage.setItem('searchResults', JSON.stringify(formattedResults));
            localStorage.setItem('hasSearched', 'true');
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
                <h2 className="text-xl font-bold mb-4 md:text-2xl text-center text-white bg-gradient-to-r from-blue-300 to-blue-600 py-2 px-4 rounded-lg">Add Variables</h2>

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
                                    className={`p-2 rounded-lg bg-red-100 flex items-center justify-between ${
                                        selectedVariable?.name === variable.name ? 'ring-2 ring-red-500' : ''
                                    }`}
                                >
                                    <div
                                        className="flex-grow cursor-pointer"
                                        onClick={() => handleVariableSelect(variable)}
                                    >
                                        {variable.name}
                                    </div>
                                    <button
                                        onClick={() => deleteVariable(variable.name)}
                                        className="text-red-600 hover:text-red-800 ml-2 px-2"
                                    >
                                        ×
                                    </button>
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
                                        className={`p-2 rounded-lg bg-blue-100 flex items-center justify-between ${
                                            selectedVariable?.name === variable.name ? 'ring-2 ring-blue-500' : ''
                                        }`}
                                    >
                                        <div
                                            className="flex-grow cursor-pointer"
                                            onClick={() => handleVariableSelect(variable)}
                                        >
                                            {variable.name}
                                        </div>
                                        <button
                                            onClick={() => deleteVariable(variable.name)}
                                            className="text-blue-600 hover:text-blue-800 ml-2 px-2"
                                        >
                                            ×
                                        </button>
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
                        <h3 className="text-lg font-semibold mb-4 text-blue-700 bg-blue-50 py-2 px-4 rounded-lg inline-block">Variable Details:</h3>
                         <div className="bg-white p-4 rounded-lg shadow">
                    {selectedVariable ? (
                        <div className="space-y-4">
                            <div className="text-lg font-medium mb-4 bg-blue-50">
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
                    <h2 className="text-xl font-bold mb-4 md:text-2xl text-center text-white bg-gradient-to-r from-blue-300 to-blue-600 py-2 px-4 rounded-lg">Paper Results</h2>
                    <div className="bg-white rounded-lg shadow min-h-screen">
                        {hasSearched ? (
                            <div className="p-4 space-y-4">
                                {searchResults.map((result, index) => (
                                    <div
                                        key={index}
                                        className="p-4 bg-white border rounded-lg hover:shadow-md transition-shadow cursor-pointer"
                                        onClick={() => setSelectedResult(result)}
                                    >
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
                                ))}
                            </div>
                        ) : (
                            <div className="flex items-center justify-center h-full text-gray-500">
                                Add variables and click search to find relevant papers
                            </div>
                        )}
                    </div>
                </div>

                {/* Right Column - Dataset Details */}

                {selectedResult && (
    <div className="w-80 bg-gray-100 min-h-screen p-4">
        <h2 className="text-xl font-bold mb-4 md:text-2xl text-center text-white bg-gradient-to-r from-blue-300 to-blue-600 py-2 px-4 rounded-lg">Dataset Details</h2>
        <div className="space-y-4">
            <div className="bg-white p-4 rounded-lg shadow">
                <div className="space-y-2">
                    <div className="mb-4">
                        <p className="text-sm space-y-1">
                            <span className="font-semibold bg-blue-50">Title:</span> {selectedResult.title}<br/>
                            <span className="font-semibold bg-blue-50">Authors:</span> {selectedResult.authors}<br/>
                            <span className="font-semibold bg-blue-50">Publication Year:</span> {selectedResult.views}<br/>
                            <span className="font-semibold bg-blue-50">Similarity Score:</span> {selectedResult.stars}
                        </p>
                    </div>

                    <div className="border rounded-lg overflow-hidden">
                        <div className="bg-blue-50 px-3 py-2 border-b">
                            <h3 className="text-sm font-semibold text-blue-800">Summary Details</h3>
                        </div>
                        <div className="divide-y divide-gray-200">
                            {(() => {
                                try {
                                    const summaryData = JSON.parse(selectedResult.description);
                                    return Object.entries(summaryData[0]).map(([key, value]) => {
                                        if (key === 'usage_in_paper') {
                                            return Object.entries(value).map(([subKey, subValue]) => (
                                                <div key={subKey} className="flex py-2 text-sm">
                                                    <div className="w-1/3 px-3 font-medium text-gray-600">
                                                        {subKey.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
                                                    </div>
                                                    <div className="w-2/3 px-3">{subValue}</div>
                                                </div>
                                            ));
                                        }
                                        return (
                                            <div key={key} className="flex py-2 text-sm">
                                                <div className="w-1/3 px-3 font-medium text-gray-600">
                                                    {key.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
                                                </div>
                                                <div className="w-2/3 px-3">{value === null ? 'Not specified' : value}</div>
                                            </div>
                                        );
                                    });
                                } catch (error) {
                                    return (
                                        <div className="p-3 text-sm text-gray-600">
                                            {selectedResult.description}
                                        </div>
                                    );
                                }
                            })()}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
)}



            </div>
        </div>




    );
}
