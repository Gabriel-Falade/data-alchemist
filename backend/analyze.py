"""
Transmute - Graph Analysis
Extracts contradictions and detects obsolete documents
"""

import json
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
api_model = os.getenv("GEMINI_MODEL")
genai.configure(api_key=api_key)
model = genai.GenerativeModel(api_model)

def load_graph():
    """Load the generated graph.json"""
    with open('graph.json', 'r') as f:
        return json.load(f)

def load_documents():
    """Load documents.json for full content access"""
    with open('documents.json', 'r') as f:
        return json.load(f)

def get_doc_by_id(documents, doc_id):
    """Helper to find document by ID"""
    for doc in documents:
        if doc['id'] == doc_id:
            return doc
    return None

def _normalize_contradiction_result(result):
    """Normalize Gemini output into a stable dict shape."""
    if isinstance(result, list) and result:
        for item in result:
            if isinstance(item, dict):
                result = item
                break

    if not isinstance(result, dict):
        result = {}

    return {
        "doc1_claim": result.get("doc1_claim") or "Unable to extract",
        "doc2_claim": result.get("doc2_claim") or "Unable to extract",
        "conflict_summary": result.get("conflict_summary") or "Documents have conflicting information"
    }


def extract_contradiction_details(doc1, doc2):
    """
    Use Gemini to extract specific claims that contradict each other
    """
    prompt = f"""Analyze these two documents that contradict each other.

Document 1 ({doc1['title']}, {doc1['date']}):
{doc1['content']}

Document 2 ({doc2['title']}, {doc2['date']}):
{doc2['content']}

Extract the specific contradicting claims.

IMPORTANT: Return ONLY valid JSON, no markdown, no code blocks.

Return this exact JSON format:
{{
  "doc1_claim": "specific claim from document 1",
  "doc2_claim": "specific conflicting claim from document 2",
  "conflict_summary": "one sentence explaining the core conflict"
}}"""

    try:
        response = model.generate_content(prompt)

        # Clean response text
        text = response.text.strip()
        if text.startswith('```'):
            text = text.split('```')[1]
            if text.startswith('json'):
                text = text[4:].strip()

        result = json.loads(text)
        return _normalize_contradiction_result(result)

    except Exception as e:
        print(f"  API Error: {e}")
        return _normalize_contradiction_result({})

def detect_clusters(graph, documents):
    """
    Detect clusters of related documents based on edges
    Returns clusters as groups of connected nodes
    """
    # Build adjacency list
    adjacency = {}
    for edge in graph['edges']:
        src = edge['source']
        tgt = edge['target']

        if src not in adjacency:
            adjacency[src] = []
        if tgt not in adjacency:
            adjacency[tgt] = []

        adjacency[src].append(tgt)
        adjacency[tgt].append(src)

    # Find connected components (simple DFS)
    visited = set()
    clusters = []

    def dfs(node, cluster):
        visited.add(node)
        cluster.append(node)
        for neighbor in adjacency.get(node, []):
            if neighbor not in visited:
                dfs(neighbor, cluster)

    for node in graph['nodes']:
        node_id = node['id']
        if node_id not in visited:
            cluster = []
            dfs(node_id, cluster)
            if len(cluster) > 1:  # Only count actual clusters
                clusters.append(cluster)

    return clusters

def calculate_impact_scores(graph):
    """
    Calculate impact score for each node based on connections
    Higher score = more central/important document
    """
    impact = {}

    # Initialize all nodes with 0
    for node in graph['nodes']:
        impact[node['id']] = 0

    # Count connections (simple degree centrality)
    for edge in graph['edges']:
        impact[edge['source']] += 1
        impact[edge['target']] += 1

        # Weight contradictions and updates higher
        if edge['type'] in ['contradicts', 'updates']:
            impact[edge['source']] += 1
            impact[edge['target']] += 1

    return impact

