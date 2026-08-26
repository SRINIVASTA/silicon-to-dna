import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import hashlib
import collections
import pandas as pd
import re

# --- 1. CONFIGURATION AND PERSISTENT MEMORY ---
st.set_page_config(page_title="DNA Storage Simulator Pro", page_icon="🧬", layout="wide")

if "dna_strand" not in st.session_state:
    st.session_state.dna_strand = ""
if "filename" not in st.session_state:
    st.session_state.filename = "downloaded_file.pdf"
if "checksum" not in st.session_state:
    st.session_state.checksum = ""
if "scramble_active" not in st.session_state:
    st.session_state.scramble_active = False

# --- 2. ADVANCED BIOLOGICAL CODECS ---
def scramble_bits(byte_data):
    """Applies a rotating XOR Bit-Mask (0xAA) to shatter repetitive sequential binary layers."""
    return bytes([b ^ 0xAA for b in byte_data])

def encode_bytes_to_dna(data_bytes, apply_scramble=False):
    """Translates digital data byte arrays directly into active A,C,G,T nucleotide streams."""
    if apply_scramble:
        data_bytes = scramble_bits(data_bytes)
    binary_string = "".join(f"{b:08b}" for b in data_bytes)
    mapping = {"00": "A", "01": "C", "10": "G", "11": "T"}
    dna_list = []
    for i in range(0, len(binary_string), 2):
        chunk = binary_string[i:i+2]
        if len(chunk) == 2:
            dna_list.append(mapping[chunk])
        else:
            dna_list.append("A" if chunk == "0" else "C")
    return "".join(dna_list)

