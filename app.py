# =====================================================
# Financial Insights Dashboard - Grid Layout Version
# =====================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------
# App Configuration
# -----------------------------------------------------
st.set_page_config(
    page_title="Financial Insights Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling with card layout
st.markdown("""
    <style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styling */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main title styling */
    h1 {
        font-weight: 700;
        font-size: 2.5rem !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem !important;
    }
    
    /* Subtitle styling */
    .subtitle {
        font-size: 1.1rem;
        color: #64748b;
        font-weight: 400;
        margin-bottom: 2rem;
    }
    
    /* Card styling */
    .insight-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        border: 1px solid #f1f5f9;
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .insight-card:hover {
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
        border-color: #e0e7ff;
    }
    
    .card-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .card-subtitle {
        font-size: 0.9rem;
        color: #64748b;
        margin-bottom: 1rem;
    }
    
    /* Section headers */
    h2, h3 {
        font-weight: 600;
        color: #1e293b;
        margin-top: 1.5rem !important;
        margin-bottom: 1rem !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #faf5ff 0%, #f3e8ff 100%);
        border-right: 1px solid #e9d5ff;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 2rem;
    }
    
    [data-testid="stSidebar"] h3 {
        color: #6b21a8;
        font-weight: 600;
        font-size: 1.3rem;
        letter-spacing: -0.02em;
        margin-bottom: 1.5rem !important;
    }
    
    [data-testid="stSidebar"] .stMultiSelect label,
    [data-testid="stSidebar"] .stSelectbox label {
        color: #7c3aed;
        font-weight: 500;
        font-size: 0.9rem;
    }
    
    [data-testid="stSidebar"] hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #ddd6fe, transparent);
    }
    
    /* Info boxes */
    .stAlert {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        border-left: 4px solid #667eea;
        border-radius: 8px;
        padding: 1rem 1.5rem;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1e293b;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
        color: #64748b;
    }
    
    /* Chart containers */
    .js-plotly-plot {
        border-radius: 12px;
    }
    
    /* Remove default spacing */
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
    }
    
    /* Warning boxes */
    .stWarning {
        background: #fef3c7;
        border-left: 4px solid #f59e0b;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------
# Header Section
# -----------------------------------------------------
st.title("📊 Financial Insights Dashboard")
st.markdown('<p class="subtitle">Interactive analytics to drive strategic business decisions with data-driven insights</p>', unsafe_allow_html=True)

# -----------------------------------------------------
# Load Dataset
# -----------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("Financial Data - DA Assesment.xlsx")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# -----------------------------------------------------
# Sidebar Filters
# -----------------------------------------------------
st.sidebar.markdown("### 🔎 Filter Controls")
st.sidebar.markdown("---")

year_options = sorted(df["Year"].dropna().unique())
country_options = sorted(df["Country"].dropna().unique())
segment_options = sorted(df["Segment"].dropna().unique())

year_filter = st.sidebar.multiselect(
    "📅 Year",
    options=year_options,
    default=year_options
)

country_filter = st.sidebar.multiselect(
    "🌍 Country",
    options=country_options,
    default=country_options
)

segment_filter = st.sidebar.multiselect(
    "🎯 Segment",
    options=segment_options,
    default=segment_options
)

st.sidebar.markdown("---")
st.sidebar.markdown("*Adjust filters to customize your analysis*")

# Apply filters
filtered_df = df[
    (df["Year"].isin(year_filter)) &
    (df["Country"].isin(country_filter)) &
    (df["Segment"].isin(segment_filter))
]

# Color scheme for charts
color_scheme = {
    'primary': '#667eea',
    'secondary': '#764ba2',
    'success': '#10b981',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    'info': '#3b82f6'
}

# -----------------------------------------------------
# ROW 1: Sales Trend (Full Width)
# -----------------------------------------------------
st.markdown("### 📈 Sales Performance")

product_options = sorted(filtered_df["Product"].dropna().unique())

if product_options:
    product_selected = st.selectbox(
        "Select Product for Trend Analysis",
        options=product_options,
        key="insight1_product"
    )

    sales_trend_df = (
        filtered_df[filtered_df["Product"] == product_selected]
        .groupby("Year", as_index=False)["Sales"]
        .sum()
    )

    if not sales_trend_df.empty:
        col_metrics, col_chart = st.columns([1, 3])
        
        with col_metrics:
            if len(sales_trend_df) > 1:
                sales_change = sales_trend_df["Sales"].iloc[-1] - sales_trend_df["Sales"].iloc[0]
                pct_change = (sales_change / sales_trend_df["Sales"].iloc[0]) * 100
                
                st.metric("Latest Year", f"${sales_trend_df['Sales'].iloc[-1]:,.0f}")
                st.metric("Total Change", f"${sales_change:,.0f}", f"{pct_change:+.1f}%")
                st.metric("Average Sales", f"${sales_trend_df['Sales'].mean():,.0f}")
        
        with col_chart:
            fig = px.line(
                sales_trend_df,
                x="Year",
                y="Sales",
                markers=True,
                title=f"Yearly Sales Trend: {product_selected}"
            )
            fig.update_traces(line_color=color_scheme['primary'], line_width=3, marker=dict(size=10))
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Inter', size=12),
                title_font=dict(size=16, color='#1e293b'),
                hovermode='x unified',
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ No sales data available for the selected filters.")
else:
    st.warning("⚠️ No products available for the selected filters.")

st.markdown("---")

# -----------------------------------------------------
# ROW 2: Profit Optimization & Market Performance (2 columns)
# -----------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 💰 Profit Optimization")
    st.caption("Top segment-country combinations")
    
    profit_by_segment_country = (
        filtered_df
        .groupby(["Segment", "Country"], as_index=False)["Profit"]
        .sum()
        .sort_values(by="Profit", ascending=False)
    )
    
    top_n = st.selectbox(
        "Show top",
        options=[5, 10, 15],
        index=0,
        key="insight2_topn"
    )
    
    top_profit_df = profit_by_segment_country.head(top_n)
    
    if not top_profit_df.empty:
        fig2 = px.bar(
            top_profit_df,
            x="Profit",
            y="Segment",
            color="Country",
            orientation="h",
            labels={"Profit": "Total Profit ($)"},
            color_discrete_sequence=px.colors.sequential.Purples_r
        )
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', size=11),
            showlegend=True,
            height=400,
            margin=dict(t=20, b=20)
        )
        st.plotly_chart(fig2, use_container_width=True)
        
        top_row = top_profit_df.iloc[0]
        st.info(
            f"🎯 **{top_row['Segment']}** in **{top_row['Country']}** leads with **${top_row['Profit']:,.0f}**"
        )
    else:
        st.warning("⚠️ No profit data available.")

with col2:
    st.markdown("#### 🌍 Market Performance")
    st.caption("Product sales by country")
    
    country_product_sales = (
        filtered_df
        .groupby(["Country", "Product"], as_index=False)["Sales"]
        .sum()
    )
    
    country_selected = st.selectbox(
        "Select country",
        options=sorted(country_product_sales["Country"].unique()),
        key="insight3_country"
    )
    
    country_sales_df = country_product_sales[
        country_product_sales["Country"] == country_selected
    ].sort_values(by="Sales", ascending=False)
    
    if not country_sales_df.empty:
        fig3 = px.bar(
            country_sales_df,
            x="Sales",
            y="Product",
            orientation="h",
            labels={"Sales": "Total Sales ($)"},
            color="Sales",
            color_continuous_scale="Purples"
        )
        fig3.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', size=11),
            showlegend=False,
            height=400,
            margin=dict(t=20, b=20)
        )
        st.plotly_chart(fig3, use_container_width=True)
        
        top_product = country_sales_df.iloc[0]
        st.info(
            f"🎯 **{top_product['Product']}** leads with **${top_product['Sales']:,.0f}**"
        )
    else:
        st.warning("⚠️ No sales data available.")

st.markdown("---")

# -----------------------------------------------------
# ROW 3: Top Products & Discount Analysis (2 columns)
# -----------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🏆 Top Performing Products")
    st.caption("Best selling products overall")
    
    top_products_n = st.selectbox(
        "Show top",
        options=[5, 10, 15],
        index=0,
        key="insight4_topn"
    )
    
    top_products_df = (
        filtered_df
        .groupby("Product", as_index=False)["Sales"]
        .sum()
        .sort_values(by="Sales", ascending=False)
        .head(top_products_n)
    )
    
    if not top_products_df.empty:
        fig4 = px.bar(
            top_products_df,
            x="Sales",
            y="Product",
            orientation="h",
            labels={"Sales": "Total Sales ($)"},
            color="Sales",
            color_continuous_scale="Viridis"
        )
        fig4.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', size=11),
            showlegend=False,
            height=400,
            margin=dict(t=20, b=20)
        )
        st.plotly_chart(fig4, use_container_width=True)
        
        top_product = top_products_df.iloc[0]
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Top Product", top_product['Product'])
        with col_b:
            st.metric("Sales", f"${top_product['Sales']:,.0f}")
    else:
        st.warning("⚠️ No product data available.")

with col2:
    st.markdown("#### 💸 Discount Impact")
    st.caption("Sales vs profit by discount band")
    
    discount_analysis_df = (
        filtered_df
        .groupby("Discount Band", as_index=False)[["Sales", "Profit"]]
        .mean()
    )
    
    if not discount_analysis_df.empty:
        fig5 = go.Figure()
        fig5.add_trace(go.Bar(
            x=discount_analysis_df["Discount Band"],
            y=discount_analysis_df["Sales"],
            name="Avg Sales",
            marker_color=color_scheme['info']
        ))
        fig5.add_trace(go.Bar(
            x=discount_analysis_df["Discount Band"],
            y=discount_analysis_df["Profit"],
            name="Avg Profit",
            marker_color=color_scheme['success']
        ))
        fig5.update_layout(
            barmode="group",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', size=11),
            height=400,
            margin=dict(t=20, b=20)
        )
        st.plotly_chart(fig5, use_container_width=True)
        
        st.info(
            "💡 Higher discounts boost sales but can erode margins."
        )
    else:
        st.warning("⚠️ No discount data available.")

st.markdown("---")

# -----------------------------------------------------
# ROW 4: Seasonal Patterns & Profitability Alert (2 columns)
# -----------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📆 Seasonal Sales Patterns")
    st.caption("Monthly trends for campaign timing")
    
    product_month_selected = st.selectbox(
        "Select product",
        options=sorted(filtered_df["Product"].unique()),
        key="insight6_product"
    )
    
    monthly_sales_df = (
        filtered_df[filtered_df["Product"] == product_month_selected]
        .groupby("Month Name", as_index=False)["Sales"]
        .sum()
    )
    
    if not monthly_sales_df.empty:
        fig6 = px.line(
            monthly_sales_df,
            x="Month Name",
            y="Sales",
            markers=True
        )
        fig6.update_traces(line_color=color_scheme['success'], line_width=3, marker=dict(size=10))
        fig6.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', size=11),
            hovermode='x unified',
            height=350,
            margin=dict(t=20, b=20)
        )
        st.plotly_chart(fig6, use_container_width=True)
        
        st.info(
            f"🎯 Target optimal windows for **{product_month_selected}** campaigns"
        )
    else:
        st.warning("⚠️ No monthly data available.")

with col2:
    st.markdown("#### ⚠️ Profitability Alert")
    st.caption("Sales vs profit by country")
    
    pricing_issue_df = (
        filtered_df
        .groupby("Country", as_index=False)[["Sales", "Profit"]]
        .sum()
    )
    
    if not pricing_issue_df.empty:
        fig7 = px.scatter(
            pricing_issue_df,
            x="Sales",
            y="Profit",
            text="Country",
            labels={"Sales": "Total Sales ($)", "Profit": "Total Profit ($)"},
            size="Sales",
            color="Profit",
            color_continuous_scale="RdYlGn"
        )
        fig7.update_traces(textposition='top center')
        fig7.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', size=11),
            height=350,
            margin=dict(t=20, b=20)
        )
        st.plotly_chart(fig7, use_container_width=True)
        
        st.info(
            "💡 High sales + low profit = pricing optimization opportunity"
        )
    else:
        st.warning("⚠️ No pricing data available.")

st.markdown("---")

# -----------------------------------------------------
# ROW 5: Market Concentration (Full Width)
# -----------------------------------------------------
st.markdown("#### 📊 Market Concentration Analysis")
st.caption("Product diversification assessment")

market_dominance_df = (
    filtered_df
    .groupby(["Country", "Product"], as_index=False)["Sales"]
    .sum()
)

country_dom_selected = st.selectbox(
    "Select Country for Market Analysis",
    options=sorted(market_dominance_df["Country"].unique()),
    key="insight8_country"
)

country_dom_df = market_dominance_df[
    market_dominance_df["Country"] == country_dom_selected
]

if not country_dom_df.empty:
    fig8 = px.treemap(
        country_dom_df,
        path=["Product"],
        values="Sales",
        title=f"Market Share Distribution: {country_dom_selected}",
        color="Sales",
        color_continuous_scale="Purples"
    )
    fig8.update_layout(
        font=dict(family='Inter', size=12),
        title_font=dict(size=16, color='#1e293b'),
        height=400
    )
    st.plotly_chart(fig8, use_container_width=True)
    
    st.info(
        f"🎯 Monitor concentration risk in **{country_dom_selected}** and explore diversification opportunities"
    )
else:
    st.warning("⚠️ No dominance data available.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #64748b; padding: 2rem 0;'>"
    "Financial Insights Dashboard | Data-Driven Business Intelligence"
    "</div>",
    unsafe_allow_html=True
)