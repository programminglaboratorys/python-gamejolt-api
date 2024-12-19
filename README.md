# python-gamejolt-api

python Game Jolt API wrapper

## TODO

- complete subcomponents /scores/
- able to operate from a User model (basically being able to open sessions, give/remove trophies, etc)
- documentation
- examples

## example/quickstart

gamejolt expects you to create the \_post and evaluate methods
\_post sends the request to the gamejolt api
evaluate: parses the response and returns a dictionary with 3 keys: success, response and message

```python
from gamejolt import GameJolt as GameJoltApi
import requests

class GameJolt(GameJoltApi):
    def _post(self, url: str) -> requests.Response:
        return requests.post(url, timeout=10)

    def evaluate(self, response: requests.Response) -> dict:
        json: dict = response.json()
        return {
            "success": json["response"]["success"],
            "response": json["response"],
            "message": json["response"].get("message"),
        }

gamejolt = GameJolt("YOUR_GAME_KEY", game="YOUR_GAME_ID")
```

### fetch a user

```py
user = gamejolt.users.fetch("1")
print(user) # output: User(id=14728, type='Developer', username='1', signed_up='12 years ago', last_logged_in='12 years ago', status='Active')
```

> [!NOTE] depending on your ide/editor; you can hover over the functions to get documentation or even read the code

> [!WARN] all the below methods require the user token to be set.
> use `User.set_token()` to set the user token

### give/fetch a trophy to/from a user

```py
the_trophy = gamejolt.trophies.fetch(user, 1234) # remove trophy id to fetch all trophies
print(the_trophy)
gamejolt.trophies.add_achieved(user, 12345) # could raises UserAlreadyHasTrophy or IncorrectTrophyID
```

### open a session and set data store item

```py
gamejolt.sessions.open(user)
gamejolt.data_store.set("key", "value") # set an item globally for the game
gamejolt.data_store.set(user, "cookies", "100") # set an item for a user
```
