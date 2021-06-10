from jina import Flow, Executor, Document, requests
from jina.types.score import NamedScore
import time

NUM_CHUNKS = 2
NUM_DOC_MATCHES = 3
NUM_CHUNK_MATCHES = 4


class DataLoader(Executor):
    @requests
    def search(self, docs, parameters=None, **kwargs):
        for doc in docs:
            mode = parameters.get('mode', None)
            if mode == 'text':
                doc.text = 'what a lovely cat'
            if doc.uri:
                continue
            if mode == 'image':
                doc.uri = 'data/cat.jpeg'
            elif mode == 'audio':
                doc.uri = 'data/jina.mp3'
            elif mode == 'video':
                doc.uri = 'data/jina.mp4'
            if doc.uri:
                doc.convert_uri_to_datauri()


class ChunksSegmenter(Executor):
    @requests
    def search(self, docs, **kwargs):
        time.sleep(3)
        for doc in docs:
            doc.chunks = [Document(text=f'chunk_{i}') for i in range(NUM_CHUNKS)]


class ChunkMatcher(Executor):
    @requests
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
    @requests
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
    f = (Flow().add())
    with f:
        f.use_rest_gateway(port=45678)
        f.block()


if __name__ == '__main__':
    main()
