import streamlit as st
import pandas as pd
from datetime import datetime, date
from streamlit_gsheets import GSheetsConnection
import matplotlib.pyplot as plt
from pathlib import Path

# ==========================================
# Configuração da página e Layout Responsivo
# ==========================================
st.set_page_config(page_title="Inquérito - MCnet", page_icon="📝", layout="wide")

# Ligar ao Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("Falha ao inicializar a ligação ao Google Sheets. Verifica o secrets.toml.")

# Caminhos e Imagens
script_dir = Path(__file__).parent
LOGO_PATH_1 = script_dir / "Logo_tipo_GtSa.jpeg"
LOGO_PATH_2 = script_dir / "Logo_tipo_gtsa.jpeg"

# Opções para os menus
opcoes_sexo = ["Masculino", "Feminino", "Outro"]
opcoes_funcao = [
    "Faturador", "Chefe de Turno", "Gestor Operacional", "Fiel do Armazem", 
    "Chefe do Terminal", "Director do Terminal", "Tecnico Informatico"
]
opcoes_departamento = ["Faturação", "Armazém", "Direção", "IT", "Gestores", "Outro"]
opcoes_situacao = [
    "🟢 Ativo (Conta Criada)",
    "🟡 Sem Formação",
    "🔵 Com Formação (Sem Conta)",
    "🔴 Bloqueado (Precisa de Reset)"
]

# ==========================================
# CABEÇALHO GLOBAL (Aparece em todos os ecrãs)
# ==========================================
col_logo1, col_logo2, col_logo3 = st.columns([1, 2, 1])
with col_logo2:
    if LOGO_PATH_1.exists():
        st.image(str(LOGO_PATH_1), use_container_width=True)
    elif LOGO_PATH_2.exists():
        st.image(str(LOGO_PATH_2), use_container_width=True)

st.markdown("<h1 style='text-align: center; color: #333;'>Gestão de Terminais, S.A.</h1>", unsafe_allow_html=True)
st.markdown("---")

# ==========================================
# MENU SUPERIOR COM BOTÕES ESTILIZADOS
# ==========================================
st.markdown("""
<style>
    div.stButton > button {
        height: 60px;
        font-size: 18px !important;
        font-weight: bold !important;
        border-radius: 12px;
        transition: all 0.3s;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    div.stButton > button[kind="primary"] {
        background-color: #0056b3; 
        color: white;
        border: none;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #004494;
    }
    div.stButton > button[kind="secondary"] {
        background-color: #ffffff;
        color: #0056b3;
        border: 2px solid #0056b3;
    }
    div.stButton > button[kind="secondary"]:hover {
        background-color: #f0f8ff;
        border: 2px solid #004494;
        color: #004494;
    }
</style>
""", unsafe_allow_html=True)

if 'pagina_atual' not in st.session_state:
    st.session_state.pagina_atual = "Inquérito"

tipo_btn_inq = "primary" if st.session_state.pagina_atual == "Inquérito" else "secondary"
tipo_btn_dash = "primary" if st.session_state.pagina_atual == "Dashboard" else "secondary"

col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    if st.button("📝 Inquérito (Público)", use_container_width=True, type=tipo_btn_inq):
        st.session_state.pagina_atual = "Inquérito"
        st.rerun() 
