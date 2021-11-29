# salesforce-oauth-sample

This is a sample code for authentication and authorization from Python & Django to Salesforce using OAuth.
You can try the following sample flows locally or on heroku.
- Username-Password Flow
- JWT Bearer Flow
- Web server Flow
- Refresh token Flow
- User agent Flow
- Device Flow

## Running Locally

Make sure you have Python 3.9 [installed locally](https://docs.python-guide.org/starting/installation/). To push to Heroku, you'll need to install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).

```sh
1. Update "oauth/jwt_flow/test.pem" and oauth/common_const.py here
2. Invoke the following commands:
$ cd salesforce-oauth-sample
$ python3 -m venv salesforce-oauth-sample
$ pip install -r requirements.txt
3. Invoke the following command if you are using linux:
$ heroku local
   Invoke the following command if you are using windows:
$ heroku local web -f Procfile.windows
```

Your app should now be running on [localhost:5000](http://localhost:5000/).


## Deploying to Heroku

```sh
$ heroku create
$ git push heroku main
$ heroku open
```