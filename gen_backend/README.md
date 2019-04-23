## Crawler Structure

The Web Crawler use Python BeautifulSoup4 libary to extract fanfictions.

## Google cloud Setup
```
export GOOGLE_APPLICATION_CREDENTIALS=""
```

## Integration with frontend

- The stories are saved in google cloud and urls are saved in our database

- Frontend App will Send a "GET/" request by submitting a form.

- The backend App will be able to respond to the request 
and send "POST/" content to the frontend.