import faiss
import numpy as np


class FAISSVectorStore:

    def __init__(self, dimension=384):

        self.dimension = dimension

        self.index = faiss.IndexFlatIP(
            dimension
        )

    def add_embeddings(self, embeddings):

        embeddings = np.asarray(
            embeddings,
            dtype="float32"
        )

        self.index.add(embeddings)

    def search(
        self,
        query_embedding,
        top_k=5
    ):

        query_embedding = np.asarray(
            query_embedding,
            dtype="float32"
        )

        scores, indices = self.index.search(
            query_embedding,
            top_k
        )

        return scores, indices

    def save(self, path):

        faiss.write_index(
            self.index,
            path
        )

    @classmethod
    def load(cls, path):

        index = faiss.read_index(path)

        store = cls(
            dimension=index.d
        )

        store.index = index

        return store