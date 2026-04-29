st.divider()
st.subheader("🔍 Teste de Padrão: 'Entrar depois de X vermelhos'")

col1, col2, col3 = st.columns(3)
with col1:
    qtd_vermelhos = st.number_input("Entrar após X vermelhos seguidos:", value=3, min_value=1, max_value=10)
with col2:
    limite_vermelho = st.number_input("Vermelho = abaixo de:", value=1.20, step=0.01, format="%.2f")
with col3:
    st.write("") # espaço
    st.write("")
    if st.button("Testar Padrão"):
        # Testa o padrão
        entradas = 0
        wins_pos_padrao = 0
        sequencia = 0
        banca_padrao = banca_inicial

        for i, mult in enumerate(multiplicadores):
            if mult < limite_vermelho:
                sequencia += 1
            else:
                sequencia = 0
            
            # Se bateu a sequência, a PRÓXIMA jogada conta
            if sequencia == qtd_vermelhos and i + 1 < len(multiplicadores):
                entradas += 1
                proxima_vela = multiplicadores[i + 1]
                if proxima_vela >= saque_alvo:
                    banca_padrao += aposta * (saque_alvo - 1)
                    wins_pos_padrao += 1
                else:
                    banca_padrao -= aposta
                sequencia = 0 # Reseta pra não contar overlap

        if entradas > 0:
            taxa_pos_padrao = wins_pos_padrao / entradas * 100
            lucro_padrao = banca_padrao - banca_inicial
            
            st.write(f"**Padrão apareceu {entradas} vezes em {total_rodadas} rodadas**")
            col1, col2, col3 = st.columns(3)
            col1.metric("Taxa após padrão", f"{taxa_pos_padrao:.1f}%")
            col2.metric("Taxa normal", f"{taxa_acerto:.1f}%")
            col3.metric("Lucro se seguisse", f"R$ {lucro_padrao:.2f}")

            if taxa_pos_padrao <= taxa_acerto + 2:
                st.error(f"❌ PADRÃO NÃO FUNCIONA. Taxa normal: {taxa_acerto:.1f}% vs Após padrão: {taxa_pos_padrao:.1f}%. É aleatório.")
            else:
                st.warning(f"⚠️ Deu {taxa_pos_padrao:.1f}% nessa amostra pequena. Testa com 1000+ velas: vai voltar pra {taxa_acerto:.1f}%")
        else:
            st.info(f"Padrão '{qtd_vermelhos} vermelhos < {limite_vermelho}x' não apareceu nenhuma vez.")
