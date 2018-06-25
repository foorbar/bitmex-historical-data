from bitmex_requests import writeLargeJson;
from datetime import datetime

start = datetime(2017, 1, 1, 0, 0);
end = datetime(2017, 1, 1, 0, 0)
cols = ["open", "close", "high", "low"];

writeLargeJson("XBTUSD", start, end, "1m", cols,"btc.txt");
writeLargeJson(".ETHXBT", start, end, "1m", cols,"eth.txt");
writeLargeJson(".LTCXBT", start, end, "1m", cols,"ltc.txt");
writeLargeJson(".XRPXBT", start, end, "1m", cols,"xrp.txt");
