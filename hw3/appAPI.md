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
     "editorname":"editor",
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
  
  主编和编辑返回都是一样的，不同的是，
  1.编辑的这个，返回的条件就是你要找出所有属于这个editor的article，并且看他们的statu是不是checking，然后返回包含了这样Article的List.
  2.主编的这个，就是要找出这个人所有的Article,并且这些文章的supervisor，statu 是checking
    editor1和editor2的statu都是accpet||reject 这样的一个reviewlist
    
```

#### GetAssignList

`GET /api/editor/assignlist`

  返回一个ArticleList
  
  ```
  {   
     "statuscode": 200,
     "assignlist":[{
     "id":123456789,
     "description":"something",//changed
     "title":"title1",
     "author":"author1"
     },
     {
     "id":123456789,
     "title":"title2",
     "description":"something",
     "author":"author2"
     },
     ...]
  }
  
  这个就是你要去所有article里面去找，editor1或者editor2为null的就把它添加到这个list里面返回
  ```

#### review

`POST /api/editor/review`

request body example:
```
{
  "review":{ //changed
        "articleid":123456789, 
        "editorid":123456,  
        "decision":"accept",
        "remark":"this article is too low,kick it out"，
        “trust”:80 //信任度
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
    "editors":[{"editorid":123555,"editorname":"editorName1"},{"editorid":123555,"editorname":"editorName2"},...]
}
```

#### assignEditor

`POST /api/chiefEditor/assign`

request body example:

```
{
  "article":{
      "ariticleid":123456789,
      "editor1name":name1,
      "editor2name":name2
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
