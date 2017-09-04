#Credit to Alexandria Ongjoco, Hannes Holste (Knight Lab), Mitchell Flagg (Ideker Lab) and Niema Moshiri (PhD student) for a bunch of input.
#Only works with CSV file 'sample-test-sheet.csv' in the folder (analyte file)

import pandas as pd     #pandas will be used to read CSV
import urllib2
from urllib2 import HTTPError

URL_TEMPLATE = ('https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/{}'
                '/property/{}/CSV')
PROPERTIES = ['MolecularFormula', 'MolecularWeight', 'CanonicalSMILES', 'IsomericSMILES', 'InChI', 'InChIKey', 'IUPACName', 'XLogP', 'ExactMass', 'MonoisotopicMass', 'TPSA', 'Complexity', 'Charge', 'Synonyms']
OUTPUT_FILENAME = 'pubchem-output.csv'
INPUT_FILENAME = 'sample-test-sheet.csv'
OUTPUT_COLUMNS =  ['Reference_Column'] + ['SMILES'] + PROPERTIES
#synonyms https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/CCCC/synonyms/XML   added synonyms to PROPERTIES

df = pd.read_csv(INPUT_FILENAME)
print 'Trying to download %d total files...' % len(df)

df_results = pd.DataFrame()
count_failed = 0
for i in range(len(df)):
    print "I'm done with this scan ... Progress"   #added attempt to this progress bar | counter/len(df)'\n' | tried incrementing a variabble before and after loop
    row = df.iloc[i]
    smiles_value = row['SMILES']

    # join properties array into one comma separated string
    request_properties = ','.join(PROPERTIES)

    # make API request and read response
    #response = urllib2.urlopen().read()
    '''
    example response:
    "CID","MolecularFormula","MolecularWeight","InChIKey"\n
    10697,"C8H10O2",138.166000,"RCNCKKACINZDOI-UHFFFAOYSA-N"
    '''
    url = URL_TEMPLATE.format(smiles_value, request_properties)
    try:
        df_api = pd.read_csv(url)
    except HTTPError as err:
        print 'Request to {} failed. Skipping. ({})'.format(url, err)
        count_failed += 1
        continue # skip remaining code in loop

    # insert SMILES identifier so we can merge dataframes later
    df_api.insert(0, 'SMILES', smiles_value)

    # append to results dataframe
    df_results = df_results.append(df_api)
print '\n{}/{} successful requests.'.format(len(df) - count_failed, len(df))

# Merge results with original dataframe
df_final = df_results.merge(df, on='SMILES')

if OUTPUT_COLUMNS is not None and len(OUTPUT_COLUMNS) != 0:
    df_final[OUTPUT_COLUMNS].to_csv(OUTPUT_FILENAME)
else:
    df_final.to_csv(OUTPUT_FILENAME)
