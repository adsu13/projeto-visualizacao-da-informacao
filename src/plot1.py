import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import os
plt.style.use('seaborn-v0_8')
cores = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
url = "https://www.vamofutebol.com/veja-todos-os-campeoes-mundiais-de-clubes-segundo-a-fifa/"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
ul = soup.find('ul', class_='inline-links multi')
titulos = {}
for li in ul.find_all('li'):
    strong = li.find('strong')
    if strong:
        nome = strong.text.replace(":", "").strip()
        texto = li.get_text()
        numeros = texto.split('(')[-1].replace(')', '')
        quantidade = len(numeros.split(','))
        titulos[nome] = quantidade
df = pd.DataFrame(list(titulos.items()), columns=['Clube', 'Títulos'])
df = df.sort_values(by='Títulos', ascending=False)
plt.figure(figsize=(12, 8))
bars = plt.barh(df['Clube'][::-1], df['Títulos'][::-1], color=cores, edgecolor='black', linewidth=0.7)
for bar in bars:
    width = bar.get_width()
    plt.text(width + 0.2, bar.get_y() + bar.get_height()/2, 
             f'{int(width)}', 
             va='center', ha='left', fontsize=10)
plt.xlabel('Número de Títulos', fontsize=12, labelpad=10)
plt.ylabel('Clubes', fontsize=12, labelpad=10)
plt.title('Clubes com Mais Títulos Mundiais\n(Fonte: Vamo Futebol)', 
          fontsize=14, pad=20, fontweight='bold')
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.tight_layout()
os.makedirs('../outputs', exist_ok=True)
plt.savefig('C:/Users/User/Documents/GitHub/projeto-visualiza--o-da-informacao/outputs/plot1.png', dpi=300, bbox_inches='tight', transparent=False)   
