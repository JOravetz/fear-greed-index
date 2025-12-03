"""CNN Fear & Greed Index Dashboard"""

import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
from fear_greed_index import CNNFearAndGreedIndex

st.set_page_config(
    page_title="CNN Fear & Greed Index",
    page_icon="📊",
    layout="wide",
)


def get_color_for_score(score: float) -> str:
    """Return color based on fear/greed score"""
    if score < 25:
        return "#8B0000"  # Extreme Fear - dark red
    elif score < 45:
        return "#FF4500"  # Fear - orange red
    elif score < 55:
        return "#FFD700"  # Neutral - gold
    elif score < 75:
        return "#32CD32"  # Greed - lime green
    else:
        return "#006400"  # Extreme Greed - dark green


def create_gauge(score: float, title: str = "Fear & Greed Index") -> go.Figure:
    """Create a gauge chart for the fear/greed score"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 24}},
        number={'font': {'size': 48}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1},
            'bar': {'color': get_color_for_score(score)},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 25], 'color': 'rgba(139, 0, 0, 0.3)'},
                {'range': [25, 45], 'color': 'rgba(255, 69, 0, 0.3)'},
                {'range': [45, 55], 'color': 'rgba(255, 215, 0, 0.3)'},
                {'range': [55, 75], 'color': 'rgba(144, 238, 144, 0.3)'},
                {'range': [75, 100], 'color': 'rgba(0, 100, 0, 0.3)'},
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    ))
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
    return fig


def create_historical_chart(data: list, title: str = "Fear & Greed Index History") -> go.Figure:
    """Create historical line chart"""
    dates = [datetime.fromtimestamp(d["x"] / 1000) for d in data]
    values = [d["y"] for d in data]

    fig = go.Figure()

    # Add colored background bands
    fig.add_hrect(y0=0, y1=25, fillcolor="rgba(139, 0, 0, 0.1)", line_width=0)
    fig.add_hrect(y0=25, y1=45, fillcolor="rgba(255, 69, 0, 0.1)", line_width=0)
    fig.add_hrect(y0=45, y1=55, fillcolor="rgba(255, 215, 0, 0.1)", line_width=0)
    fig.add_hrect(y0=55, y1=75, fillcolor="rgba(144, 238, 144, 0.1)", line_width=0)
    fig.add_hrect(y0=75, y1=100, fillcolor="rgba(0, 100, 0, 0.1)", line_width=0)

    # Color each segment based on value
    colors = [get_color_for_score(v) for v in values]

    fig.add_trace(go.Scatter(
        x=dates,
        y=values,
        mode='lines',
        line=dict(width=2),
        marker=dict(color=colors),
        hovertemplate='<b>Date:</b> %{x|%b %d, %Y}<br><b>Score:</b> %{y:.1f}<extra></extra>'
    ))

    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Score",
        yaxis=dict(range=[0, 100]),
        hovermode='x unified',
        height=400,
    )

    return fig


def create_indicators_chart(indicators: list) -> go.Figure:
    """Create horizontal bar chart for indicators"""
    names = [ind.name for ind in indicators]
    scores = [ind.score for ind in indicators]
    colors = [get_color_for_score(s) for s in scores]

    fig = go.Figure(go.Bar(
        x=scores,
        y=names,
        orientation='h',
        marker_color=colors,
        text=[f'{s:.1f}' for s in scores],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Score: %{x:.1f}<extra></extra>'
    ))

    fig.add_vline(x=50, line_dash="dash", line_color="gray", opacity=0.5)

    fig.update_layout(
        title="Individual Indicators",
        xaxis=dict(range=[0, 105], title="Score"),
        height=350,
        margin=dict(l=20, r=20, t=50, b=20),
    )

    return fig


@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_data():
    """Load Fear & Greed data with caching"""
    return CNNFearAndGreedIndex()


def main():
    st.title("📊 CNN Fear & Greed Index")
    st.markdown("Real-time market sentiment analysis from CNN Business")

    # Load data
    with st.spinner("Loading market data..."):
        cnn_fg = load_data()

    # Top row - Main gauge and summary
    col1, col2 = st.columns([1, 1])

    with col1:
        fig_gauge = create_gauge(cnn_fg.score, f"{cnn_fg.rating.title()}")
        st.plotly_chart(fig_gauge, width="stretch")

    with col2:
        st.markdown("### Market Summary")

        # Create metrics
        metric_col1, metric_col2 = st.columns(2)
        with metric_col1:
            delta = cnn_fg.score - cnn_fg.previous_close
            st.metric("Current Score", f"{cnn_fg.score:.1f}", f"{delta:+.1f} from close")
            st.metric("1 Week Ago", f"{cnn_fg.previous_1_week:.1f}")
        with metric_col2:
            st.metric("Previous Close", f"{cnn_fg.previous_close:.1f}")
            st.metric("1 Month Ago", f"{cnn_fg.previous_1_month:.1f}")

        # Rating badge
        color = get_color_for_score(cnn_fg.score)
        st.markdown(
            f'<div style="background-color: {color}; color: white; padding: 10px; '
            f'border-radius: 5px; text-align: center; font-size: 18px; font-weight: bold;">'
            f'{cnn_fg.rating.upper()}</div>',
            unsafe_allow_html=True
        )

    st.divider()

    # Historical chart
    st.markdown("### Historical Trend")
    if cnn_fg.historical_data:
        fig_history = create_historical_chart(cnn_fg.historical_data)
        st.plotly_chart(fig_history, width="stretch")

    st.divider()

    # Indicators section
    st.markdown("### Individual Indicators")

    col1, col2 = st.columns([2, 1])

    with col1:
        fig_indicators = create_indicators_chart(cnn_fg.all_indicators)
        st.plotly_chart(fig_indicators, width="stretch")

    with col2:
        st.markdown("#### Indicator Details")
        for ind in cnn_fg.all_indicators:
            color = get_color_for_score(ind.score)
            timestamp = ind.timestamp.strftime("%b %d, %I:%M %p") if ind.timestamp else "N/A"
            st.markdown(
                f'<div style="margin-bottom: 8px;">'
                f'<span style="color: {color}; font-weight: bold;">●</span> '
                f'<b>{ind.name}</b>: {ind.score:.1f} ({ind.rating.title()})<br>'
                f'<small style="color: gray;">Updated: {timestamp}</small></div>',
                unsafe_allow_html=True
            )

    # Footer
    st.divider()
    st.markdown(
        "<small style='color: gray;'>Data sourced from CNN Business Fear & Greed Index. "
        "Refreshes every 5 minutes.</small>",
        unsafe_allow_html=True
    )

    # Refresh button
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()


if __name__ == "__main__":
    main()
