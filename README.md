# Datura-ai-FastAPI-Task
## Purpose
This project was part of a coding test for Senior Python Backend Engineer position.
It provides an API endpoint to get Tao dividends from the Bittensor blockchain
and optionally provides sentiment analysis on it.

## Setup
1. Clone the repository to your local machine, to whatever path you like:
   - `cd /your/folder/here`
   - `git clone .`
2. CD into the project directory, like `cd Datura-ai-FastAPI-Task`
3. Make a copy of the `example.env` file and simply call it `.env`
4. Fill in the values. For the API_AUTH_TOKEN you can choose whatever value you want.
5. Build docker with `docker-compose build`
6. Run docker with `docker-compose up`
7. You can check if the containers are up and running with `docker-compose ps`
8. Go to http://127.0.0.0:8000/docs
Now you are fully set up.

## Using the API
Once you are at the FastAPI Docs (if you have followed the Setup steps),
you should see an `Authorize` button and an endpoint `/api/v1/tao_dividends`.
Click on the `Authorize` button and type in the auth token you set in your .env file and click "Authorize".
Now click on the `tao_dividends` endpoint and click on `Try it out`.
Here you can put in the `netuid` and `hotkey` of your choice and then click on `Execute`.
If you choose to set `trade` to `True`, it will add a stake or unstake.
You should see a result that looks something similar to this:
```JSON
{
   "netuid": 2,
   "hotkey": "abcd1234",
   "dividends": {
    "2": {
      "abcd1234": 12345678
    }
   },
   "timestamp": "2025-03-21T14:18:35.519551",
   "cached": true,
   "stake_tx_triggered": true
}
```
If `cached` is true, then the dividend value was taken from the cache instead of the Bittensor blockchain.
When values are fetched from there, they will be cached for 2 minutes.
Please note that the `netuid` and `hotkey` parameters are optional. If you don't provide them,
then it will return every `netuid` and `hotkey`.
