import os
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np

def create_dashboard():
    # Configura caminhos absolutos
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    OUTPUTS_DIR = os.path.join(BASE_DIR, 'outputs')
    
    # Carrega as imagens diretamente
    img1 = plt.imread(os.path.join(OUTPUTS_DIR, 'plot1.png'))
    img2 = plt.imread(os.path.join(OUTPUTS_DIR, 'plot2.png'))
    img3 = plt.imread(os.path.join(OUTPUTS_DIR, 'plot3.png'))

    # Cria figura e layout
    fig = plt.figure(figsize=(18, 12), facecolor='#f5f5f5')
    gs = GridSpec(2, 2, figure=fig, width_ratios=[1.5, 1], height_ratios=[1, 1.2])
    
    # Adiciona gráficos
    ax1 = fig.add_subplot(gs[:, 0])
    ax1.imshow(img1)
    ax1.axis('off')
    ax1.set_title('RANKING DE CLUBES', fontsize=18, pad=15)

    ax2 = fig.add_subplot(gs[0, 1])
    ax2.imshow(img2)
    ax2.axis('off')
    ax2.set_title('DISTRIBUIÇÃO POR PAÍS', fontsize=18, pad=15)

    ax3 = fig.add_subplot(gs[1, 1])
    ax3.imshow(img3)
    ax3.axis('off')
    ax3.set_title('EVOLUÇÃO TEMPORAL', fontsize=18, pad=15)

    # Ajusta e salva
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUTS_DIR, 'dashboard.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("Dashboard gerado com sucesso!")

if __name__ == "__main__":
    create_dashboard()