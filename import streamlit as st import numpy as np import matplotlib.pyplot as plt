import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="Simulador Aviator", layout="wide")
st.title("Simulador Aviator - Tempo Real")
st.caption("⚠️ Educacional. RTP ~97%. Cada rodada é independente e aleatória.")

col1, col2, col3 = st.columns(3)
with col1:
    n_rodadas = st.number_input("Quantas rodadas?", 10, 1000, 100)
    modo_tempo_real = st.checkbox("Modo Tempo Real", value=True)
with col2:
    saque_alvo = st.number_input("Sacar em quanto?", 1.01, 100.0, 2.00, 0.01)
    velocidade = st.slider("Velocidade", 0.01, 0.5, 0.05) if modo_tempo_real else 0
with col3:
    aposta = st.number_input("Aposta por rodada", 1.0, 1000.0, 10.0)
    banca_inicial = st.number_input("Banca inicial", 10.0, 100000.0, 500.0)

if st.button("🎲 Iniciar Simulação", type="primary"):
    r = np.random.uniform(0, 0.97, n_rodadas)
    crashes = 1 / (1 - r)
    crashes = np.maximum(crashes, 1.00)
    
    placeholder_grafico = st.empty()
    placeholder_metricas = st.empty()
    
    banca = banca_inicial
    historico_banca = [banca_inicial]
    acertos = 0
    
    for i in range(int(n_rodadas)):
        if banca <= 0:
            st.error("💀 BANCA QUEBROU! Saldo zerado.")
            break
            
        crash_atual = crashes[i]
        ganhou = crash_atual >= saque_alvo
        
        if ganhou:
            banca += aposta * (saque_alvo - 1)
            acertos += 1
        else:
            banca -= aposta
            
        historico_banca.append(banca)
        
        fig, ax = plt.subplots(1, 2, figsize=(12, 4))
        
        x = np.linspace(1, crash_atual, 100)
        y = x
        ax[0].plot(x, y, color='#ff4b4b', linewidth=3)
        ax[0].scatter(crash_atual, crash_atual, color='red', s=200, zorder=5)
        ax[0].text(crash_atual, crash_atual, f' {crash_atual:.2f}x CRASH', fontsize=12, weight='bold')
        ax[0].set_xlim(1, max(10, crash_atual * 1.2))
        ax[0].set_ylim(1, max(10, crash_atual * 1.2))
        ax[0].set_title(f"Rodada {i+1}/{n_rodadas} | {'GANHOU' if ganhou else 'PERDEU'}")
        ax[0].grid(True, alpha=0.3)
        ax[0].set_xlabel("Multiplicador")
        
        ax[1].plot(historico_banca, color='#00cc88', linewidth=2)
        ax[1].axhline(banca_inicial, color='blue', linestyle='--', alpha=0.5, label='Inicial')
        ax[1].axhline(0, color='red', linestyle='--', label='Quebrou')
        ax[1].set_title("Evolução da Banca")
        ax[1].set_ylabel("R$")
        ax[1].legend()
        ax[1].grid(True, alpha=0.3)
        
        placeholder_grafico.pyplot(fig)
        plt.close()
        
        with placeholder_metricas.container():
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Banca Atual", f"R$ {banca:.2f}")
            m2.metric("Taxa Acerto", f"{acertos/(i+1)*100:.1f}%")
            m3.metric("Lucro Total", f"R$ {banca - banca_inicial:.2f}")
            m4.metric("Saque Alvo", f"{saque_alvo:.2f}x")
        
        if modo_tempo_real:
            time.sleep(velocidade)
    
    st.success(f"Simulação finalizada! Resultado: R$ {banca:.2f}")
    perda_esperada = n_rodadas * aposta * 0.03
    st.warning(f"Perda esperada com RTP 97%: R$ {perda_esperada:.2f}")
