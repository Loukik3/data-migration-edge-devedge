import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import numpy as np
import json
import requests
import os
import datetime
import time
import statistics
import math
import random
import sys
import itertools
import traceback
import inspect
import sys
import gzip
import platform
try:
    version = platform.python_version().split(".")[0]
    if version == "3":
        import app_config.app_config as cfg
        
    elif version == "2":
        import app_config as cfg
    config = cfg.getconfig()
except:
    config = {
    "api": {
      "efficiency": "http://10.212.63.203/efficiency/",
      "meta": "http://10.212.63.203/exactapi",
      "service": "http://10.212.63.203/service",
      "datapoints": "http://10.212.63.200/api/v1/datapoints",
      "query": "http://10.212.63.203/api/v1/datapoints/query",
      "model": "http://10.212.63.203/model/",
      "batchefficiency": "http://10.212.63.203/batchefficiency/",
      "prediction": "http://10.212.63.203/model/prediction",
      "public_datacenter_url": "https://edgelive.thermaxglobal.com/",
      "fcm_send": "https://fcm.googleapis.com/fcm/send"
    },
    "telegram": {},
    "email": {
      "AWS_SECRET_KEY": "",
      "AWS_ACCESS_KEY": ""
    },
    "smtp": {
      "host": "smtp.office365.com",
      "port": 587,
      "sender_email": "Edge Live <Noreply.Edgelive@Thermaxglobal.com>"
    },
    "timeZone": 5.5,
    "loadBucketSize": 0,
    "loadTagLimit": 0,
    "modelBucketSize": "0",
    "unitsId": "61bb218e5b5042014bb996c7",
    "id": "611b80047afa992d36e308b2",
    "spaceId": "",
    "BROKER_ADDRESS": "10.212.63.200",
    "siteId": "61a0f6900408f7747ef64ec3",
    "customerId": "61a0f6890408f7747ef64ec2",
    "BROKER_PASSWORD": "iota#re-mqtt39",
    "BROKER_USERNAME": "ES-MQTT",
    "maxLoad": 0,
    "FCM_SERVER_KEY": "AAAAbLfsn9k:APA91bGqVp-WKaZyt1fkzDpQmcvZQh7SCMrNgqjtjIC3LvV4lr5NMIpGi36lVm3-og9QZbOpgOvTS2rUleVKroZmlKo2uWU3BAinZ0vGrYDdHmzv_LfGrmD1CVyqtecUHO-zS5UEr6pb",
    "batchefficiency": "http://10.212.63.203/batchefficiency/",
    "LS_PREFIX": "tmx",
    "appstoreUrl": "https://apps.apple.com/us/app/thermax-edge-live/id1626814035",
    "playstoreUrl": "https://play.google.com/store/apps/details?id=com.tmx.pulse",
    "fcm_send": "https://fcm.googleapis.com/fcm/send"
  }
