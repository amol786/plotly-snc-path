import pandas as pd
import csv

databaseloc = r'E:\GitHub\project\snc_path_data.csv'
read = csv.reader(databaseloc)
#read.__next__()
#print(read.__next__())
columnNames = ['Date Time','IP', 'Source Node','City','Node Location','SNC-ID','Node','Path','Destination Node']
df = pd.read_csv(databaseloc,names = columnNames ,sep=',',index_col=False)
#df = pd.read_csv(databaseloc,sep=',')
df = pd.DataFrame(df)
#print(df)
df.dropna(inplace=True)
df =df.reindex(columns=['Date Time','SNC-ID','Source Node','Destination Node','Path','City','Node','Node Location','IP'])
print(df)
