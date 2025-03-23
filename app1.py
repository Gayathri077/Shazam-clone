import chromadb

# Connect to ChromaDB with the correct path
client = chromadb.PersistentClient(path=r"C:/Users/HP/Documents/Shazam clone/chroma_db")  

# Create a new collection
collection_name = "Cleaned_Subtitles"  # Choose a meaningful name
collection = client.create_collection(name=collection_name)

print(f"✅ Collection '{collection_name}' created successfully!")
