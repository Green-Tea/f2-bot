## Prerequisites

- pydle
- bs4
- requests

To install run `pip3 install pydle`  `pip3 install bs4` `pip3 install requests`

## Run

**This bot will only run on python 3.8**\
`python3.8 f2ircbot.py`\
If you have trouble running the bot, feel free to message me on discord: `Seaweed#1828`

## Configure

- Add referee usernames to `reflist.py`
- Put your irc username and password in `f2bot.py`
- Put your api key in `randomMapPicker.py`
- Adjust the parameters in `randomMapPicker.py` to your preference.

## Usage

- Run the bot and your account should be connected to the bancho irc
- Open your irc client and make a multiplayer lobby
- DM yourself with !join #mp_[mpID]
- Select the stage you want to play using !f2 set [stage]
- Select the mod you want to play using !f2 [mod]
- Once done, make sure you close the lobby so the bot can stop listening to that channel

## IRC copy paste

/query banchobot\
!mp make team1 vs team2\
/msg [username] !join #mp\_\
!f2 set [stage]\
!f2 nm\
!f2 hd\
!f2 hr\
!f2 dt\
!f2 tb
