# setup
- install gcloud
    - https://cloud.google.com/sdk/docs/install
- `python -m venv server-env`
- (assuming you're on MacOS or Linux) `source ./server-env/bin/activate`
- `pip install -r requirements.txt`
- whenever you install something new, `pip freeze > requirements.txt` before pushing
