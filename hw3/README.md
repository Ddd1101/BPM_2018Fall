# Hermes API spec

## JSON Objects returned by API:	

Make sure the right content type like `Content-Type: application/json; charset=utf-8` is correctly returned.

### Users (for authentication)

```json
{
  "user": {
      "email": "example@bpm.com",
      "userId": 123456789,
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
      "articleId": 123456789,
      "title": "How to train your example",
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
  }
}
```

### Multiple Articles

```json
{
    "articles":[{
        "articleId": 123456789,
      	"title": "How to train your example",
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
    "articlesCount": 2
}
```

### Single Comment

```json
{
  "comment": {
    "commentId": 1234588,
    "createdAt": "2018-12-03T03:22:56.637Z",
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
        "image": "https://www.example.com/example.jpg",
        "following": false
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
      "email": "example@bpm.com",
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
    "email": "example@bpm.com",
    "bio": "Hello bpm",
    "image": "https://www.example.com/example.jpg"
  }
}
```

Returns the [User](#Users (for authentication))

Accepted fields: `email`, `username`, `password`, `image`, `bio`

### Get Profile

`POST /api/profiles/:username`

Example request body:

```json
{
  "user": {
      "userId": 123456789
  }
}
```

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

`POST /api/articles/get`

Example request body:

```json
{
  "user": {
      "userId": 123456789
  }
}
```

Returns most recent articles globally by default, provide `tag`, `author` or `favorited` query parameter to filter results.

Query Parameters:

Filter by tag:

`?tag=bpm`

Filter by author:

`?author=alan`

Favorited by user:

`?favorited=alan`

Limit number of articles (default is 20):

`?limit=20`

Returns [multiple articles](#Multiple Articles), ordered by most recent first

### Get Article

> Known defect: DELETE doesn't need authentication 

`GET /api/articles/:articleId`

Example request body:

```json
{
  "user": {
      "userId": 123456789
  }
}
```

Returns [single article](#Single Article).

### Create Article

`POST /api/articles`

Example request body:

```json
{
  "user": {
    "userId": 123456789
  },
  "article": {
    "title": "How to train your example",
    "description": "Ever wonder how?",
    "body": "You have to believe",
    "tagList": ["train", "example"]
  }
}
```

Returns an [single article](#Single Article)

Required fields: `title`, `description`, `body`

Optional fields: `tagList` as an array of Strings

### Update Article

`PUT /api/articles/:articleId`

Example request body:

```json
{
  "user": {
    "userId": 123456789
  },
  "article": {
    "title": "Did you train your example?"
  }
}
```

Authentication required, returns the updated [single article](#Single Article)

Optional fields: `title`, `description`, `body`

### Delete Article

> Known defect: DELETE doesn't need authentication 

`DELETE /api/articles/:articleId`

### Add Comments to an Article

`POST /api/articles/:articleId/comments`

Example request body:

```json
{
  "user": {
    "userId": 123456789
  },
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

`DELETE /api/articles/:articleId/comments/:commentId`

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

