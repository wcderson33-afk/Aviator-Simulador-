import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="Aviator Analisador", layout="wide")
st.title("🚀 Aviator - Análise de Resultados Reais")

st.markdown("**Cole os multiplicadores que saíram na plataforma** pra analisar sua estratégia")

# Input dos multiplicadores reais
col1, col2 = st.columns([3, 1])
with col1:
    entrada = st.text_area(
        "Multiplicadores separados por vírgula, espaço ou enter:",
        placeholder="1.23, 2.45, 1.01, 3.50, 1.12, 5.20...",
        height=100
    )
with col2:
    saque_alvo = st.number_input("Saque Alvo", min_value=1.01, value=1.50, step=0.01)
    aposta = st.number_input("Valor da Aposta R$", min_value=1.0, value=10.0, step=1.0)
    banca_inicial = st.number_input("Banca Inicial R$", min_value=10.0, value=1000.0, step=10.0)

if st.button("Analisar Resultados", type="primary"):
    if entrada:
        # Limpa e converte os números
        import re
        numeros = re.findall(r'\d+\.?\d*', entrada.replace(',', '.'))
        multiplicadores = [float(n) for n in numeros if float(n) >= 1.0]

        if multiplicadores:
            # Calcula resultados
            acertos = sum(1 for m in multiplicadores if m >= saque_alvo)
            total_rodadas = len(multiplicadores)
            taxa_acerto = (acertos / total_rodadas) * 100

            lucro_total = acertos * aposta * (saque_alvo - 1) - (total_rodadas - acertos) * aposta
            banca_final = banca_inicial + lucro_total

            # Métricas
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Rodadas Analisadas", total_rodadas)
            col2.metric("Taxa de Acerto", f"{taxa_acerto:.1f}%")
            col3.metric("Lucro/Prejuízo", f"R$ {lucro_total:.2f}")
            col4.metric("Banca Final", f"R$ {banca_final:.2f}")

            # Gráfico da banca
            banca_hist = [banca_inicial]
            for m in multiplicadores:
                if m >= saque_alvo:
                    banca_hist.append(banca_hist[-1] + aposta * (saque_alvo - 1))
                else:
                    banca_hist.append(banca_hist[-1] - aposta)

            fig, ax = plt.subplots(1, 2, figsize=(12, 4))

            # Gráfico 1: Evolução da banca
            ax[0].plot(banca_hist, color='blue', linewidth=2)
            ax[0].axhline(y=banca_inicial, color='gray', linestyle='--', label='Banca Inicial')
            ax[0].set_title('Evolução da Banca')
            ax[0].set_ylabel('R$')
            ax[0].legend()
            ax[0].grid(True, alpha=0.3)

            # Gráfico 2: Histograma dos multiplicadores
            ax[1].hist(multiplicadores, bins=30, color='orange', alpha=0.7, edgecolor='black')
            ax[1].axvline(x=saque_alvo, color='red', linestyle='--', linewidth=2, label=f'Alvo {saque_alvo}x')
            ax[1].set_title('Distribuição dos Multiplicadores')
            ax[1].set_xlabel('Multiplicador')
            ax[1].set_ylabel('Frequência')
            ax[1].legend()
            ax[1].grid(True, alpha=0.3)

            st.pyplot(fig)

            # Tabela com estatísticas
            st.subheader("📊 Estatísticas Detalhadas")
            stats = {
                "Métrica": ["Menor multiplicador", "Maior multiplicador", "Média", "Mediana",
                           "Rodadas < 1.20x", "Rodadas > 10x", "Maior sequência de Loss"],
                "Valor": [
                    f"{min(multiplicadores):.2f}x",
                    f"{max(multiplicadores):.2f}x",
                    f"{np.mean(multiplicadores):.2f}x",
                    f"{np.median(multiplicadores):.2f}x",
                    f"{sum(1 for m in multiplicadores if m < 1.20)}",
                    f"{sum(1 for m in multiplicadores if m > 10)}",
                    f"{max([len(list(g)) for k, g in __import__('itertools').groupby([m < saque_alvo for m in multiplicadores]) if k], default=0)}"
                ]
            }
            st.table(pd.DataFrame(stats))

            # Aviso de RTP
            st.warning(f"⚠️ RTP esperado do Aviator: 97%. Com {total_rodadas} rodadas, a perda esperada seria R$ {banca_inicial * 0.03:.2f}")

        else:
            st.error("Não encontrei números válidos. Use formato: 1.23, 2.45, 1.01")
    else:
        st.info("Cole os multiplicadores acima pra começar a análise")
else:
    st.info("👆 Cole os resultados e clique em 'Analisar Resultados'")
