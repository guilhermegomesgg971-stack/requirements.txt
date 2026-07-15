import streamlit as st
import pandas as pd
import os

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
                if not codigo:
                    lista_processada.append("")
                elif len(codigo) == 13:
                    lista_processada.append(str(codigo[7:12]))
                else:
                    lista_processada.append(str(codigo))
            
            df = pd.DataFrame(lista_processada, columns=['Codigo Material'])
            df['Codigo Material'] = df['Codigo Material'].astype(str)
            df.insert(0, 'Rack', st.session_state.rack)
            df.insert(0, 'Colaborador', st.session_state.nome)
            
            header = not os.path.exists(ARQUIVO_HISTORICO)
            df.to_csv(ARQUIVO_HISTORICO, mode='a', index=False, header=header, quoting=1)
            
            st.success("Coleta processada!")
            limpar_tudo() 

with col_btn_limpar:
    if st.button("Limpar Tela"):
        limpar_tudo()

st.divider()

st.subheader("📊 Histórico de Coletas")
if os.path.exists(ARQUIVO_HISTORICO):
    df_total = pd.read_csv(ARQUIVO_HISTORICO, dtype={'Codigo Material': str})
    df_total['Codigo Material'] = df_total['Codigo Material'].fillna('')
    st.dataframe(df_total, use_container_width=True)
    
    col_dl1, col_dl2, col_del = st.columns(3)
    
    with col_dl1:
        csv_total = df_total.to_csv(index=False, quoting=1).encode('utf-8')
        st.download_button("📥 BAIXAR TUDO", csv_total, "historico.csv", "text/csv")
        
    with col_dl2:
        # AQUI A CORREÇÃO: formato de texto puro sem aspas, mas garantindo que o CSV 
        # trate a coluna como string para não remover zeros.
        df_codigos = df_total[['Codigo Material']]
        # Adicionamos um tab (\t) antes do código se necessário, mas o CSV puro costuma bastar:
        csv_codigos = df_codigos.to_csv(index=False, header=False, quoting=0).encode('utf-8')
        st.download_button("📥 BAIXAR SÓ CÓDIGOS", csv_codigos, "codigos.csv", "text/csv")
    
    with col_del:
        if st.button("❌ APAGAR TUDO"):
            if os.path.exists(ARQUIVO_HISTORICO):
                os.remove(ARQUIVO_HISTORICO)
                st.rerun()