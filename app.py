import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulador Aviator", layout="wide")
st.title("Simulador Estatístico do Aviator")
st.caption("⚠️ Apenas para fins educacionais. Aviator é jogo de azar com RTP ~97%. Não prevê resultados reais.")

n_rodadas = st.slider("Quantas rodadas simular?", 100, 20000, 5000)
saque_alvo = st.number_input("Sacar sempre em quanto?", 1.01, 100.0, 2.00, 0.01)
aposta = st.number_input("Valor da aposta por rodada", 1.0, 1000.0, 10.0)

if st.button("🎲 Rodar Simulação", type="primary"):
    r = np.random.uniform(0, 0.97, n_rodadas)
    crashes = 1 / (1 - r)
    crashes = np.maximum(crashes, 1.00)

    ganhou = crashes >= saque_alvo
    lucro_por_rodada = np.where(ganhou, aposta * (saque_alvo - 1), -aposta)
    lucro_total = np.cumsum(lucro_por_rodada)

    col1, col2, col3 = st.columns(3)
    col1.metric("Taxa de acerto", f"{np.mean(ganhou)*100:.2f}%")
    col2.metric("Lucro/Prejuízo", f"R$ {lucro_total[-1]:.2f}")
    col3.metric("Maior crash", f"{np.max(crashes):.2f}x")

    fig, ax = plt.subplots(1, 2, figsize=(12,4))
    ax[0].hist(crashes[crashes < 20], bins=50, color='#ff4b4b')
    ax[0].set_title("Distribuição dos Crashes até 20x")
    ax[0].set_xlabel("Multiplicador")
    ax[1].plot(lucro_total, color='#00cc88', linewidth=2)
    ax[1].axhline(0, color='red', linestyle='--')
    ax[1].set_title("Evolução da Banca")
    ax[1].set_xlabel("Rodada")
    ax[1].set_ylabel("R$")
    st.pyplot(fig)
    
    perda_esperada = n_rodadas * aposta * 0.03
    st.error(f"Matemática: Com RTP 97%, a perda esperada em {n_rodadas} rodadas de R${aposta} é R${perda_esperada:.2f}")
