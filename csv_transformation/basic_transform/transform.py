from __future__ import unicode_literals, absolute_import, print_function
from pathlib import Path
import csv
import json, os
import frappe
import sys
import traceback
from .dataMapper import DataMapper
from frappe.commands import pass_context, get_site
from frappe.core.doctype.data_export.exporter import export_data
from frappe.utils.csvutils import read_csv_content

def transformFile(**kwargs) :
    from frappe.utils.csvutils import read_csv_content
    dataMapper=DataMapper()
    try:
        if isValidDataPassed(kwargs):
            jsonData=getJsonMap(kwargs['dataType'])
            print("Initiating transformation...")
            for key in jsonData:
                templateRows=getTemplate(key.title())
                mainFileData=getMainData("/"+kwargs['filePath'])
                print("Transformation started for",key,".Please wait...")
                if checkIfJsonArray(jsonData[key]):
                    for key1 in jsonData[key]:
                        mainFileData=getMainData("/"+kwargs['filePath'])
                        mappedData=dataMapper.getMappedData(templateRows,mainFileData,jsonData[key][key1])
                        saveTemplateWithData(key,mappedData)
                    print("Transformation completed for ",key)
                    print("Successfully created the file at ",Path(__file__).parent / ("output/"+str(key)+".csv"))
                else:
                    mappedData=dataMapper.getMappedData(templateRows,mainFileData,jsonData[key])
                    saveTemplateWithData(key,mappedData)
                    print("Transformation completed for ",key)
                    print("Successfully created the file at ",Path(__file__).parent / ("output/"+str(key)+".csv"))
    except Exception as error:
        print('Caught this error: ' + repr(error))
        traceback.print_exc()

def isValidDataPassed(kwargs):
    try:
        if(not kwargs['filePath'] or not kwargs['dataType']):
            print("You have entered some empty value with the argument. Do make sure you pass a valid value to be processed.")
        isValidPath("/"+kwargs['filePath'])
    except Exception as error:
        print('Caught this error: ' + repr(error))
        return False
    except:
        print('''Ooops...! You must have missed to pass some arguments essential for the transformation. 
        Please make sure you pass the arguments in given format below - 
        {'filePath' :'<your main csv file path>','dataType':'<type of data you want to transform>'} ''')
        return False
    return True



def isValidPath(filePath):
    try:
        if not(os.path.exists(filePath)):
            raise FileNotFoundError("The specified path",filePath,"doesn't exist. Please provide a valid path.")
    except FileNotFoundError as error:
        raise Exception(error)
    except Exception:
        print("There seems to be a problem with the file path (" +filePath+ ") you've sent. Please review it and try again.")
        raise Exception("Oops!",sys.exc_info()[0],"occured.")
    return True




def getJsonMap(jsonFileName):
    jsonMapPath=Path(__file__).parent / ("json_maps/"+str(jsonFileName)+".json")
    with open(str(jsonMapPath),'r') as jsonfile:
        jsonData = json.load(jsonfile)
    return jsonData


def getTemplate(doctypeName):
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

def columnExist(columnList,columnName):
    pass






    



	