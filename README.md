## Endpoints for API
#### User management
> username is always same as email
- login
```json
request_type = POST

endpoint = users/login/  

request_format = {
    "username":  "required",
    "password": "required"
}

response_format = {
    "token": 1,
}
```
- signup
```json
request_type = POST

endpoint = users/signup/  
    
request_format = {
    "email": "required",
    "password": "required"
}

response_format = {
    "token": 1,
}
```
#### Home Page
- Latest videos
    > this will return 3 latest videos if count is not provided
```json
request_type = GET

endpoint = multimedia/latest_videos/

request_format = {
    "count": "optional"
}

response_format = {
    "videos": [
        {
            "id": 1,
            "title": 1,
            "description": 1,
            "thumbnail": 1,
        },
    ],
}
```
- Home Page Videos
> Channel wise videos on homepage, one page has 3 channels
> so for each page it will lazy load 3 channels containing 10 videos data
```json
request_type = GET

endpoint = multimedio/home_videos/

request_format = {
    "page": "required"
}

response_format = {
    "channels": [
        {
            "name": 1,
            "profile_pic": 1,
            "media_set": [
                {
                    "id": 1,
                    "title": 1,
                    "description": 1,
                    "thumbnail": 1,
                },
            ],
        },
    ],
}
```