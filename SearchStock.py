##import re
##
##scan_file('./stocklist.csv', 'ap')
##
##def scan_file(path_to_file, word):
##    with open(path_to_file, 'r') as eFile:
##        all_data = {}
##        f_line = eFile.readline()
##        re.search(r'^'+word+'(.*?)$', f_line)
##        for line in eFile:
##            _elements = line[pos[1]:]
##            _ps = _elements.split(":", 1)[0]
##
##            _key = re.sub(r"([)\d(])", "", _ps)
##            if _key not in all_data:
##                all_data[_key] = []
##            all_data[_key].append(line)
##    eFile.close()
##
##    
##    return True
##
##
import re

def scan_file(path_to_file, word):
    all_data = {}
    with open(path_to_file, 'r') as eFile:
        for line in eFile:
            _stockInfo = line.split(',', 1)
            #print(_stockInfo[0])
            if re.search(r'^'+word+'(.*?)$', _stockInfo[0], re.IGNORECASE):
                all_data[_stockInfo[0]] = _stockInfo[1].strip('\n')
    eFile.close()
    print(all_data)
    
