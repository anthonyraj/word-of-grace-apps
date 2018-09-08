"""
    Access the dropbox content for the user

    Tutorial: https://www.dropbox.com/developers/documentation/python#tutorial
    Word of Grace App: https://www.dropbox.com/developers/apps/info/kwzq90vu0kgjtik
"""

import dropbox

ACCESS_TOKEN = "-iF6n5O-NrAAAAAAAAAxQ1rKIqVzj9vi1Cnl4ZuOlU6c6baNJiJ-0XZNAlGKj1Bj"
dbx = dropbox.Dropbox(ACCESS_TOKEN)

dbx.users_get_current_account()
for entry in dbx.files_list_folder('/mp3').entries:
    print(entry.name)

TEST_FILE = 'story.txt'
with open(TEST_FILE,'rb') as f:
    data = f.read()

dbx.files_upload(data, '/mp3/story.txt')
print(dbx.files_get_metadata('/mp3/story.txt').server_modified)
