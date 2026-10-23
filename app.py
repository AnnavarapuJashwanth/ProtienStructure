
import json
import html
import os
import requests
import streamlit as st
import streamlit.components.v1 as components

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="FoldCloud | AlphaFold Protein Explorer",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# CUSTOM CSS - PREMIUM SCIENTIFIC DASHBOARD
# --------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --bg: #080d19;
    --panel: #111a2b;
    --panel2: #151f33;
    --cyan: #53e6e0;
    --violet: #a78bfa;
    --text: #edf4ff;
    --muted: #96a8c4;
    --border: rgba(150, 180, 220, 0.15);
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at 5% 5%, rgba(54, 105, 190, .16), transparent 36%),
        radial-gradient(ellipse at 95% 25%, rgba(134, 79, 210, .13), transparent 32%),
        linear-gradient(150deg, #080d19 0%, #0b1221 55%, #080d19 100%);
    color: var(--text);
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1440px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: var(--text) !important;
    letter-spacing: -0.7px;
}

p, label, span {
    color: inherit;
}

#MainMenu, footer {
    visibility: hidden;
}

[data-testid="stDecoration"] {
    display: none;
}

/* Animated background decorations */
.orb {
    position: fixed;
    width: 220px;
    height: 220px;
    border-radius: 50%;
    filter: blur(75px);
    opacity: .12;
    pointer-events: none;
    z-index: 0;
    animation: drift 12s ease-in-out infinite alternate;
}

.orb-one {
    background: #53e6e0;
    top: 15%;
    left: -100px;
}

.orb-two {
    background: #8b5cf6;
    right: -100px;
    top: 48%;
    animation-delay: -4s;
}

@keyframes drift {
    from { transform: translate(0, 0) scale(1); }
    to { transform: translate(45px, -35px) scale(1.2); }
}

