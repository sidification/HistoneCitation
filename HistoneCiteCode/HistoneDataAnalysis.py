import pandas as pd
from itertools import combinations
import csv
import sys

#reading the citing - cited csv
df1 = pd.read_csv('/Users/sidahuja/Dev/HistoneCitation/HistoneCiteCode/pubmed-oc-data.csv')

#because NaN is a float value, replace it with '' so group by method works for grouping cited papers by citation
df2 = df1.fillna('')

#combine the cited papers corresponding to every citation, and return the resulting as a dataframe.
#apply(list) is used to convert the output of each 'groupby' to list. the output is of the object type 'GroupBy' which works similar
#to a pandas series
df3 = df2.groupby(['doi'])['cited'].apply(list)

#convert df3 from 'series' type to dataframe by using reset_index()
df4 = df3.reset_index()
#print(df4)
#print('')

#initiate an empty dictionary. This dictionary will store the (key, value) pairs for which 'key' will co-citation pairs, and 'value' will
#be the co-citation frequency of the corresponding pair.
cited_dict = {}

#iterate through values of the cited column. each value is a list of cited papers for a particular citation. Ignore empty lists
for values in df4['cited']:
    if values != ['']:
        #print(values)
        #print('')
        #for all non-null values
        #print('the combinations are:')

        #elements will be each tuple containing a pair of co-cited papers. sort the tuple so it will always be in the same order.
        #that way, tuple(A, B) is same as tuple(B, A)
        for elements in list(combinations(values, 2)):                   
            elements = tuple(sorted(elements))
            #print(elements)
            if elements in cited_dict:
                cited_dict[elements] += 1
            else:
                cited_dict[elements] = 1
        #print('***************')
'''
#write the dictionary to csv
with open('cocited-freq-table.csv', 'w') as f:
    writerObj = csv.writer(f)
    writerObj.writerow(['co-citation pairs', 'freq'])
    writerObj.writerows(cited_dict.items())
'''

#write the dictionary to a pandas dataframe
co_cited_df = pd.DataFrame(cited_dict.items(), columns=['co-cited pairs', 'freq'])

#sort values of the data-frame by freq
co_cited_df.sort_values(by=['freq'], inplace=True, ascending=False)

print(co_cited_df.groupby(['freq'], as_index=False)['co-cited pairs'].count())
