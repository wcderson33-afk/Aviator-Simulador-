import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re

st.set_page_config(page_title="Aviator Analisador", layout="wide")

st.title("🚀 Aviator - Análise de Resultados Reais")
st.caption("⚠️ App manual para estudo. Aviator é jogo de azar. RTP 97%. Não existe padrão.")

st.markdown("**Cole os multiplicadores que saíram na plataforma** pra analisar sua estratégia")

col1, col2, col3 = st.columns(3)
with col1:
    saque_alvo = st.number_input("Saque Alvo", min_value=1.01, value=1.50, step=0.01)
with col2:
    aposta = st.number_input("Valor da Aposta R$", min_value=1.0, value=10.0, step=1.0)
with col3:
    banca_inicial = st.number_input("Banca Inicial R$", min_value=10.0, value=1000.0, step=10.0)

entrada = st.text_area(
    "Multiplicadores separados por vírgula, espaço ou enter:",
    placeholder="1.23, 2.45, 1.01, 3.50, 1.12, 5.20...",
    height=100
)

if st.button("Analisar Resultados", type="primary"):
    if entrada:
        # Limpa e converte os números
        numeros = re.findall(r'\d+\.?\d*', entrada.replace(',', '.'))
        multiplicadores = [float(n) for n in numeros if float(n) >= 1.0]

        if len(multiplicadores) < 10:
            st.error("Cole pelo menos 10 resultados pra análise fazer sentido")
        else:
            # Calcula resultados básicos
            acertos = sum(1 for m in multiplicadores if m >= saque_alvo)
            total_rodadas = len(multiplicadores)
            taxa_acerto = (acertos / total_rodadas) * 100
            taxa_necessaria = (1/saque_alvo) * 100 / 0.97 # Ajuste RTP 97%

            lucro_total = acertos * aposta * (saque_alvo - 1) - (total_rodadas - acertos) * aposta
            banca_final = banca_inicial + lucro_total

            st.divider()
            st.subheader(f"📊 Análise de {total_rodadas} rodadas")

            # Métricas
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Rodadas Analisadas", total_rodadas)
            col2.metric("Taxa de Acerto", f"{taxa_acerto:.1f}%")
            col3.metric("Lucro/Prejuízo", f"R$ {lucro_total:.2f}")
            col4.metric("Banca Final", f"R$ {banca_final:.2f}")

            if taxa_acerto < taxa_necessaria:
                st.error(f"❌ Nessa amostra você perderia dinheiro. Precisa de {taxa_necessaria:.1f}% de acerto pra empatar, teve só {taxa_acerto:.1f}%")
            else:
                st.success(f"✅ Nessa amostra deu lucro. Mas testa com 1000 rodadas: RTP 97% te pega no longo prazo")

            # ===== CAÇADOR DE PADRÕES - A PARTE NOVA =====
            st.divider()
            st.subheader("🔍 Caçador de Padrões: 'E se eu entrar depois de X vermelhos?'")

            col1, col2 = st.columns(2)
            with col1:
                qtd_vermelhos = st.number_input("Testar entrada após X vermelhos seguidos:", value=3, min_value=1, max_value=10, key="qtd_v")
            with col2:
                limite_vermelho = st.number_input("Considerar vermelho abaixo de:", value=1.20, step=0.01, format="%.2f", key="lim_v")

            # Simula a estratégia de entrar após sequência
            entradas_padrao = 0
            wins_pos_padrao = 0
            sequencia = 0
            banca_padrao = banca_inicial
            banca_hist_padrao = [banca_inicial]

            for i, mult in enumerate(multiplicadores):
                if mult < limite_vermelho:
                    sequencia += 1
                else:
                    sequencia = 0

                # Se bateu a sequência, a PRÓXIMA jogada é a aposta
                if sequencia == qtd_vermelhos and i + 1 < len(multiplicadores):
                    entradas_padrao += 1
                    proxima_vela = multiplicadores[i + 1]
                    if proxima_vela >= saque_alvo:
                        banca_padrao += aposta * (saque_alvo - 1)
                        wins_pos_padrao += 1
                    else:
                        banca_padrao -= aposta
                    banca_hist_padrao.append(banca_padrao)
                    sequencia = 0 # Reseta pra não contar overlap

            if entradas_padrao > 0:
                taxa_pos_padrao = wins_pos_padrao / entradas_padrao * 100
                lucro_padrao = banca_padrao - banca_inicial

                st.write(f"**O padrão '{qtd_vermelhos} vermelhos < {limite_vermelho}x' apareceu {entradas_padrao} vezes**")
                col1, col2, col3 = st.columns(3)
                col1.metric(f"Taxa após padrão", f"{taxa_pos_padrao:.1f}%")
                col2.metric("Taxa normal", f"{taxa_acerto:.1f}%")
                col3.metric("Lucro seguindo padrão", f"R$ {lucro_padrao:.2f}", delta=f"{lucro_padrao:.2f}")

                if taxa_pos_padrao <= taxa_acerto + 3: # Margem de 3%
                    st.warning(f"⚠️ O padrão NÃO aumentou tua chance. Taxa normal: {taxa_acerto:.1f}% vs Após padrão: {taxa_pos_padrao:.1f}%. É aleatório, mano.")
                else:
                    st.info(f"📈 Nessa amostra deu {taxa_pos_padrao:.1f}%. Mas cola 1000 velas e testa de novo: vai cair pra {taxa_acerto:.1f}%")
            else:
                st.info(f"O padrão não apareceu nenhuma vez nesses {total_rodadas} dados. Cola mais velas.")

            # Gráficos
            st.divider()
            fig, ax = plt.subplots(1, 2, figsize=(12, 4))

            # Gráfico 1: Evolução da banca normal
            banca_hist = [banca_inicial]
            for m in multiplicadores:
                if m >= saque_alvo:
                    banca_hist.append(banca_hist[-1] + aposta * (saque_alvo - 1))
                else:
                    banca_hist.append(banca_hist[-1] - aposta)

            ax[0].plot(banca_hist, color='blue', linewidth=2, label='Apostando todas')
            if len(banca_hist_padrao) > 1:
                ax[0].plot(np.linspace(0, len(banca_hist)-1, len(banca_hist_padrao)), banca_hist_padrao, color='orange', linewidth=2, label=f'Entrando após {qtd_vermelhos} vermelhos')
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
            st.subheader("📋 Estatísticas Detalhadas")
            stats = {
                "Métrica": ["Menor multiplicador", "Maior multiplicador", "Média", "Mediana", "Velas < 1.20x", "Velas > 10x"],
                "Valor": [
                    f"{min(multiplicadores):.2f}x",
                    f"{max(multiplicadores):.2f}x",
                    f"{np.mean(multiplicadores):.2f}x",
                    f"{np.median(multiplicadores):.2f}x",
                    f"{sum(1 for m in multiplicadores if m < 1.20)} ({sum(1 for m in multiplicadores if m < 1.20)/len(multiplicadores)*100:.1f}%)",
                    f"{sum(1 for m in multiplicadores if m > 10)} ({sum(1 for m in multiplicadores if m > 10)/len(multiplicadores)*100:.1f}%)"
                ]
            }
            st.dataframe(pd.DataFrame(stats), hide_index=True)
    else:
        st.warning("Cole os multiplicadores primeiro")
