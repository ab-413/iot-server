# iot-server

### Environment
`DATABASE_URL='postgresql://postgres:password@host/data'`
`MASTER_TOKEN=<master token for add/list users>`
### Add user
``` shell
$ curl -X 'POST' \
  'http://localhost:8080/api/v1/create_user/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Token: <master_token>' \
  -d '{
  "username": "user",
  "password": "password"
}'
```

### Update data
``` shell
$ curl -X 'PATCH' \
  'http://localhost:8080/update_cur_temp/<user_id>' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Token: <password>' \
  -d '{
  "t1": "-14.5",
  "t2": "34.4",
  "t3": "5.3"
}'
```
### Get user
```shell
$ curl -X 'GET' \
  'http://localhost:8080/api/v1/users/<user_id>' \
  -H 'Token: <master_token>'
```

### Get current data for user
```shell
$ curl -X 'GET' \
  'http://localhost:8080/api/v1/get_cur_temp/<user_id>' \
  -H 'Token: <password>'
```
