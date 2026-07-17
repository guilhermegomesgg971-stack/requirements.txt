import streamlit as st
import pandas as pd
import os
import csv
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Coletor de Rack", layout="wide")
st.title("📱 Coletor de Rack")

ARQUIVO_HISTORICO = "coletas_do_dia.csv"

if 'nome' not in st.session_state: st.session_state.nome = ""
if 'rack' not in st.session_state: st.session_state.rack = ""
if 'codigos' not in st.session_state: st.session_state.codigos = ""

def limpar_tudo():
    st.session_state.nome = ""
    st.session_state.rack = ""
    st.session_state.codigos = ""
    st.rerun()

st.subheader("Nova Coleta")
col1, col2 = st.columns(2)

st.session_state.nome = col1.text_input("Colaborador:", value=st.session_state.nome)
st.session_state.rack = col2.text_input("Rack:", value=st.session_state.rack)
st.session_state.codigos = st.text_area("Bipe os códigos:", height=200, value=st.session_state.codigos)

col_btn_processar, col_btn_limpar = st.columns(2)

with col_btn_processar:
    if st.button("Processar e Adicionar ao Histórico"):
        if not st.session_state.nome or not st.session_state.rack:
            st.error("Preencha Nome e Rack!")
        elif not st.session_state.codigos:
            st.warning("A lista está vazia.")
        else:
            linhas = st.session_state.codigos.splitlines()
            dados_processados = []
            
            for linha in linhas:
                codigo_raw = linha.strip()
                # Extrai apenas o que for número puro
                codigo_final = str(codigo_raw[6:11]) if len(codigo_raw) >= 12 else str(codigo_raw)
                
                if codigo_raw:
                    dados_processados.append({
                        'Codigo Material': codigo_final
                    })
            
            df = pd.DataFrame(dados_processados)
            header = not os.path.exists(ARQUIVO_HISTORICO)
            df.to_csv(ARQUIVO_HISTORICO, mode='a', index=False, header=header, encoding='utf-8-sig')
            
            st.success("Coleta processada!")
            st.session_state.codigos = ""
            st.rerun()

with col_btn_limpar:
    if st.button("Limpar Tudo"):
        limpar_tudo()

st.divider()

st.subheader("📊 Histórico de Coletas")
if os.path.exists(ARQUIVO_HISTORICO):
    df_total = pd.read_csv(ARQUIVO_HISTORICO)
    st.dataframe(df_total, use_container_width=True)
    
    with st.columns(3)[1]:
        # EXPORTAÇÃO "ULTRA SIMPLES"
        # Sem cabeçalho, sem aspas, sem apóstrofo
        csv_puro = df_total[['Codigo Material']].to_csv(index=False, header=False, sep=';', encoding='utf-8-sig', quoting=csv.QUOTE_NONE)
        
        st.download_button(
            label="📥 BAIXAR P/ SISTEMA (LAYOUT SIMPLES)", 
            data=csv_puro.encode('utf-8-sig'), 
            file_name="importacao_vd_simples.csv", 
            mime="text/csv"
        )