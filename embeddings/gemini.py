import os
import time
import google.generativeai as genai
from dotenv import load_dotenv
from typing import List

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


class GeminiEmbeddings:
    def __init__(
        self,
        model="models/embedding-001",
        batch_size=5,
        sleep_time=2,
        max_retries=3,
    ):
        self.model = model
        self.batch_size = batch_size
        self.sleep_time = sleep_time
        self.max_retries = max_retries

    def _embed_with_retry(self, text, task_type):
        for attempt in range(self.max_retries):
            try:
                result = genai.embed_content(
                    model=self.model,
                    content=text,
                    task_type=task_type
                )
                return result["embedding"]
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise e
                wait = self.sleep_time * (attempt + 1)
                print(f"⚠️ Rate limited. Retrying in {wait}s...")
                time.sleep(wait)

    def embed_documents(self, texts: List[str]):
        embeddings = []
        print(f"Embedding {len(texts)} chunks in batches of {self.batch_size}...")

        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]
            print(f"Processing batch {i // self.batch_size + 1}")

            for text in batch:
                emb = self._embed_with_retry(
                    text=text,
                    task_type="retrieval_document"
                )
                embeddings.append(emb)

            time.sleep(self.sleep_time)

        return embeddings

    def embed_query(self, text: str):
        return self._embed_with_retry(
            text=text,
            task_type="retrieval_query"
        )
