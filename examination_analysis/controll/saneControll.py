

from service.sane import sanePaperService
from config.pathVariable import PathVariable

def mySane():
    mySane = sanePaperService.SanePaper()
    mySane.createInventory()
    

    # mysane.sane( SaneVariables, 100,mode='Color',multiple=False)
    return mySane.sanePaper()