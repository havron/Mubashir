import json
import urllib.request

num_stories = 3
TARGET = "https://reddit.com/r/UpliftingNews/hot.json?limit=%d" % num_stories
# also top.json, new.json available

# get the data and load into JSON
req = urllib.request.Request(TARGET, method='GET')
req.add_header('User-Agent', 'installed app:T9CS8svlPtNOlw:0.1 (by /u/samhavron)')
resp_json = urllib.request.urlopen(req).read().decode('utf-8')
resp = json.loads(resp_json)


if not resp:
  print("Error retrieving uplifting news from '%s' on Reddit\n" % TARGET)
else:
  for i in range(num_stories):
    print("Hot story #%d:\n" % (i+1) + resp["data"]["children"][i]["data"]["title"]) 
