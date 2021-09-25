import json
from scrape import scrape
import argparse

parser = argparse.ArgumentParser(description='TuneFind Parser')
parser.add_argument('type', help='Type ("movie" or "show")', type=str)
parser.add_argument('name', help='Name', type=str)
parser.add_argument('-y','--year', help='Year (Necessary if movie)', default="", type=str, const=1, nargs="?")
parser.add_argument('-j', '--json', help='Output to JSON file', action="store_true")
args = parser.parse_args()
name = args.name
typeName = args.type
year = args.year
outputToJSON = args.json
# Film ise yılını istemen lazım

songsList = scrape(name,typeName,year)
if outputToJSON:
    with open("data.json","w",encoding="utf-8") as jsonFile:
        json.dump(songsList,jsonFile,indent=5, ensure_ascii=True)
