
[//]: # ( challenge tech stack: streamlit )

[//]: # ( challenge instructions )

We saw in the previous challenge how to plug a website to our **Prediction API** in order to allow regular users to make predictions.

Now let's create our own website ! 🔥

We are going to use **Streamlit** which will allow us to create a website very easily and without any web development skills.

## First, let's create another website project

We will create a new project directory for the code of our website.

Again, this directory will be located inside of our *projects directory*: `~/code/<user.github_nickname>`.

Create a new project directory named `taxifare-website`.

```bash
cd ~/code/<user.github_nickname>
mkdir taxifare-website
cd taxifare-website
```

Initialise a new git repository:

```bash
git init
```

Create a corresponding repository on our **GitHub** account:

``` bash
gh repo create
```

Go to the GitHub repo in order to make sure that everything is ok:

``` bash
gh browse
```

The repository is empty, which is normal since we have not pushed any code yet...

We are now all set!

## Create a streamlit website

First, we need an `app.py` file inside of our project. The file will contain the code for our page.

``` bash
touch app.py
```

Then, let's copy the `Makefile` that is provided inside of the project... It will allow us to run useful commands for:
- `install_requirements` : dependencies
- `streamlit` : run the **Streamlit** web server in order to see what our website looks like
- `heroku_login` : login to **Heroku**
- `heroku_create_app` : create an app on **Heroku** for our website
- `deploy_heroku` : deploy our app when we are satisfied with its content

``` bash
cp ~/code/<user.github_nickname>/<program.challenges_repo_name>/07-ML-Ops/05-User-interface/02-Taxifare-website/app/Makefile ~/code/<user.github_nickname>/taxifare-website/
```

You project should look like this:

``` bash
.
├── Makefile
└── app.py
```

Not too overwhelming, right ? 😉

Well... This is half the work.

Lets add some content to our website in `app.py`:

``` python
import streamlit as st

'''
# TaxiFareModel front
'''

st.markdown('''
Remember that there are several ways to output content into your web page...

Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
''')

'''
## Here we would like to add some controllers in order to ask the user to select the parameters of the ride

1. Let's ask for:
- date and time
- pickup longitude
- pickup latitude
- dropoff longitude
- dropoff latitude
- passenger count
'''

'''
## Once we have these, let's call our API in order to retrieve a prediction

See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

🤔 How could we call our API ? Off course... The `requests` package 💡
'''

url = 'https://taxifare.lewagon.ai/predict'

if url == 'https://taxifare.lewagon.ai/predict':

    st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

'''

2. Let's build a dictionary containing the parameters for our API...

3. Let's call our API using the `requests` package...

4. Let's retrieve the prediction from the **JSON** returned by the API...

## Finally, we can display the prediction to the user
'''
```

Let's run the **Streamlit** web server and see what our website looks like:

``` bash
make streamlit
```

We have a website of our own running on our machine 🎉

## Now we want to plug our API to the website

... So that users can actually make some predictions!

👉 Let's follow the instructions inside the web page and replace the content with some `requests` package magic and a call to our API!

👉 Again, alternatively, you may use this Le Wagon **Prediction API** if you you do not have one in production:

https://taxifare.lewagon.ai/

https://taxifare.lewagon.ai/predict?pickup_datetime=2012-10-06%2012:10:20&pickup_longitude=40.7614327&pickup_latitude=-73.9798156&dropoff_longitude=40.6513111&dropoff_latitude=-73.8803331&passenger_count=2

Let's inspect `app.py` and check what is being done inside...

Replace the URL to the prediction API with your own and update the code accordingly.

Now let's get crazy with the page content 🎉

Maybe add some map 🗺

Once we are satisfied, let's push the code to production! 🔥

## Heroku setup

- Sign in to [Heroku](https://signup.heroku.com/)
- Install the Heroku CLI (Command Line Interface):

<details>
  <summary markdown='span'><strong> macOS </strong></summary>

  ``` bash
  brew tap heroku/brew && brew install heroku
  ```

</details>
<details>
  <summary markdown='span'><strong> Windows WSL or Ubuntu </strong></summary>

  ``` bash
  curl https://cli-assets.heroku.com/install.sh | sh
  ```
</details>

- Login the CLI

```bash
heroku login
```

## Deploy

Let's setup the project for **Heroku**.

❓ **What do we need to deploy our website to Heroku ?**

We need to add a few configurations files to our project:
- `setup.py` to tell heroku how to install the package of our website
- `MANIFEST.in` + `requirements.txt` for the website dependencies
- `Procfile` + `setup.sh` in order for Heroku to know how to run our website

Let's copy the files provided in the challenge to your web project...

<details>
  <summary markdown='span'><strong> 💡 Hint </strong></summary>

``` bash
cp ~/code/<user.github_nickname>/<program.challenges_repo_name>/07-ML-Ops/05-User-interface/02-Taxifare-website/app/setup.py ~/code/<user.github_nickname>/taxifare-website
cp ~/code/<user.github_nickname>/<program.challenges_repo_name>/07-ML-Ops/05-User-interface/02-Taxifare-website/app/MANIFEST.in ~/code/<user.github_nickname>/taxifare-website
cp ~/code/<user.github_nickname>/<program.challenges_repo_name>/07-ML-Ops/05-User-interface/02-Taxifare-website/app/requirements.txt ~/code/<user.github_nickname>/taxifare-website
cp ~/code/<user.github_nickname>/<program.challenges_repo_name>/07-ML-Ops/05-User-interface/02-Taxifare-website/app/Procfile ~/code/<user.github_nickname>/taxifare-website
cp ~/code/<user.github_nickname>/<program.challenges_repo_name>/07-ML-Ops/05-User-interface/02-Taxifare-website/app/setup.sh ~/code/<user.github_nickname>/taxifare-website
```

</details>

The project should now look like this:

``` bash
.
├── MANIFEST.in
├── Makefile
├── Procfile
├── app.py
├── requirements.txt
├── setup.py
└── setup.sh
```

Create an app for our website on **Heroku**... Remember the app name should be unique on the internet.

💡 You might want to [change the region](https://devcenter.heroku.com/articles/regions) if you are not located inside of Europe...

```bash
heroku create YOUR_APP_NAME --region eu
```

Remember that **Heroku** uses git in order to retrieve the files of your project to put in production.

👉 You need to `git add` and `git commit` the files of your project that you want to push to production before pushing your code to **Heroku**

``` bash
git add --all
git commit -m "code ready to be deployed to production"
```

Finally, we can push our website to **Heroku** 🚀

```bash
git push heroku master
```

Then scale it:

```bash
heroku ps:scale web=1
```

Click on the link provided by the command line `https://YOUR_APP_NAME.herokuapp.com/` and you should access to your website 🎉
