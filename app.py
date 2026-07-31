import streamlit as st
from pathlib import Path
import base64
import html
import random

st.set_page_config(page_title="Happy Birthday Komal", layout="centered", initial_sidebar_state="collapsed")

# Initialize Session State
if 'view' not in st.session_state:
    st.session_state.view = 'home'

# --- Global Scroll Settings ---
st.markdown("""
    <style>
    /* Hide the scrollbar but keep Streamlit's native scrolling active */
    * { 
        scrollbar-width: none !important; 
        -ms-overflow-style: none !important; 
    } 
    *::-webkit-scrollbar { 
        display: none !important; 
    }
    
    /* Ensure no container blocks pointer events incorrectly */
    [data-testid="stAppViewContainer"] {
        touch-action: auto !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- CSS Injection ---
st.markdown("""
<style>
/* Font Imports */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@700&family=Outfit:wght@700;800&family=Inter:wght@300;400;500;600&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Dancing+Script:wght@600&display=swap');

/* Hide Defaults */
#MainMenu {visibility: hidden !important;}
header {visibility: hidden !important;}
footer {visibility: hidden !important;}
div[data-testid="stToolbar"] {visibility: hidden !important;}
div[data-testid="stDecoration"] {visibility: hidden !important;}
div[data-testid="stStatusWidget"] {visibility: hidden !important;}

/* Fix padding for all views */
.main .block-container {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
    margin-top: -3rem !important;
    max-width: 1200px;
    z-index: 10;
}

/* Static champagne background */
.stApp {
    background: linear-gradient(135deg, #EEE7D8 0%, #E8DECA 45%, #E1D4B9 100%) !important;
    background-attachment: fixed !important;
    color: #3F3F46;
    font-family: 'Inter', sans-serif;
}

.stApp::before {
    content: '';
    position: fixed;
    top: 50%; left: 50%; width: 100vw; height: 100vh;
    transform: translate(-50%, -50%);
    background: radial-gradient(circle at 50% 45%, rgba(255, 250, 238, 0.14) 0%, transparent 55%);
    pointer-events: none;
    z-index: 0;
}

.stApp::after {
    content: '';
    position: fixed;
    top: 0; left: 0; width: 100vw; height: 100vh;
    background: radial-gradient(circle at 50% 50%, transparent 60%, rgba(150, 110, 45, 0.14) 150%);
    pointer-events: none;
    z-index: 9999;
}

/* Typography for Home Hero */
.hero-wrapper {
    position: relative;
    z-index: 10;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    margin-top: -2rem; /* Force content upwards */
    gap: 1rem;
    
    /* Stronger Glassmorphism */
    background: rgba(255, 250, 244, 0.88);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(199, 154, 45, 0.15);
    border-radius: 32px;
    padding: 2rem 1.5rem 0.8rem 1.5rem; /* Reduced height by ~50px */
    box-shadow: 0 20px 60px rgba(183, 134, 11, 0.10);
    animation: fadeIn 3s ease-out forwards, cardFloat 7s 3s ease-in-out infinite alternate;
}

.hero-wrapper::before {
    content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background: linear-gradient(135deg, rgba(255,252,244,0.45) 0%, transparent 50%, rgba(199,154,45,0.08) 100%);
    border-radius: 32px; z-index: -1; pointer-events: none;
}

.badge-pill {
    padding: 0.6rem 1.8rem;
    background: rgba(255, 250, 244, 0.88);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(199, 154, 45, 0.22);
    border-radius: 50px;
    font-family: 'Inter', sans-serif;
    font-size: 0.9rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #B8860B;
    box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.7), 0 6px 18px rgba(183, 134, 11, 0.10);
    animation: slideUp 1s ease-out forwards, floatBadge 6s infinite ease-in-out;
    opacity: 0;
}

@keyframes floatBadge {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-8px); }
}

