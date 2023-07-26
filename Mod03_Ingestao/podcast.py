#%%
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

# %%
url = 'https://piaui.folha.uol.com.br/radio-piaui/foro-de-teresina/'
ret = requests.get(url)
# %%
ret.text
# %%

soup = bs(ret.text, 'html.parser')

# %%
lst_podcast = soup.find_all('div', class_='radio-content')

for item in lst_podcast:
    try:
        print(f"EP: {item.a.text} LINK: {item.a['href']}")
    except:
        pass
# %%
df = pd.DataFrame(columns=['nome', 'link'])
for item in lst_podcast:
    try:
        df.loc[len(df)] = [item.a.text, item.a['href']]
    except:
        pass
# %%
df.sample(10)
# %%
