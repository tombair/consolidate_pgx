#!/usr/bin/python

import openpyxl
import csv
import sys

wb = openpyxl.load_workbook(filename=sys.argv[1])

sheets = wb.get_sheet_names()

ws =wb.get_sheet_by_name('Med Admin for Adverse Visits')
data = {}
phenodata = {}
adverse_meds = {}
all_meds = {}


allmedsdl = []
for r in ws.iter_rows():
    allmedsdl.append(r[8].value)
allmedsdl = list(set(allmedsdl))
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
    if not adverse_meds.has_key(r[0].value):
        adverse_meds[r[0].value] = [0]*len(allmedsdl)
    index_pos = allmedsdl.index(r[8].value)
    adverse_meds[r[0].value][index_pos] = 1

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


#get a master list of meds
drug_list = []
ws = wb.get_sheet_by_name('All Rx Medications')
for r in ws.iter_rows():
    drug_list.append(r[4].value)
ws = wb.get_sheet_by_name('All Pt Reported  Medications')
for r in ws.iter_rows():
    drug_list.append(r[4].value)
drug_list = list(set(drug_list))
drug_matrix = {"ID":drug_list}

ws = wb.get_sheet_by_name('All Rx Medications')
for r in ws.iter_rows():
    if not drug_matrix.has_key(r[0].value):
        drug_matrix[r[0].value] = [0]*len(drug_list)
    index_pos = drug_list.index(r[4].value)
    drug_matrix[r[0].value][index_pos] = 1
ws = wb.get_sheet_by_name('All Pt Reported  Medications')
for r in ws.iter_rows():
    if not drug_matrix.has_key(r[0].value):
        drug_matrix[r[0].value] = [0]*len(drug_list)
    index_pos = drug_list.index(r[4].value)
    drug_matrix[r[0].value][index_pos] = 1


header = ("Total_Charges","LOS","DX_Name","Adverse_ICD9")
allheader = header + adverse_meds['ID']
print ",".join(allheader)
for x in adverse_meds:
    if not x == 'ID':
        prefix = []
        for h in header:
            prefix.append(phenodata[h])
        print ",".join(prefix+adverse_meds[x])

        
    

    
