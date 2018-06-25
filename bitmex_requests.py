import requests;
import json;
from datetime import datetime
from datetime import timedelta

#generates a key-value pair in string format
def generateFilter(currency):
    filterDictionary = {};
    filterDictionary["symbol"] = currency;
    filter = json.dumps(filterDictionary);
    return filter;

#makes api requests, doesn't exceed limit of entries per request
def getJsonChunk(currency, startTime, endTime, interval, columns):
    filter = generateFilter(currency);
    start = startTime;
    end = endTime;
    parameters = {"binSize": interval, "columns": columns, "filter": filter, "startTime": start, "endTime": end};
    response = requests.get("https://www.bitmex.com/api/v1/trade/bucketed", params = parameters);
    data = response.json();
    print(response.status_code);
    return data;

#writes the output json out to the output file
def writeOut(output, file):
    with open(file, 'a') as outfile:
        json.dump(output, outfile);

#returns a datetime object for the next hour
def getNextHour(time):
    nextHour = time + timedelta(hours = 1);
    return nextHour;

#returns a string from the datetime object
def getTimeString(time):
    timeString = time.strftime("%Y-%m-%d %H:%M");
    return timeString;

#supports requesting data that exceed limit of entries per request
def writeLargeJson(currency, startTime, endTime, interval, columns, file):
    #creates an empty output file
    open(file, "w").close();

    currentTime = startTime;
    output = [];

    #makes api requests in hourly chunks until the endTime is reached
    while currentTime != endTime:
        nextHour = getNextHour(currentTime);
        print(getTimeString(currentTime));
        output += getJsonChunk(currency, getTimeString(currentTime), getTimeString(nextHour), interval, columns);
        currentTime = getNextHour(currentTime);
    writeOut(output, file);
