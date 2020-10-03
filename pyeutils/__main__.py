defaultquery1 = 'asthma[mesh]+AND+leukotrienes[mesh]+AND+2009[pdat]'
defaultquery2 = 'asthma[mesh]+AND+2019[pdat]' 
defaultquery3 = 'leukotrienes[mesh]+AND+2019[pdat]' 

queries = [
    defaultquery1,
    defaultquery2,
    defaultquery3
]

from efetch import esearch_elink_efetch as efetch

import sys

def main(args=[]):
   
    global queries, defautquery1
    queryno = -1

    if args:
        try:
            queryno = int(args[0])
        except:
            pass

    if queryno != -1:
        results = efetch(defaultquery1)
        print(results)
        
        return 0

    for n, q in enumerate(queries):
        results = efetch(q)
        print(results)

    return 0

if __name__ == "__main__":

    ret = main(args=sys.argv[1:])

    sys.exit(ret)
