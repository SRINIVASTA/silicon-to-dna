import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import hashlib

# --- 1. SET PAGE CONFIGURATION ---
st.set_page_config(page_title="DNA Storage Simulator Pro", page_icon="🧬", layout="wide")

# --- 2. PERSISTENT MEMORY STORAGE ---
if "dna_strand" not in st.session_state:
    st.session_state.dna_strand = ""
if "filename" not in st.session_state:
    st.session_state.filename = "downloaded_file.pdf"
if "checksum" not in st.session_state:
    st.session_state.checksum = ""

# --- 3. ADVANCED DNA CODING ENGINES ---
def encode_bytes_to_dna(data_bytes):
    """Converts raw file bytes into continuous A,C,G,T strands with validation tracking."""
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

def decode_dna_to_bytes(dna_string):
    """Reconstructs clean binary letters back into raw file byte arrays."""
    mapping = {"A": "00", "C": "01", "G": "10", "T": "11"}
    clean_dna = [base for base in dna_string.upper() if base in mapping]
    binary_string = "".join(mapping[base] for base in clean_dna)
    byte_aligned_length = (len(binary_string) // 8) * 8
    binary_string = binary_string[:byte_aligned_length]
    byte_arr = bytearray()
    for i in range(0, len(binary_string), 8):
        byte_arr.append(int(binary_string[i:i+8], 2))
    return bytes(byte_arr)

def check_homopolymers(dna_sequence):
    """Detects dangerous structural repetitions (4+ identical bases in a row)."""
    max_run = 0
    current_run = 1
    for i in range(1, len(dna_sequence)):
        if dna_sequence[i] == dna_sequence[i-1]:
            current_run += 1
            max_run = max(max_run, current_run)
        else:
            current_run = 1
    return max_run

# --- 4. DYNAMIC PLOTLY GENERATOR ---
def generate_density_chart(dna_sequence):
    """Calculates molecular chemical density profile loops across moving sequences."""
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
        x=positions, y=gc_densities, 
        mode='lines+markers', name='GC Ratio %',
        line=dict(color='#00CC96', width=2),
        marker=dict(size=4)
    ))
    
    fig.add_hline(y=50, line_dash="dash", line_color="cyan", annotation_text="Ideal Target (50%)")
    fig.add_hrect(y0=40, y1=60, line_width=0, fillcolor="rgba(0,204,150,0.1)", annotation_text="Stability Zone")
    
    fig.update_layout(
        title="Interactive Molecular Density Profile",
        xaxis_title="Nucleotide Base Index Location",
        yaxis_title="GC Density Ratio (%)",
        yaxis_range=[0, 100],
        template="plotly_dark",
        height=320,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

# --- 5. SYSTEM LAYOUT UI ---
st.title("🧬 DNA Storage Simulator Pro")
st.caption("Upload production files, encode them to biological sequences, and monitor chemical density profiles.")

tab1, tab2 = st.tabs(["📤 Upload & Encode Files", "📥 Read & Decode DNA"])

# --- TAB 1: AUTOMATED ENCODER ---
with tab1:
    st.subheader("Encode Any File")
    
    # 🚀 JAVASCRIPT INJECTION: Reaches inside Streamlit DOM to modify the system "25MB" layout rule text
    components.html(
        """
        <script>
            function patchUploader() {
                const instructions = window.parent.document.querySelectorAll('[data-testid="stFileUploaderDropzoneInstructions"]');
                instructions.forEach(el => {
                    const smallText = el.querySelector('small');
                    if (smallText && !smallText.innerHTML.includes('50KB')) {
                        smallText.innerHTML = "Limit 50KB per file • PDF, PNG, JPG, TXT";
                        smallText.style.fontSize = "13px";
                        smallText.style.fontWeight = "bold";
                        smallText.style.color = "#FF4B4B";
                    }
                });
            }
            patchUploader();
            setInterval(patchUploader, 1000);
        </script>
        """,
        height=0,
        width=0
    )

    uploaded_file = st.file_uploader("Choose a small file (Text, Image, PDF up to 50KB):", type=["pdf", "png", "jpg", "txt"])
    
    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        file_size_kb = len(file_bytes) / 1024
        
        # The 50KB Hard Guard Block
        if file_size_kb > 50.0:
            st.error(f"❌ Upload Blocked! Your file is {file_size_kb:.2f} KB. The simulator safety ceiling is exactly 50.0 KB to protect system memory strings.")
            st.warning("⚠️ Processing millions of generated text bases will freeze your web browser layout window. Please downsize your file.")
        else:
            # Operational Pipeline Execution
            dna_sequence = encode_bytes_to_dna(file_bytes)
            file_hash = hashlib.md5(file_bytes).hexdigest()
            
            st.session_state.dna_strand = dna_sequence
            st.session_state.filename = uploaded_file.name
            st.session_state.checksum = file_hash
            
            # Metrics Dashboards
            c1, c2, c3 = st.columns(3)
            c1.metric("File Weight", f"{file_size_kb:.2f} KB")
            c2.metric("Binary Size", f"{len(file_bytes)} Bytes")
            c3.metric("Synthesized Strand Length", f"{len(dna_sequence)} Bases")
            
            st.markdown("### 🔬 Real-World Biological Storage Scale")
            nanograms = (len(dna_sequence) * 650) / 1e9
            st.info(f"⚖️ **Physical DNA Weight:** This file weighs **{nanograms:.6f} nanograms** as a physical molecule.")
            
            # Sequence Interface Panel
            st.markdown("### Generated Genetic Strand Code:")
            st.text_area("Full Untruncated Sequence Stream", value=dna_sequence, height=120, disabled=True)
            
            # Direct Sequence Download Button
            st.download_button(
                label="📄 Download Raw DNA Sequence (.txt)",
                data=dna_sequence,
                file_name=f"{uploaded_file.name}_sequence.txt",
                mime="text/plain"
            )
            
            # --- QUALITY & WAVEFORM CONTROL MODULE ---
            st.markdown("### 📊 Structural Quality Validation")
            gc_count = dna_sequence.count("G") + dna_sequence.count("C")
            gc_ratio = (gc_count / len(dna_sequence)) * 100 if dna_sequence else 0
            max_run = check_homopolymers(dna_sequence)
            
            v1, v2 = st.columns(2)
            v1.metric("Overall GC Content", f"{gc_ratio:.1f}%")
            v2.metric("Max Repeating Run length", f"{max_run} Bases")
            
            # Interactive Chart Display
            fig_density = generate_density_chart(dna_sequence)
            if fig_density:
                st.plotly_chart(fig_density, use_container_width=True)
                
            # Synthesis Diagnostics Warnings
            if max_run >= 4:
                st.warning(f"⚠️ Warning: Sequence contains a homopolymer sequence of {max_run} repeating bases. This could cause synthesis lasers to slip.")
            else:
                st.success("✅ Sequence passing homopolymer safety threshold checks successfully.")

# --- TAB 2: AUTOMATED DECODER ---
with tab2:
    st.subheader("Decode DNA Strands Back to Files")
    
    dna_input = st.text_area(
        "Input continuous raw DNA base sequence (A, C, G, T):", 
        value=st.session_state.dna_strand,
        height=150,
        help="This dynamically imports your generated sequence from the upload tab."
    )
    
    output_name = st.text_input(
        "Saved output name with original extension:", 
        value=f"decoded_{st.session_state.filename}"
    )
    
    if dna_input:
        try:
            reconstructed_bytes = decode_dna_to_bytes(dna_input)
            decoded_hash = hashlib.md5(reconstructed_bytes).hexdigest()
            
            if len(reconstructed_bytes) > 0:
                st.success("🧬 Decoding sequence execution successful!")
                
                # Check file verification authenticity integrity hashes
                if st.session_state.checksum and decoded_hash == st.session_state.checksum:
                    st.success("🛡️ File Integrity Verified: MD5 matching signatures confirmed. 0% data corruption detected.")
                else:
                    st.warning("⚠️ Warning: Data mismatch detected. The DNA sequence has been modified since synthesis.")
                
                # Execution download connection link
                st.download_button(
                    label="📥 Download Restored Asset",
                    data=reconstructed_bytes,
                    file_name=output_name,
                    mime="application/octet-stream"
                )
            else:
                st.error("The sequence string entered generated 0 bytes of readable digital data.")
        except Exception as e:
            st.error(f"Processing error during biological strand tracking: {str(e)}")
