import streamlit as st
import streamlit.components.v1 as components
from llm import call_gemini
from utils import generate_system_prompt, create_radar

st.set_page_config(page_title="HubGPT", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")

# =========================================================
# CSS
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

:root {
    --bg:#000000; --bg-1:#080808; --bg-2:#0f0f0f; --bg-3:#161616; --bg-4:#1c1c1c;
    --green:#00e5a0; --green-dim:rgba(0,229,160,0.12); --green-glow:rgba(0,229,160,0.20);
    --green-line:rgba(0,229,160,0.25); --white:#f2f2f2; --grey-hi:#aaaaaa;
    --grey-mid:#555555; --red:#ff5c5c; --amber:#ffb830;
    --border:rgba(255,255,255,0.06); --r:10px; --r-lg:16px;
    --font:'Space Grotesk',sans-serif; --mono:'Space Mono',monospace;
    --glow:0 0 24px var(--green-glow);
}

html, body, [class*="css"] {
    font-family: var(--font) !important;
    background-color: var(--bg) !important;
    color: var(--white) !important;
}
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
.block-container { padding: 1.5rem 2rem 0 2rem !important; max-width: 100% !important; }

::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--green-line); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: var(--green); }

@keyframes fadeUp {
    from { opacity:0; transform:translateY(10px); }
    to   { opacity:1; transform:translateY(0); }
}
@keyframes pulse-border {
    0%,100% { border-color: var(--green-line); }
    50%      { border-color: var(--green); }
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: var(--bg-1) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 1.4rem 1.1rem !important; }

/* Hide ALL native collapse buttons */
[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"] {
    display: none !important;
    visibility: hidden !important;
    pointer-events: none !important;
}

.sidebar-brand {
    display:flex; align-items:center; gap:10px;
    margin-bottom:1.6rem; padding-bottom:1rem;
    border-bottom:1px solid var(--border);
}
.sidebar-brand .logo {
    width:32px; height:32px; background:var(--green);
    border-radius:8px; display:flex; align-items:center;
    justify-content:center; font-size:16px;
}
.sidebar-brand h1 {
    font-size:1.2rem !important; font-weight:700 !important;
    letter-spacing:-0.01em; margin:0 !important;
    color:var(--white) !important; -webkit-text-fill-color:var(--white) !important;
}

.section-label {
    font-size:0.6rem; font-weight:700; letter-spacing:0.15em;
    text-transform:uppercase; color:var(--grey-mid);
    margin:1.3rem 0 0.5rem; font-family:var(--mono) !important;
}

[data-testid="stSidebar"] .stButton > button {
    background:transparent !important;
    border:1px solid var(--border) !important;
    border-radius:var(--r) !important;
    color:var(--grey-hi) !important;
    font-family:var(--font) !important;
    font-size:0.82rem !important; font-weight:500 !important;
    text-align:left !important; width:100% !important;
    padding:0.48rem 0.8rem !important; margin-bottom:0.28rem !important;
    transition:all 0.15s ease !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background:var(--bg-3) !important;
    border-color:var(--green-line) !important;
    color:var(--green) !important;
    transform:translateX(4px) !important;
}

[data-testid="stSelectbox"] > div > div {
    background:var(--bg-2) !important; border:1px solid var(--border) !important;
    border-radius:var(--r) !important; color:var(--white) !important;
    font-family:var(--font) !important;
}

[data-testid="stToggle"] label { color:var(--grey-hi) !important; font-size:0.82rem !important; }
[data-testid="stToggle"] > div [data-checked="true"] { background:var(--green) !important; }

[data-testid="stFileUploader"] {
    background:var(--bg-2) !important;
    border:1px dashed var(--green-line) !important;
    border-radius:var(--r) !important; padding:0.4rem !important;
}

hr { border-color:var(--border) !important; margin:0.9rem 0 !important; }

.radar-container {
    background:var(--bg-2); border:1px solid var(--border);
    border-radius:var(--r-lg); padding:0.8rem; margin-bottom:0.7rem;
}
.score-grid { display:grid; grid-template-columns:1fr 1fr; gap:0.3rem; margin-top:0.55rem; }
.score-pill {
    background:var(--bg-3); border:1px solid var(--border);
    border-radius:6px; padding:4px 8px; font-size:0.68rem;
    display:flex; justify-content:space-between; align-items:center; color:var(--grey-hi);
}
.score-pill span { color:var(--green); font-weight:700; font-family:var(--mono); }

