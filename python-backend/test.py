import json

def json2dict(jsonfilename):
    with open(jsonfilename, 'r') as jsonFile:
        # print(jsonFile.read())
        jsonData = json.load(jsonFile)
        if type(jsonData) is list:
            jsonData = json.dumps(jsonData)
        return (jsonData)


if __name__ == '__main__':
    jfile = "trashCategoriesData.json"
    jdata = json2dict(jfile)
    print(jdata)

    print(type(jdata))
