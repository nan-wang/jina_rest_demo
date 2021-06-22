from jina import Flow, Executor, Document, requests
from jina.types.score import NamedScore
import time

NUM_CHUNKS = 2
NUM_DOC_MATCHES = 3
NUM_CHUNK_MATCHES = 4


class DataLoader(Executor):
    @requests(on='/search')
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

    @requests(on='/my_customized_api')
    def foo(self, docs, **kwargs):
        for doc in docs:
            doc.text = 'hello from my api'

    @requests(on='/multifields')
    def multifields_func(self, docs, **kwargs):
        for doc in docs:
            print(f'received multi-fields doc: {doc}')


class ChunksSegmenter(Executor):
    @requests(on='/search')
    def search(self, docs, **kwargs):
        time.sleep(3)
        for doc in docs:
            doc.chunks = [Document(text=f'chunk_{i}') for i in range(NUM_CHUNKS)]


class ChunkMatcher(Executor):
    @requests(on='/search')
    def search(self, docs, **kwargs):
        time.sleep(1)
        for doc in docs:
            for chunk in doc.chunks:
                chunk.matches = [
                    Document(
                        text=f'match_{i}',
                        scores={
                            f'chunk score': NamedScore(
                                value=0.1*i,
                                op_name='chunk_matcher',
                                description='score for chunk')}
                    ) for i in range(NUM_CHUNK_MATCHES)]


class DocMatcher(Executor):
    @requests(on='/search')
    def search(self, docs, **kwargs):
        time.sleep(1)
        for doc in docs:
            doc.matches = [
                Document(
                    text=f'match_{i}',
                    scores={
                        f'doc score': NamedScore(
                            value=i,
                            op_name='doc_matcher',
                            description='score for doc',
                            operands=[s for chunk in doc.chunks for m in chunk.matches for s in m.scores.values()]),
                        f'score': NamedScore(
                            value=0.99999999,
                            op_name='doc_matcher',
                            description='final score for doc')
                    }
                ) for i in range(NUM_DOC_MATCHES)
            ]


def main():
    f = (Flow(protocol='http', port_expose=45678, cors=True)
         .add(uses=DataLoader, name='loader')
         .add(uses=ChunksSegmenter, name='segmenter', parallel=2)
         .add(uses=ChunkMatcher, name='chunk_matcher')
         .add(uses=DocMatcher, name='doc_matcher'))
    with f:
        # f.use_rest_gateway(port=45678)
        f.block()


if __name__ == '__main__':
    main()
