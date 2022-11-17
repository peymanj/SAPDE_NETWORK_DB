from source.framework.initiate import Initiate
from datetime import datetime
import sys

if __name__ == '__main__':

    print('\n', 100 * ':')
    print(datetime.now())   
    Initiate.start(sys.argv)
