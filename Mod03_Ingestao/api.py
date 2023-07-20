#%% Imports
import random
import requests
import json
import backoff
import logging

#%%
log = logging.getLogger()
log.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(asctime)s  (%(name)s) :: %(levelname)s - %(message)s'
)
ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.addHandler(ch)


# %%
@backoff.on_exception(
    backoff.expo,
    (ConnectionAbortedError, ConnectionRefusedError, TimeoutError), 
    max_tries=5)
def teste_func(*args, **kwargs):
    rnd = random.random()
    log.debug(f"RND: {rnd}")
    log.info(f"ARGS: {args if args else 'Sem Args'}")
    log.info(f"KWARGS: {kwargs if kwargs else 'Sem Kwargs'}")

    if rnd < .2:
        log.error('Conexão foi Finalizada')
        raise ConnectionAbortedError('Conexão foi Finalizada')
    elif rnd < .4:
        log.error('Conexão foi Recusada')
        raise ConnectionRefusedError('Conexão foi Recusada')
    elif rnd < .6:
        log.error('Tempo de Espera Excedido')
        raise TimeoutError('Tempo de Espera Excedido')
    
    return "Ok!"
    
#%%

teste_func(100, 200, arg1 = 'argumento1', lista = [1,2,3])
# %%
