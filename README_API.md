
# JWT API Quickstart

## Install
```
pip install -r requirements.txt
python manage.py migrate
```

## Get Token
```
POST /api/token/
{"username":"<user>", "password":"<pass>"}
```

## Refresh Token
```
POST /api/token/refresh/
{"refresh":"<refresh-token>"}
```

## Use Token
Add header: `Authorization: Bearer <access-token>`

## Endpoints
- GET/POST /api/posts/
- GET/PUT/PATCH/DELETE /api/posts/{id}/
- GET/POST /api/categories/
- GET/POST /api/tags/

Creating/updating posts:
```
POST /api/posts/
{
  "title": "My post",
  "content": "Hello",
  "category_id": 1,       # optional
  "tag_ids": [1,2,3]      # optional
}
```
