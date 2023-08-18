# Description
```bash
This repo crawls posts and tweets of certain users from the PTT Stock forum.
You may found some interesting, intrcutive or even profitable information from those messages.
```

# Installation(Windows)
## Assume MySQL is installed.
## Run the following command to install requirements:
```bash
# for virtual environment
pip install pipenv
# init a virtualenv with python3.9
pipenv --python 3.9
# install requirements
pipenv install
```

## Usage
Change .demo_env to .env and set the variables according to your needs.
Apply token for Line Notification Service and set to "LINE_TOKEN" in .env.
```bash
run
# Start the crawling process.
pipenv run python crawler_scheduler.py
# Start the notifying process.
pipenv run python notifer_scheduler.py
```
