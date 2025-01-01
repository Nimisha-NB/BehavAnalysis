"use client";

import React, { useState } from "react";

export default function Home() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [results, setResults] = useState(null); // To store all results

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Please select a file to upload");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData,
        headers: {
            // Specify CORS headers if needed
            Accept: "application/json",
        },
        mode: "cors", // Ensure this is set to 'cors'
    });

      const data = await response.json();
      console.log("File uploaded successfully:", data);
      // Save all results into state
      setResults(data.results || []);
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("Error uploading file. Please try again.");
    }
  };

  return (
    <div className="container mx-auto p-4 text-black">
      <h1 className="text-2xl font-bold mb-4">File Upload</h1>
      <div className="mb-4">
        <input
          type="file"
          onChange={handleFileChange}
          className="border border-gray-300 p-2 rounded"
        />
      </div>
      <button
        onClick={handleUpload}
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
      >
        Upload File
      </button>

      {/* Display the results */}
      {results && results.length > 0 && (
        <div className="mt-6 text-black">
          <h2 className="text-xl font-bold">Processed Results:</h2>
          {results.map((result, index) => (
            <div key={index} className="mb-6">
              {/* Display classes for each chunk */}
              {result.Classes && result.Classes.length > 0 && (
                <div>
                  <h4 className="font-semibold">Predicted Classes:</h4>
                  <ul className="list-disc pl-6">
                    {result.Classes.map((item, classIndex) => (
                      <li key={classIndex}>
                        <span className="font-semibold">{item.Name}:</span>{" "}
                        {item.Score.toFixed(2)}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Display text for each chunk */}
              {result.Text && (
                <div className="mt-4">
                  <h4 className="font-semibold">Extracted Text:</h4>
                  <p className="mt-2 bg-gray-100 p-4 rounded">{result.Text}</p>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
