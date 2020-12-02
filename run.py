import json
import logging

from shared.get_page import (extractItems, extractItemUrls, generatePage,
                             pagesToBistracker)

# config log
logging.basicConfig(filename='hello.log',level=logging.DEBUG)

log('--start generatePage')
pages = generatePage()
log('--end generatePage')

log('--start extractItemUrls')
extractItemUrls(pages)
log('--end extractItemUrls')

log('--start extractItems')
extractItems(pages)
log('--end extractItems')

log('--start pagesToBistracker')
extract = pagesToBistracker(pages)
log('--end pagesToBistracker')

# export extract to json file
with open('out.txt', 'w') as f:
    print(json.dumps(extract), file=f)
