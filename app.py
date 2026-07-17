import streamlit as st
import pandas as pd
import os
import csv
from datetime import datetime

st.set_page_config(page_title="Coletor de Maquiagem", layout="wide")
st.title("💄 Coletor de Maquiagem (Endereçamento)")

ARQUIVO_HISTORICO = "coletas_maquiagem.csv"

# Inicialização de estado
if 'codigos' not in st.session_state: st.session_state.codigos = ""

st.subheader("Configuração do Endereço")
col_a, col_b, col_c, col_d = st.columns(4)

lado = col_a.selectbox("Lado", ["Lado 1", "Lado 2"])
rack = col_b.selectbox("Rack", ["Rack 1", "Rack 2"])
linha = col_c.selectbox("Linha", [str(i) for i in range(1, 13)])
# Colunas: Lado 1 (A-AA) / Lado 2 (A-I)
if lado == "Lado 1":
    colunas = [chr(i) for i in range(65, 91)] + ["AA"]
else:
    colunas = [chr(i) for i in range(65, 74)] # A até I
coluna = col_d.selectbox("Coluna", colunas)

st.session_state.codigos = st.text_area("Bipe os códigos aqui:", height=150)

if st.button("Processar Coleta"):
    if not st.session_state.codigos:
        st.warning("Lista vazia!")
    else:
        linhas_bipadas = st.session_state.codigos.splitlines()
        dados = []
        for l in linhas_bipadas:
            cod = l.strip()[6:11] if len(l.strip()) >= 12 else l.strip()
            # Montagem conforme o layout esperado pelo sistema
            dados.append({
                'Lado': lado,
                'Nr Rack': rack,
                'Linha': linha,
                'Coluna': coluna,
                'Codigo Material': cod
            })
        
        df = pd.DataFrame(dados)
        header = not os.path.exists(ARQUIVO_HISTORICO)
        df.to_csv(ARQUIVO_HISTORICO, mode='a', index=False, header=header, encoding='utf-8-sig')
        st.success("Adicionado!")
        st.session_state.codigos = ""
        st.rerun()

st.divider()
st.subheader("📊 Histórico e Exportação")
if os.path.exists(ARQUIVO_HISTORICO):
    df_total = pd.read_csv(ARQUIVO_HISTORICO)
    st.dataframe(df_total)
    
    # Exportação com Apóstrofo no código para garantir que o sistema leia como texto
    df_export = df_total.copy()
    df_export['Codigo Material'] = "'" + df_export['Codigo Material'].astype(str)
    
    csv_final = df_export.to_csv(index=False, sep=';', encoding='utf-8-sig', quoting=csv.QUOTE_NONE)
    
    st.download_button(
        label="📥 BAIXAR P/ SISTEMA (MAQUIAGEM)", 
        data=csv_final.encode('utf-8-sig'), 
        file_name="importacao_maquiagem.csv", 
        mime="text/csv"
    )

    if st.button("❌ APAGAR TUDO"):
        os.remove(ARQUIVO_HISTORICO)
        st.rerun()