.hero-title {
    font-family: 'Outfit', sans-serif;
    font-size: 68px;
    font-weight: 800;
    letter-spacing: 10px;
    text-transform: uppercase;
    margin: 0;
    padding: 0;
    line-height: 1.1;
    background: linear-gradient(180deg, #E2BC53 0%, #C89A2B 55%, #A97812 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 2px 12px rgba(199, 154, 45, 0.18);
    position: relative;
    z-index: 1;
    animation: fadeIn 4s ease forwards;
}

.hero-subtitle {
    font-family: 'Poppins', sans-serif;
    font-size: 56px;
    font-weight: 700;
    margin: 0;
    padding: 0;
    position: relative;
    z-index: 1;
    background: linear-gradient(180deg, #E2BC53 0%, #C89A2B 55%, #A97812 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 2px 10px rgba(199, 154, 45, 0.15);
    animation: slideUp 2s ease-out forwards;
}

.hero-quote {
    font-family: 'Inter', sans-serif;
    font-style: italic;
    font-size: 1.1rem;
    color: #5F6673;
    font-weight: 300;
    margin: 1rem 0 2rem 0;
    opacity: 0.9;
    animation: fadeIn 5s ease-out forwards;
}

/* Primary Buttons */
.st-key-btn_mem button,
.st-key-btn_let button {
    background: linear-gradient(180deg, #D7AA38 0%, #C79624 100%) !important;
    border: 1px solid rgba(199, 154, 45, 0.35) !important;
    border-radius: 28px !important;
    padding: 0 !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    color: #ffffff !important;
    cursor: pointer !important;
    box-shadow: inset 0 1px 0 rgba(255, 250, 235, 0.32), 0 10px 30px rgba(183, 134, 11, 0.18) !important;
    transition: all 0.4s cubic-bezier(0.2, 0.8, 0.2, 1) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 0.6rem !important;
    width: 236px !important;
    height: 72px !important;
    max-width: 100% !important;
    margin: 0 auto !important;
}

.st-key-btn_mem button:hover,
.st-key-btn_let button:hover {
    background: linear-gradient(180deg, #C79624 0%, #B8860B 100%) !important;
    border-color: rgba(184, 134, 11, 0.55) !important;
    transform: translateY(-2px) !important;
    box-shadow: inset 0 1px 0 rgba(255, 250, 235, 0.38), 0 12px 32px rgba(183, 134, 11, 0.22) !important;
    color: #ffffff !important;
}

.st-key-btn_mem button p,
.st-key-btn_let button p,
.st-key-btn_mem button span,
.st-key-btn_let button span {
    color: #ffffff !important;
    margin: 0 !important;
    font-size: 1.1rem !important;
    font-weight: 500 !important;
}

/* Animations */
@keyframes slideUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

/* Cards drift by a couple of pixels so the page feels alive but settled */
@keyframes cardFloat {
    from { transform: translateY(0); }
    to { transform: translateY(-3px); }
}

/* Decorative Elements */
.decor-container { position: fixed; width: 100vw; height: 100vh; top: 0; left: 0; pointer-events: none; overflow: hidden; z-index: 5; }
.decor { position: absolute; opacity: var(--decor-opacity, 0.5); animation: twinkleFloat 4.5s infinite ease-in-out alternate; filter: sepia(0.5) saturate(1.4) hue-rotate(-14deg); }

/* Mostly a soft opacity pulse with a hint of drift */
@keyframes twinkleFloat {
    0% { transform: translateY(0) scale(0.97); opacity: calc(var(--decor-opacity, 0.5) * 0.55); }
    100% { transform: translateY(-5px) scale(1.03); opacity: var(--decor-opacity, 0.5); }
}

/* The moon drifts slowly instead of twinkling */
.decor.decor-moon { animation: moonFloat 9s infinite ease-in-out alternate; }

@keyframes moonFloat {
    from { transform: translateY(0); }
    to { transform: translateY(-6px); }
}

/* Paper grain */
.paper-grain {
    position: fixed;
    top: 0; left: 0; width: 100vw; height: 100vh;
    pointer-events: none;
    z-index: 1;
    opacity: 0.02;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='paperNoise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='140' height='140' filter='url(%23paperNoise)'/%3E%3C/svg%3E");
    background-repeat: repeat;
    background-size: 140px 140px;
}

/* Responsive */
@media (max-width: 768px) {
    .main .block-container { padding-left: 1rem !important; padding-right: 1rem !important; }
    .hero-wrapper { margin-top: 0; padding: 2rem 1rem 1rem 1rem; border-radius: 24px; }
    .hero-title { font-size: clamp(2.4rem, 12vw, 48px); letter-spacing: 6px; }
    .hero-subtitle { font-size: clamp(1.7rem, 8.5vw, 36px); }
    .hero-quote { font-size: 0.95rem; margin: 0.75rem 0 1.5rem 0; }
    .memories-title { font-size: 28px !important; margin-top: -2.5rem !important; }
    .letter-text { font-size: 1rem; line-height: 1.7; text-align: left; }
    .handwritten { font-size: 2rem; }
    .quote-text { font-size: 1.15rem; }
    .st-key-btn_mem button, .st-key-btn_let button { width: 100% !important; height: 64px !important; }
}

/* Stack columns into a single column on small screens */
@media (max-width: 640px) {
    div[data-testid="stHorizontalBlock"] { flex-direction: column !important; }
    div[data-testid="stColumn"], div[data-testid="column"] {
        width: 100% !important;
        flex: 1 1 100% !important;
        min-width: 100% !important;
    }
}

/* Existing styles for other views */
.glass-card {
    background: rgba(255, 250, 244, 0.88);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(199, 154, 45, 0.15);
    border-radius: 28px;
    padding: 1.5rem;
    box-shadow: 0 20px 60px rgba(183, 134, 11, 0.10);
    margin: 0.5rem 0;
    position: relative;
    z-index: 10;
}
/* Needs to outrank .fade-in, which also sets `animation` on this element */
.glass-card.fade-in {
    animation: fadeIn 0.6s cubic-bezier(0.2, 0.8, 0.2, 1) forwards,
               cardFloat 7s 1s ease-in-out infinite alternate;
}
/* Memories Gallery */
.gallery-section-wrapper { position: relative; width: 100%; z-index: 10; }
.gallery-bg-glow { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 100%; height: 100%; background: radial-gradient(circle, rgba(255,250,238,0.16) 0%, transparent 70%); filter: blur(60px); z-index: 0; pointer-events: none; }
.gallery-decor-container { position: absolute; width: 100%; height: 100%; top: 0; left: 0; pointer-events: none; z-index: 0; }
.gallery-decor { position: absolute; opacity: var(--decor-opacity, 0.5); animation: twinkleFloat 4.5s infinite ease-in-out alternate; filter: sepia(0.5) saturate(1.4) hue-rotate(-14deg); }

.gallery-img-container {
    width: 100%; padding-top: 135%; position: relative; border-radius: 24px;
    overflow: hidden; 
    box-shadow: 0 20px 60px rgba(183, 134, 11, 0.10);
    border: 1px solid rgba(199, 154, 45, 0.15);
    backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
    background: rgba(255, 250, 244, 0.88);
    transition: all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1); margin-bottom: 0.5rem;
    animation: gentleFloat 6s ease-in-out infinite alternate;
}
@keyframes gentleFloat {
    0% { transform: translateY(2px); }
    100% { transform: translateY(-3px); }
}
.gallery-img-container:hover { 
    transform: scale(1.04) translateY(-8px); 
    box-shadow: 0 24px 60px rgba(183, 134, 11, 0.18);
    border: 1px solid rgba(199, 154, 45, 0.38);
    animation-play-state: paused;
}
.img-blur-bg {
    position: absolute; top: -10%; left: -10%; width: 120%; height: 120%;
    background-size: cover; background-position: center;
    filter: blur(20px) brightness(1.05) saturate(1.1); z-index: 0;
}
.gallery-img-container img { position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: contain; z-index: 1; border-radius: 24px; }
.gallery-gradient-overlay { position: absolute; bottom: 0; left: 0; width: 100%; height: 40%; background: linear-gradient(to top, rgba(90, 70, 20, 0.14) 0%, transparent 100%); z-index: 2; pointer-events: none; }
.gallery-caption {
    font-family: 'Inter', sans-serif; font-size: 0.82rem; color: #6B7280;
    text-align: center; letter-spacing: 0.04em;
    margin: 0.15rem 0 1.4rem 0;
}

/* Quote & Divider */
.gradient-divider {
    height: 1px; width: 100%; max-width: 800px; margin: 0.5rem auto;
    background: linear-gradient(90deg, transparent, rgba(199, 154, 45, 0.45), transparent);
    box-shadow: none;
}
.quote-card {
    background: rgba(255, 250, 244, 0.88); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(199, 154, 45, 0.15); border-radius: 28px;
    padding: 1rem 1.5rem; margin: 0 auto 1.4rem auto; max-width: 700px;
    box-shadow: 0 20px 60px rgba(183, 134, 11, 0.10); text-align: center;
}
.quote-text { font-family: 'Playfair Display', serif; font-size: 1.4rem; font-style: italic; color: #5F6673; line-height: 1.5; margin: 0; }

/* Section Titles */
.memories-title {
    font-family: 'Poppins', sans-serif; font-size: 42px; font-weight: 800;
    background: linear-gradient(to right, #B8860B, #C79A2D);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    text-shadow: 0 0 25px rgba(199, 154, 45, 0.18);
    margin: -3.5rem 0 1.5rem 0 !important; text-align: center;
}

.letter-text { font-family: 'Inter', sans-serif; font-size: 1.1rem; line-height: 1.8; color: #3F3F46; font-weight: 400; text-align: center; }
.letter-text p { margin-bottom: 0.8rem; }
.handwritten { font-family: 'Dancing Script', cursive; font-size: 2.5rem; color: #8B5E34; }
.text-center { text-align: center; }
.delay-1 { animation-delay: 0.15s; } .delay-2 { animation-delay: 0.3s; } .delay-3 { animation-delay: 0.45s; } .delay-4 { animation-delay: 0.6s; }
.fade-in { animation: fadeIn 0.6s cubic-bezier(0.2, 0.8, 0.2, 1) forwards; opacity: 0; }
span.home-btn-anchor { display: none; }
div.element-container:has(.home-btn-anchor) {
    display: none !important;
    margin: 0 !important;
    padding: 0 !important;
    height: 0 !important;
}
div.element-container:has(.home-btn-anchor) + div.element-container {
    position: fixed !important;
    top: 20px !important;
    left: 20px !important;
    width: auto !important;
    z-index: 99999 !important;
    margin: 0 !important;
}
div.element-container:has(.home-btn-anchor) + div.element-container button {
    background: rgba(255, 250, 244, 0.88) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(199, 154, 45, 0.15) !important;
    border-radius: 20px !important;
    color: #B8860B !important;
    font-size: 0.9rem !important;
    padding: 0.5rem 1.5rem !important;
    margin: 0 !important;
    transform: none !important;
    box-shadow: 0 10px 30px rgba(183, 134, 11, 0.14) !important;
    transition: all 0.3s ease !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    letter-spacing: 0.05em !important;
    min-height: 0 !important;
}
div.element-container:has(.home-btn-anchor) + div.element-container button p {
    color: #B8860B !important;
    margin: 0 !important;
}
div.element-container:has(.home-btn-anchor) + div.element-container button:hover {
    background: rgba(255, 253, 248, 0.97) !important;
    border-color: rgba(199, 154, 45, 0.45) !important;
    box-shadow: 0 14px 36px rgba(183, 134, 11, 0.18) !important;
    transform: scale(1.04) translateY(-2px) !important;
}
</style>
""", unsafe_allow_html=True)

# Helper function to render base64 image
@st.cache_data
def get_base64_image(image_path_str):
    try:
        with open(image_path_str, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return ""

def nav_to(view_name):
    st.session_state.view = view_name

# --- Global Background Decor ---
random.seed(42) # Consistent random placement


def mirrored_decor(glyph, top, inset, size_range, css_class="decor"):
    """Place a glyph at an equal inset from the left and right edges.

    Both halves share size, opacity and delay so the pair reads as a mirror.
    Insets stay under 15% so the glyphs clear the centred content card.
    """
    delay = round(random.uniform(0, 3), 2)
    size = round(random.uniform(*size_range), 2)
    opacity = round(random.uniform(0.3, 0.7), 2)
    return "".join(
        f'<div class="{css_class}" style="top:{top}%; {side}:{inset}%; '
        f'animation-delay:{delay}s; font-size:{size}rem; --decor-opacity:{opacity};">{glyph}</div>'
        for side in ("left", "right")
    )


decor_html = '<div class="paper-grain"></div><div class="decor-container">'

# Sparkles, mirrored left to right
for top, inset in [(16, 9), (48, 5), (78, 13)]:
    decor_html += mirrored_decor("✨", top, inset, (0.5, 0.9))

# Accent stars, mirrored left to right
for top, inset in [(34, 13), (62, 7), (90, 12)]:
    decor_html += mirrored_decor("⭐", top, inset, (0.6, 1.1))

# Balanced top corners: moon on the right, a smaller star on the left
decor_html += '<div class="decor" style="top:6%; left:6%; animation-delay:0s; font-size:1.2rem; --decor-opacity:0.5;">⭐</div>'
decor_html += '<div class="decor decor-moon" style="top:6%; right:6%; font-size:2.15rem; --decor-opacity:0.55;">🌙</div>'
decor_html += '</div>'

st.markdown(decor_html, unsafe_allow_html=True)

# ----------------- HOME VIEW -----------------
if st.session_state.view == 'home':
    st.markdown("""
        <div class="hero-wrapper">
            <div class="badge-pill">✦ Today is All About You ✦</div>
            <div style="text-align: center;">
                <h1 class="hero-title">KOMAL</h1>
                <h2 class="hero-subtitle">✦ Happy Birthday ✦</h2>
                <p class="hero-quote" style="margin-bottom: 1rem;">✦ "Talking to you is always nice." ✦</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Buttons are styled via their `st-key-<key>` container classes in the CSS above.
    col_spacer1, col1, col2, col_spacer2 = st.columns([1, 2, 2, 1], gap="medium")
    with col1:
        if st.button("Memories", key="btn_mem", icon=":material/photo_library:"):
            nav_to('memories')
            st.rerun()
    with col2:
        if st.button("Letter", key="btn_let", icon=":material/mail:"):
            nav_to('letter')
            st.rerun()
            
    # Tiny Footer Section
    st.markdown("""
        <div style="text-align: center; margin-top: 0.5rem; color: #6B7280; font-size: 0.8rem; font-family: 'Inter', sans-serif; letter-spacing: 0.1em; opacity: 0; animation: fadeIn 5s ease forwards;">
            ✦ Every memory with you is special ✦
        </div>
    """, unsafe_allow_html=True)

# ----------------- MEMORIES VIEW -----------------
elif st.session_state.view == 'memories':
    st.markdown("<span class='home-btn-anchor'></span>", unsafe_allow_html=True)
    if st.button("🏠 HOME", key="btn_home_mem"):
        nav_to('home')
        st.rerun()
    
    st.markdown("""
        <div style="text-align: center; margin-top: 1rem;">
            <h2 class="memories-title fade-in"><span style="-webkit-text-fill-color: initial;">✨</span> Some Moments Worth Keeping <span style="-webkit-text-fill-color: initial;">✨</span></h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Image discovery
    images_dir = Path("images")
    valid_exts = {".jpg", ".jpeg", ".png", ".webp"}
    image_paths = []
    
    if images_dir.exists():
        image_paths = sorted(
            (p for p in images_dir.iterdir() if p.suffix.lower() in valid_exts),
            key=lambda p: p.name.lower(),
        )
    
    if not image_paths:
        # Empty state
        st.markdown("""
            <div class='glass-card fade-in delay-1 text-center'>
                <h3 style='color: #B8860B; font-weight:300;'>A space waiting for memories.</h3>
                <p style='color: #6B7280; font-size: 0.9rem;'>Please add images to the `images/` directory.</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Gallery Layout using columns
        st.markdown("<div class='gallery-section-wrapper fade-in delay-1'><div class='gallery-bg-glow'></div>", unsafe_allow_html=True)
        
        # Twinkling stars specifically for gallery, mirrored left to right
        decor_html = '<div class="gallery-decor-container">'
        for top, inset in [(5, 9), (84, 9)]:
            decor_html += mirrored_decor("⭐", top, inset, (0.6, 1.0), css_class="gallery-decor")
        decor_html += '</div>'
        st.markdown(decor_html, unsafe_allow_html=True)

        cols = st.columns(3)
        caption_by_name = {
            "diwali": "A Warm Memory",
            "holi": "Colors of Joy",
            "random": "One More Smile",
        }
        for i, img_path in enumerate(image_paths):
            b64_img = get_base64_image(str(img_path))
            caption = html.escape(
                caption_by_name.get(
                    img_path.stem.lower(),
                    img_path.stem.replace("_", " ").replace("-", " ").title(),
                )
            )
            col_idx = i % 3
            with cols[col_idx]:
                st.markdown(f"""
                    <div class='gallery-img-container fade-in delay-{min(i%4 + 1, 4)}'>
                        <div class='img-blur-bg' style='background-image: url(data:image/jpeg;base64,{b64_img})'></div>
                        <img src="data:image/jpeg;base64,{b64_img}" alt="{caption}">
                        <div class='gallery-gradient-overlay'></div>
                    </div>
                    <div class='gallery-caption fade-in delay-{min(i%4 + 1, 4)}'>{caption}</div>
                """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
                
    # Quote Card
    st.markdown("""
        <div class="gradient-divider fade-in delay-2"></div>
        <div class="quote-card fade-in delay-3">
            <div class="quote-text">"Thanks for being there. Time is the best thing you can give to someone."</div>
        </div>
    """, unsafe_allow_html=True)
    



# ----------------- LETTER VIEW -----------------
elif st.session_state.view == 'letter':
    st.markdown("""
        <style>
        .main .block-container { padding-bottom: 6rem !important; }
        </style>
    """, unsafe_allow_html=True)
    st.markdown("<span class='home-btn-anchor'></span>", unsafe_allow_html=True)
    if st.button("🏠 HOME", key="btn_home_let"):
        nav_to('home')
        st.rerun()

    st.markdown("""
        <div style="text-align: center; margin-top: 1rem;">
            <h2 class="memories-title fade-in"><span style="-webkit-text-fill-color: initial;">🌙</span> Before This Day Ends <span style="-webkit-text-fill-color: initial;">✨</span></h2>
        </div>
    """, unsafe_allow_html=True)

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
    st.write("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
            

