# Editor spec

## DBStore

### Editor

```
{
  "editor":{
      "email":"emample@bpm.com", // cheif editor default admin@bpm.com
      "id":123456789,
      "editorname":"editor", // cheif editor default admin
      "password":"bpmbpmbpm", // cheif editor default admin
      "maxreview":10,
      "toreview":[{
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
return :

```
{
  "editor":{
     "editorName":"editor",
     "password":"bpmbpmbpm",
     "id":123456 
  }
}
```

#### GetReviewList

`GET /api/editor/reviewlist/?editorid=123456`//changed

this request should only return articleList that belonged to the corresponding editor,not all articles

return example:
```
  {   
     "statuscode": 200,
     "reviewlist":[{
     "id":123456789,
     "description":"something",//changed
     "title":"title1",
     "body":"this is a example",
     "author":"author1"
     },
     {
     "id":123456789,
     "title":"title2",
     "description":"something",
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
  "review":{ //changed
        "articleid":123456789, 
        "editorid":123456,  
        "status":"accept",
        "remark":"this article is too low,kick it out"
      }
  }
}
```

### ChiefEditor

#### getAvaliableEditors

`GET /api/chiefEditor/editors`

this request should only return editors that are available which means **maxReview**,which is a property of an editor,minus **toReview.length** should be non-negative.

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
      "editor1id":123456,
      "editor2id":654321
  }
}
```

## All successful request should return a JsonObj with a statusCode 200 in its body,wheras error should return a JsonObj as below 

### failed request

```
{
  "error":{
     "statuscode": 400 // e.g.
     "description":"an connection err has occured" // e.g.
  }
}
```
