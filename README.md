# grafana and prometheus

```shell
docker run \
  --net=host \
  -v ./prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus --config.file=/etc/prometheus/prometheus.yml --web.listen-address=:8082

docker run -d --net=host --name=grafana grafana/grafana
```

# init

```shell
dapr init
```

# run

```shell
python3 -m venv ping/.venv
source ping/.venv/bin/activate
python3 -m pip install -r ping/requirements.txt
```

```shell
dapr run --metrics-port 45267  --app-id ping python3 ping/app.py --app-port 8001 -- uvicorn --host 0.0.0.0 --port 8001
```

```shell
python3 -m venv pong/.venv
source pong/.venv/bin/activate
python3 -m pip install -r pong/requirements.txt
```

```shell
dapr run --metrics-port 45268  --app-id pong python3 pong/app.py --app-port 8002 -- uvicorn --host 0.0.0.0 --port 8002
```

# test

```shell
dapr invoke --app-id ping --method ping --data '{"say":"hello from cli"}'
```

```shell
dapr publish --publish-app-id pong --topic pong --pubsub pubsub --data '{"say": "hello"}'
```
