#!/usr/bin/python

import openpyxl
import csv
import sys

wb = openpyxl.load_workbook(filename=sys.argv[1])

sheets = wb.get_sheet_names()

ws =wb.get_sheet_by_name('Med Admin for Adverse Visits')
data = {}
phenodata = {}
for r in ws.iter_rows():
    ptId = r[0].value
    oneMonth = r[2].value
    medID =  r[7].value
    medName = r[8].value
    if not data.has_key(ptId):
        data[ptId] = {}
    if not data[ptId].has_key(medID):
        data[ptId][medID]={'Name':medName,'count':0,'oneMonth':oneMonth}
    data[ptId][medID]['count'] += 1

ws = wb.get_sheet_by_name('Patient Visits')
#go through and get pt id and total up the ammount spent (I) and LOS (E)
for r in ws.iter_rows():
    if not phenodata.has_key(r[0].value):
        phenodata[r[0].value] = {}
    phenodata[r[0].value]['Total_Charges'] = r[8].value
    phenodata[r[0].value]['LOS'] = r[4].value

ws = wb.get_sheet_by_name('DX')
# go through and associate ptid with DX_NAME(D) and E and F and G
for r in ws.iter_rows():
    if not phenodata.has_key(r[0].value):
        phenodata[r[0].value] = {}
    phenodata[r[0].value]['DX_Name'] = r[3].value
    phenodata[r[0].value]['Adverse_ICD9'] = r[6].value

ws = wb.get_sheet_by_name('All Pt Reported Medications')

# go through and create a matrix of drugs 
# go through (E) and get all drugs, then go through and for each pt list the drugs they are taking
drug_list = []
for r in ws.iter_rows():
    drug_list.append(r[4].value)
drug_list = list(set(drug_list))
drug_matrix = {"ID":drug_list}
for r in ws.iter_rows():
    if not drug_matrix.has_key(r[0].value):
        drug_matrix[r[0].value] = [0]*len(drug_list)
    index_pos = drug_list.index(r[4].value)
    try:
        drug_matrix[r[0].value][index_pos] = 1
    except:
        print r[0].value
        pass
for x in drug_matrix:
    print drug_matrix[x]

print phenodata
sys.exit()
    
newWb = openpyxl.Workbook()
#write header for new sheet
header = ('PtID','Medication ID','Medication','Medication Count')
ws = newWb.create_sheet()
ws.title = 'Collapsed Med Adverse Visits'
for idx,value in enumerate (header):
    ws.cell(row=1, column=idx+1).value = value
row_num = 2 #need  offset
for id in data:
    for medId in data[id]:
        newdata = (id,medId,data[id][medId]['Name'],data[id][medId]['count'])
        for idx, value in enumerate(newdata):
            ws.cell(row = (row_num), column = idx+1).value = value
        row_num += 1

for idx,val in enumerate(sheets):
    if not val == 'Med Admin for Adverse Visits':
        ws = newWb.create_sheet()
        ws.title = val
        oldws = wb.get_sheet_by_name(val)
        for row_num in range(oldws.min_row, oldws.max_row):
            if row_num >= 100:
                break
            for col_num in range (oldws.min_column, oldws.max_column):
                ws.cell(row = row_num, column = col_num).value = oldws.cell(row = row_num, column = col_num).value

newWb.save("test2.xlsx")
