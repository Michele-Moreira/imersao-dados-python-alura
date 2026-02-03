import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- Configuração da Página ---
st.set_page_config(
    page_title="Dashboard de Salários na Área de Dados",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS Customizado para Tema Personalizado ---
st.markdown("""
<style>
    /* Cores principais */
    :root {
        --primary: #6366f1;
        --secondary: #8b5cf6;
        --accent: #ec4899;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --dark: #1f2937;
        --light: #f9fafb;
    }
    
    /* Estilo geral */
    .main {
        background-color: #f9fafb;
    }
    
    /* Header customizado */
    .header-container {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    }
    
    /* Cards de métrica */
    [data-testid="metric-container"] {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #6366f1;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.2);
    }
    
    /* Styling para abas */
    .stTabs [data-baseweb="tab-list"] button {
        border-bottom: 3px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        border-bottom-color: #6366f1 !important;
    }
    
    /* Sidebar */
    .sidebar .sidebar-content {
        background-color: #ffffff;
    }
    
    /* Subheaders */
    h2 {
        color: #1f2937;
        border-bottom: 3px solid #6366f1;
        padding-bottom: 10px;
    }
    
    /* Markdown customizado */
    .markdown-text {
        color: #4b5563;
        font-size: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Carregamento dos dados ---
df = pd.read_csv("https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv")

# --- Renomear colunas para português ---
df = df.rename(columns={
    'work_year': 'ano',
    'experience_level': 'senioridade',
    'employment_type': 'contrato',
    'job_title': 'cargo',
    'salary_in_usd': 'usd',
    'employee_residence': 'residencia',
    'remote_ratio': 'remoto',
    'company_size': 'tamanho_empresa'
})

# --- Barra Lateral (Filtros) ---
st.sidebar.header("🔍 Filtros")

# Filtro de Ano
anos_disponiveis = sorted(df['ano'].unique())
anos_selecionados = st.sidebar.multiselect("Ano", anos_disponiveis, default=anos_disponiveis)

# Filtro de Senioridade
senioridades_disponiveis = sorted(df['senioridade'].unique())
senioridades_selecionadas = st.sidebar.multiselect("Senioridade", senioridades_disponiveis, default=senioridades_disponiveis)

# Filtro por Tipo de Contrato
contratos_disponiveis = sorted(df['contrato'].unique())
contratos_selecionados = st.sidebar.multiselect("Tipo de Contrato", contratos_disponiveis, default=contratos_disponiveis)

# Filtro por Tamanho da Empresa
tamanhos_disponiveis = sorted(df['tamanho_empresa'].unique())
tamanhos_selecionados = st.sidebar.multiselect("Tamanho da Empresa", tamanhos_disponiveis, default=tamanhos_disponiveis)

# --- Filtragem do DataFrame ---
df_filtrado = df[
    (df['ano'].isin(anos_selecionados)) &
    (df['senioridade'].isin(senioridades_selecionadas)) &
    (df['contrato'].isin(contratos_selecionados)) &
    (df['tamanho_empresa'].isin(tamanhos_selecionados))
]

# --- Conteúdo Principal ---
st.markdown("""
<div class="header-container">
    <h1>🎲 Dashboard de Análise de Salários na Área de Dados</h1>
    <p>Explore os dados salariais na área de dados nos últimos anos. Utilize os filtros à esquerda para refinar sua análise.</p>
</div>
""", unsafe_allow_html=True)

# --- Métricas Principais (KPIs) ---
st.subheader("📊 Métricas Gerais (Salário Anual em USD)")

if not df_filtrado.empty:
    salario_medio = df_filtrado['usd'].mean()
    salario_maximo = df_filtrado['usd'].max()
    salario_minimo = df_filtrado['usd'].min()
    salario_mediano = df_filtrado['usd'].median()
    total_registros = df_filtrado.shape[0]
    cargo_mais_frequente = df_filtrado["cargo"].mode()[0]
else:
    salario_medio, salario_maximo, salario_minimo, salario_mediano, total_registros, cargo_mais_frequente = 0, 0, 0, 0, 0, ""
 
col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("💰 Média Salarial", f"${salario_medio:,.0f}")
col2.metric("📈 Salário Máximo", f"${salario_maximo:,.0f}")
col3.metric("📉 Salário Mínimo", f"${salario_minimo:,.0f}")
col4.metric("🎯 Mediana", f"${salario_mediano:,.0f}")
col5.metric("📋 Total de Registros", f"{total_registros:,}")
col6.metric("💼 Cargo Mais Comum", cargo_mais_frequente)

st.markdown("---")

# --- Análises Visuais com Plotly ---
st.subheader("📈 Gráficos de Análise")

# Criar abas para melhor organização
tab1, tab2, tab3, tab4 = st.tabs(["📊 Visão Geral", "💼 Cargos & Experiência", "🌍 Geográfica", "📍 Tipo de Trabalho"])

with tab1:
    col_graf1, col_graf2 = st.columns(2)
    
    with col_graf1:
        if not df_filtrado.empty:
            top_cargos = df_filtrado.groupby('cargo')['usd'].mean().nlargest(10).sort_values(ascending=True).reset_index()
            grafico_cargos = px.bar(
                top_cargos,
                x='usd',
                y='cargo',
                orientation='h',
                title="🏆 Top 10 Cargos por Salário Médio",
                labels={'usd': 'Média salarial anual (USD)', 'cargo': 'Cargo'},
                color='usd',
                color_continuous_scale='Viridis'
            )
            grafico_cargos.update_layout(
                title_x=0.1, 
                yaxis={'categoryorder':'total ascending'},
                height=500,
                coloraxis_showscale=False
            )
            st.plotly_chart(grafico_cargos, use_container_width=True)
        else:
            st.warning("Nenhum dado para exibir no gráfico de cargos.")
    
    with col_graf2:
        if not df_filtrado.empty:
            grafico_hist = px.histogram(
                df_filtrado,
                x='usd',
                nbins=30,
                title="📊 Distribuição de Salários Anuais",
                labels={'usd': 'Faixa salarial (USD)', 'count': 'Frequência'},
                color_discrete_sequence=['#6366f1']
            )
            grafico_hist.update_layout(title_x=0.1, height=500)
            st.plotly_chart(grafico_hist, use_container_width=True)
        else:
            st.warning("Nenhum dado para exibir no gráfico de distribuição.")

with tab2:
    col_graf3, col_graf4 = st.columns(2)
    
    with col_graf3:
        if not df_filtrado.empty:
            # Box plot por experiência
            grafico_box = px.box(
                df_filtrado,
                x='senioridade',
                y='usd',
                title="📦 Distribuição Salarial por Nível de Experiência",
                labels={'senioridade': 'Nível de Experiência', 'usd': 'Salário (USD)'},
                color='senioridade',
                color_discrete_sequence=['#6366f1', '#8b5cf6', '#ec4899', '#f59e0b']
            )
            grafico_box.update_layout(title_x=0.1, height=500, showlegend=False)
            st.plotly_chart(grafico_box, use_container_width=True)
        else:
            st.warning("Nenhum dado para exibir.")
    
    with col_graf4:
        if not df_filtrado.empty:
            # Scatter: Experiência vs Salário
            grafico_scatter = px.scatter(
                df_filtrado,
                x='senioridade',
                y='usd',
                title="🎯 Salários por Nível de Experiência",
                labels={'senioridade': 'Nível de Experiência', 'usd': 'Salário (USD)'},
                color='senioridade',
                size='usd',
                color_discrete_sequence=['#6366f1', '#8b5cf6', '#ec4899', '#f59e0b'],
                size_max=20
            )
            grafico_scatter.update_layout(title_x=0.1, height=500, showlegend=False)
            st.plotly_chart(grafico_scatter, use_container_width=True)
        else:
            st.warning("Nenhum dado para exibir.")
    
    # Evolução de salários por ano
    col_graf5, col_graf6 = st.columns(2)
    with col_graf5:
        if not df_filtrado.empty and df_filtrado['ano'].nunique() > 1:
            evolucao = df_filtrado.groupby('ano')['usd'].agg(['mean', 'median']).reset_index()
            grafico_evolucao = px.line(
                evolucao,
                x='ano',
                y=['mean', 'median'],
                title="📈 Evolução de Salários por Ano",
                labels={'ano': 'Ano', 'value': 'Salário (USD)', 'variable': 'Métrica'},
                markers=True
            )
            grafico_evolucao.update_traces(line=dict(width=3))
            grafico_evolucao.update_layout(title_x=0.1, height=500)
            st.plotly_chart(grafico_evolucao, use_container_width=True)
        else:
            st.info("Apenas um ano de dados disponível.")
    
    with col_graf6:
        if not df_filtrado.empty:
            # Distribuição por tamanho de empresa
            empresa_dist = df_filtrado['tamanho_empresa'].value_counts().reset_index()
            empresa_dist.columns = ['Tamanho', 'Quantidade']
            grafico_empresa = px.pie(
                empresa_dist,
                names='Tamanho',
                values='Quantidade',
                title="🏢 Distribuição por Tamanho da Empresa",
                hole=0.4,
                color_discrete_sequence=['#6366f1', '#8b5cf6', '#ec4899']
            )
            grafico_empresa.update_traces(textinfo='percent+label')
            grafico_empresa.update_layout(title_x=0.1, height=500)
            st.plotly_chart(grafico_empresa, use_container_width=True)
        else:
            st.warning("Nenhum dado para exibir.")

with tab3:
    col_graf7, col_graf8 = st.columns(2)
    
    with col_graf7:
        if not df_filtrado.empty:
            # Top 10 países por salário médio
            paises = df_filtrado.groupby('residencia')['usd'].agg(['mean', 'count']).reset_index()
            paises = paises[paises['count'] >= 2]  # Apenas países com 2+ registros
            paises = paises.nlargest(10, 'mean').sort_values('mean', ascending=True)
            
            grafico_paises = px.bar(
                paises,
                x='mean',
                y='residencia',
                orientation='h',
                title="🌍 Top 10 Países por Salário Médio",
                labels={'mean': 'Salário Médio (USD)', 'residencia': 'País'},
                color='mean',
                color_continuous_scale='RdYlGn'
            )
            grafico_paises.update_layout(title_x=0.1, yaxis={'categoryorder':'total ascending'}, height=500)
            st.plotly_chart(grafico_paises, use_container_width=True)
        else:
            st.warning("Nenhum dado para exibir.")
    
    with col_graf8:
        if not df_filtrado.empty:
            # Mapa de calor: Cargo x Experiência
            df_heatmap = df_filtrado.groupby(['cargo', 'senioridade'])['usd'].mean().reset_index()
            
            # Pegar top 8 cargos para melhor visualização
            top_jobs = df_filtrado['cargo'].value_counts().head(8).index
            df_heatmap_filtered = df_heatmap[df_heatmap['cargo'].isin(top_jobs)]
            
            # Pivot para criar matriz
            pivot_data = df_heatmap_filtered.pivot(index='cargo', columns='senioridade', values='usd')
            
            grafico_heatmap = go.Figure(data=go.Heatmap(
                z=pivot_data.values,
                x=pivot_data.columns,
                y=pivot_data.index,
                colorscale='Viridis',
                colorbar=dict(title="Salário (USD)")
            ))
            grafico_heatmap.update_layout(
                title="🔥 Heatmap: Cargo vs Experiência",
                xaxis_title="Nível de Experiência",
                yaxis_title="Cargo",
                height=500,
                title_x=0.1
            )
            st.plotly_chart(grafico_heatmap, use_container_width=True)
        else:
            st.warning("Nenhum dado para exibir.")

with tab4:
    col_graf9, col_graf10 = st.columns(2)
    
    with col_graf9:
        if not df_filtrado.empty:
            remoto_contagem = df_filtrado['remoto'].value_counts().reset_index()
            remoto_contagem.columns = ['tipo_trabalho', 'quantidade']
            
            # Mapear valores de remoto para labels
            mapeamento_remoto = {
                'Presencial': 'Presencial',
                'Remoto': 'Remoto',
                'Híbrido': 'Híbrido',
                0: 'Presencial',
                100: 'Remoto',
                50: 'Híbrido'
            }
            remoto_contagem['tipo_trabalho'] = remoto_contagem['tipo_trabalho'].map(
                lambda x: mapeamento_remoto.get(x, str(x))
            )
            
            grafico_remoto = px.pie(
                remoto_contagem,
                names='tipo_trabalho',
                values='quantidade',
                title="💻 Proporção dos Tipos de Trabalho",
                hole=0.5,
                color_discrete_sequence=['#6366f1', '#8b5cf6', '#ec4899']
            )
            grafico_remoto.update_traces(textinfo='percent+label')
            grafico_remoto.update_layout(title_x=0.1, height=500)
            st.plotly_chart(grafico_remoto, use_container_width=True)
        else:
            st.warning("Nenhum dado para exibir.")
    
    with col_graf10:
        if not df_filtrado.empty:
            # Comparação: Remoto vs Presencial por salário
            salario_remoto = df_filtrado.groupby('remoto')['usd'].agg(['mean', 'median']).reset_index()
            salario_remoto['remoto'] = salario_remoto['remoto'].map(
                lambda x: mapeamento_remoto.get(x, str(x))
            )
            
            grafico_remoto_sal = px.bar(
                salario_remoto,
                x='remoto',
                y=['mean', 'median'],
                title="💰 Salários Médios: Remoto vs Presencial",
                labels={'remoto': 'Tipo de Trabalho', 'value': 'Salário (USD)', 'variable': 'Métrica'},
                barmode='group',
                color_discrete_sequence=['#6366f1', '#8b5cf6']
            )
            grafico_remoto_sal.update_layout(title_x=0.1, height=500)
            st.plotly_chart(grafico_remoto_sal, use_container_width=True)
        else:
            st.warning("Nenhum dado para exibir.")

# --- Tabela de Dados Detalhados ---
st.subheader("📋 Dados Detalhados")
st.dataframe(df_filtrado, use_container_width=True)
