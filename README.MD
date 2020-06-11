<h1 align="center">Epigeek - BotyGeek :robot:</h1>

<p align="center">
  <img src="https://img.shields.io/github/go-mod/go-version/epigeek/BotyGeek/master?style=flat-square"/>
  <img src="https://img.shields.io/github/license/epigeek/BotyGeek?style=flat-square"/>
  <img src="https://img.shields.io/github/languages/code-size/epigeek/BotyGeek?style=flat-square"/>
</p>

botygeek is a discord bot to manage epigeek discord server.

## :star: Feature
### logs
the bot logs all the event in the server :
- menber join
- menber quit
- message send
- message delete
- message edit
- message ping
- reation add
- reaction remove

### staff
- clear
- ping

### roles
- add roles when player join the server
- add and remove Gaming roles

## :heavy_check_mark: Require
- python >= 3.6.9
- view [`Require.txt`](Require.txt)

## :blue_book: Usage
### Install 
```sh
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r Require.txt
```

### Config
the config file is in `run/config.yaml`.
```yaml
token : abcdefghijklmnopqrstovwxyzABCDEFGHIJKLMNOPQRSTOVWXYZ0123456 
logs : run/logs
roleOnJoin : []
```
inside it you can find 2 propery:
- `token` : the token of the discord bot
- `logs` : the path to the logs folder
- `roleOnJoin` : list of role id, will be added when a user join
- `roleSelector` : list of gaming role id, will be added when a player ask the bot fot it

### Launch 
to run the bot
```sh
python3 main.py
```



## :family: Contributor
[![Contributor](https://contributors-img.web.app/image?repo=epigeek/BotyGeek)](https://github.com/epigeek/BotyGeek/graphs/contributors)
