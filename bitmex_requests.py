import requests;
import json;
from datetime import datetime
from datetime import timedelta

open('data.txt', 'w').close();

def generateFilter(currency):
    filterDictionary = {};
    filterDictionary["symbol"] = currency;
    filter = json.dumps(filterDictionary);
    return filter;

def getCurrencyJson(currency, startTime, endTime, interval, columns):
    filter = generateFilter(currency);
    start = startTime;
    end = endTime;
    parameters = {"binSize": interval, "columns": columns, "filter": filter, "startTime": start, "endTime": end};
    response = requests.get("https://www.bitmex.com/api/v1/trade/bucketed", params = parameters);
    data = response.json();
    print(response.status_code);
    return data;

def writeOut(output):
    with open('data.txt', 'a') as outfile:
        json.dump(output, outfile);

def getNextHour(time):
    nextHour = time + timedelta(hours = 1);
    return nextHour;

def getTimeString(time):
    timeString = time.strftime("%Y-%m-%d %H:%M");
    return timeString;

def getBoundedCurrencyJson(currency, startTime, endTime, interval, columns):
    currentTime = startTime;
    output = [];
    while currentTime != endTime:
        nextHour = getNextHour(currentTime);
        print(getTimeString(currentTime));
        output += getCurrencyJson(currency, getTimeString(currentTime), getTimeString(nextHour), interval, columns);
        currentTime = getNextHour(currentTime);
    writeOut(output);

start = datetime(2017, 1, 1, 0, 0);
end = datetime(2017, 1, 2, 0, 0)
cols = ["open", "close", "high", "low"];

getBoundedCurrencyJson("XBTUSD", start, end, "1m", cols)
