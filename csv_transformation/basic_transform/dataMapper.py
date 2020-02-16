import sys

class DataMapper:
    def getMappedData(self,templateContent,mainContent,jsonMap):
        templateColumn=templateContent[15]
        dataColumn=mainContent.pop(0)
        listArray=[]
        itemGroupList=set()
        itemCodeList=set()
        for value in mainContent:
            itemGroupList.add(value[dataColumn.index('Type')])
        for index,val in enumerate(mainContent):
            listArray=[]
            for i in templateColumn:
                listArray.append(None)
            for jsonData in jsonMap:
                try:
                    #If column doesn't exist this condition will throw Value error
                    if(not val[dataColumn.index(jsonData["source"])]):
                        listArray[templateColumn.index(jsonData["destination"])]=jsonData["default"]   
                    else:
                        listArray[templateColumn.index(jsonData["destination"])]=val[dataColumn.index(jsonData["source"])]
                except ValueError:
                    try:
                        if ":" in jsonData["source"]:
                            funcName=str(jsonData["source"].split(':')[1]).split('(')[0]
                            params=str(jsonData["source"].split(':')[1]).split('(')[1]
                            concatVal=getattr(self,funcName)(dataColumn,jsonData,val,params)
                            listArray[templateColumn.index(jsonData["destination"])]=concatVal
                        else:
                            listArray[templateColumn.index(jsonData["destination"])]=jsonData["default"]
                    except ValueError:
                        raise ValueError("Unable to find Column Name ["+jsonData["destination"]+"] in the template. The columns in the template are - ",templateColumn)
                except KeyError:
                    raise KeyError(sys.exc_info()[0],"Unable to map the data for the column ["+jsonData["source"]+"] .Please ensure if default value is needed in the json map.")
                except:
                    raise Exception("Oops!",sys.exc_info()[0],"occured.")
            templateContent.append(listArray)
        return templateContent

    def concat(self,dataColumn,jsonData,masterVal,params):
        concatenatedValue=''
        for val in params.replace(')','').split(','):
            concatenatedValue=concatenatedValue+' '+masterVal[dataColumn.index(val)]
        return concatenatedValue