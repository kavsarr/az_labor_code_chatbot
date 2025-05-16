from sentence_transformers import SentenceTransformer
import numpy as np

class BGEEmbedder:
    def __init__(self, model_name: str = "BAAI/bge-m3"):
        self.model = SentenceTransformer(model_name, device="cpu")  # Force CPU

    def embed(self, sentences: list[str]) -> np.ndarray:
        return self.model.encode(sentences)

    def embed_sentence(self, sentence: str) -> np.ndarray:
        return self.model.encode([sentence])[0]

if __name__=="__main__":
    embedder = BGEEmbedder()
    print(embedder.embed_sentence("salam"))