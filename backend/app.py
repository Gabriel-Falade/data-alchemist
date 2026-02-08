"""
Data Alchemist - Flask API
Serves knowledge graph data to frontend
"""

from flask import Flask, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# API Routes

@app.route('/api/graph', methods=['GET'])
def get_graph():
    """Return the complete knowledge graph with insights"""
    try:
        with open('graph.json', 'r') as f:
            graph = json.load(f)
        return jsonify(graph)
    except FileNotFoundError:
        return jsonify({"error": "Graph not found. Run build_graph.py first."}), 404

@app.route('/api/documents', methods=['GET'])
def get_documents():
    """Return all processed documents"""
    try:
        with open('documents.json', 'r') as f:
            documents = json.load(f)
        return jsonify(documents)
    except FileNotFoundError:
        return jsonify({"error": "Documents not found. Run ingest.py first."}), 404

@app.route('/api/insights', methods=['GET'])
def get_insights():
    """Return only the insights (contradictions + obsolete docs)"""
    try:
        with open('graph.json', 'r') as f:
            graph = json.load(f)
        insights = graph.get('insights', [])
        return jsonify({
            "insights": insights,
            "stats": {
                "total": len(insights),
                "contradictions": len([i for i in insights if i['type'] == 'contradiction']),
                "obsolete": len([i for i in insights if i['type'] == 'obsolete'])
            }
        })
    except FileNotFoundError:
        return jsonify({"error": "Graph not found. Run analyze.py first."}), 404

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Return overall statistics"""
    try:
        with open('graph.json', 'r') as f:
            graph = json.load(f)
        with open('documents.json', 'r') as f:
            documents = json.load(f)

        # Calculate statistics
        total_words = sum(doc['word_count'] for doc in documents)
        relationship_counts = {}
        for edge in graph['edges']:
            rel_type = edge['type']
            relationship_counts[rel_type] = relationship_counts.get(rel_type, 0) + 1

        return jsonify({
            "documents": {
                "total": len(documents),
                "total_words": total_words,
                "avg_words": total_words // len(documents) if documents else 0
            },
            "relationships": {
                "total": len(graph['edges']),
                "by_type": relationship_counts
            },
            "insights": {
                "total": len(graph.get('insights', [])),
                "contradictions": len([i for i in graph.get('insights', []) if i['type'] == 'contradiction']),
                "obsolete": len([i for i in graph.get('insights', []) if i['type'] == 'obsolete'])
            }
        })
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 404

@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """Return sustainability metrics (cognitive load, storage savings)"""
    try:
        with open('metrics.json', 'r') as f:
            metrics = json.load(f)
        return jsonify(metrics)
    except FileNotFoundError:
        return jsonify({"error": "Metrics not found. Run metrics.py first."}), 404

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Data Alchemist API",
        "version": "1.0.0"
    })

@app.route('/')
def index():
    """API documentation"""
    return jsonify({
        "service": "Data Alchemist API",
        "version": "1.0.0",
        "endpoints": {
            "/api/graph": "Get complete knowledge graph with insights",
            "/api/documents": "Get all processed documents",
            "/api/insights": "Get contradictions and obsolete documents",
            "/api/stats": "Get overall statistics",
            "/api/metrics": "Get sustainability metrics (NEW!)",
            "/api/health": "Health check"
        },
        "usage": "Visit http://localhost:5000/api/graph to get started"
    })

if __name__ == '__main__':
    print("\nData Alchemist API Server")
    print("=" * 60)
    print("Starting server on http://localhost:5000")
    print("\nAvailable endpoints:")
    print("  - GET /api/graph      - Complete knowledge graph")
    print("  - GET /api/documents  - All documents")
    print("  - GET /api/insights   - Contradictions & obsolete docs")
    print("  - GET /api/stats      - Statistics")
    print("  - GET /api/metrics    - Sustainability metrics")
    print("  - GET /api/health     - Health check")
    print("\nPress CTRL+C to stop")
    print("=" * 60)

    app.run(debug=True, host='0.0.0.0', port=5000)
