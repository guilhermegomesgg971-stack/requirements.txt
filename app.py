import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Coletor Automático", layout="wide")
st.title("💄 Coletor Automático (Linha/Coluna)")

ARQUIVO_HISTORICO = "coletas_final.csv"
COLUNAS = [chr(i) for i in range(65, 91)] + ["AA"]

# Inicialização do estado
if 'linha' not in st.session_state: st.session_state.linha = 1
if 'col_idx' not in st.session_state: st.session_state.col_idx = 0

st.subheader(f"Próxima posição: Linha {st.session_state.linha} | Coluna {COLUNAS[st.session_state.col_idx]}")

# O campo "Bipe aqui" limpa o estado após cada leitura
def processar_bipagem():
    cod_raw = st.session_state.bipagem.strip()
    if cod_raw:
        # Limpeza do código (extrai 5 dígitos se tiver 12+)
        cod_limpo = cod_raw[6:11] if len(cod_raw) >= 12 else cod_raw
        
        # Salva a linha no CSV
        df_novo = pd.DataFrame([{
            'Linha': st.session_state.linha,
            'Coluna': COLUNAS[st.session_state.col_idx],
            'Codigo': cod_limpo
        }])
        header = not os.path.exists(ARQUIVO_HISTORICO)
        df_novo.to_csv(ARQUIVO_HISTORICO, mode='a', index=False, header=header, encoding='utf-8-sig')
        
        # Avança a posição automaticamente
        st.session_state.col_idx += 1
        if st.session_state.col_idx >= len(COLUNAS):
            st.session_state.col_idx = 0
            st.session_state.linha += 1
    
    st.session_state.bipagem = "" # Limpa o campo para o próximo bipe

st.text_input("Bipe o código aqui:", key="bipagem", on_change=processar_bipagem)

st.divider()

if os.path.exists(ARQUIVO_HISTORICO):
    df = pd.read_csv(ARQUIVO_HISTORICO)
    st.write("Últimos itens coletados:")
    st.dataframe(df.tail(10))
    
    # Exportação (O sistema VD+ deve ler este formato perfeitamente)
    csv_data = df.to_csv(index=False, sep=';', encoding='utf-8-sig')
    st.download_button("📥 BAIXAR ARQUIVO FINAL", csv_data, "importacao_maquiagem.csv", "text/csv")

if st.button("Resetar Tudo"):
    if os.path.exists(ARQUIVO_HISTORICO): os.remove(ARQUIVO_HISTORICO)
    st.session_state.linha = 1
    st.session_state.col_idx = 0
    st.rerun()