devEdgePreProdConfig = {
    "api": {
      "meta": "http://10.211.68.75/exactapi",
      "datapoints": "http://10.211.71.252/api/v1/datapoints",
      "query": "http://10.211.68.75/api/v1/datapoints/query",
      "model": "http://10.211.68.75/model/",
      "prediction": "http://10.211.68.75/prediction",
      "fcm_send": "https://fcm.googleapis.com/fcm/send",
      "efficiency": "http://10.211.68.75/efficiency/",
      "service": "http://10.211.68.75/service",
      "public_datacenter_url": "https://devedgelive.thermaxglobal.com/",
      "batchefficiency": "http://10.211.68.75/batchefficiency/"
    },
    "telegram": {

    },
    "email": {
      "AWS_ACCESS_KEY": "",
      "AWS_SECRET_KEY": ""
    },
    "smtp": {
      "host": "smtp.office365.com",
      "port": 587,
      "sender_email": "Edge Live \u003CNoreply.Edgelive@Thermaxglobal.com\u003E"
    },
    "timeZone": 5.5,
    "loadBucketSize": 0,
    "loadTagLimit": 0,
    "modelBucketSize": "0",
    "unitsId": "61bb218e5b5042014bb996c7",
    "id": "611b80047afa992d36e308b2",
    "spaceId": "dev",
    "BROKER_ADDRESS": "10.211.71.252",
    "siteId": "61a0f6900408f7747ef64ec3",
    "customerId": "61a0f6890408f7747ef64ec2",
    "BROKER_PASSWORD": "iota#re-mqtt39",
    "BROKER_USERNAME": "ES-MQTT",
    "maxLoad": 0,
    "FCM_SERVER_KEY": "AAAAbLfsn9k:APA91bGqVp-WKaZyt1fkzDpQmcvZQh7SCMrNgqjtjIC3LvV4lr5NMIpGi36lVm3-og9QZbOpgOvTS2rUleVKroZmlKo2uWU3BAinZ0vGrYDdHmzv_LfGrmD1CVyqtecUHO-zS5UEr6pb",
    "batchefficiency": "http://10.211.68.75/batchefficiency/",
    "LS_PREFIX": "sandbox",
    "appstoreUrl": "https://apps.apple.com/us/app/thermax-edge-live/id1626814035",
    "playstoreUrl": "https://play.google.com/store/apps/details?id=com.tmx.pulse",
    "fcm_send": "https://fcm.googleapis.com/fcm/send",
    "activity_types": [],
    "activity_types_debug": [],
    "service_ports": {

    }
  }

def tr():
    print(traceback.format_exc())


def modeloutputtag():
    url = "https://data.exactspace.co/exactapi/units/6581818964ee3f0007e6c471/modelpipelines?filter={%22fields%22:[%22outputTag%22]}"
    model = requests.get(url).json()
    tags = [tag["outputTag"] for tag in model]
    return tags

modetags = modeloutputtag()

def createConfig(fileName,lst,key=""):
    try:
        data = {}
        for i in lst:
            if key != "":
                data[i[key]] = ""
            else:
                data[i] = ""
        with open(fileName, "w") as json_file:
            json.dump(data, json_file)
    except:
        tr()


