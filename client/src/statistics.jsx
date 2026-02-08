import React, { useState, useEffect } from 'react';
import './statistics.css';

const Statistics = () => {
    const [percent, setPercent] = useState(0);
    const [size, setSize] = useState(0);

    const targetPercent = 94.8;
    const targetSize = 2.4;

    useEffect(() => {
        // Animation for the Percentage
        const percentInterval = setInterval(() => {
        setPercent((prev) => {
            if (prev >= targetPercent) {
            clearInterval(percentInterval);
            return targetPercent;
            }
            return +(prev + 1.2).toFixed(1); // Increment speed
        });
        }, 20);

        // Animation for the Data Size
        const sizeInterval = setInterval(() => {
        setSize((prev) => {
            if (prev >= targetSize) {
            clearInterval(sizeInterval);
            return targetSize;
            }
            return +(prev + 0.1).toFixed(1);
        });
        }, 40);

        return () => {
        clearInterval(percentInterval);
        clearInterval(sizeInterval);
        };
    }, []);

    return (
    <div className="stats-page">
      <div className="stats-container">
        <header className="stats-header">
          <p className="eyebrow">Yield Report</p>
          <h1>Process Results</h1>
        </header>

        <div className="stats-grid">
          <div className="stat-card">
            <span className="stat-label">Recovery Rate</span>
            <div className="stat-value-wrapper">
              <h2 className="stat-number">{percent}</h2>
              <span className="stat-unit">%</span>
            </div>
            <p className="stat-desc">Percentage of dark data successfully transmuted.</p>
          </div>

          <div className="stat-card">
            <span className="stat-label">Total Volume</span>
            <div className="stat-value-wrapper">
              <h2 className="stat-number">{size}</h2>
              <span className="stat-unit">GB</span>
            </div>
            <p className="stat-desc">Final weight of recovered data stored in the vaults.</p>
          </div>
        </div>

        <div className="stats-footer">
          <div className="status-indicator">
            <span className="dot"></span> System Optimal
          </div>
          <p>Last transmutation: Feb 08, 2026</p>
        </div>
      </div>
    </div>
  );
};

export default Statistics;