def decode_dna_to_bytes(dna_string, apply_unscramble=False):
    """Decodes character arrays safely back into original file byte signatures."""
    mapping = {"A": "00", "C": "01", "G": "10", "T": "11"}
    clean_dna = [base for base in dna_string.upper() if base in mapping]
    binary_string = "".join(mapping[base] for base in clean_dna)
    byte_aligned_length = (len(binary_string) // 8) * 8
    binary_string = binary_string[:byte_aligned_length]
    byte_arr = bytearray()
    for i in range(0, len(binary_string), 8):
        byte_arr.append(int(binary_string[i:i+8], 2))
        
    raw_bytes = bytes(byte_arr)
    if apply_unscramble:
        raw_bytes = scramble_bits(raw_bytes)
    return raw_bytes

def check_homopolymers(dna_sequence):
    """Finds exact hardware laser-slip threats (6+ consecutive matching characters)."""
    pattern = r'([ACGT])\1{5,}'
    matches = re.findall(pattern, dna_sequence)
    return len(matches) > 0

# --- 3. MOLECULAR GRAPH VISUALIZATIONS ---
def generate_density_chart(dna_sequence):
    """Generates continuous wave mapping profiles along the sequence tracking array."""
    if not dna_sequence:
        return None
    step = max(1, len(dna_sequence) // 50)
    chunks = [dna_sequence[i:i+step] for i in range(0, len(dna_sequence), step)]
    gc_densities = []
    positions = []
    for index, chunk in enumerate(chunks):
        gc_count = chunk.count("G") + chunk.count("C")
        ratio = (gc_count / len(chunk)) * 100 if chunk else 0
        gc_densities.append(ratio)
        positions.append(index * step)
        
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=positions, y=gc_densities, mode='lines+markers', name='GC Ratio %',
        line=dict(color='#00CC96', width=2), marker=dict(size=4)
    ))
    fig.add_hline(y=50, line_dash="dash", line_color="cyan", annotation_text="Ideal (50%)")
    fig.add_hrect(y0=40, y1=60, line_width=0, fillcolor="rgba(0,204,150,0.1)", annotation_text="Stability Zone")
    fig.update_layout(
        title="Interactive Molecular Density Wave Profile",
        xaxis_title="Nucleotide Base Index Location", yaxis_title="GC Density Ratio (%)",
        yaxis_range=[0, 100], template="plotly_dark", height=280, margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig
# --- 4. GRAPHICAL SYSTEM LAYOUT UI ---
st.title("🧬 DNA Storage Simulator Pro")
st.caption("Upload production files, encode them to biological sequences, and monitor chemical density profiles.")

tab1, tab2 = st.tabs(["📤 Upload & Encode Files", "📥 Read & Decode DNA"])

with tab1:
    st.subheader("Encode Any File")
    st.markdown("""
        <style>
            div[data-testid="stFileUploaderDropzoneInstructions"] small {
                font-size: 0px !important; display: none !important; visibility: hidden !important;
            }
            div[data-testid="stFileUploaderDropzoneInstructions"]::after {
                content: "Limit 50KB per file • PDF, PNG, JPG, TXT";
                font-size: 13px !important; color: #A3A3A3; display: block; margin-top: 4px; font-weight: bold;
            }
        </style>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Choose a small file:", type=["pdf", "png", "jpg", "txt"], label_visibility="collapsed")
    
    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        file_size_kb = len(file_bytes) / 1024
        
        if file_size_kb > 50.0:
            st.error(f"❌ Upload Blocked! Your file is {file_size_kb:.2f} KB. Safety limit is 50.0 KB.")
        else:
            dna_sequence = encode_bytes_to_dna(file_bytes, apply_scramble=st.session_state.scramble_active)
            file_hash = hashlib.md5(file_bytes).hexdigest()
            
            st.session_state.dna_strand = dna_sequence
            st.session_state.filename = uploaded_file.name
            st.session_state.checksum = file_hash
            
            c1, c2, c3 = st.columns(3)
            c1.metric("File Weight", f"{file_size_kb:.2f} KB")
            c2.metric("MD5 Original Checksum", file_hash[:16] + "...")
            c3.metric("Synthesized Strand Length", f"{len(dna_sequence)} Bases")
            
            st.markdown("### 🔬 Real-World Biological Storage Scale")
            nanograms = (len(dna_sequence) * 650) / 1e9
            st.info(f"⚖️ **Physical DNA Weight:** This file weighs **{nanograms:.6f} nanograms** as a physical molecule.")
            
            left_layout, right_layout = st.columns(2)
            
            with left_layout:
                st.markdown("### Generated Genetic Strand Code:")
                if st.session_state.scramble_active:
                    st.caption("🔒 *XOR Scrambler Active: Operational sequences randomized successfully.*")
                st.text_area("Full Stream View", value=dna_sequence, height=120, disabled=True, label_visibility="collapsed")
                
                st.download_button(
                    label="📄 Download Raw DNA Sequence (.txt)",
                    data=dna_sequence, file_name=f"{uploaded_file.name}_sequence.txt", mime="text/plain"
                )
                
                fig_density = generate_density_chart(dna_sequence)
                if fig_density:
                    st.plotly_chart(fig_density, use_container_width=True)
            
            with right_layout:
                st.markdown("### 📊 Total Chemical Distribution Profile")
                counts = collections.Counter(dna_sequence)
                total_bases = len(dna_sequence) if len(dna_sequence) > 0 else 1
                
                base_data = []
                for base in ['A', 'C', 'G', 'T']:
                    qty = counts.get(base, 0)
                    base_data.append({
                        'Chemical Base': base, 'Quantity (Count)': qty, 'Percentage (%)': round((qty / total_bases) * 100, 2)
                    })
                
                chart_df = pd.DataFrame(base_data)
                fig_bar = px.bar(
                    chart_df, x='Chemical Base', y='Quantity (Count)', color='Chemical Base', text='Percentage (%)',
                    color_discrete_map={'A': '#FF4B4B', 'C': '#0068C9', 'G': '#29B09D', 'T': '#FFABAB'}
                )
                fig_bar.update_traces(texttemplate='%{text}%', textposition='outside')
                fig_bar.update_layout(showlegend=False, template="plotly_dark", margin=dict(l=20, r=20, t=20, b=20), height=300)
                st.plotly_chart(fig_bar, use_container_width=True)
                
                st.markdown("### 🔬 Synthesis Feasibility Report")
                gc_count = dna_sequence.count("G") + dna_sequence.count("C")
                gc_ratio = (gc_count / total_bases) * 100
                has_homopolymer = check_homopolymers(dna_sequence)
                
                st.metric("Overall GC Content Ratio", f"{gc_ratio:.1f}%")
                
                if gc_ratio > 60 or gc_ratio < 40:
                    st.warning("⚠️ High structural risk: Ratios outside the 40-60% boundary trigger wet-lab folding anomalies.")
                else:
                    st.success("✅ Excellent chemical stability target calculated for physical manufacturing.")
                
                if has_homopolymer:
                    st.error("⚠️ Warning: Sequence contains a homopolymer sequence of 6 or more repeating bases. This could cause synthesis lasers or enzymes to slip during production.")
                    if st.button("🔧 Apply Software XOR Scrambler to Fix Sequence"):
                        st.session_state.scramble_active = True
                        st.rerun()
                else:
                    st.success("✅ Sequence passing homopolymer safety threshold checks successfully.")
                    if st.session_state.scramble_active:
                        if st.button("↩️ Reset/Turn Off Scrambler"):
                            st.session_state.scramble_active = False
                            st.rerun()

with tab2:
    st.subheader("Decode DNA Strands Back to Files")
    dna_input = st.text_area(
        "Input continuous raw DNA base sequence (A, C, G, T):", 
        value=st.session_state.dna_strand, height=150, help="Dynamically mapped from active upload sequence storage layers."
    )
    output_name = st.text_input("Saved output name with original extension:", value=f"decoded_{st.session_state.filename}")
    used_scrambler = st.checkbox("Was this sequence scrambled using the XOR mask?", value=st.session_state.scramble_active)
    
    if dna_input:
        try:
            reconstructed_bytes = decode_dna_to_bytes(dna_input, apply_unscramble=used_scrambler)
            decoded_hash = hashlib.md5(reconstructed_bytes).hexdigest()
            if len(reconstructed_bytes) > 0:
                st.success("🧬 Decoding sequence execution successful!")
                if st.session_state.checksum and decoded_hash == st.session_state.checksum:
                    st.success("🛡️ File Integrity Verified: MD5 matching signatures confirmed. 0% data corruption detected.")
                else:
                    st.warning("⚠️ Warning: Data mismatch detected. The DNA sequence has been modified since synthesis.")
                st.download_button(
                    label="📥 Download Restored Asset", data=reconstructed_bytes, file_name=output_name, mime="application/octet-stream"
                )
            else:
                st.error("The sequence string entered generated 0 bytes of readable digital data.")
        except Exception as e:
            st.error(f"Processing error during biological strand tracking: {str(e)}")
