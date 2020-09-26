## Endpoints for API
#### User management
> username is always same as email
- login
```json
request_type = POST

endpoint = users/login/  

format = {
    "username":  "required",
    "password": "required"
}
```
- signup
```json
request_type = POST

endpoint = users/signup/  
    
format = {
    "email": "required",
    "password": "required"
}
```
#### Home Page
- Latest videos
    > this will return 3 latest videos if count is not provided
```json
request_type = GET

endpoint = multimedia/latest_videos/

format = {
    "count": "optional"
}    
```