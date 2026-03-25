import streamlit as st
import pandas as pd
import altair as alt

def render_chartly_spec(spec):
    """
    Mock Chartly API client translating generic declarative specifications into 
    local high-fidelity Streamlit + Altair component executions resilient to timeouts.
    """
    title = spec.get("chart_title", "Chart")
    ctype = spec.get("chart_type", "bar")
    data = spec.get("dataset", [])
    x = spec.get("x_axis_field")
    y = spec.get("y_axis_field")
    
    st.markdown(f'<div style="font-weight:700;color:#2FFF00;margin-bottom:8px;font-size:0.9rem;text-transform:uppercase;letter-spacing:1px">{title}</div>', unsafe_allow_html=True)
    
    if not data:
        st.info("API No Data / Timeout: Fallback Rendering Active")
        return
        
    df = pd.DataFrame(data)
    
    try:
        if ctype in ["bar", "grouped_bar"]:
            st.bar_chart(df.set_index(x)[y])
        elif ctype == "line":
            st.line_chart(df.set_index(x)[y])
        elif ctype == "pie":
            chart = alt.Chart(df).mark_arc().encode(
                theta=alt.Theta(field=y, type="quantitative"),
                color=alt.Color(field=x, type="nominal")
            )
            st.altair_chart(chart, use_container_width=True)
        elif ctype == "histogram":
            chart = alt.Chart(df).mark_bar().encode(
                alt.X(f"{x}:Q", bin=True),
                y='count()'
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            st.dataframe(df)
    except Exception as e:
        st.error(f"Chartly API Edge Failure: {e}")

def render_executive_charts():
    from visualization.chart_specs import get_executive_specs
    st.markdown("<br/>", unsafe_allow_html=True)
    specs = get_executive_specs()
    c1, c2 = st.columns(2)
    with c1:
        render_chartly_spec(specs[0])
        st.markdown("<br/>", unsafe_allow_html=True)
        render_chartly_spec(specs[1])
    with c2:
        render_chartly_spec(specs[2])
        st.markdown("<br/>", unsafe_allow_html=True)
        render_chartly_spec(specs[3])

def render_ml_charts():
    from visualization.chart_specs import get_ml_specs
    st.markdown("<br/>", unsafe_allow_html=True)
    specs = get_ml_specs()
    c1, c2 = st.columns(2)
    with c1:
        render_chartly_spec(specs[0])
        if len(specs) > 2:
            st.markdown("<br/>", unsafe_allow_html=True)
            render_chartly_spec(specs[2])
    with c2:
        render_chartly_spec(specs[1])
