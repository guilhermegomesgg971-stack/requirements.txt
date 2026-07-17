import streamlit as st
import pandas as pd
import os
import csv

st.set_page_config(page_title="Coletor Maquiagem", layout="wide")
st.title("💄 Coletor de Maquiagem - Lado Único")

ARQUIVO_HISTORICO = "coletas_maquiagem_lado1.csv"

colunas_letras = [chr(i) for i in range(65, 91)] + ["AA"]

if 'codigos' not in st.session_state: st.session_state.codigos = ""
if 'linha_atual' not in st.session_state: st.session_state.linha_atual = 1
if 'coluna_idx' not in st.session_state: st.session_state.coluna_idx = 0

st.subheader(f"Posição: Linha {st.session_state.linha_atual} | Coluna {colunas_letras[st.session_state.coluna_idx]}")
st.session_state.codigos = st.text_area("Bipe o código:", height=100, value=st.session_state.codigos)

col1, col2 = st.columns(2)
with col1:
    if st.button("Processar e Avançar"):
        if st.session_state.codigos:
            cod_raw = st.session_state.codigos.strip()
            cod_limpo = cod_raw[6:11] if len(cod_raw) >= 12 else cod_raw
            
            nova_linha = {
                'Linha': st.session_state.linha_atual,
                'Coluna': colunas_letras[st.session_state.coluna_idx],
                'Codigo': cod_limpo
            }
            
            df = pd.DataFrame([nova_linha])
            header = not os.path.exists(ARQUIVO_HISTORICO)
            df.to_csv(ARQUIVO_HISTORICO, mode='a', index=False, header=header, encoding='utf-8-sig')
            
            st.session_state.coluna_idx += 1
            if st.session_state.coluna_idx >= len(colunas_letras):
                st.session_state.coluna_idx = 0
                st.session_state.linha_atual += 1
                if st.session_state.linha_atual > 12: st.session_state.linha_atual = 1
            
            st.session_state.codigos = ""
            st.rerun()

with col2:
    if st.button("Resetar Posição"):
        st.session_state.linha_atual = 1
        st.session_state.coluna_idx = 0
        st.rerun()

st.divider()
if os.path.exists(ARQUIVO_HISTORICO):
    df_total = pd.read_csv(ARQUIVO_HISTORICO)
    st.dataframe(df_total)
    
    # CORREÇÃO: Exportação simplificada sem forçar o QUOTE_NONE
    # O Pandas cuidará das aspas corretamente agora
    csv_final = df_total.to_csv(index=False, sep=';', encoding='utf-8-sig')
    
    st.download_button(
        label="📥 BAIXAR P/ SISTEMA (FIXO)", 
        data=csv_final.encode('utf-8-sig'), 
        file_name="importacao_maquiagem.csv", 
        mime="text/csv"
    )

    if st.button("❌ APAGAR TUDO"):
        os.remove(ARQUIVO_HISTORICO)
        st.rerun()