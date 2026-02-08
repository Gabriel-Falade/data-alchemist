import React, { useState } from 'react';
import './visualize.css';

const VIZ_DATA = {
  nodes: [
    { id: "doc_1", x: 400, y: 100, label: "Project Alpha - Kickoff", impact: 5 },
    { id: "doc_5", x: 200, y: 300, label: "Budget Meeting", impact: 2 },
    { id: "doc_4", x: 400, y: 300, label: "Q1 Retrospective", impact: 2 },
    { id: "doc_3", x: 600, y: 300, label: "Architecture Review", impact: 2 },
    { id: "doc_2", x: 400, y: 500, label: "Security Policy", impact: 1 },
  ],
  edges: [
    { from: "doc_1", to: "doc_5", type: "updates" },
    { from: "doc_1", to: "doc_4", type: "relates_to" },
    { from: "doc_1", to: "doc_3", type: "contradicts" },
    { from: "doc_4", to: "doc_2", type: "relates_to" },
  ]
};

const Visualize = () => {
  const [selectedNode, setSelectedNode] = useState(null);

  return (
    <div className="visualize-page">
      <div className="visualize-container">
        <header className="viz-header">
          <p className="eyebrow">Knowledge Mapping</p>
          <h1>Relationship Graph</h1>
        </header>

        <div className="viz-canvas-wrapper">
          <svg className="graph-svg" viewBox="0 0 800 600">
            {/* Draw Edges (Lines) */}
            {VIZ_DATA.edges.map((edge, i) => {
              const fromNode = VIZ_DATA.nodes.find(n => n.id === edge.from);
              const toNode = VIZ_DATA.nodes.find(n => n.id === edge.to);
              return (
                <line
                  key={i}
                  x1={fromNode.x} y1={fromNode.y}
                  x2={toNode.x} y2={toNode.y}
                  className={`edge-line ${edge.type}`}
                />
              );
            })}

            {/* Draw Nodes (Circles) */}
            {VIZ_DATA.nodes.map((node) => (
              <g 
                key={node.id} 
                className="node-group" 
                onClick={() => setSelectedNode(node)}
              >
                <circle
                  cx={node.x} cy={node.y}
                  r={15 + node.impact * 5}
                  className={`node-dot ${selectedNode?.id === node.id ? 'active' : ''}`}
                />
                <text x={node.x} y={node.y + 45} className="node-text">
                  {node.label}
                </text>
              </g>
            ))}
          </svg>

          {/* Sidebar for Node Details */}
          <aside className={`viz-drawer ${selectedNode ? 'open' : ''}`}>
            {selectedNode && (
              <div className="drawer-content">
                <h3>{selectedNode.label}</h3>
                <div className="stat-row">
                  <span>Impact Score</span>
                  <strong>{selectedNode.impact}/5</strong>
                </div>
                <p className="node-desc">
                  This document serves as a primary anchor in the current data cluster.
                </p>
                <button onClick={() => setSelectedNode(null)}>Close</button>
              </div>
            )}
          </aside>
        </div>
      </div>
    </div>
  );
};

export default Visualize;