from datetime import datetime

def API_RESPONSE(status,statusCode,data=None):
    return{"status":status,"statusCode":statusCode,"data":data,"timeStamp":str(datetime.now())}