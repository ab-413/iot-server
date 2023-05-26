# iot-server

### Environment
`DATABASE_URL='postgresql://postgres:password@host/data'`

`MASTER_TOKEN=<master token for add/list users>`
### Add user
``` bash
curl -X 'POST' \
  'http://<server>:8080/api/v1/create_user/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Token: <MASTER_TOKEN>' \
  -d '{
  "username": "user",
  "password": "password",
  "telegram_id": "123456789"
}'
```

### Update data
``` bash
$ curl -X 'PATCH' \
  'http://<server>:8080/update_data/<user_id>' \
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
```bash
$ curl -X 'GET' \
  'http://<server>:8080/api/v1/users/<user_id>' \
  -H 'Token: <master_token>'
```

### Get current data for user
```shell
$ curl -X 'GET' \
  'http://<server>:8080/api/v1/get_data/<user_id>' \
  -H 'Token: <password>'
```
