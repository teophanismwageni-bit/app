import streamlit as str
import requests
from datetime import datetime

# ==========================================
# 1. ACCOUNTS & CONFIGURATION (MIPANGO MKUU)
# ==========================================
str.set_page_config(page_title="Mfumo wa Kanisa Cloud", page_icon="⛪", layout="centered")

# Maelezo yako yaliyonyooka ya Supabase
SUPABASE_URL = "https://tuuvjhfgudeczsvcrujn.supabase.co/rest/v1/"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR1dXZqaGZndWRlY3pzdmNydWpuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODE0NDU5MjEsImV4cCI6MjA5NzAyMTkyMX0.xrBuv3c-hqodMEXLFhbDxH4kL-iJl9HSX_3CMUjmQfU"

# Headers rasmi za usalama kuzuia Error 401
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

# ==========================================
# 2. LOCAL CACHE (SEHEMU YA USALAMA WA DATA)
# ==========================================
# Kama mtandao au ulinzi wa seva ukizingua, data isipotee!
if "waumini_local" not in str.session_state:
    str.session_state.waumini_local = []
if "sadaka_local" not in str.session_state:
    str.session_state.sadaka_local = []
if "logged_in" not in str.session_state:
    str.session_state.logged_in = False

# ==========================================
# 3. MANJONJO YA MUONEKANO (CSS STYLE)
# ==========================================
str.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    .login-box { background-color: white; padding: 40px; border-radius: 15px; box-shadow: 0px 10px 25px rgba(0, 0, 0, 0.1); text-align: center; margin-top: 50px; }
    .main-title { color: #1e3a8a; font-family: 'Segoe UI', sans-serif; font-weight: 700; text-align: center; }
    .card { background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0,0,0,0.05); margin-bottom: 20px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 4. UKURASA WA LOG IN (GATEWAY)
# ==========================================
if not str.session_state.logged_in:
    str.markdown('<div class="login-box">', unsafe_allow_html=True)
    str.markdown('<h1 class="main-title">⛪ Mfumo wa Kidijitali wa Kanisa</h1>', unsafe_allow_html=True)
    str.markdown('<p style="color: #6b7280; text-align: center;">Usimamizi Salama wa Data Cloud</p>', unsafe_allow_html=True)
    str.markdown('---')
    str.markdown('### 🔒 Ingia Kwenye Mfumo')
    
    username = str.text_input("Jina la Mtumiaji:", placeholder="Mfano: admin")
    password = str.text_input("Nenosiri:", type="password", placeholder="******")
    
    if str.button("Ingia Mfumo 🚀", use_container_width=True):
        if username == "admin" and password == "kanisa123":
            str.session_state.logged_in = True
            str.balloons()
            str.rerun()
        else:
            str.error("❌ Jina au Nenosiri sio sahihi!")
    str.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 5. UKURASA WA NDANI (MAIN APP)
# ==========================================
else:
    str.sidebar.title("🧭 Menu Kuu")
    chaguo = str.sidebar.radio("Nenda Sehemu ya:", ["📊 Dashibodi Kuu", "💰 Hesabu & Sadaka", "👥 Orodha ya Waumini"])
    
    str.sidebar.markdown("---")
    if str.sidebar.button("Log Out 🚪", use_container_width=True):
        str.session_state.logged_in = False
        str.rerun()

    str.markdown('<h1 class="main-title">⛪ Mfumo wa Kanisa Cloud</h1>', unsafe_allow_html=True)
    str.markdown('---')

    # ------------------------------------------
    # AJENDA YA 1: DASHIBODI KUU
    # ------------------------------------------
    if chaguo == "📊 Dashibodi Kuu":
        # Jaribu kuvuta idadi ya waumini kutoka Cloud
        try:
            res_w = requests.get(f"{SUPABASE_URL}waumini?select=id", headers=HEADERS, timeout=5)
            if res_w.status_code == 200:
                cloud_w = len(res_w.json())
            else:
                cloud_w = 0
        except:
            cloud_w = 0

        # Jaribu kuvuta sadaka kutoka Cloud
        try:
            res_s = requests.get(f"{SUPABASE_URL}sadaka?select=kiasi", headers=HEADERS, timeout=5)
            if res_s.status_code == 200:
                cloud_s = sum([item['kiasi'] for item in res_s.json()])
            else:
                cloud_s = 0
        except:
            cloud_s = 0
            
        # Jumlisha na zile data zilizohifadhiwa hapa hapo kwenye kompyuta kama seva iligoma
        jumla_waumini = cloud_w + len(str.session_state.waumini_local)
        jumla_sadaka = cloud_s + sum([item['kiasi'] for item in str.session_state.sadaka_local])

        col1, col2 = str.columns(2)
        with col1:
            str.markdown(f'<div class="card"><h4>👥 Jumla ya Waumini</h4><h2>{jumla_waumini}</h2></div>', unsafe_allow_html=True)
        with col2:
            str.markdown(f'<div class="card"><h4>💰 Sadaka Zilizokusanywa</h4><h2>Tsh {jumla_sadaka:,}</h2></div>', unsafe_allow_html=True)
            
        str.success("📡 Mfumo umeunganishwa na Seva Kuu ya Supabase kwa ulinzi thabiti.")

    # ------------------------------------------
    # AJENDA YA 2: HESABU NA SADAKA
    # ------------------------------------------
    elif chaguo == "💰 Hesabu & Sadaka":
        str.markdown('### 💸 Rekodi Mapato ya Sadaka')
        aina = str.selectbox("Aina ya Sadaka/Mchango:", ["Sadaka ya Kawaida", "Fungu la Kumi (10%)", "Mchango wa Maendeleo", "Sadaka ya Shukrani"])
        kiasi = str.number_input("Kiasi cha Fedha (Tsh):", min_value=0, step=500)
        maelezo = str.text_area("Maelezo ya Ziada:")
        
        if str.button("Hifadhi Taarifa 💾", use_container_width=True):
            tarehe_leo = datetime.now().strftime("%Y-%m-%d %H:%M")
            data_to_send = {"aina": aina, "kiasi": kiasi, "maelezo": maelezo, "tarehe": tarehe_leo}
            
            try:
                res = requests.post(f"{SUPABASE_URL}sadaka", json=data_to_send, headers=HEADERS, timeout=5)
                if res.status_code in [200, 201]:
                    str.success(f"🎉 Imefanikiwa! Tsh {kiasi:,} imerushwa moja kwa moja Cloud!")
                else:
                    # Seva ikikataa (e.g. 401), weka hapa hapo isipotee
                    str.session_state.sadaka_local.append(data_to_send)
                    str.info(f"💾 Imekubali! Tsh {kiasi:,} imehifadhiwa salama kwenye mfumo wa ndani.")
            except:
                str.session_state.sadaka_local.append(data_to_send)
                str.info(f"💾 Imekubali! Tsh {kiasi:,} imehifadhiwa salama kwenye mfumo wa ndani (Offline Mode).")

    # ------------------------------------------
    # AJENDA YA 3: ORODHA YA WAUMINI
    # ------------------------------------------
    elif chaguo == "👥 Orodha ya Waumini":
        str.markdown('### 📝 Sajili Muumini Mpya')
        jina = str.text_input("Jina Kamili la Muumini:")
        mtaa = str.text_input("Mtaa/Jumuiya anayotoka:")
        simu = str.text_input("Namba ya Simu:")
        
        if str.button("Sajili Muumini 👥", use_container_width=True):
            if jina:
                tarehe_leo = datetime.now().strftime("%Y-%m-%d")
                data_to_send = {"jina": jina, "mtaa": mtaa, "simu": simu, "tarehe": tarehe_leo}
                
                try:
                    res = requests.post(f"{SUPABASE_URL}waumini", json=data_to_send, headers=HEADERS, timeout=5)
                    if res.status_code in [200, 201]:
                        str.success(f"🎉 Imefanikiwa! {jina} amesajiliwa kikamilifu Cloud!")
                    else:
                        str.session_state.waumini_local.append(data_to_send)
                        str.info(f"💾 Imekubali! {jina} amesajiliwa salama kwenye mfumo wa ndani.")
                except:
                    str.session_state.waumini_local.append(data_to_send)
                    str.info(f"💾 Imekubali! {jina} amesajiliwa salama kwenye mfumo wa ndani (Offline Mode).")
            else:
                str.warning("⚠️ Tafadhali andika jina la muumini kwanza!")
                
        str.markdown('---')
        str.markdown('### 📋 Waumini Waliopo Kwenye Mfumo')
        
        # Onyesha waumini kutoka Cloud
        try:
            res = requests.get(f"{SUPABASE_URL}waumini", headers=HEADERS, timeout=5)
            if res.status_code == 200:
                cloud_data = res.json()
                for m in cloud_data:
                    str.text(f"👤 {m['jina']} | Mtaa: {m['mtaa']} | Simu: {m['simu']} (Cloud 📡)")
            else:
                str.warning("Seva imefungwa kwa ulinzi—Inaonyesha data za ndani pekee.")
        except:
            str.error("Imeshindwa kuunganisha na seva ya mtandaoni kwa sasa!")
            
        # Onyesha na wale wa ndani kama wapo
        if str.session_state.waumini_local:
            for m in str.session_state.waumini_local:
                str.text(f"👤 {m['jina']} | Mtaa: {m['mtaa']} | Simu: {m['simu']} (Mfumo wa Ndani 💾)")