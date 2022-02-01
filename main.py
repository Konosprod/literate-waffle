import sys
import os
import json
import fnmatch
import collections

def hasText(l):
    for x in l:
        for c in x:
            if x["code"] == 101 or x["code"] == 401:
                return True
    return False

def extract_text(file, filename):
    with open(file, "r", encoding="utf8") as f:
        print(file)
        j = json.load(f, object_pairs_hook=collections.OrderedDict)
        prevcode = 0
        text = ""
        csv = ""
        
        if isinstance(j, dict):
            if j["events"]:
                for event in j["events"]:
                    if event is not None:
                        eid = str(event["id"])
                        p = 0
                        for page in event["pages"]:    
                            if hasText(page["list"]):                             
                                csv += ("Event"+eid +";\n")
                                csv +=("Page"+str(p+1)+";\n")

                            for command in page["list"]:
                                if command["code"] == 101:
                                    actor = command["parameters"][4]
                                if command["code"] == 401:
                                    if prevcode == 401:
                                        text += (" " + command["parameters"][0])
                                    else:
                                        text = command["parameters"][0]
                                
                                if command["code"] != 401 and prevcode == 401:
                                    csv+=(actor + ";" + text+"\n")
                                    #print(text)
                                    text = ""

                                prevcode = command["code"]
                            p += 1
        else:
            for o in j:
                if o is not None:
                    if hasText(o["list"]):
                        csv += ("Event"+ str(o["id"])+";\n")
                        for command in o["list"]:
                            if command["code"] == 101:
                                actor = command["parameters"][4]
                            if command["code"] == 401:
                                if prevcode == 401:
                                    text += (" " + command["parameters"][0])
                                else:
                                    text = command["parameters"][0]
                                    
                            if command["code"] != 401 and prevcode == 401:
                                csv+=(actor + ";" + text+"\n")
                                #print(text)
                                text = ""

                            prevcode = command["code"]

        with open(filename.replace(("json"), "csv"), "w+", encoding="utf8") as out:
            out.write(csv)


def main():

    path = sys.argv[1]

    for file in os.listdir(path):
        if fnmatch.fnmatch(file, "Map[0-9]*.json") :
            extract_text(os.path.join(path, file), file)
        if fnmatch.fnmatch(file, "CommonEvents.json"):
            extract_text(os.path.join(path, file), file)




if __name__ == "__main__":
    main()
