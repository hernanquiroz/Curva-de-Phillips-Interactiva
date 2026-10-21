import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

# ───────────────────────────────────────────────────────────────
# Configuración de la página
# ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Curva de Phillips Interactiva",
    page_icon="📉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────────────────────
# Título y descripción
# ─────────────────────────────────────────────────────────────
st.title("📉 Curva de Phillips (Interactiva)")
st.markdown("""
Analiza la relación inversa entre **inflación (π)** y **desempleo (u)**.
-  **Curva verde fija**: Curva de Phillips original
- ⚫ **Punto negro**: Se desplaza a lo largo de la curva original
- 🔵 **Curva punteada**: Curva duplicada desplazable en diagonal
""")

# ──────────────────────────────────────────────────────────────
# Parámetros de la Curva de Phillips
# Forma: π = a/u + b  (hiperbólica, como en la imagen)
# ──────────────────────────────────────────────────────────────
st.sidebar.header("️ Parámetros de la Curva")

a = st.sidebar.number_input("Parámetro 'a' (forma de la curva)", value=7.2, step=0.1)
b = st.sidebar.number_input("Parámetro 'b' (inflación base)", value=1.2, step=0.1)

st.sidebar.markdown("---")

# ───────────────────────────────────────────────────────────────
# Control del punto negro sobre la curva fija
# ──────────────────────────────────────────────────────────────
st.sidebar.header(" Punto de Equilibrio (sobre curva fija)")

u_punto = st.sidebar.slider(
    "Tasa de desempleo del punto (u)",
    min_value=1.0,
    max_value=9.0,
    value=4.0,
    step=0.1,
    format="%.1f"
)

# Calcular inflación correspondiente en la curva fija
pi_punto = a / u_punto + b

st.sidebar.markdown("---")

# ───────────────────────────────────────────────────────────────
# Desplazamiento de la curva duplicada (diagonal)
# ──────────────────────────────────────────────────────────────
st.sidebar.header("🔵 Desplazamiento de Curva Duplicada")

delta_u = st.sidebar.slider(
    "Desplazamiento horizontal (Δu)",
    min_value=-4.0,
    max_value=4.0,
    value=0.0,
    step=0.1,
    format="%.1f"
)

delta_pi = st.sidebar.slider(
    "Desplazamiento vertical (Δπ)",
    min_value=-4.0,
    max_value=4.0,
    value=0.0,
    step=0.1,
    format="%.1f"
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Leyenda de colores:**")
st.sidebar.markdown("🟢 Verde = Curva original (fija)")
st.sidebar.markdown("🔵 Azul punteada = Curva desplazada")
st.sidebar.markdown("⚫ Negro = Punto sobre curva original")

# ───────────────────────────────────────────────────────────────
# Calcular las curvas
# ──────────────────────────────────────────────────────────────
u = np.linspace(1, 9, 200)

# Curva de Phillips original (fija)
pi_original = a / u + b

# Curva de Phillips duplicada (desplazada)
# Desplazamiento: u' = u - delta_u, π' = π + delta_pi
u_desplazada = u + delta_u
pi_desplazada = a / u + b + delta_pi

# ──────────────────────────────────────────────────────────────
# Mostrar métricas
# ──────────────────────────────────────────────────────────────
st.markdown("###  Punto sobre la Curva Original")
col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="Tasa de Desempleo (u)",
        value=f"{u_punto:.1f}%"
    )

with col2:
    st.metric(
        label="Tasa de Inflación (π)",
        value=f"{pi_punto:.2f}%"
    )

st.markdown("---")

# ───────────────────────────────────────────────────────────────
# Crear la gráfica
# ──────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(11, 7))

# Grid
ax.grid(True, linestyle='--', alpha=0.6)
ax.set_axisbelow(True)

# Curva de Phillips original (verde, fija)
ax.plot(u, pi_original, 'g-', linewidth=3, 
        label=f'Curva de Phillips Original (πe={b:.1f})')