.retake-btn > div > button {
    background:transparent !important; border:1px solid var(--border) !important;
    border-radius:var(--r) !important; color:var(--grey-mid) !important;
    font-size:0.76rem !important; transition:all 0.15s !important;
}
.retake-btn > div > button:hover {
    border-color:var(--red) !important; color:var(--red) !important;
    background:rgba(255,92,92,0.06) !important;
}

/* ── CHAT MESSAGES ── */
[data-testid="stChatMessage"] {
    background:var(--bg-2) !important; border:1px solid var(--border) !important;
    border-radius:var(--r-lg) !important; margin-bottom:0.6rem !important;
    padding:0.85rem 1.1rem !important; animation:fadeUp 0.2s ease both;
}
[data-testid="stChatMessage"]:last-child {
    border-color:var(--green-line) !important;
    box-shadow:0 0 20px var(--green-glow) !important;
}
[data-testid="stChatMessage"] p {
    color:var(--white) !important; font-size:0.91rem !important;
    line-height:1.74 !important; font-family:var(--font) !important;
}

/* ── CHAT INPUT ── */
[data-testid="stChatInput"] > div {
    background:var(--bg-2) !important; border:1px solid var(--green-line) !important;
    border-radius:var(--r-lg) !important; box-shadow:var(--glow) !important;
    animation:pulse-border 3s ease infinite;
}
[data-testid="stChatInput"] textarea {
    background:transparent !important; color:var(--white) !important;
    -webkit-text-fill-color:var(--white) !important; caret-color:var(--green) !important;
    font-family:var(--font) !important; font-size:0.91rem !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color:var(--grey-mid) !important; -webkit-text-fill-color:var(--grey-mid) !important;
}
[data-testid="stChatInput"] button {
    background:var(--green) !important; border-radius:8px !important;
    color:#000 !important; border:none !important; font-weight:700 !important;
}
[data-testid="stChatInput"] button:hover { opacity:0.85 !important; }

/* ── RADIO ── */
.stRadio > div { gap:0.38rem !important; }
.stRadio > div > label {
    background:var(--bg-3) !important; border:1px solid var(--border) !important;
    border-radius:var(--r) !important; padding:0.75rem 1rem !important;
    width:100% !important; cursor:pointer !important;
    transition:all 0.15s !important; font-family:var(--font) !important;
}
.stRadio > div > label:hover {
    border-color:var(--green-line) !important; background:var(--green-dim) !important;
}
.stRadio [data-testid="stMarkdownContainer"] p {
    font-size:0.89rem !important; color:var(--white) !important; font-family:var(--font) !important;
}
.stRadio > label { display:none !important; }

/* ── TEST continue button ── */
.test-continue button {
    background:var(--green) !important; border:none !important;
    border-radius:var(--r) !important; color:#000000 !important;
    -webkit-text-fill-color:#000000 !important; font-family:var(--font) !important;
    font-weight:700 !important; font-size:0.9rem !important;
    padding:0.65rem 2rem !important; width:100% !important;
    box-shadow:0 4px 20px var(--green-glow) !important;
    transition:all 0.2s !important; margin-top:0.6rem !important;
}
.test-continue button:hover {
    transform:translateY(-2px) !important;
    box-shadow:0 8px 30px var(--green-glow) !important; opacity:0.9 !important;
}