# print(unitsId)
class dataMiragtion():
    def __init__(self,unitsId) -> None:
        self.unitsId = unitsId
        self.mappedDf = pd.read_csv("metaExactSpaceDemo.csv")[["dataTagId","actual tags"]].reset_index(drop=True)
        self.mappedDf["dataTagId"] = "NJT_" + self.mappedDf["dataTagId"]
        self.n = len(self.mappedDf)


    def getResponseBody(self,response,word="",printa=False):
        try:
            if(response.status_code==200):
                if printa:
                    print(f"Got {word} successfully.....")

                body = json.loads(response.content)
                if type(body) != list:
                    body = [body]
                
            else:
                body =[]
                print(f"Did not get{word} successfully.....")
                print(response.status_code)
                # print(response.content)
            return body
        except:
            print(traceback.format_exc())

    def getTagmeta(self,unitsId):
        try:
            query = {"unitsId":unitsId}
            urlQuery = config["api"]["meta"] + '/tagmeta?filter={"where":' + json.dumps(query) + ',"fields":["dataTagId"]}'
            response = requests.get(urlQuery)
            word = "tagmeta"
            body = self.getResponseBody(response,word,1)
            return body
        except:
            tr()

    def getForms(self,unitsId):
        try:
            urlQuery = config["api"]["meta"] + "/units/" + unitsId + "/forms"
            print(urlQuery)
            response = requests.get(urlQuery)
            word = "forms body"
            body = self.getResponseBody(response,word,1)
            return body
        except:
            tr()


    def getValuesProd(self,tagList,startTime, endTime,agg=False):
        try:
            url = config["api"]["query"]
            print("url for getting data", url)
            metrics = []
            
            for tag in tagList:
                if agg:
                    agg = [{"name": "avg","sampling": {"value": "1","unit": "minutes"},"align_end_time": True}]
                    tagDict = {
                        "tags":{},
                        "name":tag,
                        "aggregators": agg
                    }
                else:
                    # print("Not using agg...")
                    tagDict = {
                        "tags":{},
                        "name":tag,
                        # "aggregators": agg
                    }
                metrics.append(tagDict)
                
            query ={
                "metrics":metrics,
                "plugins": [],
                "cache_time": 0,
                "start_absolute": startTime,
                "end_absolute": endTime
                
            }
        #     print(json.dumps(query,indent=4))
            res=requests.post(url=url, json=query)
            values=json.loads(res.content)
            finalDF = pd.DataFrame()
            for i in values["queries"]:
                df = pd.DataFrame(i["results"][0]["values"],columns=["time",i["results"][0]["name"]])

                try:
                    # print(i["results"][0]["name"])
                    # finalDF = pd.join([finalDF,df.set_index("time")],axis=1)
                    finalDF = finalDF.join(df.set_index("time"),how="outer")
                except Exception as e:
                    print(e)
                    finalDF = pd.concat([finalDF,df],axis=1)
                
            # finalDF.dropna(inplace=True)
            # finalDF.interpolate(inplace=True,limit_direction="both")

            finalDF.reset_index(inplace=True)

            # print(dates)
            return finalDF
        except Exception as e:
            print(traceback.format_exc())
            return pd.DataFrame()
            
    def getValuesPreProd(self,tagList,startTime, endTime,agg):
        try:
            url = preProdconfig["api"]["query"]
            print("url for getting data", url)
            metrics = []
            
            for tag in tagList:
                tagDict = {
                    "tags":{},
                    "name":tag,
                    "aggregators": agg
                }
                metrics.append(tagDict)
                
            query ={
                "metrics":metrics,
                "plugins": [],
                "cache_time": 0,
                "start_absolute": startTime,
                "end_absolute": endTime
                
            }
        #     print(json.dumps(query,indent=4))
            res=requests.post(url=url, json=query)
            values=json.loads(res.content)
            finalDF = pd.DataFrame()
            for i in values["queries"]:
                df = pd.DataFrame(i["results"][0]["values"],columns=["time",i["results"][0]["name"]])

                try:
                    # print(i["results"][0]["name"])
                    # finalDF = pd.join([finalDF,df.set_index("time")],axis=1)
                    finalDF = finalDF.join(df.set_index("time"),how="outer")
                except Exception as e:
                    print(e)
                    finalDF = pd.concat([finalDF,df],axis=1)
                
            # finalDF.dropna(inplace=True)
            # finalDF.interpolate(inplace=True,limit_direction="both")

            finalDF.reset_index(inplace=True)

            # print(dates)
            return finalDF
        except Exception as e:
            print(traceback.format_exc())
            return pd.DataFrame()
    
    
    def deleteKairos(self,taglist,startTime,endTime):
        try:
            query = {}
            query["metrics"] = []
            for metric in taglist:
                query["metrics"].append({"name":metric})
                
            query["start_absolute"] = startTime
            query["end_absolute"] = endTime
            
            url = preProdconfig["api"]["datapoints"] + "/delete"
            res = requests.post(url, json=query)
            
            if res.status_code == 200 or res.status_code == 204:
                print("deleting successful...")
            else:
                print("deleting unsuccessful",res.status_code)
        except:
            tr()
            
            
    def postOnKairos(self,df):
        try:
            for dataTagId in df.columns:
                if dataTagId != "time":
                    print("*"*30,str(dataTagId),"*"*30)
                    postUrl = preProdconfig["api"]["datapoints"]
                    reqDataPoints = 25000 
                    print(f"len of df {len(df)}")
                    for i in range(0,len(df),reqDataPoints):
                        print(i)
                        new_df =  df[["time",dataTagId]][i:i+reqDataPoints]
                        new_df.dropna(inplace=True,axis=0)

                        if len(new_df) > 0:
                            postArray = new_df[["time",dataTagId]].values.tolist()
                            print(f"len of post array {len(postArray)}")
                            postBody = [{
                                "name":dataTagId,
                                "datapoints":postArray,
                                # "tags":{"type":"derived"}
                            }]
                            print(postUrl)
                            res = requests.post(postUrl,json=postBody)
                        
                            if res.status_code == 200 or res.status_code == 204:
                                print("posted on kairos successfully")
                            else:
                                print(res.status_code)
                                print(res.content)
        except:
            print(traceback.format_exc())
            
            
    def postOnKairosV2(self,df):
        try:
            for dataTagId in df.columns:
                if dataTagId != "time":
                    postUrl = preProdconfig["api"]["datapoints"]
                    reqDataPoints = 2500
                    print(f"len of df {len(df)}")
                    for i in range(0,len(df),reqDataPoints):
                        
                        print("*"*30,str(dataTagId),str(i),"*"*30)
                        new_df =  df[["time",dataTagId]][i:i+reqDataPoints]
                        new_df.dropna(inplace=True,axis=0)

                        if len(new_df) > 0:
                            postArray = new_df[["time",dataTagId]].values.tolist()
                            print(f"len of post array {len(postArray)}")
                            
                            postBody = [{
                                "name":dataTagId,
                                "datapoints":postArray,
                                "tags":{"type":"derived"}
                            }]

                            gzipped = gzip.compress(bytes(json.dumps(postBody), 'UTF-8'))

                            headers = {'content-type': 'application/gzip'}
                            print(postUrl)
                            res = requests.post(postUrl,gzipped, headers=headers)
                            time.sleep(1)
                            if res.status_code == 200 or res.status_code == 204:
                                print(res.status_code)
                                print("posted on kairos successfully")
                                
                            else:
                                print(res.status_code)
                                print(res.content)
                            
        except:
            print(traceback.format_exc())


    def createBodyForForms(self,formBody):
        try:
            returnLst = []
            for i in formBody:
                if "fields" in i.keys():
                    for feild in i["fields"]:
                        body = {}
                        body["dataTagId"] = feild["dataTagId"]
                        returnLst.append(body)
            # print(returnLst)
            return returnLst
        except:
            tr()

    def queueSize(self,qTag,limit):
        try:
            et = time.time() * 1000
            st = et - 1*1000*60*15
            agg = [{"name": "sum","sampling": {"value": "1","unit": "minutes"},"align_end_time": True}]
            try:
                qSize = list(self.getValuesPreProd([qTag],st,et,agg).tail(1)[qTag])[0]
            except:
                tr()
                qSize = limit -1
            print("qSize:",qSize)
            while qSize > limit:
                time.sleep(30)
                print("qSize:",qSize)
                try:
                    et = time.time() * 1000
                    st = et - 1*1000*60*60
                    qSize = list(self.getValuesPreProd([qTag],st,et,agg).tail(1)[qTag])[0]
                except:
                    tr()
                    qSize = limit - 1
        except:
            tr()
            
   

    def prodFuncHistoricData(self,deleteData = False):
        try:
            mappedDf = pd.read_csv("metaExactSpaceDemo.csv")[["dataTagId","actual tags"]].reset_index(drop=True)
            mappedDf["dataTagId"] = "NJT_" + mappedDf["dataTagId"]

            et = time.time() * 1000
            st = et - 1*1000*60*60*24*31*6
            lennn = len(mappedDf)
            count = 0

            for idx,dataTagId in enumerate(mappedDf["dataTagId"]):
                oldTagId = mappedDf.loc[idx,"actual tags"]
                
                    
                print("*"*30,str(self.unitsId),str(dataTagId),str(oldTagId),str(count),"*"*30)
                print("remaining tags:" , str(lennn-count))

                try:
                    dfProd = self.getValuesProd([oldTagId],st,et,False)
                except:
                    dfProd = self.getValuesProd([oldTagId],st,et,False)
                
                dfProd.columns = ["time",dataTagId]

                if deleteData:
                    self.deleteKairos([dataTagId],st,et)

                self.queueSize("kairosdb.queue.file_queue.size",1000000)
                self.queueSize("kairosdb.http.ingest_count",9000000)

                print(dfProd)
                self.postOnKairosV2(dfProd)

                count += 1
                
        except:
            tr()


    def postDataDefaultTags(self,remainingTags,numTag,iniTL,currentTimeStamp,client):
        for i in range(0, len(remainingTags) ,numTag):
            tagList = list(remainingTags[i:numTag+i])
            start = 1691346600000
            end = 1693420200000
            st = random.randint(start, end)
            et = st + 1*1000*60*10
            df = self.getValuesProd(tagList,st,et)
            
            df.fillna(method="bfill",inplace=True)
            df.fillna(method="ffill",inplace=True)
            # print(df)

            for tag in tagList:
                topicLine = iniTL + f"{tag}/r"
                topicLine2 = "u/6581818964ee3f0007e6c471/" + f"{tag}/r"
                try:
                    v = float(df.loc[0,tag])
                    ### TESTING ONLY ONGC -- Scaling DATA for certain tags
                    # if tag in modetags:
                    #     v = v*1.1
                    ######################################################
                    if not pd.isnull(v):
                        postBody = {
                            "v" : v,
                            "t" : currentTimeStamp
                        }

                        print(postBody)
                        client.publish(topicLine,json.dumps([postBody]))
                        client.publish(topicLine2,json.dumps([postBody]))

                        topicForwarded = "kairoswriteexternal"
                        postbody = [{"name":tag,"datapoints":[[postBody["t"], postBody["v"]]],"tags":{"type":"raw"}}]
                        print(postbody)

                        client.publish(topicForwarded, json.dumps(postbody))
                    else:
                        pass
                except:
                    pass



    def mainFuncLiveData(self,client):
        try:
            x = [8,9,10,11]
            currentTimeStamp = int(time.time() * 1000)
            currentTime = datetime.datetime.now()
            currentMonth = currentTime.month
            currentQuarter = (currentMonth-1)//4 + 1
            currentDay = currentTime.day
            currentHour = currentTime.hour
            currentMinute =  currentTime.minute
            currentSecond = currentTime.second
            last5Minute = abs(currentMinute  - 2)
            validMonth = x[currentMonth - currentQuarter*4 + 3]

            if validMonth == 9 and currentDay > 15:
                validMonth = 10

            startDate = "2023/{}/{} {}:{}:{}".format(validMonth,currentDay,currentHour,last5Minute,currentSecond)
            endDate = "2023/{}/{} {}:{}:{}".format(validMonth,currentDay,currentHour,currentMinute,currentSecond)

            startDate = datetime.datetime.strptime(startDate, '%Y/%m/%d %H:%M:%S')
            endDate = datetime.datetime.strptime(endDate, '%Y/%m/%d %H:%M:%S')

            print(startDate,endDate)

            startTimestamp=time.mktime(startDate.timetuple())*1000
            endTimestamp=time.mktime(endDate.timetuple())*1000

            numTag = 30
            iniTL = f"u/{self.unitsId}/"
            remainingTags = []

            for i in range(0, self.n ,numTag):
                tagList = list(self.mappedDf["dataTagId"][i:numTag+i])

                ## FOR ONGC -calc tag  ########################
                if "NJT_R2_steam_to_fuel_ratio" in tagList:
                    # print("NJT_R2_steam_to_fuel_ratio -- found ")

                    # Calculate the timestamp for 2 days ago (48 hours * 60 minutes * 60 seconds * 1000 milliseconds)
                    twoDaysAgoTimeStamp = currentTimeStamp - (2 * 24 * 60 * 60 * 1000)
                    startTimestamp = twoDaysAgoTimeStamp
                    # Add 5 minutes in milliseconds to the twoDaysAgoTimeStamp
                    twoDaysAgoTimeStamp += (2 * 60 * 1000)
                    endTimestamp = twoDaysAgoTimeStamp

                ################################################

                df = self.getValuesProd(tagList,startTimestamp,endTimestamp)


                df.fillna(method="bfill",inplace=True)
                df.fillna(method="ffill",inplace=True)
                print(df)

                for tag in tagList:
                    topicLine = iniTL + f"{tag}/r"

                    topicLine2 = "u/6581818964ee3f0007e6c471/" + f"{tag}/r"

                    try:
                        v = float(df.loc[0,tag])
                        print(v)
                        ### TESTING ONLY ONGC-- Scaling DATA for certain tags
                        # if tag in modetags:
                        #     v = v*1.1
                        ######################################################
                                                        
                        if not pd.isnull(v):
                            postBody = {
                                "v" : v,
                                "t" : currentTimeStamp
                            }
                            print(postBody)
                            client.publish(topicLine,json.dumps([postBody]))
                            client.publish(topicLine2,json.dumps([postBody]))

                            topicForwarded = "kairoswriteexternal"
                            postbody = [{"name":tag,"datapoints":[[postBody["t"], postBody["v"]]],"tags":{"type":"raw"}}]
                            print (postbody)
                            client.publish(topicForwarded, json.dumps(postbody))
                        else:
                            print("appending tag",tag)
                            remainingTags.append(tag)
                    except Exception as e:
                        # tr()
                        # print("exception error--", e)
                        print("appending tag",tag)
                        remainingTags.append(tag)

            print("len of faulty tags", len(remainingTags))
            self.postDataDefaultTags(remainingTags,numTag,iniTL,currentTimeStamp,client)

                
        except:

            tr()


        
            
    def mainFuncDataMigration(self,count,file_path="",deleteData=False,monthNum=1,onlyRaw = True): 
        try:
            
            tagmetaBody = []
            tagmetaBody = self.getTagmeta(self.unitsId)

            formBody = self.getForms(self.unitsId)
            formBody = self.createBodyForForms(formBody)
            tagmetaBody += formBody

            if not onlyRaw:
                tagmetaBody = []
                tagmetaBody1 = self.getDeviationsTags(self.unitsId)
                tagmetaBody += self.createBodyForDevs(tagmetaBody1)
            
            lennn = (len(tagmetaBody))
            tagmetaBody = tagmetaBody[count:]
            
            # return
            if monthNum == 1:
                st = 1663230600000
                et = 1694769170000
            else:
                et = time.time() * 1000 - 1*1000*60*60*24*30*monthNum
                st = et - 1*1000*60*60*24*30 
                
            et = time.time() * 1000
            st = et - 1*1000*60*60*24*365*5
            
            
            
            for tag in tagmetaBody:
                try:
                    dataTagId = tag["dataTagId"]
                except:
                    dataTagId = tag
                    
                print("*"*30,str(self.unitsId),str(dataTagId),str(count),"*"*30)
                print("remaining tags:" , str(lennn-count),"Running month:", str(monthNum))

                try:
                    dfProd = self.getValuesProd([dataTagId],st,et,False)
                except:
                    dfProd = self.getValuesProd([dataTagId],st,et,False)
                
                # self.queueSize("kairosdb.queue.file_queue.size",1000000)
                # self.queueSize("kairosdb.http.ingest_count",9000000)
                
                
                if deleteData:
                    self.deleteKairos([dataTagId],st,et)

                print(dfProd)
                self.postOnKairosV2(dfProd)
                
                count += 1
                try:
                    with open(file_path, "r") as json_file:
                        data = json.load(json_file)
                        
                    data[self.unitsId] = count
                    # Open the file in write mode and save the data as JSON
                    with open(file_path, "w") as json_file:
                        json.dump(data, json_file)
                except:
                    pass
                
        except:
            tr()
            
    