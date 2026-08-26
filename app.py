import streamlit as st
import pandas as pd
import collections
import plotly.express as px
import re

# Binary to DNA translation dictionary (Base-4 Mapping System)
BINARY_TO_DNA = {'00': 'A', '01': 'C', '10': 'G', '11': 'T'}
DNA_TO_BINARY = {v: k for k, v in BINARY_TO_DNA.items()}

def scramble_bits(byte_data):
    # Applies an XOR Bit-Mask (0xAA = 10101010) to scramble long sequences of repetitive bits
    return bytes([b ^ 0xAA for b in byte_data])

def bytes_to_dna(byte_data, apply_scramble=False):
    if apply_scramble:
        byte_data = scramble_bits(byte_data)
    # Convert raw data bytes directly into a clean binary bit stream string
    binary_str = ''.join(format(b, '08b') for b in byte_data)
    # Parse bits in pairs and map directly to chemical bases
    dna_seq = ""
    for i in range(0, len(binary_str), 2):
        pair = binary_str[i:i+2]
        dna_seq += BINARY_TO_DNA[pair]
    return dna_seq, binary_str

def dna_to_bytes(dna_seq, apply_unscramble=False):
    try:
        # Convert character bases back to digital binary fragments
        binary_str = ''.join(DNA_TO_BINARY[base] for base in dna_seq if base in DNA_TO_BINARY)
        byte_list = []
        # Re-group binary bits into standard 8-bit bytes
        for i in range(0, len(binary_str), 8):
            byte = binary_str[i:i+8]
            if len(byte) == 8:
                byte_list.append(int(byte, 2))
        
        raw_bytes = bytes(byte_list)
        if apply_unscramble:
            raw_bytes = scramble_bits(raw_bytes) # XORing again with 0xAA perfectly reverses it
        return raw_bytes
    except Exception:
        return None

def check_homopolymers(dna_seq):
    # Regex to find any base repeating 6 or more times (e.g., AAAAAA, CCCCCC)
    pattern = r'([ACGT])\1{5,}'
    matches = re.findall(pattern, dna_seq)
    return len(matches) > 0

# --- STREAMLIT USER INTERFACE CONFIGURATION ---
st.set_page_config(page_title="DNA Data Storage Simulator Pro", page_icon="🧬", layout="wide")

st.title("🧬 DNA Storage Simulator Pro")
st.markdown("Upload production files, encode them to biological sequences, and monitor chemical density profiles.")

# Keep track of scramble states across button clicks using Session State
if 'scramble_active' not in st.session_state:
    st.session_state.scramble_active = False

tab1, tab2 = st.tabs(["📤 Upload & Encode Files", "📥 Read & Decode DNA"])

