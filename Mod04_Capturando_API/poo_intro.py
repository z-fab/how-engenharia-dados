#%% Imports
import datetime
import math

#%% Classe Pessoa
class Pessoa:
    
    def __init__(self, nome: str, sobrenome: str, nasc: datetime.date):
        self.nome = nome
        self.sobrenome = sobrenome
        self.nasc = nasc
    
    @property    
    def idade(self) -> int:
        return math.floor((datetime.date.today() - self.nasc).days / 365.2425)  
    
    def __str__(self) -> str:
        return f'{self.nome} {self.sobrenome}, {self.idade} anos'        
        

#%% Instanciando um objeto  
fab = Pessoa('Fabricio', 'Zillig', datetime.date(1993, 1, 19))
print(fab)
print(fab.nome)
print(fab.sobrenome)
print(fab.idade)
# %%
