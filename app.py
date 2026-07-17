import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Coletor de Rack", layout="wide")
st.title("📱 Coletor de Rack")

ARQUIVO_HISTORICO = "coletas_do_dia.csv"

# Inicialização do estado da sessão
if 'nome' not in st.session_state: st.session_state.nome = ""
if 'rack' not in st.session_state: st.session_state.rack = ""
if 'codigos' not in st.session_state: st.session_state.codigos = ""

def limpar_tudo():
    st.session_state.nome = ""
    st.session_state.rack = ""
    st.session_state.codigos = ""
    st.rerun()

# Interface
st.subheader("Nova Coleta")
col1, col2 = st.columns(2)

st.session_state.nome = col1.text_input("Colaborador:", value=st.session_state.nome)
st.session_state.rack = col2.text_input("Rack:", value=st.session_state.rack)
st.session_state.codigos = st.text_area("Bipe os códigos (um por linha):", height=200, value=st.session_state.codigos)

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
                
                # Se a linha estiver vazia, marca como "SEM CÓDIGO" para manter a contagem
                if not codigo_raw:
                    codigo_final = "SEM CÓDIGO"
                else:
                    # Lógica de extração: 7º ao 12º caractere
                    if len(codigo_raw) >= 12:
                        codigo_final = str(codigo_raw[7:12])
                    else:
                        codigo_final = str(codigo_raw)
                
                dados_processados.append({
                    'Data/Hora': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    'Colaborador': st.session_state.nome,
                    'Rack': st.session_state.rack,
                    'Codigo Material': codigo_final
                })
            
            df = pd.DataFrame(dados_processados)
            
            # Salvar no CSV
            header = not os.path.exists(ARQUIVO_HISTORICO)
            df.to_csv(ARQUIVO_HISTORICO, mode='a', index=False, header=header, encoding='utf-8-sig')
            
            st.success("Coleta processada com sucesso!")
            st.session_state.codigos = "" # Limpa apenas os códigos para o próximo
            st.rerun()

with col_btn_limpar:
    if st.button("Limpar Tudo"):
        limpar_tudo()

st.divider()

# Histórico
st.subheader("📊 Histórico de Coletas")
if os.path.exists(ARQUIVO_HISTORICO):
    df_total = pd.read_csv(ARQUIVO_HISTORICO)
    st.dataframe(df_total, use_container_width=True)
    
    col_dl1, col_dl2, col_del = st.columns(3)
    
    with col_dl1:
        csv_total = df_total.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 BAIXAR TUDO (CSV)", csv_total, "historico_completo.csv", "text/csv")
        
    with col_dl2:
        # Formatação para Excel não corromper códigos
        df_excel = df_total.copy()
        df_excel['Codigo Material'] = '="' + df_excel['Codigo Material'].astype(str) + '"'
        csv_excel = df_excel.to_csv(index=False, sep=';', encoding='utf-8-sig').encode('utf-8-sig')
        st.download_button("📥 BAIXAR P/ EXCEL", csv_excel, "codigos_para_excel.csv", "text/csv")
    
    with col_del:
        if st.button("❌ APAGAR TUDO"):
            if os.path.exists(ARQUIVO_HISTORICO):
                os.remove(ARQUIVO_HISTORICO)
                st.rerun()