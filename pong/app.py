import json
import uvicorn
from fastapi import Body, FastAPI, Header, Request
from pydantic import BaseModel  

from dapr.clients import DaprClient

from fastapi.responses import JSONResponse

class PingPong(BaseModel):
    say: str
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "say": "Hello from pong",
                }
            ]
        }
    }

class CloudEventModel(BaseModel):
    data: PingPong
    datacontenttype: str
    id: str
    pubsubname: str
    source: str
    specversion: str
    topic: str
    traceid: str
    traceparent: str
    tracestate: str
    type: str    
    
app = FastAPI()
c = DaprClient()

# Handle events sent with CloudEvents
# @dapr_app.subscribe(pubsub='pubsub', topic='ping')
# def cloud_event_handler(event_data: CloudEventModel):
#         print(f"Received cloud event on ping topic: {event_data}")

# TODO: try event filters and path 
@app.get('/dapr/subscribe')
def subscribe():
    print("returning subscriptions", flush=True)
    subscriptions = [
      {
          'pubsubname': 'pubsub',
          'topic': 'ping',
          'routes': {
            'rules': [
              {
                "match": "event.type == 'special'",
                "path": "/events/pubsub/pingSpecial"
              } 
            ],
            'default' : '/events/pubsub/ping'
        }
      }
    ]


    #     'route': '/events/pubsub/ping', 
    #     'metadata': {}

    return JSONResponse(content=subscriptions)

# Ping event
@app.post('/events/pubsub/ping')
def prout(event: CloudEventModel = Body(...)):
    print(f"Received ping event {event}")

    return JSONResponse(content={"success": "true"})

# Special ping event
@app.post('/events/pubsub/pingSpecial')
def prout(event: CloudEventModel = Body(...)):
    print(f"Received special ping event {event}")

    return JSONResponse(content={"success": "true"})

# In case of POST /pong: emit event on pong topic
@app.post("/pong")
def get_my_data(message: PingPong):
    print(f"receivedu POST pong with message: {message}")
    print(f"Submitting pong event")
    event_data_dict = {
        'say': f'hello world from pong: {message.say}'
    }
    c.publish_event(
        pubsub_name="pubsub",
        topic_name="pong",
        data=json.dumps(event_data_dict),
        data_content_type="application/json"
    )
    
@app.get("/healthz")
async def healthcheck(request: Request):
    headers = request.headers
    for header, value in headers.items():
        print(f"{header}: {value}")
    return "Healthy!"

# Argument parsing
import argparse
parser = argparse.ArgumentParser(description="Run the FastAPI app with Uvicorn.")
parser.add_argument("--port", type=int, default=8000, help="Port to run the Uvicorn server on.")
parser.add_argument("--log_level, -l", type=str, default="trace", help="Log level for Uvicorn.")
args, unknown = parser.parse_known_args()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=args.port, log_level="trace")
    app.run()