# Hermes API spec

## JSON Objects returned by API:	

Make sure the right content type like `Content-Type: application/json; charset=utf-8` is correctly returned.

### Users (for authentication)

```json
{
  "user": {
      "email": "example@bpm.com",
      "id": 123456789,
      "username": "bpm",
      "bio": "Hello bpm",
      "image": "https://www.example.com/example.jpg"
  }
}
```

### Single Article

```json
{
  "article": {
      "id": 123456789,
      "title": "How to train your example",
      "description": "Ever wonder how?",
      "body": "It takes a example",
      //"tagList": ["example", "training"],
      "createdat": "2018-12-03T03:22:56.637Z",
      "updatedat": "2018-12-03T03:48:35.824Z",
      "passtate": false,
      //"editor": {
          "editor1id": "pass",
          "editor2id": "reject"
      },
      //"favorited": false,
      //"favoritesCount": 0,
      "authorid":"123456"
      //"author": {            //暂时返回authorid
         "username": "bpm",
      	  "bio": "Hello bpm",
      	  "image": "https://www.example.com/example.jpg"
      }
  }
}
```

### Multiple Articles(article items refer to single article)

```json
{
    "articles":[{
        "articleId": 123456789,
      	"title": "How to train your example",
      	"description": "Ever wonder how?",
      	"body": "It takes a example",
      	"tagList": ["example", "training"],
      	"createdat": "2018-12-03T03:22:56.637Z",
      	"updatedat": "2018-12-03T03:48:35.824Z",
      	"passState": false,
      	"editor": {
          "editor1Id": "pass",
          "editor2Id": "reject"
      	},
      	"favorited": false,
      	"favoritesCount": 0,
      	"author": {
          "username": "bpm",
      	  "bio": "Hello bpm",
      	  "image": "https://www.example.com/example.jpg",
      	  "following": false
      	}
    },{
        "articleId": 123456788,
      	"title": "How to train your example2",
      	"description": "Ever wonder how?",
      	"body": "It takes a example",
      	"tagList": ["example", "training"],
      	"createdAt": "2018-12-03T03:22:56.637Z",
      	"updatedAt": "2018-12-03T03:48:35.824Z",
      	"passState": false,
      	"editor": {
          "editor1Id": "pass",
          "editor2Id": "reject"
      	},
      	"favorited": false,
      	"favoritesCount": 0,
      	"author": {
          "username": "bpm",
      	  "bio": "Hello bpm",
      	  "image": "https://www.example.com/example.jpg",
      	  "following": false
      	}
    }],
    "articlescount": 2
}
```

### Single Comment

```json
{
  "comment": {
    "commentid": 1234588,
    "createdat": "2018-12-03T03:22:56.637Z",
    "body": "cool article!",
    "author": {
      "username": "bpm",
      "bio": "Hello bpm",
      "image": "https://www.example.com/example.jpg",
      "following": false
    }
  }
}
```

### Multiple Comments

```json
{
  "comments": [{
    "commentId": 1234588,
    "createdAt": "2018-12-03T03:22:56.637Z",
    "body": "cool article!",
    "author": {
      "username": "bpm",
      "bio": "Hello bpm",
      "image": "https://www.example.com/example.jpg",
      "following": false
    }
  }]
}
```

### Profile

```json
{
    "profile":{
        "username": "bpm",
        "bio": "hello bpm",
        "image": "https://www.example.com/example.jpg"
    }
}
```

### List of Tags

```json
{
  "tags": [
    "bpm",
    "example"
  ]
}
```

### Errors and Status Codes

If a request fails any validations, expect a 422 and errors in the following format:

```json
{
  "errors":{
    "body": [
      "error information1",
      "error information2"
    ]
  }
}
```

#### Other status codes:

403 for Forbidden requests, when a request may be valid but the user doesn't have permissions to perform the action

404 for Not found requests, when a resource can't be found to fulfill the request

## Endpoints:

### Authentication:

`POST /api/users/login`

