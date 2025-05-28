import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from matplotlib import font_manager
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['font.family'] = 'DejaVu Sans'
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
titulos_por_pais = df.groupby("País")["Total de Títulos"].sum().sort_values(ascending=False)
plt.figure(figsize=(10, 8))
colors = cm.tab20c(np.linspace(0, 1, len(titulos_por_pais)))
def format_pct(pct, allvals):
    absolute = int(round(pct/100.*sum(allvals)))
    return f"{absolute} ({pct:.1f}%)" if pct > 5 else ""
wedges, texts, autotexts = plt.pie(
    titulos_por_pais,
    labels=None,
    autopct=lambda pct: format_pct(pct, titulos_por_pais),
    startangle=140,
    colors=colors,
    wedgeprops={'linewidth': 1, 'edgecolor': 'white'},
    textprops={'fontsize': 11, 'color': 'black', 'weight': 'bold'},
    pctdistance=0.85
)
plt.title("Distribuição de Títulos Mundiais por País", pad=20, fontsize=16, weight='bold')
plt.legend(
    wedges,
    [f"{pais} ({titulos_por_pais[pais]})" for pais in titulos_por_pais.index],
    title="Países",
    loc="center left",
    bbox_to_anchor=(1, 0.5),
    fontsize=10
)
plt.tight_layout()
plt.savefig('../outputs/plot2.png', dpi=300, bbox_inches='tight', facecolor='white')