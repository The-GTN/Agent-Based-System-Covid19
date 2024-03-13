import pandas as pd

def collecte_donnees(granularite='national'):

     data_brute = pd.read_csv('chiffres-cles.csv')
     dates = pd.read_csv('dates.csv')
     
     # National
     if granularite == "national":
         data_brute = data_brute.loc[data_brute['source_type'] ==
"ministere-sante"]
         data_brute = data_brute.loc[data_brute['granularite'] ==
"pays"].reset_index()
         data_brute = data_brute[['date','cas_confirmes', 'deces',
                                  'deces_ehpad', 'reanimation', 'hospitalises', 'gueris']]
         data_brute = dates.set_index('date').join(data_brute.set_index('date'))
         data = data_brute.interpolate(limit_area='inside')
         data = data.dropna(how='all')
         data['reanimation'][0:3] = 0
         data['gueris'][0:3] = 0

     # Regional
     if granularite == "regional":
         data_brute = data_brute.loc[data_brute['source_type'] ==
"opencovid19-fr"]
         data_brute = data_brute.loc[data_brute['maille_code'] ==
"REG-32"].reset_index()
         data_brute = data_brute[['date','cas_confirmes', 'deces',
'deces_ehpad', 'reanimation', 'hospitalises', 'gueris']]
         data_brute = dates.set_index('date').join(data_brute.set_index('date'))
         data = data_brute.interpolate(limit_area='inside')
         data = data.dropna(how='all')
         data = data.loc['2020-03-18':]

     # Departemental
     if granularite == "departemental":
         import glob
         data_brute = pd.read_csv(glob.glob('donnees-hospitalieres-covid19-*')[-1], sep=";")
         data_brute = data_brute.loc[data_brute['dep'] == "59"]
         data_brute[data_brute['sexe']==0].groupby(['jour']).sum()
         data = data.drop(columns=['sexe'])

     return data
