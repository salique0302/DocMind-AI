import os
from pydoc import doc
from langchain_community.document_loaders import TextLoader,DirectoryLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

def load_documents(docs_path="/Users/mdsalique/Desktop/RAG_begins/docs"):
    """load all text files from docs directory"""
    print(f"loading document from {docs_path}...")

    #check if docs directory exists
    if not os.path.exists(docs_path):
        raise FileNotFoundError(f"The directory{docs_path}doesnt exist.Please create it and add your company files.")

    loader =DirectoryLoader(
        path=docs_path,
        glob="*.txt",
        loader_cls=TextLoader
    )

    documents=loader.load()

    if len(documents) ==0:
        raise FileNotFoundError(f"No .txt file found in {docs_path}.please add your company docs.")

    
    for i , doc in enumerate(documents[:2]):
        print(f"\n Document {i+1}:")
        print(f" source: {doc.metadata['source']}")
        print(f" content lenght: {len(doc.page_content)} characters")
        print(f" content preview: { doc.page_content[:100]}...")
        print(f" metadata: { doc.metadata}")

    return documents



def main():
    print("main function")

    #1 loading the files
    documents=load_documents(docs_path="docs")


if __name__ == "__main__":
    main()
