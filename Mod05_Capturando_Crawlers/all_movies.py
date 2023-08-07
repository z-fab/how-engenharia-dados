#%%
import time
from selenium import webdriver
import argparse
import pandas as pd

def tem_item(xpath, driver:webdriver):
    try:
        return driver.find_element('xpath', xpath)
    except:
        return False

driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get('https://pt.wikipedia.org/wiki/Nicolas_Cage')

#%%
while not tem_item('//*[@id="mw-content-text"]/div[1]/table[2]', driver):
    time.sleep(1)
    pass

# %%
tabela_filmes = driver.find_element('xpath', '//*[@id="mw-content-text"]/div[1]/table[2]')
tabela_filmes = tabela_filmes.get_attribute('outerHTML')
driver.close()
# %%
df = pd.read_html(tabela_filmes)[0]
# %%
df.head()
# %%
df.to_csv('filmes_nicolas_cage.csv', index=False)
# %%
