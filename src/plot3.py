import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import matplotlib.pyplot as plt
import numpy as np
url = "https://exame.com/esporte/palmeiras-tem-mundial-confira-os-times-brasileiros-que-mais-tem-titulos-no-campeonato/"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
news_body = soup.find(id="news-body")
ols = news_body.find_all("ol")
ol = ols[1]
times = []
paises = []
titulos = []
anos = []
for li in ol.find_all("li"):
    p = li.find("p")
    strong = p.find("strong")
    time = strong.text.strip()
    texto = p.get_text().strip()
    pais_match = re.search(rf"{re.escape(time)}\s*\(([^)]+)\)", texto)
    pais = pais_match.group(1) if pais_match else None
    titulos_match = re.search(r"(\d+)\s+títul", texto)
    total_titulos = int(titulos_match.group(1)) if titulos_match else None
    anos_match = re.search(r"\(([\d, e\s]+)\)$", texto)
    anos_titulos = anos_match.group(1).replace(" e", ",").strip() if anos_match else None
    times.append(time)
    paises.append(pais)
    titulos.append(total_titulos)
    anos.append(anos_titulos)
df = pd.DataFrame({
    "Time": times,
    "País": paises,
    "Total de Títulos": titulos,
    "Anos dos Títulos": anos
})
regioes_map = {
    'BRA': 'América do Sul',
    'ARG': 'América do Sul',
    'URU': 'América do Sul',
    'PAR': 'América do Sul',
    'ESP': 'Europa',
    'ITA': 'Europa',
    'ALE': 'Europa',
    'HOL': 'Europa',
    'ING': 'Europa',
    'POR': 'Europa',
    'SER': 'Europa',
}

df['Região'] = df['País'].map(regioes_map)
df['Anos dos Títulos'] = df['Anos dos Títulos'].str.replace(' ', '')
df = df.assign(Ano=df['Anos dos Títulos'].str.split(',')).explode('Ano')
df['Ano'] = pd.to_numeric(df['Ano'], errors='coerce')
df = df.dropna(subset=['Ano'])
titulos_por_regiao_ano = df.groupby(['Região', 'Ano']).size().reset_index(name='Títulos')
pivot = titulos_por_regiao_ano.pivot(index='Ano', columns='Região', values='Títulos').fillna(0)
pivot_acumulado = pivot.cumsum()
plt.figure(figsize=(14, 8))
cores = {
    'América do Sul': '#1f77b4',
    'Europa': '#ff7f0e'
}

for regiao in pivot_acumulado.columns:
    plt.plot(pivot_acumulado.index, pivot_acumulado[regiao], marker='o', label=regiao, color=cores.get(regiao, None))
plt.title('Evolução dos Títulos Mundiais por Região ao Longo dos Anos', fontsize=18, weight='bold')
plt.xlabel('Ano', fontsize=14)
plt.ylabel('Total Acumulado de Títulos', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(title='Região', fontsize=12)
plt.tight_layout()
plt.savefig('C:/Users/User/Documents/GitHub/projeto-visualiza--o-da-informacao/outputs/plot3.png', dpi=300, bbox_inches='tight', facecolor='white')
