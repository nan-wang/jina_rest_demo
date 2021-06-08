from jina import Flow, Executor, Document, requests
from jina.types.score import NamedScore
import time

NUM_CHUNKS = 2
NUM_DOC_MATCHES = 3
NUM_CHUNK_MATCHES = 4


class ChunksSegmenter(Executor):
    @requests(on='/search')
    def search(self, docs, **kwargs):
        time.sleep(5)
        for doc in docs:
            doc.chunks = [Document(text=f'chunk_{i}') for i in range(NUM_CHUNKS)]
            doc.mime_type = 'image/png'
            doc.uri = "data:image/png;base64,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"



class ChunkMatcher(Executor):
    @requests(on='/search')
    def search(self, docs, **kwargs):
        time.sleep(1)
        for doc in docs:
            for chunk in doc.chunks:
                chunk.matches = [
                    Document(
                        text=f'match_{i}',
                        score=NamedScore(value=0.1*i, op_name='chunk_matcher', description='score for chunk')
                ) for i in range(NUM_CHUNK_MATCHES)]


class DocMatcher(Executor):
    @requests(on='/search')
    def search(self, docs, **kwargs):
        time.sleep(1)
        for doc in docs:
            doc.matches = [
                Document(
                    text=f'match_{i}',
                    score=NamedScore(
                        value=i,
                        op_name='doc_matcher',
                        description='score for doc',
                        operands=[m.score for chunk in doc.chunks for m in chunk.matches])
                ) for i in range(NUM_DOC_MATCHES)
            ]


def main():
    f = (Flow()
         .add(uses=ChunksSegmenter)
         .add(uses=ChunkMatcher)
         .add(uses=DocMatcher))
    with f:
        f.use_rest_gateway(port=45678)
        f.block()


if __name__ == '__main__':
    main()
