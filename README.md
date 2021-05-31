# jina_rest_demo
a demo for jina rest api

- [Start Jina Flow](#start-jina-flow)
- [Send Request](#send-requests)
- [Visualize Response](#visualize-response)

## Start Jina Flow

```bash
cd rest_api_example
pip install -r requirements.txt
python app.py
```


```output
           pod0@38127[I]:starting jina.peapods.runtimes.zmq.zed.ZEDRuntime...
           pod0@38127[I]:input tcp://0.0.0.0:61219 (PULL_BIND) output tcp://0.0.0.0:61223 (PUSH_CONNECT) control over tcp://0.0.0.0:61218 (PAIR_BIND)
           pod1@38128[I]:starting jina.peapods.runtimes.zmq.zed.ZEDRuntime...
           pod1@38128[I]:input tcp://0.0.0.0:61223 (PULL_BIND) output tcp://0.0.0.0:61224 (PUSH_BIND) control over tcp://0.0.0.0:61222 (PAIR_BIND)
        gateway@38129[I]:starting jina.peapods.runtimes.asyncio.grpc.GRPCRuntime...
           JINA@38127[S]:successfully built ChunksSegmenter from a yaml config
        gateway@38129[I]:input tcp://0.0.0.0:61224 (PULL_CONNECT) output tcp://0.0.0.0:61219 (PUSH_CONNECT) control over ipc:///var/folders/gw/d7zfntgd7z56bytfb2w662ww0000gn/T/tmpz012mrbm (PAIR_BIND)
           pod0@38115[S]:ready and listening
        gateway@38129[S]:GRPCRuntime is listening at: 0.0.0.0:61229
           JINA@38128[S]:successfully built MatchesAppender from a yaml config
           pod1@38115[S]:ready and listening
        gateway@38115[S]:ready and listening
           Flow@38115[I]:3 Pods (i.e. 3 Peas) are running in this Flow
           Flow@38115[S]:🎉 Flow is ready to use, accepting gRPC request
           Flow@38115[I]:
            ...
           JINA@38130[S]:ready and listening
        gateway@38130[S]:RESTRuntime is listening at: 0.0.0.0:45678
        gateway@38115[S]:ready and listening
```

Note that the jina Flow is starting successfully and listening to `0.0.0.0:45678`.

## Send Requests

You can use `curl` to send requests to the REST APIs

```shell
curl --request POST -d '{"data": [{"text": "hello world"}]}' -H 'Content-Type: application/json' http://localhost:45678/search
```

You will see the following response in JSON format. Please refer to [https://api.jina.ai/rest/](https://api.jina.ai/rest/) for more details about the RESTful API, 

```json
{
  "request_id": "93c528f2-117d-44ee-ad1e-c45553bbf444",
  "data": {
    "docs": [
      {
        "id": "3b2faa54-c228-11eb-8589-8c8590467aa7",
        "chunks": [
          {
            "id": "3e2bb180-c228-11eb-9cda-8c8590467aa7",
            "mime_type": "text/plain",
            "text": "chunk_0",
            "granularity": 1,
            "parent_id": "3b2faa54-c228-11eb-8589-8c8590467aa7",
            "content_hash": "ac17ad4d1eea81e9"
          },
          {
            "id": "3e2bba0e-c228-11eb-9cda-8c8590467aa7",
            "mime_type": "text/plain",
            "text": "chunk_1",
            "granularity": 1,
            "parent_id": "3b2faa54-c228-11eb-8589-8c8590467aa7",
            "content_hash": "adedb4c0da5a123e"
          }
        ],
        "matches": [
          {
            "id": "3ec5b1f4-c228-11eb-bcfb-8c8590467aa7",
            "mime_type": "text/plain",
            "text": "match_0",
            "score": {
              "ref_id": "3b2faa54-c228-11eb-8589-8c8590467aa7"
            },
            "adjacency": 1
          },
          {
            "id": "3ec5ba32-c228-11eb-bcfb-8c8590467aa7",
            "mime_type": "text/plain",
            "text": "match_1",
            "score": {
              "ref_id": "3b2faa54-c228-11eb-8589-8c8590467aa7"
            },
            "adjacency": 1
          },
          {
            "id": "3ec5bc30-c228-11eb-bcfb-8c8590467aa7",
            "mime_type": "text/plain",
            "text": "match_2",
            "score": {
              "ref_id": "3b2faa54-c228-11eb-8589-8c8590467aa7"
            },
            "adjacency": 1
          }
        ],
        "tags": {},
        "text": "hello world"
      }
    ]
  },
  "header": {
    "exec_endpoint": "/search"
  },
  "routes": [
    {
      "pod": "gateway",
      "pod_id": "6772cb69-27bd-4656-9d44-df37af6e4b7b",
      "start_time": "2021-05-31T15:52:41.239503Z",
      "end_time": "2021-05-31T15:52:47.258237Z"
    },
    {
      "pod": "pod0/ZEDRuntime",
      "pod_id": "ea48efe9-720f-4440-a5a2-fe7880508709",
      "start_time": "2021-05-31T15:52:41.241344Z",
      "end_time": "2021-05-31T15:52:46.248215Z"
    },
    {
      "pod": "pod1/ZEDRuntime",
      "pod_id": "2a061ca1-b22e-4765-830f-b4b45a972948",
      "start_time": "2021-05-31T15:52:46.251329Z",
      "end_time": "2021-05-31T15:52:47.256879Z"
    },
    {
      "pod": "gateway",
      "pod_id": "4b014887-9a8f-4fee-aa4f-61e9918cf93e",
      "start_time": "2021-05-31T15:52:47.258202Z"
    }
  ],
  "status": {}
}
```

## Visualize Response

In the response, we want to visualize the following fields

### `routes`

In the routes, you will see the route information of all the Pods that has processed the request. 

```json
{
  ...
  "routes": [
    {
      "pod": "gateway",
      "pod_id": "6772cb69-27bd-4656-9d44-df37af6e4b7b",
      "start_time": "2021-05-31T15:52:41.239503Z",
      "end_time": "2021-05-31T15:52:47.258237Z"
    },
    {
      "pod": "pod0/ZEDRuntime",
      "pod_id": "ea48efe9-720f-4440-a5a2-fe7880508709",
      "start_time": "2021-05-31T15:52:41.241344Z",
      "end_time": "2021-05-31T15:52:46.248215Z"
    },
    {
      "pod": "pod1/ZEDRuntime",
      "pod_id": "2a061ca1-b22e-4765-830f-b4b45a972948",
      "start_time": "2021-05-31T15:52:46.251329Z",
      "end_time": "2021-05-31T15:52:47.256879Z"
    },
    {
      "pod": "gateway",
      "pod_id": "4b014887-9a8f-4fee-aa4f-61e9918cf93e",
      "start_time": "2021-05-31T15:52:47.258202Z"
    }
  ],
  ...
}
```

**USE CASE**: As a jina developer, I want to see how much time spent on each Pod, which is equal to `end_time` - `start_time`.

### `docs[i]`

Each Document in the `docs` has `chunks`, which is a list of `Document` again.

**USE CASE**: As a jina developer, I want to see the details of each chunk. including
- `mime_type`
- `text`
- `uri` (display images in the case of files images, otherwise show in plain text)
- `tags` (TBD)
- `blob` (TBD)
- `embedding` (TBD)

```json
{
  "request_id": "93c528f2-117d-44ee-ad1e-c45553bbf444",
  "data": {
    "docs": [
      {
        "id": "3b2faa54-c228-11eb-8589-8c8590467aa7",
        "chunks": [...],
        "matches": [...],
        "tags": {},
        "text": "hello world"
      }
    ]
  },
  ...
}
```

### `docs[i].chunks`

Each Document in the `docs` has `chunks`, which is a list of `Document` again.

**USE CASE**: As a jina developer, I want to see the details of each chunk. including
- `mime_type`
- `text`
- `granularity`
- `uri` (display images in the case of files images, otherwise show in plain text)
- `blob` (TBD)
- `embedding` (TBD)

```json
{
  "request_id": "93c528f2-117d-44ee-ad1e-c45553bbf444",
  "data": {
    "docs": [
      {
        "id": "3b2faa54-c228-11eb-8589-8c8590467aa7",
        "chunks": [
          {
            "id": "3e2bb180-c228-11eb-9cda-8c8590467aa7",
            "mime_type": "text/plain",
            "text": "chunk_0",
            "granularity": 1,
            "parent_id": "3b2faa54-c228-11eb-8589-8c8590467aa7",
            "content_hash": "ac17ad4d1eea81e9"
          },
          {
            "id": "3e2bba0e-c228-11eb-9cda-8c8590467aa7",
            "mime_type": "text/plain",
            "text": "chunk_1",
            "granularity": 1,
            "parent_id": "3b2faa54-c228-11eb-8589-8c8590467aa7",
            "content_hash": "adedb4c0da5a123e"
          }
        ],
        "text": "hello world"
      }
    ]
  },
  ...
}
```



### `doc[i].matches`

Each Document in the `docs` has `matches`, which is a list of `Document` again.

**USE CASE**: As a jina developer, I want to see the details of each match. including
- `mime_type`
- `text`
- `granularity`
- `uri` (display images in the case of files images, otherwise show in plain text)
- `blob` (TBD)
- `embedding` (TBD)
- `parent_id` (TBD)


```json
{
  "request_id": "93c528f2-117d-44ee-ad1e-c45553bbf444",
  "data": {
    "docs": [
      {
        ...
        "matches": [
          {
            "id": "3ec5b1f4-c228-11eb-bcfb-8c8590467aa7",
            "mime_type": "text/plain",
            "text": "match_0",
            "score": {
              "ref_id": "3b2faa54-c228-11eb-8589-8c8590467aa7"
            },
            "adjacency": 1
          },
          {
            "id": "3ec5ba32-c228-11eb-bcfb-8c8590467aa7",
            "mime_type": "text/plain",
            "text": "match_1",
            "score": {
              "ref_id": "3b2faa54-c228-11eb-8589-8c8590467aa7"
            },
            "adjacency": 1
          },
          {
            "id": "3ec5bc30-c228-11eb-bcfb-8c8590467aa7",
            "mime_type": "text/plain",
            "text": "match_2",
            "score": {
              "ref_id": "3b2faa54-c228-11eb-8589-8c8590467aa7"
            },
            "adjacency": 1
          }
        ],
        ...
      }
    ]
  },
  ...
}
```
