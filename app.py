import streamlit as st
import time
from pathlib import Path
import base64
import random

st.set_page_config(page_title="Happy Birthday Komal", layout="centered", initial_sidebar_state="collapsed")

# Initialize Session State
if 'view' not in st.session_state:
    st.session_state.view = 'home'
if 'hidden_star_revealed' not in st.session_state:
    st.session_state.hidden_star_revealed = False

# --- Custom Cursor Base64 ---
# A small elegant glowing dot cursor
cursor_svg = """<svg width="24" height="24" xmlns="http://www.w3.org/2000/svg">
  <circle cx="12" cy="12" r="4" fill="#c7d2fe" filter="drop-shadow(0 0 4px #a5b4fc)"/>
</svg>"""
cursor_b64 = base64.b64encode(cursor_svg.encode()).decode()

# --- CSS Injection ---
st.markdown(f"""
<style>
/* Font Imports */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@300;400;500&family=Dancing+Script:wght@600&display=swap');

/* Hide Defaults */
#MainMenu {{visibility: hidden;}}
header {{visibility: hidden;}}
footer {{visibility: hidden;}}
div[data-testid="stToolbar"] {{visibility: hidden;}}
div[data-testid="stDecoration"] {{visibility: hidden;}}

/* Custom Cursor */
* {{
    cursor: url(data:image/svg+xml;base64,{cursor_b64}) 12 12, auto !important;
}}

/* Fix padding */
.main .block-container {{
    padding-top: 1rem;
    padding-bottom: 1rem;
    max-width: 800px;
    z-index: 10;
}}

/* Background Animation */
.stApp {{
    background: linear-gradient(135deg, #09090b 0%, #151520 50%, #0a1118 100%);
    color: #e2e8f0;
    font-family: 'Inter', sans-serif;
    overflow-x: hidden;
}}

/* Floating Background Orbs for Interactive Feel */
.bg-orb {{
    position: fixed;
    border-radius: 50%;
    filter: blur(90px);
    z-index: 0;
    pointer-events: none;
    animation: drift 20s infinite ease-in-out alternate;
}}
.orb-1 {{ top: 10%; left: 10%; width: 350px; height: 350px; background: rgba(99, 102, 241, 0.12); animation-delay: 0s; }}
.orb-2 {{ bottom: 10%; right: 10%; width: 450px; height: 450px; background: rgba(236, 72, 153, 0.08); animation-delay: -5s; }}
.orb-3 {{ top: 40%; left: 50%; width: 250px; height: 250px; background: rgba(167, 139, 250, 0.1); animation-delay: -10s; }}

@keyframes drift {{
    0% {{ transform: translate(0px, 0px) scale(1); }}
    100% {{ transform: translate(50px, -50px) scale(1.1); }}
}}

/* Animations */
@keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(15px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}
.fade-in {{ animation: fadeIn 1.2s cubic-bezier(0.2, 0.8, 0.2, 1) forwards; opacity: 0; }}
.delay-1 {{ animation-delay: 0.3s; }}
.delay-2 {{ animation-delay: 0.6s; }}
.delay-3 {{ animation-delay: 0.9s; }}
.delay-4 {{ animation-delay: 1.2s; }}

/* Text Reveal Animation for Letter */
@keyframes revealText {{
    from {{ opacity: 0; transform: translateY(10px); filter: blur(4px); }}
    to {{ opacity: 1; transform: translateY(0); filter: blur(0px); }}
}}
.reveal-p1 {{ animation: revealText 1.5s ease-out forwards; animation-delay: 0.5s; opacity: 0; }}
.reveal-p2 {{ animation: revealText 1.5s ease-out forwards; animation-delay: 2.0s; opacity: 0; }}
.reveal-p3 {{ animation: revealText 1.5s ease-out forwards; animation-delay: 3.5s; opacity: 0; }}
.reveal-p4 {{ animation: revealText 1.5s ease-out forwards; animation-delay: 5.0s; opacity: 0; }}
.reveal-p5 {{ animation: revealText 1.5s ease-out forwards; animation-delay: 6.5s; opacity: 0; }}
.reveal-p6 {{ animation: revealText 1.5s ease-out forwards; animation-delay: 8.0s; opacity: 0; }}

/* Typography */
.text-center {{ 
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    width: 100%;
}}
.hero-title {{
    font-family: 'Playfair Display', serif;
    font-size: 4.5rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    background: linear-gradient(to right, #ffffff, #c7d2fe);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0; padding: 0;
    text-align: center;
}}
.hero-subtitle {{
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 400;
    color: #cbd5e1;
    margin: 0 0 1.5rem 0;
    text-align: center;
}}
.hero-quote {{
    font-family: 'Inter', sans-serif;
    font-size: 1.05rem;
    color: #94a3b8;
    font-weight: 300;
    max-width: 500px;
    margin: 0 auto 3rem auto;
    line-height: 1.6;
    text-align: center;
}}

/* Badges & Cards */
.badge-container {{
    display: flex;
    justify-content: center;
    margin-bottom: 2rem;
}}
.badge {{
    padding: 0.4rem 1.2rem;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 50px;
    font-size: 0.8rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #cbd5e1;
    backdrop-filter: blur(10px);
}}

.glass-card {{
    background: rgba(20, 20, 28, 0.4);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 20px;
    padding: 1.5rem;
    box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.5);
    margin: 0.5rem 0;
    position: relative;
    z-index: 10;
}}

/* Streamlit Button Overrides */
.stButton > button {{
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    color: #f8fafc;
    font-family: 'Inter', sans-serif;
    font-weight: 400;
    letter-spacing: 0.05em;
    padding: 1.5rem;
    transition: all 0.4s cubic-bezier(0.2, 0.8, 0.2, 1);
    width: 100%;
}}
.stButton > button:hover {{
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(255, 255, 255, 0.3);
    transform: translateY(-3px);
    box-shadow: 0 10px 25px -10px rgba(99, 102, 241, 0.3);
    color: #fff;
}}

/* Home button specific completely top left */
span.home-btn-anchor {{ display: none; }}
div.element-container:has(.home-btn-anchor) + div.element-container {{
    position: fixed !important;
    top: 20px !important;
    left: 20px !important;
    width: auto !important;
    z-index: 99999 !important;
}}
div.element-container:has(.home-btn-anchor) + div.element-container button {{
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: #64748b !important;
    font-size: 0.9rem !important;
    padding: 0.5rem !important;
    margin: 0 !important;
    transform: none !important;
}}
div.element-container:has(.home-btn-anchor) + div.element-container button:hover {{
    color: #e2e8f0 !important;
    background: rgba(255, 255, 255, 0.05) !important;
}}

/* Memories Gallery */
.gallery-img-container {{
    width: 100%;
    padding-top: 125%; /* 4:5 Aspect Ratio */
    position: relative;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 10px 30px -5px rgba(0,0,0,0.3);
    border: 1px solid rgba(255, 255, 255, 0.05);
    transition: all 0.5s ease;
    margin-bottom: 1.5rem;
}}
.gallery-img-container:hover {{
    transform: translateY(-8px);
    box-shadow: 0 20px 40px -5px rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.15);
}}
.gallery-img-container img {{
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    object-fit: contain;
    background: rgba(0, 0, 0, 0.2);
}}

/* Quote Card */
.quote-card {{
    text-align: center;
    padding: 1.5rem;
    border-top: 1px solid rgba(255,255,255,0.1);
    border-bottom: 1px solid rgba(255,255,255,0.1);
    margin: 1.5rem 0;
}}
.quote-text {{
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    font-style: italic;
    color: #e2e8f0;
    line-height: 1.4;
    margin-bottom: 1rem;
}}

/* Letter */
.letter-text {{
    font-family: 'Inter', sans-serif;
    font-size: 1.1rem;
    line-height: 1.8;
    color: #d1d5db;
    font-weight: 300;
    text-align: center;
}}
.letter-text p {{ margin-bottom: 0.8rem; }}
.handwritten {{
    font-family: 'Dancing Script', cursive;
    font-size: 2.5rem;
    color: #c7d2fe;
}}

/* Hidden Star */
.hidden-star-btn {{
    text-align: center;
    margin-top: 2rem;
}}
</style>

<!-- Inject Floating Background Orbs -->
<div class="bg-orb orb-1"></div>
<div class="bg-orb orb-2"></div>
<div class="bg-orb orb-3"></div>

<!-- Ambient Music Player (Hidden UI, Soft Volume) -->
<audio id="ambient-music" autoplay loop style="display: none;">
    <source src="https://assets.mixkit.co/music/preview/mixkit-beautiful-dream-493.mp3" type="audio/mpeg">
</audio>
<script>
    var audio = document.getElementById("ambient-music");
    audio.volume = 0.3; 
    // Auto-play is often blocked by browsers until user interaction.
    document.body.addEventListener('click', function() {{
        if(audio.paused) {{ audio.play(); }}
    }}, {{ once: true }});
</script>
""", unsafe_allow_html=True)

