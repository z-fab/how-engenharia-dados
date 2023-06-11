#%% Imports
import datetime
import math

#%%
class Vivente:
    
    def __init__(self, nome: str, sobrenome: str, nasc: datetime.date) -> None:
        self.nome = nome
        self.sobrenome = sobrenome
        self.nasc = nasc
    
    @property    
    def idade(self) -> int:
        return math.floor((datetime.date.today() - self.nasc).days / 365.2425)
    
    def emite_ruido(self, ruido: str) -> None:
        print(f'{self.nome} {self.sobrenome} fez ruido: {ruido}')

#%% Classe Pessoa
class Pessoa(Vivente):
    
    def __str__(self) -> str:
        return f'{self.nome} {self.sobrenome}, {self.idade} anos'
    
    def fala(self, frase: str) -> None:
        return self.emite_ruido(frase)

#%%
class Cachorro(Vivente):
    
    def __init__(self, nome: str, sobrenome: str, nasc: datetime.date, raca: str) -> None:
        super().__init__(nome, sobrenome, nasc)
        self.raca = raca
    
    def __str__(self) -> str:
        return f'{self.nome} {self.sobrenome} é da raça {self.raca} e tem {self.idade} anos'
    
    def late(self) -> None:
        return self.emite_ruido("Au! Au!")

    
# %%
class Curriculo:
    
    def __init__(self, pessoa: Pessoa, experiencias: list[str]) -> None:
        self.pessoa = pessoa
        self.experiencias = experiencias
        
    @property
    def quantidade_experiencias(self) -> int:
        return len(self.experiencias)
        
    @property
    def empresa_atual(self) -> str:
        return self.experiencias[-1]
    
    def adiciona_experiencia(self, experiencia: str) -> None:
        self.experiencias.append(experiencia)
    
    def __str__(self) -> str:
        return f'{self.pessoa.nome} {self.pessoa.sobrenome} tem {self.pessoa.idade} anos e já ' \
                f'trabalhou em {self.quantidade_experiencias} empresas. Atualmente trabalha ' \
                f'na {self.empresa_atual}'
    

# %%
fab = Pessoa('Fabricio', 'Zillig', datetime.date(1993, 1, 19))
print(fab)

curriculo_fab = Curriculo(
    pessoa=fab, 
    experiencias=['Empresa A', 'Empresa B', 'Empresa C', 'Empresa D']
)

print(curriculo_fab)

# %%
curriculo_fab.adiciona_experiencia('Empresa E')
print(curriculo_fab)
# %%
doguinho = Cachorro(nome="Doguinho", sobrenome="Zillig", nasc=datetime.date(2019, 4, 15), raca="Vira-lata")
print(doguinho)

# %%
fab.fala("Olá, mundo!")
doguinho.late()
# %%
