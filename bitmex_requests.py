import requests;
import json;
import time;
from datetime import datetime
from datetime import timedelta

requestNum = 0;

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
    global requestNum;
    requestNum += 1;
    data = response.json();
    print(response.status_code);
    print (requestNum);
    return data;

#writes the output json out to the output file
def writeOut(output, file):
    with open(file, 'a') as outfile:
        json.dump(output, outfile);

#returns a datetime object 480 minutes later
def jump(time, interval):
    if interval == '1m':
        nextTime = time + timedelta(minutes = 480);

    if interval == '1h':
        nextTime = time + timedelta(hours = 480);

    if interval == '1d':
        nextTime = time + timedelta(days = 480);

    return nextTime;


#returns a string from the datetime object
def getTimeString(time):
    timeString = time.strftime("%Y-%m-%d %H:%M");
    return timeString;

#supports requesting data that exceed limit of entries per request
def writeJson(currency, startTime, endTime, interval, columns, file):
    #creates an empty output file
    open(file, "w").close();

    currentTime = startTime;
    output = [];

    #makes api requests in 480 minutes chunks until the endTime is reached
    while currentTime < endTime:
        nextTime = jump(currentTime, interval);
        print(getTimeString(currentTime));
        output += getJsonChunk(currency, getTimeString(currentTime), getTimeString(nextTime), interval, columns);
        currentTime = jump(currentTime, interval);

        if requestNum > 120:
            print("reached maximum amount of requests");
            time.sleep(320);
            global requestNum;
            requestNum = 0;

    writeOut(output, file);