# Helper function to render base64 image
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return ""

def nav_to(view_name):
    st.session_state.view = view_name

# ----------------- HOME VIEW -----------------
if st.session_state.view == 'home':
    st.markdown("""
        <div class="badge-container fade-in delay-1">
            <span class="badge">🎂 IT'S YOUR DAY</span>
        </div>
        <div class="text-center fade-in delay-2">
            <h1 class="hero-title">KOMAL</h1>
            <h2 class="hero-subtitle">Happy Birthday</h2>
            <p class="hero-quote">"Talking to you is always nice."</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    col_spacer1, col1, col2, col_spacer2 = st.columns([1, 1.5, 1.5, 1], gap="medium")
    with col1:
        if st.button("📸 OPEN MEMORIES", key="btn_mem"):
            nav_to('memories')
            st.rerun()
    with col2:
        if st.button("📝 OPEN LETTER", key="btn_let"):
            nav_to('letter')
            st.rerun()

# ----------------- MEMORIES VIEW -----------------
elif st.session_state.view == 'memories':
    st.markdown("<span class='home-btn-anchor'></span>", unsafe_allow_html=True)
    if st.button("🏠 HOME", key="btn_home_mem"):
        nav_to('home')
        st.rerun()
    
    st.markdown("<h2 class='text-center fade-in' style='margin-bottom:1.5rem; font-family:Playfair Display;'>✨ Some Moments Worth Keeping ✨</h2>", unsafe_allow_html=True)
    
    # Image discovery
    images_dir = Path("images")
    valid_exts = {".jpg", ".jpeg", ".png", ".webp"}
    image_paths = []
    
    if images_dir.exists():
        image_paths = [p for p in images_dir.iterdir() if p.suffix.lower() in valid_exts]
    
    if not image_paths:
        # Empty state
        st.markdown("""
            <div class='glass-card fade-in delay-1 text-center'>
                <h3 style='color: #cbd5e1; font-weight:300;'>A space waiting for memories.</h3>
                <p style='color: #64748b; font-size: 0.9rem;'>Please add images to the `images/` directory.</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Gallery Layout using columns
        cols = st.columns(3)
        for i, img_path in enumerate(image_paths):
            b64_img = get_base64_image(img_path)
            col_idx = i % 3
            with cols[col_idx]:
                st.markdown(f"""
                    <div class='gallery-img-container fade-in delay-{min(i%4 + 1, 4)}'>
                        <img src="data:image/jpeg;base64,{b64_img}" alt="Memory {i}">
                    </div>
                """, unsafe_allow_html=True)
                
    # Quote Card
    st.markdown("""
        <div class="quote-card fade-in delay-3">
            <div class="quote-text">"Thanks for being there, Time is the best thing you can give to someone."</div>
        </div>
    """, unsafe_allow_html=True)
    



# ----------------- LETTER VIEW -----------------
elif st.session_state.view == 'letter':
    st.markdown("<span class='home-btn-anchor'></span>", unsafe_allow_html=True)
    if st.button("🏠 HOME", key="btn_home_let"):
        nav_to('home')
        st.rerun()

    st.markdown("""
        <div class='glass-card fade-in'>
            <div class='handwritten fade-in' style='margin-bottom: 2rem;'>Dear Komal,</div>
            <div class='letter-text'>
                <p>I don’t really know how to start this, but I just wanted to say something that’s been on my mind.</p>
                <p>You’re genuinely one of the easiest people to talk to. It felt natural talking to you. Whether it was something important or complete nonsense, talking to you was always nice.</p>
                <p>I still remember you saying, <em>“If something ever bothers you, you can always talk to me.”</em> Maybe you don't even remember saying it, but I do. It wasn't some life-changing moment or anything dramatic, it just felt nice knowing someone genuinely meant it.</p>
                <p>Since it's your birthday, I just wanted to take the chance to say all of this. I hope this year brings you a lot of good memories, people who make you happy, and plenty of moments that make you smile.</p>
            </div>
            <div class='handwritten fade-in' style='text-align: right; margin-top: 3rem;'>Happy Birthday</div>
            <div class='handwritten fade-in' style='text-align: right; font-size: 1.8rem; margin-top: -10px;'>— Rajveer</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Hidden Surprise
    col_empty1, col_star, col_empty2 = st.columns([4,1,4])
    with col_star:
        # Using a very basic Streamlit button for the star
        st.markdown("<div style='text-align: center; animation: revealText 2s ease forwards; opacity: 0;'>", unsafe_allow_html=True)
        if st.button("⭐", key="btn_star"):
            st.session_state.hidden_star_revealed = True
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
            
    if st.session_state.hidden_star_revealed:
        st.markdown("""
            <div class='text-center fade-in' style='margin-top: 1rem; color: #a5b4fc; font-family: Playfair Display; font-style: italic;'>
                "Thank you for being exactly the kind of friend people are lucky to find."
            </div>
        """, unsafe_allow_html=True)
    
    st.write("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
            