@keyframes enter {
    from { opacity: 0; transform: translateY(15px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes pulse {
    0%, 100% { box-shadow: 0 0 8px rgba(83,230,224,.15); }
    50% { box-shadow: 0 0 24px rgba(83,230,224,.32); }
}

/* Hero */
.hero {
    position: relative;
    overflow: hidden;
    padding: 34px 36px;
    border: 1px solid rgba(116, 183, 222, .22);
    border-radius: 25px;
    background:
        radial-gradient(ellipse at 90% 10%, rgba(83,230,224,.13), transparent 36%),
        linear-gradient(125deg, rgba(21,34,57,.98), rgba(13,20,36,.96));
    animation: enter .65s ease-out both;
    margin-bottom: 24px;
}

.hero::after {
    content: "";
    position: absolute;
    height: 2px;
    bottom: 0;
    left: 8%;
    right: 8%;
    background: linear-gradient(90deg, transparent, #53e6e0, #a78bfa, transparent);
    opacity: .8;
}

.eyebrow {
    color: #69e8df;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2.6px;
    text-transform: uppercase;
    margin-bottom: 15px;
}

.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(30px, 4.3vw, 51px);
    line-height: 1.12;
    font-weight: 700;
    color: #f4f7ff;
    letter-spacing: -1.7px;
    margin-bottom: 15px;
}

.gradient-text {
    background: linear-gradient(90deg, #53e6e0, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-description {
    color: #a8b8d2;
    font-size: 15px;
    line-height: 1.8;
    max-width: 720px;
}

.pill-row {
    display: flex;
    flex-wrap: wrap;
    gap: 9px;
    margin-top: 23px;
}

.pill {
    padding: 7px 12px;
    border-radius: 30px;
    font-size: 11px;
    border: 1px solid rgba(125, 180, 220, .23);
    color: #c9d9ef;
    background: rgba(255,255,255,.035);
}

/* Cards */
.panel {
    background: linear-gradient(145deg, rgba(20,31,51,.95), rgba(13,22,38,.96));
    border: 1px solid var(--border);
    border-radius: 19px;
    padding: 23px;
    margin-bottom: 18px;
    transition: transform .25s ease, border-color .25s ease,
                box-shadow .25s ease;
    animation: enter .55s ease-out both;
}

.panel:hover {
    transform: translateY(-4px);
    border-color: rgba(83,230,224,.45);
    box-shadow: 0 15px 40px rgba(0,0,0,.20),
                0 0 20px rgba(83,230,224,.04);
}

.section-label {
    color: #65e5de;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.panel-title {
    font-family: 'Space Grotesk', sans-serif;
    color: #f0f5ff;
    font-size: 21px;
    font-weight: 600;
    margin-bottom: 7px;
}

.muted {
    color: #9aacc8;
    font-size: 13px;
    line-height: 1.7;
}

.metric-card {
    padding: 19px;
    min-height: 122px;
    border: 1px solid rgba(130,165,210,.16);
    border-radius: 17px;
    background: linear-gradient(140deg, #142038, #10192a);
    transition: all .25s ease;
    animation: enter .6s ease-out both;
}

.metric-card:hover {
    transform: translateY(-5px);
    border-color: rgba(83,230,224,.5);
    animation: pulse 2s infinite;
}

.metric-icon {
    font-size: 21px;
    margin-bottom: 13px;
}

.metric-label {
    font-size: 11px;
    color: #91a5c4;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.metric-value {
    color: #f1f6ff;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 23px;
    font-weight: 700;
    margin-top: 5px;
    overflow-wrap: anywhere;
}

.status-dot {
    display: inline-block;
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #53e6a6;
    box-shadow: 0 0 10px rgba(83,230,166,.7);
    margin-right: 8px;
}

.viewer-frame {
    overflow: hidden;
    border: 1px solid rgba(83,230,224,.32);
    border-radius: 17px;
    padding: 5px;
    background: linear-gradient(135deg, #53e6e0, #a78bfa, #263b63);
    box-shadow: 0 0 30px rgba(83,230,224,.08);
}

.viewer-inner {
    background: #f7f9fc;
    border-radius: 12px;
    overflow: hidden;
}

.info-row {
    padding: 13px 0;
    border-bottom: 1px solid rgba(140,165,200,.13);
}

.info-key {
    color: #91a6c5;
    font-size: 12px;
    margin-bottom: 4px;
}

.info-value {
    color: #edf4ff;
    font-size: 14px;
    font-weight: 600;
    overflow-wrap: anywhere;
}

.footer {
    text-align: center;
    padding: 30px 10px 10px;
    color: #7386a5;
    font-size: 12px;
    line-height: 2;
}

div.stButton > button {
    background: linear-gradient(100deg, #53e6e0, #82b9ff);
    color: #07121f;
    border: none;
    border-radius: 11px;
    padding: 0.72rem 1.3rem;
    font-weight: 700;
    min-height: 46px;
    transition: all .2s ease;
}

div.stButton > button:hover {
    color: #07121f;
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(83,230,224,.2);
    border: none;
}

div[data-testid="stTextInput"] input {
    background: #111c30;
    border: 1px solid #2a3c59;
    border-radius: 10px;
    color: #f3f7ff;
    min-height: 46px;
}

div[data-testid="stTextInput"] input:focus {
    border-color: #53e6e0;
    box-shadow: 0 0 0 1px #53e6e0;
}

div[data-testid="stAlert"] {
    border-radius: 12px;
}

a {
    color: #53e6e0 !important;
}

hr {
    border-color: rgba(140,165,200,.15);
}
</style>

<div class="orb orb-one"></div>
<div class="orb orb-two"></div>
""", unsafe_allow_html=True)



# --------------------------------------------------
# FOLDCloud MULTI-PAGE NAVIGATION
# --------------------------------------------------
if "active_accession" not in st.session_state:
    st.session_state.active_accession = "P69905"

st.sidebar.markdown("""
<div style="padding:10px 4px 16px;">
  <div style="font-size:11px;letter-spacing:2px;color:#53e6e0;font-weight:800;">
    FOLD CLOUD · BIOPLATFORM
  </div>
  <div style="font-size:22px;font-weight:800;margin-top:5px;">Workspace</div>
  <div style="font-size:12px;color:#96a8c4;margin-top:4px;">
    AlphaFold structure intelligence
  </div>
</div>
""", unsafe_allow_html=True)

selected_page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Live Protein Search",
        "Structure Search UI",
        "Batch Prediction UI",
        "Cloud Architecture UI",
        "Saved Structures UI",
    ],
    index=0,
)

page_files = {
    "Structure Search UI": "structure_search.html",
    "Batch Prediction UI": "batch_prediction.html",
    "Cloud Architecture UI": "cloud_architecture.html",
    "Saved Structures UI": "saved_structures.html",
}


def fetch_alpha_fold_record(accession):
    """Return the first AlphaFold record for an accession, or an error."""
    accession = accession.strip().upper()
    if not accession or not accession.replace("-", "").isalnum():
        return None, "Enter a valid-looking UniProt accession."

    try:
        response = requests.get(
            "https://alphafold.ebi.ac.uk/api/prediction/" + accession,
            timeout=30,
            headers={"User-Agent": "FoldCloud/1.0"},
        )
        if response.status_code == 404:
            return None, f"No AlphaFold record was found for {accession}."
        response.raise_for_status()
        data = response.json()
    except requests.RequestException:
        return None, "Could not connect to the AlphaFold database."
    except ValueError:
        return None, "The AlphaFold database returned invalid data."

    if not isinstance(data, list) or not data:
        return None, "No protein structure record was returned."
    if not isinstance(data[0], dict):
        return None, "The AlphaFold response had an unexpected format."
    return data[0], None


def populate_design_page(page_html, record, accession):
    """Replace the supplied page's example protein values with live values."""
    if not record:
        return page_html

    name = str(record.get("uniprotDescription") or "Protein structure")
    gene = str(record.get("gene") or "Unknown")
    sequence = record.get("uniprotSequence") or ""
    length = len(sequence)
    if not length:
        try:
            length = (
                int(record.get("uniprotEnd") or 0)
                - int(record.get("uniprotStart") or 1)
                + 1
            )
        except (TypeError, ValueError):
            length = 0
    confidence = record.get("confidenceAvgLocalScore")
    try:
        confidence_text = f"{float(confidence):.1f}"
    except (TypeError, ValueError):
        confidence_text = "N/A"

    replacements = {
        "P69905": html.escape(accession),
        "HBA1": html.escape(gene),
        "Hemoglobin subunit alpha": html.escape(name),
        "142 aa": f"{length} aa",
        "92.4": confidence_text,
    }
    for old_value, new_value in replacements.items():
        page_html = page_html.replace(old_value, new_value)

    sequence_json = json.dumps(str(sequence))
    accession_json = json.dumps(accession)
    name_json = json.dumps(name)
    live_data_script = f"""
    <script>
      (() => {{
        const accession = {accession_json};
        const proteinName = {name_json};
        const sequence = {sequence_json};
        const fastaInput = document.getElementById("fastaInput");
        if (fastaInput && sequence) {{
          fastaInput.value = `>${{accession}} ${{proteinName}}\\n${{sequence}}`;
          fastaInput.dispatchEvent(new Event("input", {{ bubbles: true }}));
          fastaInput.dispatchEvent(new Event("change", {{ bubbles: true }}));
        }}
        const heading = document.querySelector("h1");
        if (heading && heading.textContent.includes("Batch Prediction")) {{
          heading.textContent = `${{proteinName}} · ${{accession}} | Batch Prediction`;
        }}
        const accessionTargets = document.querySelectorAll(
          '[data-protein-accession], #activeAccession'
        );
        accessionTargets.forEach((target) => {{
          target.textContent = accession;
        }});
        document.title = `FoldCloud | ${{accession}}`;
      }})();
    </script>
    """
    page_html = page_html.replace("</body>", live_data_script + "</body>", 1)
    return page_html


def remove_embedded_navigation(page_html):
    """Keep the Streamlit navigation as the single navigation controller."""
    embedded_layout_css = """
    <style>
      body > aside.fixed.left-0 {
        display: none !important;
      }
      body > div.pl-72 {
        padding-left: 0 !important;
      }
      body > div.pl-72 > header {
        left: 0 !important;
      }
      body > div.pl-72 > main {
        min-width: 0 !important;
      }
    </style>
    """
    return page_html.replace("</head>", embedded_layout_css + "</head>", 1)


def apply_design_theme(page_html):
    """Apply the shared FoldCloud visual language to every supplied UI."""
    visual_theme_css = """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

      :root {
        --fold-bg: #081321;
        --fold-panel: #101e31;
        --fold-panel-soft: #14263d;
        --fold-border: rgba(126, 180, 220, .22);
        --fold-text: #eaf4ff;
        --fold-muted: #91a8c5;
        --fold-accent: #53e6e0;
        --fold-blue: #82b9ff;
      }

      html, body {
        background:
          radial-gradient(circle at 85% 8%, rgba(72, 119, 210, .20), transparent 30%),
          radial-gradient(circle at 8% 92%, rgba(46, 192, 190, .12), transparent 28%),
          var(--fold-bg) !important;
        color: var(--fold-text) !important;
        font-family: 'DM Sans', sans-serif !important;
      }

      body, main, header, aside,
      [class*="bg-white"], [class*="bg-slate-50"],
      [class*="bg-[#f8fafc]"], [class*="bg-[#f1f5f9]"] {
        background-color: var(--fold-bg) !important;
        color: var(--fold-text) !important;
      }

      header, aside,
      [class*="border-[#e2e8f0]"],
      [class*="border-slate-200"] {
        border-color: var(--fold-border) !important;
        background: rgba(12, 25, 43, .94) !important;
      }

      [class*="rounded-xl"], [class*="rounded-lg"],
      [class*="rounded-2xl"] {
        border-color: var(--fold-border) !important;
      }

      main > div > div > div,
      main section,
      [class*="shadow-sm"], [class*="shadow-md"] {
        background: linear-gradient(145deg, rgba(20, 38, 61, .96), rgba(12, 27, 46, .96)) !important;
        color: var(--fold-text) !important;
      }

      [class*="text-[#0f172a]"], [class*="text-[#1e293b]"],
      [class*="text-slate-700"], [class*="text-slate-800"],
      [class*="text-[#334155]"] {
        color: var(--fold-text) !important;
      }

      [class*="text-[#475569]"], [class*="text-[#64748b]"],
      [class*="text-[#94a3b8]"], [class*="text-slate-500"] {
        color: var(--fold-muted) !important;
      }

      [class*="text-[#0284c7]"], [class*="text-[#0369a1]"],
      [class*="text-sky-700"], [class*="text-sky-800"] {
        color: var(--fold-accent) !important;
      }

      input, textarea, select {
        background: #0b1a2d !important;
        color: var(--fold-text) !important;
        border-color: var(--fold-border) !important;
      }

      input::placeholder, textarea::placeholder {
        color: #7188a5 !important;
      }

      [class*="bg-[#e0f2fe]"], [class*="bg-sky-100"],
      [class*="bg-emerald-50"], [class*="bg-amber-50"] {
        background: rgba(83, 230, 224, .12) !important;
        color: var(--fold-accent) !important;
        border-color: rgba(83, 230, 224, .28) !important;
      }

      button, [role="button"] {
        border-color: var(--fold-border) !important;
      }

      h1, h2, h3, h4 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: var(--fold-text) !important;
        letter-spacing: -.35px;
      }

      code, pre, textarea, [class*="font-code"] {
        font-family: 'IBM Plex Mono', monospace !important;
      }

      ::-webkit-scrollbar { width: 8px; height: 8px; }
      ::-webkit-scrollbar-track { background: #091524; }
      ::-webkit-scrollbar-thumb {
        background: #294565;
        border-radius: 10px;
      }
      ::-webkit-scrollbar-thumb:hover { background: #3b6d91; }
    </style>
    """
    return page_html.replace("</head>", visual_theme_css + "</head>", 1)


if selected_page != "Live Protein Search":
    selected_file = page_files[selected_page]
    selected_path = os.path.join(os.path.dirname(__file__), "html_pages", selected_file)
    try:
        with open(selected_path, "r", encoding="utf-8") as html_file:
            page_html = html_file.read()
        backend_accession = st.sidebar.text_input(
            "BACKEND ACCESSION",
            value=st.session_state.active_accession,
            help="Live UniProt accession used to populate this design page.",
        ).strip().upper()
        if backend_accession:
            st.session_state.active_accession = backend_accession
        backend_record, backend_error = fetch_alpha_fold_record(backend_accession)
        if backend_error:
            st.sidebar.warning(backend_error)
        page_html = populate_design_page(
            page_html,
            backend_record,
            backend_accession,
        )
        page_html = remove_embedded_navigation(page_html)
        page_html = apply_design_theme(page_html)
        components.html(page_html, height=1900, scrolling=True)
    except OSError as exc:
        st.error(f"Could not load {selected_file}: {exc}")
    st.stop()


# --------------------------------------------------
# HERO SECTION
# --------------------------------------------------
st.markdown("""
<div class="hero">
    <div class="eyebrow">COMPUTATIONAL BIOLOGY · CLOUD TECHNOLOGY</div>
    <div class="hero-title">
        Explore the hidden<br>
        <span class="gradient-text">architecture of life.</span>
    </div>
    <div class="hero-description">
        Discover protein structures through an interactive scientific
        workspace. Search by protein ID, explore a 3D molecular model,
        and inspect available prediction information.
    </div>
    <div class="pill-row">
        <span class="pill">🧬 AlphaFold Database</span>
        <span class="pill">✦ Interactive 3D</span>
        <span class="pill">☁ AWS-ready</span>
        <span class="pill">⌘ Python + Streamlit</span>
    </div>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SEARCH SECTION
# --------------------------------------------------
left, right = st.columns([1.5, 1], gap="large")

with left:
    st.markdown("""
    <div class="panel">
        <div class="section-label">01 / STRUCTURE SEARCH</div>
        <div class="panel-title">Find a protein</div>
        <div class="muted">
            Enter a UniProt accession to retrieve an available
            AlphaFold structure.
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("protein_search_form"):
        protein_id = st.text_input(
            "UniProt accession",
            value=st.session_state.active_accession,
            placeholder="Example: P69905"
        ).strip().upper()

        submitted = st.form_submit_button(
            "✦  Explore protein",
            use_container_width=True
        )

with right:
    st.markdown("""
    <div class="panel">
        <div class="section-label">QUICK START</div>
        <div class="panel-title">Try an example</div>
        <div class="muted">
            <b>Hemoglobin alpha</b><br>
            P69905 · Oxygen transport<br><br>
            <b>Hemoglobin beta</b><br>
            P68871 · Oxygen transport<br><br>
            <b>Insulin</b><br>
            P01308 · Blood sugar regulation<br><br>
            <b>p53</b><br>
            P04637 · Cell growth regulation
        </div>
    </div>
    """, unsafe_allow_html=True)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "protein_record" not in st.session_state:
    st.session_state.protein_record = None

if "pdb_text" not in st.session_state:
    st.session_state.pdb_text = None

if "searched_id" not in st.session_state:
    st.session_state.searched_id = None

if "search_error" not in st.session_state:
    st.session_state.search_error = None


# --------------------------------------------------
# API REQUEST
# --------------------------------------------------
if submitted:
    st.session_state.protein_record = None
    st.session_state.pdb_text = None
    st.session_state.searched_id = None
    st.session_state.search_error = None

    if not protein_id:
        st.session_state.search_error = "Please enter a protein ID."

    elif not protein_id.replace("-", "").isalnum():
        st.session_state.search_error = (
            "Please enter a valid-looking UniProt accession."
        )

    else:
        st.session_state.active_accession = protein_id
        api_url = (
            "https://alphafold.ebi.ac.uk/api/prediction/"
            + protein_id
        )

        try:
            with st.spinner("Connecting to the AlphaFold database..."):
                response = requests.get(
                    api_url,
                    timeout=30,
                    headers={"User-Agent": "HelixProteinExplorer/1.0"}
                )

                if response.status_code == 404:
                    st.session_state.search_error = (
                        "No AlphaFold record was found for this ID."
                    )
                else:
                    response.raise_for_status()
                    data = response.json()

                    if not isinstance(data, list) or not data:
                        st.session_state.search_error = (
                            "No protein structure record was returned."
                        )
                    else:
                        record = data[0]
                        st.session_state.protein_record = record
                        st.session_state.searched_id = protein_id

                        pdb_url = record.get("pdbUrl")

                        if pdb_url:
                            pdb_response = requests.get(
                                pdb_url,
                                timeout=30,
                                headers={
                                    "User-Agent": "HelixProteinExplorer/1.0"
                                }
                            )
                            pdb_response.raise_for_status()
                            st.session_state.pdb_text = pdb_response.text

                        elif record.get("cifUrl"):
                            st.session_state.search_error = (
                                "The record was found, but only an "
                                "mmCIF file is available. This version "
                                "of the viewer needs a PDB file."
                            )

        except requests.RequestException:
            st.session_state.search_error = (
                "Could not connect to the database or download the "
                "structure. Please try again."
            )
        except (ValueError, TypeError, IndexError):
            st.session_state.search_error = (
                "The database returned data that could not be processed."
            )


# --------------------------------------------------
# RESULTS
# --------------------------------------------------
record = st.session_state.protein_record
pdb_text = st.session_state.pdb_text

if st.session_state.search_error:
    st.error(st.session_state.search_error)

if record:
    name = record.get("uniprotDescription", "Unknown protein")
    accession = record.get(
        "uniprotAccession",
        st.session_state.searched_id
    )
    organism = record.get(
        "organismScientificName",
        "Not available"
    )
    gene = record.get("gene", "Not available")
    confidence = record.get("confidenceAvgLocalScore")
    sequence = record.get("uniprotSequence", "")
    sequence_length = len(sequence) if sequence else (
        record.get("uniprotEnd", 0)
        - record.get("uniprotStart", 1) + 1
    )
    model_version = record.get("latestVersion", "Available")
    structure_url = record.get("pdbUrl") or record.get("cifUrl")

    st.markdown("---")

    st.markdown(f"""
    <div class="section-label">02 / ANALYSIS WORKSPACE</div>
    <div class="panel-title" style="font-size:28px;">
        Protein overview
    </div>
    <div class="muted" style="margin-bottom:20px;">
        <span class="status-dot"></span>
        Structure record retrieved successfully
    </div>
    """, unsafe_allow_html=True)

    # Metric cards
    m1, m2, m3, m4 = st.columns(4, gap="medium")

    # AlphaFold API metadata may omit the mean score. In AlphaFold PDB files,
    # the B-factor column stores per-residue pLDDT, so compute its mean if needed.
    try:
        confidence = float(confidence) if confidence is not None else None
    except (ValueError, TypeError):
        confidence = None

    if confidence is None and pdb_text:
        residue_scores = []
        for line in pdb_text.splitlines():
            if line.startswith(("ATOM  ", "HETATM")) and len(line) >= 66:
                try:
                    residue_scores.append(float(line[60:66].strip()))
                except (ValueError, TypeError):
                    pass
        if residue_scores:
            confidence = sum(residue_scores) / len(residue_scores)

    confidence_text = (
        f"{confidence:.1f} / 100"
        if confidence is not None
        else "Not provided by AlphaFold"
    )

    metrics = [
        (m1, "🧬", "ACCESSION", accession),
        (m2, "🔗", "GENE", gene),
        (m3, "📏", "SEQUENCE LENGTH", str(sequence_length)),
        (m4, "✦", "AVG. CONFIDENCE", confidence_text)
    ]

    for col, icon, label, value in metrics:
        with col:
            safe_value = html.escape(str(value))
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">{icon}</div>
                <div class="metric-label">{label}</div>
                <div class="metric-value">{safe_value}</div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")

    # Protein information and 3D viewer
    info_col, viewer_col = st.columns([0.85, 1.5], gap="large")

    with info_col:
        st.markdown(f"""
        <div class="panel">
            <div class="section-label">PROTEIN PROFILE</div>
            <div class="panel-title">
                {html.escape(str(name))}
            </div>
            <div class="muted">
                Scientific protein information retrieved from
                the AlphaFold Database.
            </div>
            <div class="info-row">
                <div class="info-key">UniProt accession</div>
                <div class="info-value">{html.escape(str(accession))}</div>
            </div>
            <div class="info-row">
                <div class="info-key">Organism</div>
                <div class="info-value">{html.escape(str(organism))}</div>
            </div>
            <div class="info-row">
                <div class="info-key">Gene</div>
                <div class="info-value">{html.escape(str(gene))}</div>
            </div>
            <div class="info-row">
                <div class="info-key">Model version</div>
                <div class="info-value">{html.escape(str(model_version))}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="panel">
            <div class="section-label">HOW TO EXPLORE</div>
            <div class="panel-title">Navigate the molecule</div>
            <div class="muted">
                <b>Rotate:</b> Click and drag the model.<br><br>
                <b>Zoom:</b> Use your mouse wheel or trackpad.<br><br>
                <b>Inspect:</b> Look at the protein's overall
                folded shape and colored regions.<br><br>
                <b>Download:</b> Save the PDB file for further
                exploration in compatible software.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with viewer_col:
        st.markdown("""
        <div class="section-label">03 / MOLECULAR VISUALIZATION</div>
        <div class="panel-title">Interactive 3D structure</div>
        <div class="muted" style="margin-bottom:12px;">
            Drag to rotate · Scroll to zoom · Explore the fold
        </div>
        """, unsafe_allow_html=True)

        if pdb_text:
            # JSON encoding safely transfers the PDB text to JavaScript.
            pdb_json = (
                json.dumps(pdb_text)
                .replace("<", "\\u003c")
                .replace(">", "\\u003e")
                .replace("&", "\\u0026")
            )

            viewer_html = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    * { box-sizing: border-box; }
                    body {
                        margin: 0;
                        background: #f7f9fc;
                        font-family: sans-serif;
                        overflow: hidden;
                    }
                    #viewer {
                        height: 510px;
                        width: 100%;
                        background:
                            radial-gradient(circle at 50% 45%,
                            #ffffff, #eef4fb);
                    }
                    .viewer-caption {
                        text-align: center;
                        font-size: 11px;
                        color: #63748c;
                        padding: 8px;
                        background: #f7f9fc;
                    }
                </style>
            </head>
            <body>
                <div id="viewer"></div>
                <div class="viewer-caption">
                    MOLECULAR MODEL · DRAG TO ROTATE · SCROLL TO ZOOM
                </div>

                <script src="https://3dmol.org/build/3Dmol-min.js"></script>
                <script>
                    const pdbText = PDB_PLACEHOLDER;
                    const element = document.getElementById("viewer");

                    function showModel() {
                        if (!window.$3Dmol) {
                            element.innerHTML =
                                "3D viewer unavailable. Check your internet connection.";
                            return;
                        }

                        const viewer = $3Dmol.createViewer(
                            element,
                            {
                                backgroundColor: "#f7f9fc",
                                antialias: true
                            }
                        );

                        viewer.addModel(pdbText, "pdb");

                        viewer.setStyle(
                            {},
                            {
                                cartoon: {
                                    color: "spectrum",
                                    thickness: 0.8
                                }
                            }
                        );

                        viewer.zoomTo();
                        viewer.render();
                    }

                    if (window.$3Dmol) {
                        showModel();
                    } else {
                        element.innerHTML = "Loading molecular viewer...";
                        window.addEventListener("load", showModel);
                    }
                </script>
            </body>
            </html>
            """

            viewer_html = viewer_html.replace(
                "PDB_PLACEHOLDER",
                pdb_json
            )

            components.html(
                viewer_html,
                height=545,
                scrolling=False
            )

            st.download_button(
                label="↓  Download protein structure (.pdb)",
                data=pdb_text,
                file_name=f"{accession}.pdb",
                mime="chemical/x-pdb",
                use_container_width=True
            )

            if structure_url:
                st.markdown(
                    f"[View original structure file ↗]({structure_url})"
                )

        else:
            st.warning(
                "The protein record is available, but its PDB file "
                "could not be loaded for visualization."
            )

    # Sequence panel
    if sequence:
        with st.expander("View amino-acid sequence"):
            st.code(sequence, language=None)
            st.caption(
                f"Sequence length: {len(sequence)} amino acids."
            )

    st.caption(
        "Scientific note: AlphaFold structures are predictions. "
        "Confidence scores do not establish experimental accuracy."
    )


# --------------------------------------------------
# EMPTY STATE
# --------------------------------------------------
else:
    if not st.session_state.search_error:
        st.markdown("""
        <div class="panel" style="text-align:center;padding:38px 20px;">
            <div style="font-size:48px;margin-bottom:15px;">🧬</div>
            <div class="panel-title">Your discovery starts here</div>
            <div class="muted">
                Search for a protein to reveal its information
                and explore its predicted 3D structure.
            </div>
        </div>
        """, unsafe_allow_html=True)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("""
<div class="footer">
    <div style="color:#53e6e0;font-weight:700;letter-spacing:2px;">
        HELIX · PROTEIN EXPLORER
    </div>
    Built with Python · Streamlit · AlphaFold Database · 3Dmol.js<br>
    Academic prototype · Cloud deployment planned with AWS EC2
</div>
""", unsafe_allow_html=True)
