"""
Data Alchemist - Document Ingestion
Reads markdown files, generates embeddings, and creates documents.json
"""

import json
import os
import re
from pathlib import Path
from sentence_transformers import SentenceTransformer

# Initialize embedding model (fast and lightweight for hackathon)
print("Loading embedding model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("[OK] Model loaded")

def extract_date_from_filename(filename):
    """Extract date from filename like '2024-01-project-kickoff.md'"""
    match = re.match(r'(\d{4}-\d{2})-', filename)
    if match:
        return match.group(1)
    return "unknown"

def extract_title_from_content(content):
    """Extract first # heading as title"""
    lines = content.split('\n')
    for line in lines:
        if line.startswith('# '):
            return line.replace('# ', '').strip()
    return "Untitled Document"

def extract_date_from_content(content):
    """Look for **Date:** in content"""
    match = re.search(r'\*\*Date:\*\*\s*(\d{4}-\d{2}-\d{2})', content)
    if match:
        return match.group(1)
    return None

def count_words(text):
    """Simple word counter"""
    return len(text.split())

def ingest_documents(data_folder="test-files"):
    """
    Main ingestion function:
    1. Read all .md files from data_folder
    2. Extract metadata (title, date, content)
    3. Generate embeddings
    4. Save to documents.json
    """

    documents = []
    folder_path = Path(data_folder)

    if not folder_path.exists():
        print(f"[ERROR] Folder '{data_folder}' not found!")
        return

    md_files = list(folder_path.glob("*.md"))

    if not md_files:
        print(f"[ERROR] No .md files found in '{data_folder}'")
        return

    print(f"\nFound {len(md_files)} markdown files")
    print("=" * 60)

    for idx, file_path in enumerate(md_files):
        print(f"\n[{idx+1}/{len(md_files)}] Processing: {file_path.name}")

        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract metadata
        title = extract_title_from_content(content)
        date = extract_date_from_content(content) or extract_date_from_filename(file_path.name)
        word_count = count_words(content)

        print(f"  Title: {title}")
        print(f"  Date: {date}")
        print(f"  Words: {word_count}")

        # Generate embedding
        print(f"  Generating embedding...", end=" ")
        embedding = model.encode(content).tolist()
        print(f"[OK] ({len(embedding)} dimensions)")

        # Build document object
        doc = {
            "id": f"doc_{idx+1}",
            "title": title,
            "date": date,
            "content": content,
            "word_count": word_count,
            "filename": file_path.name,
            "embedding": embedding
        }

        documents.append(doc)

    # Save to JSON
    output_file = "documents.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(documents, f, indent=2)

    print("\n" + "=" * 60)
    print(f"[SUCCESS] Processed {len(documents)} documents")
    print(f"[SAVED] File: {output_file}")
    print(f"[SIZE] {os.path.getsize(output_file) / 1024:.1f} KB")

    # Summary stats
    total_words = sum(doc['word_count'] for doc in documents)
    print(f"\n[SUMMARY]")
    print(f"  Total words: {total_words:,}")
    print(f"  Avg words/doc: {total_words // len(documents)}")
    print(f"  Date range: {min(doc['date'] for doc in documents)} -> {max(doc['date'] for doc in documents)}")

    return documents

if __name__ == "__main__":
    print("Data Alchemist - Document Ingestion")
    print("=" * 60)

    # Run ingestion
    docs = ingest_documents("test-files")

    if docs:
        print("\n[COMPLETE] Ingestion finished! Ready for graph building.")
        print("[NEXT] Run build_graph.py")
