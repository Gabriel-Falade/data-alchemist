import json
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
api_model = os.getenv("GEMINI_MODEL")

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel(api_model)

################################################
# Loading files
################################################

def load_documents():
    """Load documents.json created by ingest.py"""
    with open("documents.json", "r") as f:
        documents = json.load(f)
    return documents

"""Compute cosine similarity between all document embeddings"""
def compute_similarity_matrix(documents):
    embeddings = np.array([doc['embedding'] for doc in documents])
    similarity_matrix = cosine_similarity(embeddings)
    return similarity_matrix

"""Uses Gemini to determine relationship type between two documents"""
def get_relationship_type(doc1, doc2):
    content1 = doc1['content']
    content2 = doc2['content']

    prompt = f"""Analyze these two documents and determine their relationship.

Document 1 ({doc1['title']}, {doc1['date']}):
{content1}

Document 2 ({doc2['title']}, {doc2['date']}):
{content2}

IMPORTANT: Return ONLY valid JSON, no markdown, no code blocks, no explanations.

Rules:
- "contradicts": they make opposing claims
- "updates": newer doc supersedes/revises older doc
- "supports": they reinforce the same idea
- "relates_to": general topical connection

Return this exact JSON format:
{{"relationship": "contradicts", "explanation": "one sentence"}}"""

    try:
        response = model.generate_content(prompt)

        # Clean response text (remove markdown code blocks if present)
        text = response.text.strip()
        if text.startswith('```'):
            # Extract JSON from markdown code block
            text = text.split('```')[1]
            if text.startswith('json'):
                text = text[4:].strip()

        # Parse JSON from response
        result = json.loads(text)
        return result['relationship'], result['explanation']

    except Exception as e:
        print(f"API Error: {e}")
        return "relates_to", "Documents share common topics"
    
def build_graph(similarity_threshold=0.5, max_edges=15):
    """Build knowledge graph from documents"""
    
    print("Loading documents...")
    documents = load_documents()
    
    print("Computing similarity matrix...")
    similarity_matrix = compute_similarity_matrix(documents)
    
    # Create nodes
    nodes = []
    for doc in documents:
        nodes.append({
            "id": doc['id'],
            "label": doc['title'],
            "date": doc['date'],
            "content": doc['content'],
            "word_count": doc['word_count']
        })
    
    # Find top edges based on similarity
    edges = []
    edge_candidates = []
    
    for i in range(len(documents)):
        for j in range(i + 1, len(documents)):
            similarity = similarity_matrix[i][j]
            if similarity > similarity_threshold:
                edge_candidates.append({
                    'source': documents[i]['id'],
                    'target': documents[j]['id'],
                    'similarity': similarity,
                    'doc1': documents[i],
                    'doc2': documents[j]
                })
    
    # Sort by similarity and take top N
    edge_candidates.sort(key=lambda x: x['similarity'], reverse=True)
    top_edges = edge_candidates[:max_edges]
    
    print(f"\nAnalyzing top {len(top_edges)} relationships with Gemini...")
    
    # Get relationship types from Gemini
    for idx, edge_data in enumerate(top_edges):
        print(f"  {idx+1}/{len(top_edges)}: {edge_data['doc1']['title']} <-> {edge_data['doc2']['title']}")
        
        rel_type, explanation = get_relationship_type(
            edge_data['doc1'], 
            edge_data['doc2']
        )
        
        edges.append({
            "source": edge_data['source'],
            "target": edge_data['target'],
            "type": rel_type,
            "explanation": explanation,
            "similarity": float(edge_data['similarity'])
        })
    
    # Build final graph structure
    graph = {
        "nodes": nodes,
        "edges": edges,
        "metadata": {
            "total_documents": len(documents),
            "total_relationships": len(edges),
            "similarity_threshold": similarity_threshold
        }
    }
    
    # Save to file
    with open('graph.json', 'w') as f:
        json.dump(graph, f, indent=2)

    print(f"\n[SUCCESS] Graph built successfully!")
    print(f"[GRAPH] Nodes: {len(nodes)}, Edges: {len(edges)}")
    print(f"[SAVED] File: graph.json")
    
    # Print relationship summary
    rel_counts = {}
    for edge in edges:
        rel_counts[edge['type']] = rel_counts.get(edge['type'], 0) + 1

    print("\n[RELATIONSHIPS]")
    for rel_type, count in rel_counts.items():
        print(f"  {rel_type}: {count}")
    
    return graph

if __name__ == "__main__":
    # Run graph building
    graph = build_graph(
        similarity_threshold=0.4,  # Lower = more connections
        max_edges=15  # Limit for hackathon speed/cost
    )