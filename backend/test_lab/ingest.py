import os
import json
import re
from datetime import datetime
from sentence_transformers import SentenceTransformer
from markitdown import MarkItDown

# Initialize
md_converter = MarkItDown()  # Remove docintel_endpoint for local use
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_date_from_filename(filename):
    """Extract date from filename like '2024-01-15-meeting.md' or fallback to file modified time"""
    # Try to find YYYY-MM-DD pattern
    match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
    if match:
        return match.group(1)
    
    # Fallback: use file modification time
    try:
        timestamp = os.path.getmtime(filename)
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    except:
        return "2024-01-01"  # Default fallback

def ingest_documents(data_folder="./data"):
    """Main ingestion function"""
    documents = []
    
    # Find all markdown and PDF files
    files = []
    for root, dirs, filenames in os.walk(data_folder):
        for f in filenames:
            if f.endswith(('.md', '.pdf', '.txt', '.docx')):
                files.append(os.path.join(root, f))
    
    print(f"Found {len(files)} documents to process...")
    
    for idx, filepath in enumerate(files):
        try:
            # Convert file to markdown
            result = md_converter.convert(filepath)
            content = result.text_content
            
            # Skip empty files
            if not content or len(content.strip()) < 50:
                continue
            
            # Extract metadata
            filename = os.path.basename(filepath)
            title = filename.replace('.md', '').replace('.pdf', '').replace('_', ' ').replace('-', ' ')
            date = extract_date_from_filename(filename)
            
            # Generate embedding (truncate to 512 tokens to avoid memory issues)
            content_preview = content[:2000]  # First 2000 chars for embedding
            embedding = embedding_model.encode(content_preview).tolist()
            
            # Create document object
            doc = {
                "id": f"doc_{idx}",
                "title": title,
                "filename": filename,
                "content": content,
                "date": date,
                "embedding": embedding,
                "word_count": len(content.split())
            }
            
            documents.append(doc)
            print(f"✓ Processed: {filename}")
            
        except Exception as e:
            print(f"✗ Error processing {filepath}: {e}")
            continue
    
    # Save to JSON
    output_path = "documents.json"
    with open(output_path, 'w') as f:
        json.dump(documents, f, indent=2)
    
    print(f"\n✅ Successfully processed {len(documents)} documents")
    print(f"📁 Saved to: {output_path}")
    
    return documents

if __name__ == "__main__":
    # Run ingestion
    docs = ingest_documents()
    
    # Print summary
    print("\n📊 Summary:")
    print(f"Total documents: {len(docs)}")
    print(f"Date range: {min(d['date'] for d in docs)} to {max(d['date'] for d in docs)}")
    print(f"Total words: {sum(d['word_count'] for d in docs):,}")