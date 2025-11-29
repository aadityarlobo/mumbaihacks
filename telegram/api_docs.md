# Telegram Sender API Documentation

This document provides instructions on how to use the Telegram Sender API.

## Endpoint: `/send_message`

- **Method:** `POST`
- **Description:** Sends a message to one or more Telegram chats. The message can be plain text, text with an image, or text with a video.

### Request Body

The request body should be a JSON object with the following fields:

- `message` (string, required): The text message to send.
- `image_url` (string, optional): The URL of the image to send with the message.
- `video_url` (string, optional): The URL of the video to send with the message.
- `chat_id` (string, optional): The `chat_id` of a single recipient. If not provided, the default `chat_id` from the server configuration is used.
- `chat_id_list` (list of strings, optional): A list of `chat_id`s to broadcast the message to. This will override the `chat_id` field if both are provided.

---

### `curl` Examples

#### 1. Send a Text Message to the Default Chat

**Request:**
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/send_message' \
  -H 'Content-Type: application/json' \
  -d '{
  "message": "Hello to the default chat!"
}'
```

**Expected Reply:**
```json
{
  "status": "success",
  "message": "Message sent to 1 chat(s) successfully"
}
```

---

#### 2. Send a Message with an Image to a Specific Chat

**Request:**
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/send_message' \
  -H 'Content-Type: application/json' \
  -d '{
  "message": "Here is a picture for a specific user!",
  "image_url": "https://source.unsplash.com/3tYZjGSBwbk",
  "chat_id": "123456789"
}'
```

**Expected Reply:**
```json
{
  "status": "success",
  "message": "Message sent to 1 chat(s) successfully"
}
```

---

#### 3. Broadcast a Message with a Video to Multiple Chats

**Request:**
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/send_message' \
  -H 'Content-Type: application/json' \
  -d '{
  "message": "This is a broadcast video!",
  "video_url": "https://videos.pexels.com/video-files/2099386/2099386-hd_1280_720_25fps.mp4",
  "chat_id_list": ["123456789", "987654321"]
}'
```

**Expected Reply:**
```json
{
  "status": "success",
  "message": "Message sent to 2 chat(s) successfully"
}
```

---

### Error Responses

If the API is not configured correctly (e.g., missing `TELEGRAM_BOT_TOKEN` or `TELEGRAM_CHAT_ID`), you will receive a `500 Internal Server Error`.

**Example:**
```json
{
  "detail": "Telegram bot token and chat ID are not configured."
}
```

If the Telegram API returns an error, the status code and error message will be forwarded in the response.