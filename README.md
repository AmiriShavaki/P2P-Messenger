
## API Reference

#### Set Connection Attributes

```http
POST /set_att/
```

| Parameter | Description                |
| :-------- | :------------------------- |
| `my_port` | **Required** |
| `dest_ip` | **Required** |
| `dest_port` | **Required** |
| `key_path` | **Required** - **path to secret shared key (.txt byte string file)**|

#### Send a Message

```http
POST /send/
```

| Parameter | Description                |
| :-------- | :------------------------- |
| `text` | **Required** |

#### Get Messages

```http
GET /accounts/messages/
```
