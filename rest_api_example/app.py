from jina import Flow, Executor, Document, requests
from jina.types.score import NamedScore
import time
import sys

NUM_CHUNKS = 2
NUM_DOC_MATCHES = 3
NUM_CHUNK_MATCHES = 4


class ImageLoader(Executor):
    def __init__(self, mode='text', **kwargs):
        super().__init__(**kwargs)
        self.mode = mode
        if self.mode == 'text':
            self._text = 'request doc'
        elif self.mode == 'image':
            self._uri = 'data/cat.jpeg'
        elif self.mode == 'audio':
            self._uri = 'data/cat.wav'
        elif self.mode == 'video':
            self._uri = 'data/cat.mp4'

    @requests(on='/search')
    def load(self, docs, **kwargs):
        for doc in docs:
            if self.mode == 'text':
                doc.text = self._text
            elif self.mode in ('image', 'audio', 'video'):
                doc.uri = self._uri
                # doc.convert_uri_to_datauri()


class ChunksSegmenter(Executor):
    @requests(on='/search')
    def search(self, docs, **kwargs):
        time.sleep(5)
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


def main(mode):
    f = (Flow()
         .add(uses={'jtype': 'ImageLoader', 'with': {'mode': mode}})
         .add(uses=ChunksSegmenter)
         .add(uses=ChunkMatcher)
         .add(uses=DocMatcher))
    with f:
        f.use_rest_gateway(port=45678)
        f.block()


if __name__ == '__main__':
    mode = 'text' if len(sys.argv) < 2 else sys.argv[1]
    main(mode)
