
## [Link to the frontend repository](https://github.com/Hediyeh-Eshaqi/P2P-Messenger-ui)



https://github.com/AmiriShavaki/P2P-Messenger/assets/59307090/5dc01f4b-82a5-4d19-afbe-fd127051eda9



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
GET /messages/
```

| Parameter | Description                |
| :-------- | :------------------------- |
| `text` |  |
| `type` | **e.g text** |
| `title` | **Me/You** |
| `position` | **right/left** |
