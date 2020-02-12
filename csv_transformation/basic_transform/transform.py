from __future__ import unicode_literals, absolute_import, print_function
from pathlib import Path
import csv
import json, os
import frappe
from frappe.commands import pass_context, get_site
from frappe.core.doctype.data_export.exporter import export_data
from frappe.utils.csvutils import read_csv_content

def transformFile(masterFilePath=None) :
    from frappe.utils.csvutils import read_csv_content
    prepareColumnAndGetData('Item')
    if isValidPath("/"+masterFilePath):
        jsonData=getJsonMap()
        print("Initiating transformation...")
        for key in jsonData:
            templateRows=getTemplate(key.title())
            mainFileData=getMainData("/"+masterFilePath)
            print("Transformation started for",key,".Please wait...")
            if checkIfJsonArray(jsonData[key]):
                for key1 in jsonData[key]:
                    mainFileData=getMainData("/"+masterFilePath)
                    mappedData=getMappedData(templateRows,mainFileData,jsonData[key][key1])
                    saveTemplateWithData(key,mappedData)
                print("Transformation completed for ",key)
                print("Successfully created the file at ",Path(__file__).parent / ("output/"+str(key)+".csv"))
            else:
                mappedData=getMappedData(templateRows,mainFileData,jsonData[key])
                saveTemplateWithData(key,mappedData)
                print("Successfully created the file at ",Path(__file__).parent / ("output/"+str(key)+".csv"))


def isValidPath(*args):
    try:
        for arg in args:
            if not(os.path.exists(arg)):
                print("The specified path",arg,"doesn't exist. Please provide a valid path.")
                return False
    except:
        return False
    return True


def getMappedData(templateContent,mainContent,jsonMap):
    templateColumn=templateContent[15]
    dataColumn=mainContent.pop(0)
    listArray=[]
    itemGroupList=set()
    itemCodeList=set()
    append=True
    for value in mainContent:
        itemGroupList.add(value[dataColumn.index('Type')])
    for index,val in enumerate(mainContent):
        append=True
        listArray=[]
        for i in templateColumn:
            listArray.append(None)
        for jsonData in jsonMap:
            try:
                if(not (val[dataColumn.index(jsonData["source"])] and val[dataColumn.index(jsonData["source"])].strip())):
                    listArray[templateColumn.index(jsonData["destination"])]=jsonData["default"]
                else:
                    itemCode=val[dataColumn.index('Product')]
                    if not(itemCode in itemGroupList):
                        listArray[templateColumn.index(jsonData["destination"])]=val[dataColumn.index(jsonData["source"])] 
                    else:
                        if jsonData["source"] == 'Product':
                            print(val[dataColumn.index(jsonData["source"])]+str(index))
                            listArray[templateColumn.index(jsonData["destination"])]=val[dataColumn.index(jsonData["source"])]+str(index)
                        else:
                            listArray[templateColumn.index(jsonData["destination"])]=val[dataColumn.index(jsonData["source"])]
            except ValueError:
                try:
                    listArray[templateColumn.index(jsonData["destination"])]=jsonData["default"]
                except KeyError:
                    print(val[dataColumn.index(jsonData["source"])])
        if append:
            templateContent.append(listArray)
    return templateContent


def getJsonMap():
    jsonMapPath = Path(__file__).parent / "json_maps/item-data.json"
    with open(str(jsonMapPath),'r') as jsonfile:
        jsonData = json.load(jsonfile)
    return jsonData


def getTemplate(doctypeName):
    # downloadTemplate(doctypeName)
    # templatePath=Path(__file__).parent / ("data/"+str(doctypeName)+".csv")
    # with open(str(templatePath),'r') as tempcsvfile:
    #     templateContent=read_csv_content(tempcsvfile.read())
    return read_csv_content(prepareColumnAndGetData(doctypeName))


def getMainData(fileLocation):
    with open(str(fileLocation),'r') as csvFile:
        fileContent=read_csv_content(csvFile.read())
    return fileContent


def saveTemplateWithData(fileName,mappedData):
    with open(str(Path(__file__).parent / ("output/"+str(fileName)+".csv")), 'w', newline='') as file:
            writer = csv.writer(file,quoting=csv.QUOTE_ALL)
            writer.writerows(mappedData)


def checkIfJsonArray(jsonData):
    for key in jsonData:
        try:
            for val in jsonData[key]:
                return True
        except TypeError:
            return False

def downloadTemplate(doctypeName):
    response=prepareColumnAndGetData(doctypeName)
    templatePath=Path(__file__).parent / ("data/"+str(doctypeName)+".csv")
    with open('itemTemplate.csv','wb') as csvFile:
        csvFile.write(response)


def prepareColumnAndGetData(doctypeName):
    print(doctypeName)
    ignoreArray=['Section Break','Column Break','Table','Button']
    columnArray1=[ val.fieldtype for val in frappe.get_meta(doctypeName).fields if val.fieldname=='set_meta_tags']
    columnArray=[ val.fieldname for val in frappe.get_meta(doctypeName).fields if not val.fieldtype in ignoreArray and not val.hidden==1]
    filteredColumn=[val for val in filter(None,columnArray)]
    dictValueWithColumnData={}
    dictValueWithColumnData[doctypeName]=filteredColumn
    for val in frappe.get_meta(doctypeName).get_table_fields():
        columnArray=[val.fieldname for val in frappe.get_meta(val.options).fields if not val.fieldtype in ignoreArray and not val.hidden==1]
        filteredColumn=[val for val in filter(None,columnArray)]
        dictValueWithColumnData[val.options]=filteredColumn
    export_data(doctypeName, doctypeName, True, False,json.dumps(dictValueWithColumnData),'CSV', True)
    return frappe.response['result']






    



	