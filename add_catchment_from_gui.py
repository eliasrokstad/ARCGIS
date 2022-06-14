import arcpy
import os
import pandas as pd


task = 'ADD TASK NAME'
output = 'ADD OUTPUT FILE NAME'
path = r'ADD PATH TO FILE DIR'
catchments = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]

merge_files = [os.path.join(path, catchment, 'dataset.shp') for catchment in catchments]
arcpy.management.Merge(merge_files, output)

extand = ['Name', 'Fs', 'Fc', 'Fu', 'T', 'Tc', 'I', 'C', 'Q']
ws = arcpy.env.workspace
for ex in extand:
    if ex == 'Name':
        arcpy.management.AddField(output, ex, 'Text')
    else:
        arcpy.management.AddField(output, ex, 'Double')

arcpy.management.AddField(output, 'nsluk', 'Double')
arcpy.management.AddField(output, 'png', 'Text')

with arcpy.da.Editor(ws) as edit:
    with arcpy.da.UpdateCursor(output, extand) as cursor:
        n = 0
        for row in cursor:
            for file in os.listdir(os.path.join(path, catchments[n])):
                if '.xlsx' in file:
                    data = pd.read_excel(os.path.join(path, catchments[n], file))
            for i, ex in enumerate(extand):
                row[i] = data.loc[data['Entry'] == ex, 'Value'].tolist()[0]
            cursor.updateRow(row)
            n += 1

    with arcpy.da.UpdateCursor(output, ['Q', 'nsluk', 'png']) as cursor:
        n = 0
        for row in cursor:
            row[1] = row[0] / 20
            for file in os.listdir(os.path.join(path, catchments[n])):
                if '.png' in file:
                    temp = os.path.join(path, catchments[n], file)
                    temp = temp.replace('\\', '/')
                    row[2] = temp

            cursor.updateRow(row)
            n += 1