import streamlit as st
import os
import google.generativeai as genai

# ======================================================
# CONFIGURATION (SECURE & UPDATED)
# ======================================================

# This pulls from your .streamlit/secrets.toml file
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    # Fallback for local testing if secrets aren't set yet
    API_KEY = "YOUR_NEW_KEY_HERE" 

genai.configure(api_key=API_KEY)

# ======================================================
# PAGE SETUP
# ======================================================

st.set_page_config(page_title="CogniTrack Dashboard", layout="centered")
st.title("🧠 CogniTrack – Cognitive Stress Tracker")

st.markdown("""
**Multimodal cognitive load estimation**

Combines:
- 👁️ Eye / blink behaviour  
- 🖥️ Screen content complexity  
- 🤖 AI reasoning for stress & intervention
""")

st.divider()

# ======================================================
# BLINK INPUT (MANUAL – PROTOTYPE)
# ======================================================

st.subheader("👁️ Eye / Blink Signal (Manual)")

blink_rate = st.slider(
    "Blink rate (blinks per minute)",
    min_value=5,
    max_value=30,
    value=15
)

if blink_rate >= 15:
    blink_state = "NORMAL"
elif blink_rate >= 11:
    blink_state = "REDUCED"
else:
    blink_state = "LOW"

st.caption(f"Eye activity state: **{blink_state}**")

st.divider()

# ======================================================
# SCREEN CONTEXT INPUT (MANUAL – PROTOTYPE)
# ======================================================

st.subheader("🖥️ Screen Context (Manual)")

screen_load = st.selectbox(
    "Screen cognitive load level",
    ["LOW", "MEDIUM", "HIGH"]
)

screen_reason = st.text_input(
    "Reason (from screen analysis)",
    value="High text density and multiple windows open"
)

st.divider()

# ======================================================
# AI FUSION: BLINK + SCREEN → FINAL STRESS
# ======================================================

st.subheader("🧠 Cognitive Stress Assessment")

def get_final_stress(blink_rate, blink_state, screen_load, screen_reason):
    # FIXED: Using gemini-1.5-flash instead of deprecated gemini-pro
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
    Eye / Blink data:
    - Blink rate: {blink_rate} blinks per minute
    - Eye activity state: {blink_state}

    Screen context:
    - Screen load level: {screen_load}
    - Reason: {screen_reason}

    Based on BOTH signals, return ONLY:
    1. Final cognitive stress level (LOW / MEDIUM / HIGH)
    2. One-sentence explanation
    3. One practical suggestion
    """

    response = model.generate_content(prompt)
    return response.text.strip()

if st.button("Generate Cognitive Stress Result"):
    with st.spinner("AI is consolidating signals..."):
        try:
            result = get_final_stress(
                blink_rate,
                blink_state,
                screen_load,
                screen_reason
            )
            st.success("Final Cognitive Stress Result")
            st.write(result)
        except Exception as e:
            st.error(f"An error occurred: {e}")

st.divider()

# ======================================================
# PRIVACY NOTE
# =====================================
st.caption(
    "🔒 Privacy-first design: inputs are manually provided for the prototype. "
    "No continuous monitoring or storage. Sensors and AI layers are modular."
)


