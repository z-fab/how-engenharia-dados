#%%
from selenium import webdriver
import re
import argparse

#%%

def regex_type(arg_value, pat=re.compile(r"^[0-9]{8}$")):
    if not pat.match(arg_value):
        raise argparse.ArgumentTypeError("Formato de CEP inválido")
    return arg_value

parser = argparse.ArgumentParser(description='Get CEP')
parser.add_argument("--cep", "-c", help='CEP (sem hifem ou espaço)', default='', type=regex_type)

args = parser.parse_args()


# %%
driver = webdriver.Chrome()

#%% Acesso ao site da How
#driver.get('http://www.howedu.com.br')
#driver.find_element('xpath', '/html/body/div[3]/div/div[2]/button[2]').click()
#driver.find_element('xpath', '//*[@id="menu-1-739815d"]/li[2]/a').click()

# %% Buscando CEP no site dos Correios
driver.get('https://buscacepinter.correios.com.br/app/endereco/index.php?t')

elem_cep = driver.find_element('name', 'endereco')
elem_tipo = driver.find_element('name', 'tipoCEP')
# %%
elem_cep.clear()
elem_cep.send_keys(args.cep)

elem_tipo.click()
option_tipo = driver.find_element('xpath', '//*[@id="tipoCEP"]/optgroup/option[1]')
option_tipo.click()

btn_buscar = driver.find_element('id', 'btn_pesquisar')
btn_buscar.click()
# %%
logradouro = driver.find_element('xpath', '//*[@id="resultado-DNEC"]/tbody/tr/td[1]')
logradouro = logradouro.text.split(' - ')[0]

bairro = driver.find_element('xpath', '//*[@id="resultado-DNEC"]/tbody/tr/td[2]')
bairro = bairro.text

localidade = driver.find_element('xpath', '//*[@id="resultado-DNEC"]/tbody/tr/td[3]')
localidade = localidade.text

driver.close()
# %%
print(f"""
      Para o CEP: {args.cep}:
      
      Logradouro: {logradouro} 
      Bairro: {bairro} 
      Localidade: {localidade}
      """)
# %%