with col_btn2:
    if st.button("📊 Dashboard da Direção", use_container_width=True, type=tipo_btn_dash):
        st.session_state.pagina_atual = "Dashboard"
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# PÁGINA 1: INQUÉRITO PÚBLICO
# ==========================================
if st.session_state.pagina_atual == "Inquérito":
    
    # NOVA MENSAGEM EXPLICATIVA
    st.info("""
    ℹ️ **Objetivo deste Registo:**  
    Este formulário destina-se à atualização rigorosa da base de dados de acessos ao sistema **MCnet (Janela Única)**. 
    O preenchimento é obrigatório para todos os colaboradores envolvidos na operação da GTSA. Os dados recolhidos garantem que as suas credenciais, alocação de turnos e nível de formação estão devidamente registados para manter a operação sem interrupções.
    """)
    st.markdown("<br>", unsafe_allow_html=True)

    with st.form("inquerito_mcnet", clear_on_submit=True):
        st.subheader("Secção 1: Identificação")
        col1, col2 = st.columns(2)
        with col1:
            primeiro_nome = st.text_input("Primeiro Nome (First Name) *")
        with col2:
            apelido = st.text_input("Apelido (Last Name) *")
            
        nome_meio = st.text_input("Nome do meio (Middle Name)")
        
        col3, col4 = st.columns(2)
        with col3:
            bi = st.text_input("Número do Bilhete de Identidade (BI)")
        with col4:
            nuit = st.text_input("NUIT")
            
        col5, col6 = st.columns(2)
        with col5:
            sexo = st.selectbox("Sexo (Gender)", opcoes_sexo)
        with col6:
            data_nascimento = st.date_input(
                "Data de Nascimento (Date of Birth)",
                value=date(1995, 1, 1),
                min_value=date(1950, 1, 1),
                max_value=date(2010, 12, 31)
            )
        
        st.markdown("---")
        st.subheader("Secção 2: Contactos e Empresa")
        
        col7, col8 = st.columns(2)
        with col7:
            funcao = st.selectbox("Função (Designation-Role)", opcoes_funcao)
        with col8:
            departamento = st.selectbox("Afectação (Department)", opcoes_departamento)
        
        # LOGICA DO TURNO CONDICIONAL
        turno = ""
        if funcao in ["Faturador", "Chefe de Turno"]:
            turno = st.radio("Selecione o Turno", ["A", "B", "C", "D"], horizontal=True)
            
        col9, col10 = st.columns(2)
        with col9:
            whatsapp = st.text_input("Número do WhatsApp")
        with col10:
            telemovel = st.text_input("Telemóvel (Mobile Phone No)")
            
        email = st.text_input("e-mail")
            
        st.markdown("---")
        st.subheader("Secção 3: Ponto de Situação")
        situacao = st.radio("Ponto de Situação (Janela Única)", opcoes_situacao)
        
        st.markdown("*Campos com asterisco (*) são obrigatórios.*")
        btn_submeter = st.form_submit_button("Submeter Formulário")
        
    if btn_submeter:
        if not primeiro_nome.strip() or not apelido.strip():
            st.error("⚠️ Por favor, preencha os campos obrigatórios: Primeiro Nome e Apelido.")
        else:
            try:
                df_atual = conn.read(ttl=0)
                
                data_nasc_str = data_nascimento.strftime("%Y-%m-%d") if data_nascimento else ""
                carimbo_tempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                nova_linha = {
                    'Carimbo de Data/Hora': carimbo_tempo,
                    'Primeiro Nome (First Name)': primeiro_nome.strip(),
                    'Nome do meio (Middle Name)': nome_meio.strip(),
                    'Apelido (Last Name)': apelido.strip(),
                    'Número do Bilhete de Identidade (BI)': bi.strip(),
                    'NUIT': nuit.strip(),
                    'Sexo (Gender)': sexo,
                    'Data de Nascimento (Date of Birth)': data_nasc_str,
                    'Função (Designation-Role)': funcao,
                    'Turno': turno, 
                    'Afectação (Department)': departamento,
                    'Número do WhatsApp': whatsapp.strip(),
                    'Telemóvel (Mobile Phone No)': telemovel.strip(),
                    'e-mail': email.strip(),
                    'Ponto de Situação (Janela Única)': situacao
                }
                
                novo_df = pd.DataFrame([nova_linha])
                df_atualizado = pd.concat([df_atual, novo_df], ignore_index=True)
                
                conn.update(data=df_atualizado)
                
                st.success(f"✅ Registo submetido com sucesso! Obrigado, {primeiro_nome.strip()}.")
                st.balloons()
            except Exception as e:
                st.error(f"❌ Ocorreu um erro ao comunicar com o servidor: {e}")

    # Rodapé 
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #777; font-size: 14px;'>Sistema Desenvolvido Pelo Departamento De Tecnologias De Informação E Comunicação - GTSA</p>", unsafe_allow_html=True)