# Curva de Phillips duplicada (azul punteada, desplazada)
# Filtrar valores válidos (u > 0)
mask = u_desplazada > 0
ax.plot(u_desplazada[mask], pi_desplazada[mask], 
        'b--', linewidth=2.5, 
        label=f'Curva Desplazada (Δu={delta_u:+.1f}, Δπ={delta_pi:+.1f})')

# Punto negro sobre la curva original
ax.plot(u_punto, pi_punto, 'ko', markersize=12, 
        markeredgecolor='black', markerfacecolor='black', 
        markeredgewidth=2, zorder=10)

# Etiqueta del punto
ax.annotate(f'Punto (u={u_punto:.1f}, π={pi_punto:.2f})', 
            xy=(u_punto, pi_punto), 
            xytext=(u_punto + 0.8, pi_punto + 0.8),
            fontsize=10, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

# Líneas punteadas desde el punto a los ejes
ax.axhline(y=pi_punto, color='gray', linestyle=':', alpha=0.5, linewidth=1)
ax.axvline(x=u_punto, color='gray', linestyle=':', alpha=0.5, linewidth=1)

# Configuración de ejes
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_xlabel('Tasa de Desempleo (u)', fontsize=13, fontweight='bold')
ax.set_ylabel('Tasa de Inflación (π)', fontsize=13, fontweight='bold')
ax.set_title('Curva de Phillips (Interactiva)', 
             fontsize=15, fontweight='bold', pad=20)

# Leyenda
ax.legend(loc='upper right', fontsize=11, framealpha=0.9)

# Marcas en los ejes
ax.set_xticks(np.arange(0, 11, 2))
ax.set_yticks(np.arange(0, 11, 2))

plt.tight_layout()

# ───────────────────────────────────────────────────────────────
# Mostrar gráfica en Streamlit
# ──────────────────────────────────────────────────────────────
st.pyplot(fig)

# ───────────────────────────────────────────────────────────────
# Interpretación económica
# ──────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 📚 Interpretación Económica")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**🟢 Curva Original (Fija)**")
    st.markdown(f"""
    - Ecuación: **π = {a}/u + {b}**
    - Representa la relación de corto plazo entre inflación y desempleo
    - El **punto negro** se mueve a lo largo de esta curva
    - **Inflación esperada (πe)** = {b:.1f}%
    """)
    
    if u_punto < 4:
        st.success(f"""
        **📈 Baja desempleo ({u_punto:.1f}%)**
        - Alta inflación: {pi_punto:.2f}%
        - Economía sobrecalentada
        """)
    elif u_punto > 6:
        st.warning(f"""
        **📉 Alto desempleo ({u_punto:.1f}%)**
        - Baja inflación: {pi_punto:.2f}%
        - Economía en recesión
        """)
    else:
        st.info(f"""
        **⚖️ Desempleo moderado ({u_punto:.1f}%)**
        - Inflación: {pi_punto:.2f}%
        """)

with col2:
    st.markdown("**🔵 Curva Desplazada (Punteada)**")
    st.markdown(f"""
    - Desplazamiento: Δu = {delta_u:+.1f}, Δπ = {delta_pi:+.1f}
    """)
    
    if delta_pi > 0:
        st.error(f"""
        **️ Desplazamiento hacia arriba**
        - Aumento de inflación esperada
        - Shock de oferta negativo
        - La curva se desplaza **arriba/derecha**
        """)
    elif delta_pi < 0:
        st.success(f"""
        **⬇️ Desplazamiento hacia abajo**
        - Disminución de inflación esperada
        - Shock de oferta positivo
        - La curva se desplaza **abajo/izquierda**
        """)
    else:
        st.info("➡️ Sin desplazamiento vertical")
    
    if delta_u > 0:
        st.markdown(f"**→ Desplazamiento derecho de {delta_u:+.1f}**")
    elif delta_u < 0:
        st.markdown(f"**← Desplazamiento izquierdo de {delta_u:+.1f}**")
    else:
        st.markdown("➡️ Sin desplazamiento horizontal")

# ───────────────────────────────────────────────────────────────
# Escenarios predefinidos
# ──────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 🎯 Escenarios de Política Económica")

scenario = st.selectbox(
    "Selecciona un escenario:",
    ["Selecciona...",
     "1. Aumento de Inflación Esperada",
     "2. Disminución de Inflación Esperada",
     "3. Shock de Oferta Negativo",
     "4. Shock de Oferta Positivo",
     "5. Política Contractiva (↑ desempleo)",
     "6. Política Expansiva (↓ desempleo)"]
)

if scenario == "1. Aumento de Inflación Esperada":
    st.info("📈 **Aumento de πe:** Los agentes esperan mayor inflación")
    st.markdown("- La curva se desplaza **hacia arriba** (Δπ = +2.0)")
    st.markdown("- Para mismo desempleo, mayor inflación")
    st.markdown("- **Ejemplo:** Indexación salarial")
    
elif scenario == "2. Disminución de Inflación Esperada":
    st.success(" **Disminución de πe:** Credibilidad del banco central")
    st.markdown("- La curva se desplaza **hacia abajo** (Δπ = -2.0)")
    st.markdown("- Para mismo desempleo, menor inflación")
    st.markdown("- **Ejemplo:** Política monetaria creíble")
    
elif scenario == "3. Shock de Oferta Negativo":
    st.error("⚠️ **Shock negativo:** ↑ precios del petróleo")
    st.markdown("- La curva se desplaza **arriba/derecha** (Δu = +1.5, Δπ = +2.0)")
    st.markdown("- **Estanflación:** ↑ inflación y ↑ desempleo")
    
elif scenario == "4. Shock de Oferta Positivo":
    st.success("✅ **Shock positivo:** Avance tecnológico")
    st.markdown("- La curva se desplaza **abajo/izquierda** (Δu = -1.5, Δπ = -2.0)")
    st.markdown("- **Mejor escenario:** ↓ inflación y ↓ desempleo")
    
elif scenario == "5. Política Contractiva (↑ desempleo)":
    st.warning("📉 **Política contractiva:** Reducir inflación")
    st.markdown("- Mover el punto negro hacia la **derecha** (↑u)")
    st.markdown("- Ejemplo: u = 7.0 → π baja")
    st.markdown("- **Costo:** Mayor desempleo")
    
elif scenario == "6. Política Expansiva (↓ desempleo)":
    st.info("📈 **Política expansiva:** Reducir desempleo")
    st.markdown("- Mover el punto negro hacia la **izquierda** (↓u)")
    st.markdown("- Ejemplo: u = 2.0 → π sube")
    st.markdown("- **Costo:** Mayor inflación")

# ───────────────────────────────────────────────────────────────
# Ecuación
# ──────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 📐 Ecuación de la Curva de Phillips")

st.latex(rf"\pi = \frac{{{a}}}{{u}} + {b}")

st.markdown(f"""
**Donde:**
- π = Tasa de inflación
- u = Tasa de desempleo
- a = {a} (parámetro de forma)
- b = {b} (inflación esperada / base)

**Punto actual sobre la curva:**
- u = {u_punto:.1f}%
- π = {pi_punto:.2f}%
""")

# ───────────────────────────────────────────────────────────────
# Explicación del trade-off
# ──────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("###  Trade-off Inflación-Desempleo")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**📉 Bajo desempleo**")
    st.markdown("u < 4%")
    st.markdown("π alta")
    st.markdown("Economía sobrecalentada")

with col2:
    st.markdown("**⚖️ NAIRU**")
    st.markdown("u ≈ 4-5%")
    st.markdown("π estable")
    st.markdown("Equilibrio de largo plazo")

with col3:
    st.markdown("**📈 Alto desempleo**")
    st.markdown("u > 6%")
    st.markdown("π baja")
    st.markdown"Recesión económica")
