import streamlit as st
import pandas as pd
import os
import csv

# Configuração da página
st.set_page_config(page_title="Coletor Maquiagem", layout="wide")
st.title("💄 Coletor de Maquiagem - Lado Único")

ARQUIVO_HISTORICO = "coletas_maquiagem_lado1.csv"

# Definição das colunas A até AA
colunas_letras = [chr(i) for i in range(65, 91)] + ["AA"]

# Inicialização do estado
if 'codigos' not in st.session_state: st.session_state.codigos = ""
if 'linha_atual' not in st.session_state: st.session_state.linha_atual = 1
if 'coluna_idx' not in st.session_state: st.session_state.coluna_idx = 0

st.subheader(f"Posição Atual: Linha {st.session_state.linha_atual} | Coluna {colunas_letras[st.session_state.coluna_idx]}")

st.session_state.codigos = st.text_area("Bipe o código:", height=100, value=st.session_state.codigos)

col1, col2 = st.columns(2)

with col1:
    if st.button("Processar e Avançar"):
        if not st.session_state.codigos:
            st.warning("Bipe um código!")
        else:
            cod_raw = st.session_state.codigos.strip()
            cod_limpo = cod_raw[6:11] if len(cod_raw) >= 12 else cod_raw
            
            # Salvar no histórico
            nova_linha = {
                'Linha': st.session_state.linha_atual,
                'Coluna': colunas_letras[st.session_state.coluna_idx],
                'Codigo Material': cod_limpo
            }
            
            df = pd.DataFrame([nova_linha])
            header = not os.path.exists(ARQUIVO_HISTORICO)
            df.to_csv(ARQUIVO_HISTORICO, mode='a', index=False, header=header, encoding='utf-8-sig')
            
            # Lógica de avanço automático
            st.session_state.coluna_idx += 1
            if st.session_state.coluna_idx >= len(colunas_letras):
                st.session_state.coluna_idx = 0
                st.session_state.linha_atual += 1
                if st.session_state.linha_atual > 12:
                    st.session_state.linha_atual = 1 # Reinicia se passar de 12
            
            st.session_state.codigos = ""
            st.rerun()

with col2:
    if st.button("Resetar Posição"):
        st.session_state.linha_atual = 1
        st.session_state.coluna_idx = 0
        st.rerun()

st.divider()
st.subheader("📊 Histórico")
if os.path.exists(ARQUIVO_HISTORICO):
    df_total = pd.read_csv(ARQUIVO_HISTORICO)
    st.dataframe(df_total)
    
    # Exportação com Apóstrofo para o VD+
    df_export = df_total.copy()
    df_export['Codigo Material'] = "'" + df_export['Codigo Material'].astype(str)
    csv_final = df_export.to_csv(index=False, sep=';', encoding='utf-8-sig', quoting=csv.QUOTE_NONE)
    
    st.download_button("📥 BAIXAR P/ SISTEMA (MAQUIAGEM)", csv_final, "importacao_maquiagem.csv", "text/csv")

    if st.button("❌ APAGAR TUDO"):
        os.remove(ARQUIVO_HISTORICO)
        st.rerun()