with tab1:
    st.header("Encode Any File")
    uploaded_file = st.file_uploader("Choose a small file (Text, Image, PDF up to 50KB):", type=['txt', 'png', 'jpg', 'pdf'])
    
    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        
        # Execute Codec Conversion Engine (Checks state of Scrambler)
        dna_output, raw_binary = bytes_to_dna(file_bytes, apply_scramble=st.session_state.scramble_active)
        
        # Metric Layout Matrix Configuration
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="File Weight", value=f"{len(file_bytes)} Bytes")
        with col2:
            st.metric(label="Binary Size", value=f"{len(raw_binary)} Bits")
        with col3:
            st.metric(label="Synthesized Strand Length", value=f"{len(dna_output)} Bases")
            
        # --- PHYSICAL SCALE & CAPACITY CALCULATOR ---
        st.markdown("---")
        st.subheader("🔬 Real-World Biological Storage Scale")
        
        physical_weight_ng = len(dna_output) * 0.0000033
        sand_grain_capacity_bytes = 4400 / 0.0000033
        copies_in_sand = int(sand_grain_capacity_bytes / len(dna_output)) if len(dna_output) > 0 else 0
        
        calc_col1, calc_col2, calc_col3 = st.columns(3)
        with calc_col1:
            st.info(f"⚖️ **Physical DNA Weight:**\n\n This file weighs **{physical_weight_ng:.6f} nanograms** as a physical molecule.")
        with calc_col2:
            st.info(f"⏳ **Format Lifespan:**\n\n Kept dry in cold capsules, this physical file will last for **thousands of years** without corruption.")
        with calc_col3:
            st.info(f"🏜️ **Density Scale:**\n\n You could pack **{copies_in_sand:,} perfect copies** of this exact file onto **a single grain of sand**.")
        st.markdown("---")
        
        # Layout Division for Interface Alignment
        left_panel, right_panel = st.columns(2)
        
        with left_panel:
            st.subheader("Generated Genetic Strand Code:")
            if st.session_state.scramble_active:
                st.caption("🔒 *XOR Scrambler Active: Repeating bit patterns broken down.*")
                
            preview_len = 1000
            if len(dna_output) > preview_len:
                st.code(dna_output[:preview_len] + f"\n\n[... Truncated: {len(dna_output) - preview_len} more letters synthesized ...]", language="text")
            else:
                st.code(dna_output, language="text")
                
            st.download_button(
                label="🧬 Download Synthesized DNA Sequence (.txt)",
                data=dna_output,
                file_name="synthesized_dna.txt",
                mime="text/plain"
            )
                
        with right_panel:
            st.subheader("📊 Interactive Molecular Density Profile")
            counts = collections.Counter(dna_output)
            total_bases = len(dna_output) if len(dna_output) > 0 else 1
            
            base_data = []
            for base in ['A', 'C', 'G', 'T']:
                qty = counts.get(base, 0)
                base_data.append({
                    'Chemical Base': base,
                    'Quantity (Count)': qty,
                    'Percentage (%)': round((qty / total_bases) * 100, 2)
                })
            
            chart_df = pd.DataFrame(base_data)
            fig = px.bar(
                chart_df, x='Chemical Base', y='Quantity (Count)', color='Chemical Base', text='Percentage (%)',
                color_discrete_map={'A': '#FF4B4B', 'C': '#0068C9', 'G': '#29B09D', 'T': '#FFABAB'}
            )
            fig.update_traces(texttemplate='%{text}%', textposition='outside')
            fig.update_layout(showlegend=False, margin=dict(l=20, r=20, t=20, b=20), height=350)
            st.plotly_chart(fig, use_container_width=True)
            
            # --- STRUCTURAL CONSTRAINT VALIDATION ALERTS ---
            st.subheader("🔬 Synthesis Feasibility Report")
            
            gc_count = counts.get('G', 0) + counts.get('C', 0)
            gc_percentage = (gc_count / total_bases) * 100
            st.metric(label="Total GC-Content Ratio", value=f"{gc_percentage:.1f}%")
            
            if gc_percentage > 60 or gc_percentage < 40:
                st.warning("⚠️ High structural risk: Ratios outside the 40-60% margin can trigger structural folding errors in physical wet labs.")
            else:
                st.success("✅ Excellent chemical stability target calculated for physical manufacturing.")
                
            has_homopolymer = check_homopolymers(dna_output)
            if has_homopolymer:
                st.error("⚠️ Warning: Sequence contains a homopolymer sequence of 6 or more repeating bases. This could cause synthesis lasers or enzymes to slip during production.")
                
                # Active Remediation Button
                if st.button("🔧 Apply Software XOR Scrambler to Fix Sequence"):
                    st.session_state.scramble_active = True
                    st.rerun()
            else:
                st.success("✅ No severe homopolymer repeats detected. Optical synthesis alignment is highly secure.")
                if st.session_state.scramble_active:
                    if st.button("↩️ Reset/Turn Off Scrambler"):
                        st.session_state.scramble_active = False
                        st.rerun()

with tab2:
    st.header("Decode DNA Strands Back to Files")
    dna_input = st.text_area("Input continuous raw DNA base sequence (A, C, G, T):", "")
    target_filename = st.text_input("Saved output name with original extension (e.g., invoice_recovered.pdf):", "invoice_recovered.pdf")
    
    # User toggles based on whether they used the scrambler tool
    used_scrambler = st.checkbox("Was this sequence scrambled using the XOR mask?")
    
    if st.button("Run Sequencing Pipeline") and dna_input:
        cleaned_dna = dna_input.upper().replace("\n", "").replace(" ", "").strip()
        decoded_bytes = dna_to_bytes(cleaned_dna, apply_unscramble=used_scrambler)
        
        if decoded_bytes:
            st.success("🧬 Decoding sequence execution successful!")
            st.download_button(
                label="📥 Download Recovered File to Local Drive",
                data=decoded_bytes,
                file_name=target_filename,
                mime="application/octet-stream"
            )
        else:
            st.error("Failed to sequence file. Ensure base groupings follow rigid data bit pairings.")