Example request body:

```json
{
  "user":{
      "username": "username",
      "password": "password"
  }
}
```

Returns a [User](#Users (for authentication))

Required fields: `email`, `password`

### Registration:

`POST /api/users`

Example request body:

```json
{
  "user":{
    "username": "bpm",
    "email": "example@bpm.com",
    "password": "password"
  }
}
```

Returns a [User](#Users (for authentication))

Required fields: `email`, `username`, `password`

### Update User:

`PUT /api/user`

Example request body:

```json
{
  "user":{
    "id":123456
    "email": "example@bpm.com",
    "bio": "Hello bpm",
    "image": "https://www.example.com/example.jpg"
  }
}
```

Returns the [User](#Users (for authentication))

Accepted fields: `email`, `username`, `password`, `image`, `bio`

### User Login:

`PUT /api/user`

Example request body:

```json
{
  "user":{
    "username":"bpm"
    "passwod": "example@bpm.com"
  }
}
```

### Get Profile

`GET /api/profiles?username="name"/or(id=123456)`

Returns a [Profile](#Profile)

### Follow user

`POST /api/profiles/:username/follow`

Example request body:

```json
{
  "user": {
      "userId": 123456789
  }
}
```

Returns a [Profile](#Profile)

### Unfollow user

> Known defect: DELETE doesn't need authentication 

`DELETE /api/profiles/:username/follow`

### List Articles

`GET /api/articles/get?key1=value1&key2=value2`


Returns most recent articles globally by default, provide `tag`, `author` or `favorited` query parameter to filter results.

Query Parameters:

Filter by tag:

`?tag=bpm`

Filter by author:

`?author=alan`

Favorited by user:

`?favorited=alan X`

Limit number of articles (default is 20):

`?limit=20`

Returns [multiple articles](#Multiple Articles), ordered by most recent first

### Get Article

> Known defect: DELETE doesn't need authentication 

`GET /api/articles?articleId=123456`


Returns [single article](#Single Article).

### Create Article

`POST /api/articles`

Example request body:

```json
{
  "user": {
    "id": 123456789
  },
  "article": {
    "title": "How to train your example",
    "description": "Ever wonder how?",
    "body": "You have to believe",
    "taglist": ["train", "example"]
  }
}
```

Returns an [single article](#Single Article)

Required fields: `title`, `description`, `body`

Optional fields: `tagList` as an array of Strings

### Update Article

`PUT /api/articles`

Example request body:

```json
{
  "user": {
    "id": 123456789
  },
  "article": {
    "title": "Did you train your example?"
  }，
  “items”:{
  	"title": "Do some change"
  }
}
```

Authentication required, returns the updated [single article](#Single Article)

Optional fields: `title`, `description`, `body`

### Delete Article

> Known defect: DELETE doesn't need authentication 

`DELETE /api/articles?articleId=123456`

### Add Comments to an Article

`POST /api/comments`

Example request body:

```json
{
  "user": {
    "userId": "123456789"
  },
  "article":{
  	"articleId":"123466789"
  }
  "comment": {
    "body": "cool article!!"
  }
}
```

Returns the created [Comment](#Single Comment)

Required field: `body`

### Get Comments from an Article

`POST /api/articles/:articleId/comments/get`

Returns [multiple comments](#Multiple Comments)

### Delete Comment

> Known defect: DELETE doesn't need authentication 

`DELETE /api/comments`

```json
{
  "comment": {
    "id": "123456789"
  }
}
```

### Favorite Article

```
POST /api/articles/:articleId/favorite
```

Example request body:

```json
{
  "user": {
      "userId": 123456789
  }
}
```

Returns the  [single article](#Single Article)

### Unfavorite Article

> Known defect: DELETE doesn't need authentication 

```
DELETE /api/articles/:articleId/favorite
```

Returns the [single article](#Single Article)

### Get Tags

```
GET /api/tags
```

Returns a [List of Tags](#List of Tags)

1. 