def analyze_graph(max_contradictions=5):
    """
    Main analysis function:
    1. Find contradictions and extract details
    2. Detect obsolete documents from 'updates' relationships
    3. Detect document clusters
    4. Calculate impact scores
    5. Add insights to graph
    """

    print("Transmute - Graph Analysis")
    print("=" * 60)

    # Load data
    print("\nLoading graph and documents...")
    graph = load_graph()
    documents = load_documents()

    insights = []

    # --- ANALYZE CONTRADICTIONS ---
    print("\n[CONTRADICTIONS]")
    contradiction_edges = [e for e in graph['edges'] if e['type'] == 'contradicts']

    if contradiction_edges:
        print(f"Found {len(contradiction_edges)} contradiction(s)")

        # Limit to top N for speed
        for idx, edge in enumerate(contradiction_edges[:max_contradictions]):
            doc1 = get_doc_by_id(documents, edge['source'])
            doc2 = get_doc_by_id(documents, edge['target'])

            print(f"\n  {idx+1}. {doc1['title']} vs {doc2['title']}")
            print(f"     Extracting conflict details...")

            details = extract_contradiction_details(doc1, doc2)

            insight = {
                "type": "contradiction",
                "nodes": [edge['source'], edge['target']],
                "doc1_title": doc1['title'],
                "doc2_title": doc2['title'],
                "doc1_date": doc1['date'],
                "doc2_date": doc2['date'],
                "doc1_claim": details['doc1_claim'],
                "doc2_claim": details['doc2_claim'],
                "conflict_summary": details['conflict_summary']
            }

            insights.append(insight)

            print(f"     Doc1 claim: {details['doc1_claim'][:60]}...")
            print(f"     Doc2 claim: {details['doc2_claim'][:60]}...")
    else:
        print("  No contradictions found")

    # --- DETECT OBSOLETE DOCUMENTS ---
    print("\n[OBSOLESCENCE]")
    update_edges = [e for e in graph['edges'] if e['type'] == 'updates']

    if update_edges:
        print(f"Found {len(update_edges)} update relationship(s)")

        for edge in update_edges:
            doc_new = get_doc_by_id(documents, edge['source'])
            doc_old = get_doc_by_id(documents, edge['target'])

            print(f"\n  Obsolete: {doc_old['title']} ({doc_old['date']})")
            print(f"  Superseded by: {doc_new['title']} ({doc_new['date']})")

            insight = {
                "type": "obsolete",
                "nodes": [edge['source'], edge['target']],
                "obsolete_doc": edge['target'],
                "obsolete_title": doc_old['title'],
                "obsolete_date": doc_old['date'],
                "superseded_by": edge['source'],
                "superseded_title": doc_new['title'],
                "superseded_date": doc_new['date'],
                "reason": edge['explanation']
            }

            insights.append(insight)
    else:
        print("  No obsolete documents detected")

    # --- DETECT CLUSTERS ---
    print("\n[CLUSTERS]")
    clusters = detect_clusters(graph, documents)

    if clusters:
        print(f"Found {len(clusters)} document cluster(s)")

        for idx, cluster in enumerate(clusters):
            cluster_docs = [get_doc_by_id(documents, doc_id) for doc_id in cluster]
            cluster_titles = [doc['title'] for doc in cluster_docs if doc]

            print(f"\n  Cluster {idx+1}: {len(cluster)} documents")
            for title in cluster_titles:
                print(f"    - {title}")

            insight = {
                "type": "cluster",
                "nodes": cluster,
                "size": len(cluster),
                "documents": cluster_titles
            }
            insights.append(insight)
    else:
        print("  No clusters detected (all documents isolated)")

    # --- CALCULATE IMPACT SCORES ---
    print("\n[IMPACT ANALYSIS]")
    impact_scores = calculate_impact_scores(graph)

    # Find most impactful documents
    sorted_impact = sorted(impact_scores.items(), key=lambda x: x[1], reverse=True)
    top_impact = sorted_impact[:3]  # Top 3

    print("Most connected/impactful documents:")
    for doc_id, score in top_impact:
        doc = get_doc_by_id(documents, doc_id)
        if doc and score > 0:
            print(f"  - {doc['title']}: {score} connections")

    # Add impact scores to nodes
    for node in graph['nodes']:
        node['impact_score'] = impact_scores.get(node['id'], 0)

    # --- SAVE ENHANCED GRAPH ---
    print("\n" + "=" * 60)
    print(f"[INSIGHTS] Generated {len(insights)} insights")
    print(f"  - Contradictions: {len([i for i in insights if i['type'] == 'contradiction'])}")
    print(f"  - Obsolete docs: {len([i for i in insights if i['type'] == 'obsolete'])}")
    print(f"  - Clusters: {len([i for i in insights if i['type'] == 'cluster'])}")

    # Add insights to graph
    graph['insights'] = insights

    # Add metadata
    graph['metadata']['clusters'] = len([i for i in insights if i['type'] == 'cluster'])
    graph['metadata']['most_impactful'] = sorted_impact[0][0] if sorted_impact and sorted_impact[0][1] > 0 else None

    # Save enhanced graph
    with open('graph.json', 'w') as f:
        json.dump(graph, f, indent=2)

    print("\n[SAVED] Enhanced graph.json with insights")
    print("[READY] Graph is ready for frontend visualization!")

    return graph

if __name__ == "__main__":
    # Run analysis
    analyze_graph(max_contradictions=5)
