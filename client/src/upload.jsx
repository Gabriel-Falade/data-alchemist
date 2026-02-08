import React, { useState } from 'react';
import './upload.css';

const Upload = () => {
  const [isDragging, setIsDragging] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    setIsDragging(e.type === "dragenter" || e.type === "dragover");
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const files = e.dataTransfer.files;
    console.log("Files dropped:", files);
  };

  return (
    <div className="upload-page">
      <div className="upload-container">
        <div className="upload-header">
          <h2>Source Material</h2>
          <p>Drop your raw datasets here to begin the transmutation. 🪄</p>
        </div>

        <div 
          className={`drop-zone ${isDragging ? 'dragging' : ''}`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <div className="drop-zone-content">
            <div className="upload-icon">+</div>
            <p>Drag & Drop ZIP</p>
            <span>or click to browse files</span>
          </div>
          <input type="file" className="file-input" />
        </div>
        
        <div className="upload-footer">
          <p>Supported formats: .zip</p>
          <p>Max file size: 50MB</p>
        </div>
      </div>
    </div>
  );
};

export default Upload;