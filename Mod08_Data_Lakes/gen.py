#%%
import pandas as pd
import faker as fk

#%%
fake = fk.Faker('PT-BR')
fake.city()

#%%
df = pd.DataFrame(
    {
        "Nome": [fake.name() for _ in range(100)],
        "Idade": [fake.random_int(min=18, max=80) for _ in range(100)],
        "Cidade": [fake.city() for _ in range(100)],
    }
)
# %%
df.to_csv("customers.csv", index=False)
