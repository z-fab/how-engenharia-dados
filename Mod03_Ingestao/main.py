#%% Imports
import requests
import json

# %%
def conversaoDolar(valor: float = 1) -> float:

    url = 'https://economia.awesomeapi.com.br/last/USD-BRL'
    ret = requests.get(url)
    
    if ret:
        dolar = json.loads(ret.text)['USDBRL']
        return round(float(dolar['bid'])*valor,2)

    return -1

def error_check(func):
    def inner_func(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print(f'Função {func.__name__} Falhou: {e}')
    return inner_func

@error_check
def cotacao(valor: float = 1, moeda: str | list[str] = 'USD-BRL') -> float:

    if type(moeda) == str:
        moeda = [moeda]
        
    for m in moeda:
        url = f'https://economia.awesomeapi.com.br/last/{m}'
        ret = requests.get(url)
        
        result = json.loads(ret.text)[m.replace('-','')]
        print(f"{m[:3]} {valor:.2f}  = {m[-3:]} {float(result['bid']):.2f}")

# %%
try:
    cotacao(moeda = 'JPY-BRL')
except Exception as e:
    print(f'Erro: {e}')
else:
    print('Sucesso')
    
# %%

lst_moeda = [
    'USD-BRL',
    'EUR-BRL',
    'BTC-BRL',
    'JPY-BRL',
    'GBP-BRL',
    'ARS-BRL',
    'CHF-BRL',
    'RPL-BRL'
]

cotacao(moeda = lst_moeda)

