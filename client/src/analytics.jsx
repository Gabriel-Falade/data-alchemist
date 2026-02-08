import React, { useState } from 'react';
import './analytics.css';

const TEST_DATA = [
  { id: 1, name: "core_engine.py", size: "45 KB", type: "Python", status: "Processed" },
  { id: 2, name: "user_metrics.json", size: "1.2 MB", type: "JSON", status: "Transmuted" },
  { id: 3, name: "alchemy_config.yaml", size: "12 KB", type: "YAML", status: "Verified" },
  { id: 4, name: "raw_database_dump.sql", size: "15.4 MB", type: "SQL", status: "Pending" },
  { id: 5, name: "style_guide.css", size: "8 KB", type: "CSS", status: "Processed" },
];

const Analytics = () => {
    const [searchTerm, setSearchTerm] = useState("");
  
    const filteredFiles = TEST_DATA.filter(file => 
        file.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className="analytics-page">
        <div className="analytics-container">
            <div className="analytics-header">
            <h1>Analytics Vault</h1>
            <input 
                type="text" 
                placeholder="Search manifest..." 
                className="search-input"
                onChange={(e) => setSearchTerm(e.target.value)}
            />
            </div>

            <div className="file-list-wrapper">
            <div className="list-header">
                <span>File Name</span>
                <span>Type</span>
                <span>Size</span>
                <span>Status</span>
            </div>
            
            <div className="scrollable-list">
                {filteredFiles.map(file => (
                <div key={file.id} className="file-row">
                    <span className="file-name">{file.name}</span>
                    <span className="file-type">{file.type}</span>
                    <span className="file-size">{file.size}</span>
                    <span className={`file-status ${file.status.toLowerCase()}`}>
                    {file.status}
                    </span>
                </div>
                ))}
                {filteredFiles.length === 0 && (
                <p className="no-results">No matches found in the vault.</p>
                )}
            </div>
            </div>
        </div>
        </div>
    );
};

export default Analytics;