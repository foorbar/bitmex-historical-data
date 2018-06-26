from bitmex_requests import writeJson;
from datetime import datetime

start = datetime(2018, 3, 30, 0, 0);
end = datetime(2018, 6, 26, 0, 0)
cols = ["open", "close", "high", "low"];

writeJson("ETHM18", start, end, "1m", cols,"eth_minutes.txt");