/* ── TEST CARD ── */
.test-card-top {
    background:#0f0f0f; border:1px solid rgba(255,255,255,0.07);
    border-bottom:none; border-radius:16px 16px 0 0;
    padding:2rem 2.2rem 1.5rem; animation:fadeUp 0.3s ease both;
}
.tc-header { display:flex; align-items:center; gap:9px; margin-bottom:1.4rem; }
.tc-logo {
    width:30px; height:30px; background:#00e5a0; border-radius:7px;
    display:flex; align-items:center; justify-content:center;
    font-size:15px; flex-shrink:0;
}
.tc-title { font-size:1.05rem; font-weight:700; color:#f2f2f2; }
.tc-count {
    margin-left:auto; font-size:0.65rem; font-weight:700;
    letter-spacing:0.12em; text-transform:uppercase; color:#555;
    font-family:'Space Mono',monospace;
}
.tc-progress-track {
    background:#1c1c1c; border-radius:99px; height:2px;
    width:100%; margin-bottom:1.5rem; overflow:hidden;
}
.tc-progress-fill {
    height:2px; border-radius:99px; background:#00e5a0;
    transition:width 0.4s ease;
}
.tc-question { font-size:1.08rem; font-weight:600; color:#f2f2f2; line-height:1.55; }
.test-card-bottom {
    background:#0f0f0f; border:1px solid rgba(255,255,255,0.07);
    border-top:1px solid #1c1c1c; border-radius:0 0 16px 16px;
    padding:1.3rem 2.2rem 1.8rem; margin-top:-1px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# SESSION STATE
# =========================================================
PERSONAS = ["Default","Azaan Founder","Creative Reel Maker","Einstein","Elon Musk","Sundar Pichai"]
PERSONA_ICONS = {
    "Default":"🤖","Azaan Founder":"🚀","Creative Reel Maker":"🎬",
    "Einstein":"⚛️","Elon Musk":"🛸","Sundar Pichai":"🔍"
}

_defaults = {
    "step":"test", "index":0,
    "scores":{"analytical":0,"intuitive":0,"critical":0,"supportive":0,
              "structured":0,"freeform":0,"concise":0,"elaborate":0},
    "chats":{"Chat 1":[]}, "current_chat":"Chat 1",
    "persona":"Default", "reference_mode":False, "reference_text":"",
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# =========================================================
# PERSONALITY TEST
# =========================================================
questions = [
    ("How do you prefer to solve problems?",
     ("Break it down step-by-step logically","Explore creative possibilities freely"),
     ("analytical","intuitive")),
    ("What kind of feedback works best for you?",
     ("Direct, honest criticism — no sugarcoating","Encouragement first, then suggestions"),
     ("critical","supportive")),
    ("How do you prefer to learn something new?",
     ("Follow a structured framework or curriculum","Get the big picture, fill gaps as I go"),
     ("structured","freeform")),
    ("What communication style do you prefer?",
     ("Short and precise — get to the point","Detailed and expansive — full context"),
     ("concise","elaborate")),
    ("How do you usually make decisions?",
     ("Data and evidence drive my choices","Vision and intuition guide my path"),
     ("analytical","intuitive")),
    ("How do you like discussions structured?",
     ("Organized with clear agenda and steps","Flexible, let the conversation flow"),
     ("structured","freeform")),
]

if st.session_state.step == "test":
    idx = st.session_state.index
    pct = int((idx / len(questions)) * 100)
    q, opts, traits = questions[idx]

    st.markdown("<div style='height:6vh'></div>", unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 1.4, 1])

    with mid:
        st.markdown(
            f'<div class="test-card-top">'
            f'<div class="tc-header">'
            f'<div class="tc-logo">🧠</div>'
            f'<span class="tc-title">HubGPT</span>'
            f'<span class="tc-count">{idx+1} / {len(questions)}</span>'
            f'</div>'
            f'<div class="tc-progress-track"><div class="tc-progress-fill" style="width:{pct}%"></div></div>'
            f'<div class="tc-question">{q}</div>'
            f'</div>',
            unsafe_allow_html=True
        )
        st.markdown('<div class="test-card-bottom">', unsafe_allow_html=True)
        choice = st.radio("opts", opts, label_visibility="collapsed", key=f"q_{idx}")
        st.markdown('<div class="test-continue">', unsafe_allow_html=True)
        if st.button("Continue →", key=f"btn_{idx}", use_container_width=True):
            st.session_state.scores[traits[0 if choice == opts[0] else 1]] += 1
            st.session_state.index += 1
            if st.session_state.index >= len(questions):
                st.session_state.step = "chat"
            st.rerun()
        st.markdown("</div></div>", unsafe_allow_html=True)

    st.stop()

# =========================================================
# HAMBURGER FAB
# Key insight: inject the button directly into window.parent.document.body
# via JavaScript — this escapes the height=0 iframe constraint entirely
# and makes it appear as a true fixed element on the real page.
# =========================================================
components.html("""
<script>
(function() {
    var doc = window.parent.document;

    /* ── sidebar toggle ── */
    function getSidebarBtn() {
        var selectors = [
            '[data-testid="stSidebarCollapseButton"] button',
            '[data-testid="stSidebarCollapseButton"]',
            '[data-testid="stSidebarCollapsedControl"] button',
            '[data-testid="collapsedControl"] button',
            'button[aria-label="Close sidebar"]',
            'button[aria-label="Open sidebar"]',
            'section[data-testid="stSidebar"] > div > div > button',
        ];
        for (var i = 0; i < selectors.length; i++) {
            var el = doc.querySelector(selectors[i]);
            if (el) return el;
        }
        return null;
    }

    function toggleSidebar() {
        var btn = getSidebarBtn();
        if (btn) { btn.click(); return; }
        // Fallback: manually show/hide the sidebar element
        var sb = doc.querySelector('[data-testid="stSidebar"]');
        if (sb) sb.style.display = (sb.style.display === 'none') ? '' : 'none';
    }

    window.parent.toggleSidebar = toggleSidebar;

    /* ── inject FAB into parent body ── */
    function injectFAB() {
        if (doc.getElementById('hubgpt-fab')) return;

        // Inject styles
        if (!doc.getElementById('hubgpt-fab-css')) {
            var s = doc.createElement('style');
            s.id = 'hubgpt-fab-css';
            s.textContent =
                '#hubgpt-fab{' +
                '  position:fixed;top:14px;left:14px;z-index:9999999;' +
                '  width:40px;height:40px;background:#111111;' +
                '  border:1px solid rgba(0,229,160,0.30);border-radius:11px;' +
                '  cursor:pointer;display:flex;align-items:center;' +
                '  justify-content:center;flex-direction:column;gap:5px;' +
                '  box-shadow:0 2px 20px rgba(0,0,0,.6),0 0 14px rgba(0,229,160,.12);' +
                '  transition:all .18s ease;padding:0;outline:none;' +
                '}' +
                '#hubgpt-fab:hover{' +
                '  background:rgba(0,229,160,.10)!important;' +
                '  border-color:rgba(0,229,160,.65)!important;' +
                '  box-shadow:0 2px 20px rgba(0,0,0,.6),0 0 22px rgba(0,229,160,.28)!important;' +
                '  transform:scale(1.06)' +
                '}' +
                '#hubgpt-fab span{' +
                '  display:block;width:17px;height:2px;' +
                '  background:#aaa;border-radius:2px;' +
                '  transition:background .18s;pointer-events:none' +
                '}' +
                '#hubgpt-fab:hover span{background:#00e5a0}';
            doc.head.appendChild(s);
        }

        // Create button
        var fab = doc.createElement('button');
        fab.id = 'hubgpt-fab';
        fab.title = 'Toggle Sidebar';
        fab.setAttribute('aria-label', 'Toggle Sidebar');
        fab.innerHTML = '<span></span><span></span><span></span>';
        fab.addEventListener('click', toggleSidebar);
        doc.body.appendChild(fab);
    }

    // Run immediately + retry to handle slow Streamlit DOM init
    injectFAB();
    setTimeout(injectFAB, 200);
    setTimeout(injectFAB, 600);
    setTimeout(injectFAB, 1200);

    /* ── keyboard shortcut: backslash ── */
    if (!window.parent._hubgpt_bound) {
        window.parent._hubgpt_bound = true;
        doc.addEventListener('keydown', function(e) {
            if (e.key === '\\' && !e.target.matches('textarea,input,[contenteditable]')) {
                toggleSidebar();
            }
        });
    }
})();
</script>
""", height=0)

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="logo">🧠</div>
        <h1>HubGPT</h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">// Conversations</div>', unsafe_allow_html=True)
    for chat_name in list(st.session_state.chats.keys()):
        is_active = chat_name == st.session_state.current_chat
        label = f"{'▶' if is_active else '○'}  {chat_name}"
        if st.button(label, key=f"cb_{chat_name}", use_container_width=True):
            st.session_state.current_chat = chat_name
            st.rerun()
    if st.button("＋  New Chat", key="new_chat_btn", use_container_width=True):
        nn = f"Chat {len(st.session_state.chats)+1}"
        st.session_state.chats[nn] = []
        st.session_state.current_chat = nn
        st.rerun()

    st.divider()

    st.markdown('<div class="section-label">// Cognitive Profile</div>', unsafe_allow_html=True)
    st.markdown('<div class="radar-container">', unsafe_allow_html=True)
    st.pyplot(create_radar(st.session_state.scores), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    s = st.session_state.scores
    st.markdown(f"""
    <div class="score-grid">
        <div class="score-pill">Analytical <span>{s['analytical']}</span></div>
        <div class="score-pill">Intuitive  <span>{s['intuitive']}</span></div>
        <div class="score-pill">Critical   <span>{s['critical']}</span></div>
        <div class="score-pill">Supportive <span>{s['supportive']}</span></div>
        <div class="score-pill">Structured <span>{s['structured']}</span></div>
        <div class="score-pill">Freeform   <span>{s['freeform']}</span></div>
        <div class="score-pill">Concise    <span>{s['concise']}</span></div>
        <div class="score-pill">Elaborate  <span>{s['elaborate']}</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown('<div class="section-label">// Persona</div>', unsafe_allow_html=True)
    st.selectbox("Persona", PERSONAS, key="persona", label_visibility="collapsed")

    st.divider()

    st.markdown('<div class="section-label">// Reference Mode</div>', unsafe_allow_html=True)
    st.session_state.reference_mode = st.toggle(
        "Enable Reference Only", value=st.session_state.reference_mode
    )
    if st.session_state.reference_mode:
        up = st.file_uploader("Upload .txt", type=["txt"], label_visibility="collapsed")
        if up:
            st.session_state.reference_text = up.read().decode("utf-8")
            st.success("Reference loaded ✓")

    st.divider()

    st.markdown('<div class="retake-btn">', unsafe_allow_html=True)
    if st.button("↩  Retake Personality Test", use_container_width=True):
        st.session_state.step  = "test"
        st.session_state.index = 0
        st.session_state.scores = {k:0 for k in st.session_state.scores}
        st.session_state.chats  = {"Chat 1":[]}
        st.session_state.current_chat = "Chat 1"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# MAIN CHAT
# =========================================================
cur_persona = st.session_state.persona
cur_icon    = PERSONA_ICONS.get(cur_persona, "🤖")
ref_on      = st.session_state.reference_mode and bool(st.session_state.reference_text)

# ── Header via components.html so <div> tags are NOT sanitized ──
ref_badge_html = (
    '<span style="display:inline-flex;align-items:center;gap:4px;'
    'background:rgba(255,184,48,0.08);border:1px solid rgba(255,184,48,0.25);'
    'border-radius:6px;padding:3px 10px;font-size:0.68rem;font-weight:700;'
    'color:#ffb830;letter-spacing:0.06em;text-transform:uppercase;'
    'font-family:\'Space Mono\',monospace;">📎 Ref Only</span>'
    if ref_on else ""
)

components.html(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Space+Mono:wght@700&display=swap');
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ background:transparent; overflow:hidden; }}
  .hdr {{
    display:flex; align-items:center; justify-content:space-between;
    padding-bottom:14px; border-bottom:1px solid rgba(255,255,255,0.06);
    font-family:'Space Grotesk',sans-serif;
  }}
  .title {{ font-size:1.4rem; font-weight:700; color:#f2f2f2; letter-spacing:-0.02em; }}
  .title em {{ color:#00e5a0; font-style:normal; }}
  .badges {{ display:flex; align-items:center; gap:8px; }}
  .pbadge {{
    display:inline-flex; align-items:center; gap:5px;
    background:rgba(0,229,160,0.12); border:1px solid rgba(0,229,160,0.25);
    border-radius:6px; padding:4px 12px; font-size:0.74rem; font-weight:600;
    color:#00e5a0; font-family:'Space Mono',monospace;
  }}
</style>
<div class="hdr">
  <div class="title">Hub<em>GPT</em></div>
  <div class="badges">
    <span class="pbadge">{cur_icon} {cur_persona}</span>
    {ref_badge_html}
  </div>
</div>
""", height=56)

# =========================================================
# MESSAGES
# =========================================================
messages = st.session_state.chats[st.session_state.current_chat]

system_prompt = generate_system_prompt(st.session_state.scores, "User", cur_persona)
if ref_on:
    system_prompt += (
        "\n\nIMPORTANT: Answer ONLY using the reference text below. "
        "Do not use external knowledge.\n\nREFERENCE:\n"
        + st.session_state.reference_text
    )

if not messages:
    st.markdown(f"""
    <div style="display:flex;flex-direction:column;align-items:center;
                justify-content:center;padding:4rem 2rem;text-align:center;gap:1rem;">
      <div style="font-size:2.5rem;opacity:0.25;">{cur_icon}</div>
      <div style="font-size:1rem;font-weight:600;color:#aaaaaa;">{cur_persona} is ready</div>
      <div style="font-size:0.84rem;max-width:280px;line-height:1.8;color:#555555;">
        Your cognitive profile is mapped.<br>
        Responses adapt structurally to your thinking style.
      </div>
    </div>
    """, unsafe_allow_html=True)
else:
    for msg in messages:
        avatar = "👤" if msg["role"] == "User" else cur_icon
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

# ── CHAT INPUT ──
user_input = st.chat_input("Ask anything…")

if user_input:
    messages.append({"role":"User","content":user_input})
    with st.chat_message("User", avatar="👤"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar=cur_icon):
        with st.spinner(""):
            response = call_gemini(system_prompt, messages, user_input)
        st.markdown(response)

    messages.append({"role":"AI","content":response})
    st.rerun()