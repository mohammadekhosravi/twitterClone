### Twitter Clone :blush:
![twitter home](https://github.com/mohammadekhosravi/twitterClone/blob/master/github/2.jpg)
------------------------------------------------------------------------------------------
#### What it has:
- UI very similar to dim theme of twitter.
- Home page with latest tweet mode.
- Follow and like notifications.
![twitter notifications](https://github.com/mohammadekhosravi/twitterClone/blob/master/github/1.jpg)
- User profile similar to twitter one.
![twitter profile](https://github.com/mohammadekhosravi/twitterClone/blob/master/github/3.jpg)
- Following/Followers list.
- Who to follow section (with simple algorithm).
- Full-text search via Postgress for tweet body only.
- Full user flow
  - Login
  - Registration
  - Logout
  - Change email
  - Change password
  - Reset password
-------------------------------------------------------------------------------------------
#### What it has with Ajax functionality:
- Tweet
- Mention
- Like/Unlike
- Follow/Unfollow (from user profile page only)
--------------------------------------------------------------------------------------------
#### What it hasn't: :sweat_smile:
- Responseiv UI.
- Follow/Unfollow from anywhere except user profile.
- Retweet
- Mention except from tweet detail page.
- Almost all of twitter functionality that isn't listed above.
--------------------------------------------------------------------------------------------
### How to install:
***Because the Full-text search capability is done via Postgress you need to install it locally.***

------------------------------------------------------------------------------------------

*Some of naming below are just my prefrences and aren't mandatory*
```shell
python3 -m venv venv      # create a virtual environment
source venv/bin/activate
pip install -r requirement.txt
```
------------------------------------------------------------------------------------------
Next we need to install and set Postgresql (if this doesn't work for you, please refer to their documentation)
```shell
sudo apt-get install postgresql postgresql-contrib      # for ubuntu
sudo su postgres
createuser -dP twitter      # you will be prompted for a password for the new user
createdb -E utf8 -U twitter twitter     # create twitter database for user twitter.
# using the same name for DB and user is the easiest way for postgres authentication.
```
we have five environment variable in this project you can set them in `.env` file in project root dirctory
lets first make a new SECRET_KEY, shall we :stuck_out_tongue_winking_eye:
```python3
python3 -c 'import secrets; print(secrets.token_urlsafe(38))'
```
now set environment variable (preferably in `.env` file)
```shell
export DEBUG=True
export SECRET_KEY={your generated SECRET_KEY}
export DATABASE_URL=postgres://twitter:{your chosen password for this user}@localhost:5432/twitter
# for email functionality we need a SMTP server, the simplest one is using your gamil account for this.
export DJANGO_EMAIL_HOST_USER={your gmail address}
export DJANGO_EMAIL_HOST_PASSWORD={your gamil password}
```
That was long setup. !Poof :drooling_face:

-------------------------------------------------------------------
Now that configuration is done lets start the server.
```shell
python manage.py migrate      # do the migration
python manage.py createsuperuser      # create a superuser for admin panel
python manage.py runserver
```
go to http://127.0.0.1:8000 and the site should be working.
because we create a new DB, the site is empty and you need to ceate some user, tweet, mention and ... .

--------------------------------------------------------------------
**ALL DONE** :heavy_check_mark:
