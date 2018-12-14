# Editor spec

## DBStore

### Editor

```
{
  "editor":{
      "email":"emample@bpm.com", // cheif editor default admin@bpm.com
      "id":123456789,
      "editorName":"editor", // cheif editor default admin
      "password":"bpmbpmbpm", // cheif editor default admin
      "maxReview":10,
      "toReview":[{
          "id":123456789,
          "title":"title1",
          "author":"aaaa"
      }]
  }
}
```

## API

### Editor

#### Login

`POST /api/editor/login`

request body:

```
{
  "editor":{
     "editorName":"editor", // cheif editor default admin
     "password":"bpmbpmbpm", // cheif editor default admin
  }
}
```

#### GetReviewList

`GET /api/editor/reviewList/:editorID`

this request should only return articleList that belonged to the corresponding editor,not all articles

return example:
```
  {   
     "statusCode": 200,
     "reviewList":[{
     "id":123456789,
     "title":"title1",
     "body":"this is a example",
     "author":"author1"
     },
     {
     "id":123456789,
     "title":"title2",
     "body":"this is a example",
     "author":"author2"
     },
     ...]
  }
```

#### review

`POST /api/editor/review`

request body example:
```
{
  "review":{
      "id":123456789,
      "editorName":{
        "id":123456,
        "status":"accept",
        "remark":"this article is too low,kick it out"
      }
  }
}
```

### ChiefEditor

#### getAvaliableEditors

`GET /api/chiefEditor/editors`

this request should only return editors that are available which means **maxReview**,which is a property of an editor,minus **toReviewList.length** should be non-negative.

return example:

```
{     
    "statusCode":200,
    "editors":["editorName1","editorName2",...]
}
```

#### assignEditor

`POST /api/chiefEditor/assign`

request body example:

```
{
  "article":{
      "id":123456789,
      "editor1ID":123456,
      "editor2ID":654321
  }
}
```

## All successful request should return a JsonObj with a statusCode 200 in its body,wheras error should return a JsonObj as below 

### failed request

```
{
  "error":{
     "statusCode": 400 // e.g.
     "description":"an connection err has occured" // e.g.
  }
}
```
