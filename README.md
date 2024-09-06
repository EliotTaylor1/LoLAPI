# LoLAPI-CLI
## What is LoLAPI-CLI
LoLAPI-CLI is a CLI tool written in Python that allows you to look-up stats for a League account using Riot's API.

*This project is currently WIP. See roadmap below.*
## How to run
1. Install Python3
   `https://www.python.org/downloads/`
2. Clone this repo `git clone https://github.com/EliotTaylor1/LoLAPI-CLI.git`
3. Open `config.json`
4. Insert your riot API key
5. Insert the region and server of the player you want to search
6. run either `run.bat` (Windows) or `run.sh` (Unix)
    *The script will create a venv in the directory you're running in*
## Roadmap
1. Remove need for region and server setting in config.json
2. UI?

## FAQ
### Q: Where do I get a Riot API key?
A: Go to https://developer.riotgames.com/ and login with a riot account
### Q: What is a 'Name' and a 'Tag'
A: A 'Name' is the player's name. A 'Tag' is the characters after the #.

*For example: Eiiot#EUW*
### Q: What are regions?
A: Regions are clusters of servers. For example the 'europe' region covers EUW and EUNE
### Q: What are servers?
A: This is the specific server the account plays on. For example EUW1 or NA1
### Q: Is there a list of regions and servers?
A: Here is a table:

| **Server** | **Region** |
|------------|------------|
| euw1       | europe     |
| eun1       | europe     |
| na1        | americas   |
| br1        | americas   |
| la1        | americas   |
| la2        | americas   |
| kr         | asia       |
| jp1        | asia       |
| oc1        | asia       |
| ph2        | asia       |
| sg2        | asia       |
| tr1        | asia       |
| th2        | asia       |
| tw2        | asia       |
| vn2        | asia       |