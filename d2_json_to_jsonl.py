# script to do some light cleanup of our data
# 1) convert from JSON to JSONL (newline)
# 2) replace whitespace in keys to _ (underscores)
# 3) if first char in key is numeric, prefix with _
# this script brute forces some stuff so wouldn't be suitable for larger data volumes

import json

# open weapons.json
source = open('weapons.json')
data = json.load(source)

with open('weapons.jsonl', 'w') as outfile:
    for entry in data:
        #print(data[entry])
        for key in data[entry].copy(): # modifying keys so need to iterate over copy
            if ' ' in key and key[0].isnumeric():
                data[entry]['_' + key.replace(' ','_')] = data[entry].pop(key)
            elif ' ' in key:
                data[entry][key.replace(' ','_')] = data[entry].pop(key)
            elif key[0].isnumeric():
                data[entry]['_' + key] = data[entry].pop(key)
        json.dump(data[entry], outfile)
        outfile.write('\n')