import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Coletor Automático", layout="wide")
st.title("💄 Coletor de Maquiagem - Alerta de Zeros")

ARQUIVO_HISTORICO = "coletas_final.csv"
COLUNAS = [chr(i) for i in range(65, 91)] + ["AA"]

if 'linha' not in st.session_state: st.session_state.linha = 1
if 'col_idx' not in st.session_state: st.session_state.col_idx = 0

def processar_bipagem():
    cod_raw = st.session_state.bipagem.strip()
    if cod_raw:
        cod_limpo = cod_raw[6:11] if len(cod_raw) >= 12 else cod_raw
        
        # Verifica se começa com zero
        status = "ALERTA: ZERO À ESQUERDA" if cod_limpo.startswith('0') else "OK"
        
        df_novo = pd.DataFrame([{
            'Linha': st.session_state.linha,
            'Coluna': COLUNAS[st.session_state.col_idx],
            'Codigo': "'" + cod_limpo,
            'Status': status
        }])
        header = not os.path.exists(ARQUIVO_HISTORICO)
        df_novo.to_csv(ARQUIVO_HISTORICO, mode='a', index=False, header=header, encoding='utf-8-sig')
        
        st.session_state.col_idx += 1
        if st.session_state.col_idx >= len(COLUNAS):
            st.session_state.col_idx = 0
            st.session_state.linha += 1
            
    st.session_state.bipagem = ""

st.subheader(f"📍 Próxima posição: Linha {st.session_state.linha} | Coluna {COLUNAS[st.session_state.col_idx]}")
st.text_input("Bipe o código:", key="bipagem", on_change=processar_bipagem)

st.divider()

if os.path.exists(ARQUIVO_HISTORICO):
    df = pd.read_csv(ARQUIVO_HISTORICO)
    
    # Função para colorir linhas em vermelho se houver alerta
    def destacar_alerta(row):
        return ['background-color: #ffcccc' if row['Status'] == "ALERTA: ZERO À ESQUERDA" else '' for _ in row]

    st.write("Últimos itens coletados:")
    st.dataframe(df.tail(15).style.apply(destacar_alerta, axis=1), use_container_width=True)
    
    csv_data = df.to_csv(index=False, sep=';', encoding='utf-8-sig')
    st.download_button("📥 BAIXAR ARQUIVO FINAL", csv_data, "importacao_maquiagem.csv", "text/csv")

if st.button("❌ Resetar Tudo"):
    if os.path.exists(ARQUIVO_HISTORICO): os.remove(ARQUIVO_HISTORICO)
    st.session_state.linha = 1
    st.session_state.col_idx = 0
    st.rerun()