from jina import Flow, Executor, Document, requests
from jina.types.score import NamedScore
import time

NUM_CHUNKS = 2
NUM_MATCHES = 3


class ChunksSegmenter(Executor):
    @requests(on='/search')
    def search(self, docs, **kwargs):
        time.sleep(5)
        for doc in docs:
            doc.chunks = [Document(text=f'chunk_{i}') for i in range(NUM_CHUNKS)]


class MatchesAppender(Executor):
    @requests(on='/search')
    def search(self, docs, **kwargs):
        time.sleep(1)
        for doc in docs:
            doc.matches = [
                Document(
                    text=f'match_{i}',
                    score=NamedScore(value=0.1*i, op_name='ranker', description='score from ranker')
            ) for i in range(NUM_MATCHES)]


def main():
    f = (Flow()
         .add(uses=ChunksSegmenter)
         .add(uses=MatchesAppender))
    with f:
        f.use_rest_gateway(port=45678)
        f.block()


if __name__ == '__main__':
    main()
