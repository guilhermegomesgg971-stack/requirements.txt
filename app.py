import streamlit as st
import pandas as pd
import os

# Configuração da página
st.set_page_config(page_title="Coletor de Rack", layout="wide")
st.title("📱 Coletor de Rack")

ARQUIVO_HISTORICO = "coletas_do_dia.csv"

# Inicialização do estado
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

nome = col1.text_input("Colaborador:", key="nome_input", value=st.session_state.nome)
rack = col2.text_input("Rack:", key="rack_input", value=st.session_state.rack)
codigos = st.text_area("Bipe os códigos:", height=200, key="codigos_input", value=st.session_state.codigos)

st.session_state.nome = nome
st.session_state.rack = rack
st.session_state.codigos = codigos

col_btn_processar, col_btn_limpar = st.columns(2)

with col_btn_processar:
    if st.button("Processar e Adicionar ao Histórico"):
        if not st.session_state.nome or not st.session_state.rack:
            st.error("Preencha Nome e Rack!")
        elif not st.session_state.codigos:
            st.warning("A lista está vazia.")
        else:
            linhas = st.session_state.codigos.splitlines()
            lista_processada = []
            for linha in linhas:
                codigo = linha.strip()
                if not codigo: continue
                # Mantém o código como string pura (preserva zeros)
                lista_processada.append(str(codigo))
            
            df = pd.DataFrame(lista_processada, columns=['Codigo Material'])
            df.insert(0, 'Rack', st.session_state.rack)
            df.insert(0, 'Colaborador', st.session_state.nome)
            
            header = not os.path.exists(ARQUIVO_HISTORICO)
            df.to_csv(ARQUIVO_HISTORICO, mode='a', index=False, header=header)
            
            st.success("Coleta processada!")
            st.session_state.codigos = "" # Limpa apenas os códigos
            st.rerun()

with col_btn_limpar:
    if st.button("Limpar Tudo"):
        limpar_tudo()

st.divider()

# Histórico e Exportação
st.subheader("📊 Histórico de Coletas")
if os.path.exists(ARQUIVO_HISTORICO):
    df_total = pd.read_csv(ARQUIVO_HISTORICO, dtype={'Codigo Material': str})
    st.dataframe(df_total, use_container_width=True)
    
    col_dl1, col_dl2, col_del = st.columns(3)
    
    with col_dl1:
        csv_total = df_total.to_csv(index=False).encode('utf-8')
        st.download_button("📥 BAIXAR TUDO (CSV)", csv_total, "historico_completo.csv", "text/csv")
        
    with col_dl2:
        # Exportação em TXT (cada código em uma linha, sem aspas, sem títulos)
        txt_codigos = "\n".join(df_total['Codigo Material'].astype(str))
        st.download_button("📥 BAIXAR SÓ CÓDIGOS (TXT)", txt_codigos, "codigos.txt", "text/plain")
    
    with col_del:
        if st.button("❌ APAGAR TUDO"):
            if os.path.exists(ARQUIVO_HISTORICO):
                os.remove(ARQUIVO_HISTORICO)
                st.rerun()