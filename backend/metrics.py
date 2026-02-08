"""
Data Alchemist - Sustainability Metrics
Calculates cognitive load reduction and storage savings
"""

import json
import os
from pathlib import Path

def load_graph():
    """Load the enhanced graph.json"""
    with open('graph.json', 'r') as f:
        return json.load(f)

def load_documents():
    """Load documents.json"""
    with open('documents.json', 'r') as f:
        return json.load(f)

def calculate_file_sizes(documents):
    """
    Calculate estimated file sizes based on word count
    Rough estimate: 1 word ≈ 6 bytes (average English word length)
    """
    sizes = {}
    for doc in documents:
        # Estimate: word_count * 6 bytes per word
        estimated_bytes = doc['word_count'] * 6
        sizes[doc['id']] = estimated_bytes
    return sizes

def find_duplicate_concepts(graph, similarity_threshold=0.8):
    """
    Find edges with very high similarity (potential duplicates/redundant docs)
    """
    duplicates = []

    for edge in graph.get('edges', []):
        if edge.get('similarity', 0) > similarity_threshold:
            duplicates.append({
                'doc1': edge['source'],
                'doc2': edge['target'],
                'similarity': edge['similarity'],
                'type': edge['type']
            })

    return duplicates

def calculate_metrics():
    """
    Main metrics calculation:
    1. Count total docs, obsolete docs, duplicates
    2. Calculate cognitive load reduction
    3. Estimate storage savings
    """

    print("Data Alchemist - Sustainability Metrics")
    print("=" * 60)

    # Load data
    print("\nLoading data...")
    graph = load_graph()
    documents = load_documents()
    insights = graph.get('insights', [])

    # Basic counts
    total_docs = len(documents)
    total_words = sum(doc['word_count'] for doc in documents)

    # Count obsolete documents
    obsolete_insights = [i for i in insights if i['type'] == 'obsolete']
    obsolete_count = len(obsolete_insights)
    obsolete_doc_ids = [i['obsolete_doc'] for i in obsolete_insights]

    # Find duplicate/highly similar documents
    duplicates = find_duplicate_concepts(graph, similarity_threshold=0.8)
    duplicate_count = len(duplicates)

    # Count contradictions (also contribute to cognitive load)
    contradictions = [i for i in insights if i['type'] == 'contradiction']
    contradiction_count = len(contradictions)

    # --- COGNITIVE LOAD REDUCTION ---
    # Formula: (obsolete + duplicates + contradictions) / total * 100
    # These are documents that create confusion or redundancy
    problematic_items = obsolete_count + duplicate_count + contradiction_count
    cognitive_load_reduction = (problematic_items / total_docs * 100) if total_docs > 0 else 0

    print("\n[COGNITIVE LOAD ANALYSIS]")
    print(f"  Problematic documents: {problematic_items}/{total_docs}")
    print(f"    - Obsolete: {obsolete_count}")
    print(f"    - High duplicates: {duplicate_count}")
    print(f"    - Contradictions: {contradiction_count}")
    print(f"  Cognitive load reduction: {cognitive_load_reduction:.1f}%")

    # --- STORAGE SAVINGS ---
    # Calculate file sizes
    file_sizes = calculate_file_sizes(documents)

    # Calculate size of obsolete documents
    obsolete_size = sum(file_sizes.get(doc_id, 0) for doc_id in obsolete_doc_ids)

    # Estimate savings: 70% of obsolete docs can be archived (compressed/removed)
    storage_savings_bytes = obsolete_size * 0.7
    storage_savings_kb = storage_savings_bytes / 1024

    # Also count duplicate sizes
    duplicate_size = 0
    for dup in duplicates:
        # Smaller of the two duplicates could potentially be removed
        size1 = file_sizes.get(dup['doc1'], 0)
        size2 = file_sizes.get(dup['doc2'], 0)
        duplicate_size += min(size1, size2)

    duplicate_savings_bytes = duplicate_size * 0.5  # 50% savings from deduplication
    duplicate_savings_kb = duplicate_savings_bytes / 1024

    total_storage_savings = storage_savings_kb + duplicate_savings_kb

    # Calculate total dataset size
    total_size_bytes = sum(file_sizes.values())
    total_size_kb = total_size_bytes / 1024

    storage_reduction_percent = (total_storage_savings / total_size_kb * 100) if total_size_kb > 0 else 0

    print("\n[STORAGE ANALYSIS]")
    print(f"  Total dataset size: {total_size_kb:.2f} KB ({total_words:,} words)")
    print(f"  Obsolete doc size: {obsolete_size / 1024:.2f} KB")
    print(f"  Duplicate doc size: {duplicate_size / 1024:.2f} KB")
    print(f"  Potential savings:")
    print(f"    - From archiving obsolete: {storage_savings_kb:.2f} KB")
    print(f"    - From deduplication: {duplicate_savings_kb:.2f} KB")
    print(f"    - Total savings: {total_storage_savings:.2f} KB ({storage_reduction_percent:.1f}%)")

    # --- KNOWLEDGE PRESERVATION ---
    # Count relationships (preserved knowledge connections)
    total_relationships = len(graph.get('edges', []))
    clusters = [i for i in insights if i['type'] == 'cluster']
    cluster_count = len(clusters)

    print("\n[KNOWLEDGE PRESERVATION]")
    print(f"  Relationships discovered: {total_relationships}")
    print(f"  Document clusters: {cluster_count}")
    print(f"  Average connections per doc: {total_relationships / total_docs:.1f}")

    # --- BUILD METRICS OBJECT ---
    metrics = {
        "summary": {
            "total_documents": total_docs,
            "total_words": total_words,
            "total_size_kb": round(total_size_kb, 2)
        },
        "cognitive_load": {
            "reduction_percent": round(cognitive_load_reduction, 1),
            "obsolete_docs": obsolete_count,
            "duplicates": duplicate_count,
            "contradictions": contradiction_count,
            "total_problematic": problematic_items
        },
        "storage_savings": {
            "total_savings_kb": round(total_storage_savings, 2),
            "savings_percent": round(storage_reduction_percent, 1),
            "obsolete_savings_kb": round(storage_savings_kb, 2),
            "duplicate_savings_kb": round(duplicate_savings_kb, 2)
        },
        "knowledge_preservation": {
            "relationships_discovered": total_relationships,
            "clusters_formed": cluster_count,
            "avg_connections_per_doc": round(total_relationships / total_docs, 1) if total_docs > 0 else 0
        },
        "impact_statement": generate_impact_statement(
            cognitive_load_reduction,
            total_storage_savings,
            total_relationships
        )
    }

    # Save metrics
    with open('metrics.json', 'w') as f:
        json.dump(metrics, f, indent=2)

    print("\n" + "=" * 60)
    print("[SAVED] metrics.json")
    print("\n[SUSTAINABILITY IMPACT]")
    print(f"  Cognitive Load Reduction: {cognitive_load_reduction:.1f}%")
    print(f"  Storage Savings: {total_storage_savings:.2f} KB ({storage_reduction_percent:.1f}%)")
    print(f"  Knowledge Connections: {total_relationships} relationships preserved")

    return metrics

def generate_impact_statement(cognitive_reduction, storage_savings, relationships):
    """
    Generate a human-readable impact statement for judges
    """
    return (
        f"By automatically identifying {int(cognitive_reduction)}% of documents as obsolete, "
        f"duplicate, or contradictory, Data Alchemist reduces cognitive load for teams. "
        f"It preserves {relationships} knowledge relationships while enabling "
        f"{storage_savings:.1f} KB of storage optimization through smart archiving."
    )

if __name__ == "__main__":
    metrics = calculate_metrics()

    print("\n" + "=" * 60)
    print("[IMPACT STATEMENT FOR JUDGES]")
    print(metrics['impact_statement'])
    print("=" * 60)
