from datetime import date, timedelta
from datetime import datetime
from dateutil import parser

def ConvertDate(dt = "Today"):
   """Return date in mm/dd/yyyy format"""
   
   if dt.find("Today") != -1:
        #try:
          dts = dt.split(" ")
          hm = dts[1]
          m = hm.split(':')[1]
          h = hm.split(':')[0]
          ampm = dts[2]   
          #print(h)
          if ampm =="PM":                         
             h = int(h) 
             if h < 12:
                h = h+12
          today2 = datetime(date.today().year, date.today().month, date.today().day, int(h), int(m), 0)
          #print(today2)          
          return today2.strftime('%m/%d/%Y  %H:%M')
        #except: return ''
   elif dt.find("Yesterday") != -1:
        try:
          yest = date.today() - timedelta(days=1)
          dts = dt.split(" ")
          hm = dts[1]
          m = hm.split(':')[1]
          h = hm.split(':')[0]
          ampm = dts[2]        
          if ampm =="PM":             
             h = int(h) 
             if h < 12:
                h = h+12
          yest2 = datetime(yest.year, yest.month, yest.day, int(h), int(m), 0)          
          return yest2.strftime('%m/%d/%Y %H:%M')
        except: return ''
   elif dt.find(",") != -1 :
       try:
         dts = dt.split(",")
         if(len(dts)>=2):
           dtnew =  dts[1].strip()+ ' ' + str(datetime.now().year)
           #print(dtnew)
         dt_new_format = datetime.strptime(dtnew, '%b. %d %Y')        
         return dt_new_format.strftime("%m/%d/%Y")
       except: return ''
   elif ((dt.find("hours") != -1) | (dt.find("hour") != -1)) :
        try:
          dts = dt.split(" ")
          #print(dts[0])
          today = datetime.now() - timedelta(hours=int(dts[0]))         
          return today.strftime('%m/%d/%Y %H:%M')
        except: return ''
   elif dt.find("min") != -1 :
       try:
        dts = dt.split(" ")
        today = datetime.now() - timedelta(minutes=int(dts[0]))        
        return today.strftime('%m/%d/%Y %H:%M')
       except: return ''
   elif dt.find("am") != -1 :
       try:
        dts = dt.split("am")
        dts1 = dts[0].split(":")
        today = datetime.today()      
        todaydt = datetime(today.year, today.month, today.day, int(dts1[0]), int(dts1[1]), 0) 
        return todaydt.strftime('%m/%d/%Y %H:%M')
       except: return ''
   elif dt.find(str(datetime.now().year)) != -1 : 
       try:
          dt1 = datetime.strptime(dt, '%b %d %Y')
          return dt1.strftime('%m/%d/%Y')
       except: return ''
   elif dt.find('/') != -1 :
       try:
         return dt
       except:           
           return datetime.today()
   else: 
        return datetime.today()