# ==========================================
# PÁGINA 2: DASHBOARD DA DIREÇÃO AVANÇADO
# ==========================================
elif st.session_state.pagina_atual == "Dashboard":
    st.header("🔒 Acesso Restrito à Direção")
    senha = st.text_input("Insere a palavra-passe para ver os resultados:", type="password")
    
    if senha == "admin123":
        st.success("Acesso Concedido.")
        st.markdown("---")
        
        try:
            df_dash = conn.read(ttl=0)
            
            if not df_dash.empty:
                # ------------------------------------
                # EXPORTAÇÃO E FILTROS 
                # ------------------------------------
                col_filt, col_exp = st.columns([2, 1])
                
                with col_filt:
                    lista_dept = ["Todos"] + list(df_dash['Afectação (Department)'].dropna().unique())
                    filtro_dept = st.selectbox("Filtro: Selecione o Departamento para analisar", lista_dept)
                    
                    if filtro_dept != "Todos":
                        df_dash = df_dash[df_dash['Afectação (Department)'] == filtro_dept]
                
                with col_exp:
                    st.markdown("<br>", unsafe_allow_html=True)
                    csv_export = df_dash.to_csv(index=False, sep=';', encoding='utf-8-sig')
                    st.download_button(
                        label="📥 Descarregar para Excel",
                        data=csv_export,
                        file_name=f"Relatorio_MCnet_GTSA_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                
                st.info("💡 **Dica para PDF:** Para gerar um relatório em PDF com o Logótipo e Gráficos da GTSA, pressione **Ctrl + P** no seu teclado e escolha 'Guardar como PDF'.")
                st.markdown("---")

                # ------------------------------------
                # MÉTRICAS E GRÁFICOS
                # ------------------------------------
                total_colab = len(df_dash)
                st.markdown(f"### 👥 Colaboradores Encontrados (Filtro Atual): **{total_colab}**")
                
                if 'Ponto de Situação (Janela Única)' in df_dash.columns:
                    counts = df_dash['Ponto de Situação (Janela Única)'].value_counts()
                    
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("🟢 Ativos", counts.get(opcoes_situacao[0], 0))
                    col2.metric("🟡 Sem Formação", counts.get(opcoes_situacao[1], 0))
                    col3.metric("🔵 Com Formação", counts.get(opcoes_situacao[2], 0))
                    col4.metric("🔴 Bloqueados", counts.get(opcoes_situacao[3], 0))
                    
                    st.markdown("---")
                    
                    col_graf1, col_graf2 = st.columns(2)
                    
                    with col_graf1:
                        st.subheader("Estado dos Acessos")
                        fig, ax = plt.subplots(figsize=(6, 4))
                        cores_mapa = {
                            opcoes_situacao[0]: "#28a745",
                            opcoes_situacao[1]: "#ffc107",
                            opcoes_situacao[2]: "#17a2b8",
                            opcoes_situacao[3]: "#dc3545"
                        }
                        cores = [cores_mapa.get(x, '#cccccc') for x in counts.index]
                        ax.pie(counts.values, labels=counts.index, colors=cores, autopct='%1.1f%%', startangle=140, wedgeprops={'edgecolor': 'white'})
                        ax.axis('equal')
                        fig.patch.set_alpha(0.0)
                        st.pyplot(fig)
                        
                    with col_graf2:
                        st.subheader("Distribuição por Departamento")
                        if 'Afectação (Department)' in df_dash.columns:
                            dept_counts = df_dash['Afectação (Department)'].value_counts()
                            st.bar_chart(dept_counts, color="#0056b3")
                    
                    st.markdown("---")
                    st.subheader("Dados Brutos da Operação")
                    st.dataframe(df_dash, use_container_width=True)
                else:
                    st.warning("O formato do Google Sheets ainda não contém a coluna de Ponto de Situação.")
            else:
                st.info("O Google Sheets está atualmente vazio. Aguarde pelas primeiras submissões.")
        except Exception as e:
            st.error(f"Erro ao carregar o Dashboard: {e}")
            
    elif senha:
        st.error("Palavra-passe incorreta.")
