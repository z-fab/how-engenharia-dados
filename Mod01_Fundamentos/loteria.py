#%%
import requests
import pandas as pd
import numpy as np
import collections
import urllib3
import argparse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#%%
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument("--url", "-u", help='URL para coleta dos dados da LotoFácil', default='https://servicebus2.caixa.gov.br/portaldeloterias/api/resultados?modalidade=Lotofácil')
args = parser.parse_args()

url = args.url

#Request
print(f'Buscando dados...', end='')
r = requests.get(url, verify=False)
r_text = r.text.replace('\\r\\n', '')
r_text = r_text.replace('"\r\n}', '')
r_text = r_text.replace('{\r\n  "html": "', '')
print('OK')

#%% Create df and lean data
df_raw = pd.read_html(r_text)
df = df_raw[0].copy()
df = df[df['Bola1'].notna()]

nr_pop = list(range(1, 26))
nr_pares = list(range(2, 26, 2))
nr_impares = list(range(1, 26, 2))
nr_primos = [2, 3, 5, 7, 11, 13, 17, 19, 23]

#%%
print('Calculando valores... ', end='')
comb = []
vn = [0] * 25
colunas = ['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6', 'Bola7', 'Bola8', 'Bola9', 'Bola10', 'Bola11', 'Bola12', 'Bola13', 'Bola14', 'Bola15']

for index, row in df.iterrows():
    vpares = 0
    vimpar = 0
    vprimo = 0
    for campo in colunas:
        if row[campo] in nr_pares:
            vpares += 1
        if row[campo] in nr_impares:
            vimpar += 1
        if row[campo] in nr_primos:
            vprimo += 1
        vn[int(row[campo])-1] += 1
    comb.append(str(vpares)+'p-'+str(vimpar)+'i-'+str(vprimo)+'np')

# %%
freq_nr = list(zip(list(range(1, 26)), vn))
freq_nr.sort(key=lambda x: x[1], reverse=True)
freq_nr
# %%
counter = collections.Counter(comb)
df_freq_comb = pd.DataFrame(counter.items(), columns=['Combinacao', 'Frequencia'])
df_freq_comb['p'] = df_freq_comb['Frequencia']/df_freq_comb['Frequencia'].sum()
df_freq_comb.sort_values(by=['Frequencia'], inplace=True, ascending=False)
print('OK', end='\n\n')
# %%
print(  
f'''
O número que mais saiu foi o {freq_nr[0][0]} com {freq_nr[0][1]} ocorrências.
O número que menos saiu foi o {freq_nr[-1][0]} com {freq_nr[-1][1]} ocorrências.
A combinação que mais saiu foi {df_freq_comb['Combinacao'].values[1]} com a frequencia de {round(df_freq_comb['p'].values[1]*100,2):.2f}%.
'''
)

# %%
