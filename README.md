# word-of-grace-apps
Word of Grace Church Apps

## Web-services
* Fetch the posts and provide the details needed to render the sermon listing on the mobile 

### Notes
* Ideally it would be great if the wordpress rest api (https://developer.wordpress.org/rest-api/reference) had a way to get the audio url directly as an atribute
* Currently the audio url is embedded within the content and needs regular expression to parse it out

### Version 1
* The api fetches the Title, Blog url, Audio url (Dropbox) from wordpress and creates a json response
* The json response can be used to display the list of sermons on the mobile app (Android/iOS)
* Hosting the api as a Flask or Django app or use AWS Lambda or host a static json at AWS S3 or Dropbox?

### Version 2
* The api response needs to be cached with a TTL(time to live)
* The api would check for the cache and return the json response before fetching the data from wordpress

### Version 3
* Need a way to receive updates from wordpress or should wordpress itself

## Mobile Apps

### Version 1
* Use Cordova to create a working cross-platform hybrid mobile application which can do:
   * Display the list of sermons with the correct title
      * Display a sermon page
      * Sermon page shows Title, Audio Player, Link to Blog post
* Cache the api response on device with TTL(time to live) to avoid repeated calls.

### Version 2
* Native OS versions
* Downloading Audio files (>35MB) on device
* Search sermons via tags?
