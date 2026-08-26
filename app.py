import streamlit as st
import base64
import math

# --- 1. CONFIGURATION & STATE SYSTEM ---
st.set_page_config(page_title="DNA Storage Simulator Pro", page_icon="🧬", layout="wide")

# Persistent data handshake between operations
if "dna_strand" not in st.session_state:
    st.session_state.dna_strand = ""
if "filename" not in st.session_state:
    st.session_state.filename = "downloaded_file.pdf"
if "binary_size" not in st.session_state:
    st.session_state.binary_size = 0

# --- 2. BIOLOGICAL CORE ENGINE FUNCTIONS ---
def encode_bytes_to_dna(data_bytes):
    """Dynamically converts raw uploaded file bytes into continuous A,C,G,T strands."""
    # Convert bytes into a clean stream of 1s and 0s
    binary_string = "".join(f"{b:08b}" for b in data_bytes)
    
    # Map 2 bits to 1 nucleotide base
    mapping = {"00": "A", "01": "C", "10": "G", "11": "T"}
    dna_list = []
    
    for i in range(0, len(binary_string), 2):
        chunk = binary_string[i:i+2]
        if len(chunk) == 2:
            dna_list.append(mapping[chunk])
        else:
            # Handle leftover single bit pad
            dna_list.append("A" if chunk == "0" else "C")
            
    return "".join(dna_list), len(binary_string)

def decode_dna_to_bytes(dna_string):
    """Dynamically reconstructs clean binary letters back into the original raw byte stream."""
    mapping = {"A": "00", "C": "01", "G": "10", "T": "11"}
    
    # Filter away spaces or accidental punctuation marks
    clean_dna = [base for base in dna_string.upper() if base in mapping]
    binary_chunks = [mapping[base] for base in clean_dna]
    binary_string = "".join(binary_chunks)
    
    # Ensure binary length aligns correctly with whole 8-bit bytes
    byte_aligned_length = (len(binary_string) // 8) * 8
    binary_string = binary_string[:byte_aligned_length]
    
    byte_arr = bytearray()
    for i in range(0, len(binary_string), 8):
        byte_arr.append(int(binary_string[i:i+8], 2))
        
    return bytes(byte_arr)

# --- 3. DASHBOARD USER INTERFACE ---
st.title("🧬 DNA Storage Simulator Pro")
st.caption("Upload production files, encode them to biological sequences, and monitor chemical density profiles.")

# Navigation UI tabs
tab1, tab2 = st.tabs(["📤 Upload & Encode Files", "📥 Read & Decode DNA"])

# --- TAB 1: DYNAMIC ENCODING PROCESS ---
with tab1:
    st.subheader("Encode Any File")
    uploaded_file = st.file_uploader("Choose a small file (Text, Image, PDF up to 50KB):", type=["pdf", "png", "jpg", "txt", "docx"])
    
    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        file_size_bytes = len(file_bytes)
        
        # Guard checking size boundaries to protect cloud processing threads
        if file_size_bytes > 150000:
            st.error(f"File too large ({file_size_bytes / 1024:.2f} KB). Please upload a file smaller than 50KB.")
        else:
            # Execution Block: Trigger dynamic synthesis
            dna_sequence, bit_count = encode_bytes_to_dna(file_bytes)
            
            # Save calculations directly to application environment cache
            st.session_state.dna_strand = dna_sequence
            st.session_state.filename = uploaded_file.name
            st.session_state.binary_size = bit_count
            
            # Metric Columns
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("File Weight", f"{file_size_bytes / 1024:.1f} KB")
            with col2:
                st.metric("Binary Size", f"{file_size_bytes} Bytes")
            with col3:
                st.metric("Synthesized Strand Length", f"{len(dna_sequence)} Bases")
                
            st.markdown("### 🔬 Real-World Biological Storage Scale")
            # Mathematical constants approximating base density physics
            nanograms = (len(dna_sequence) * 650) / 1e9
            
            st.info(f"⚖️ **Physical DNA Weight:** This file weighs **{nanograms:.6f} nanograms** as a physical molecule.")
            st.success("⏳ **Format Lifespan:** Kept dry in cold capsules, this physical file will last for thousands of years without corruption.")
            
            # Sequence Display Panel
            st.markdown("### Generated Genetic Strand Code:")
            st.text_area("Live Data Stream", value=dna_sequence, height=180, disabled=True)
            
            # Chemical Stability Monitoring (GC-Content Calculation)
            gc_count = dna_sequence.count("G") + dna_sequence.count("C")
            gc_ratio = (gc_count / len(dna_sequence)) * 100 if dna_sequence else 0
            
            st.markdown("### 📊 Interactive Molecular Density Profile")
            st.metric("Total GC-Content Ratio", f"{gc_ratio:.1f}%")
            if 40 <= gc_ratio <= 60:
                st.success("✅ Excellent chemical stability target calculated for physical manufacturing.")
            else:
                st.warning("⚠️ Warning: Extreme GC balance variation could complicate thermal synthesis loops.")

# --- TAB 2: DYNAMIC DECODING PROCESS ---
with tab2:
    st.subheader("Decode DNA Strands Back to Files")
    
    # AUTOMATIC CROSS-OVER PASTE LINK
    # Pulls directly from st.session_state.dna_strand so you never have to paste manually.
    dna_input = st.text_area(
        "Input continuous raw DNA base sequence (A, C, G, T):", 
        value=st.session_state.dna_strand,
        height=180,
        help="This automatically captures the sequence string generated in the previous step."
    )
    
    # AUTOMATIC FILENAME EXTENSION RETENTION
    output_name = st.text_input(
        "Saved output name with original extension:", 
        value=f"decoded_{st.session_state.filename}"
    )
    
    if dna_input:
        try:
            # Process text content into raw assembly bytes dynamically
            reconstructed_bytes = decode_dna_to_bytes(dna_input)
            
            if len(reconstructed_bytes) > 0:
                st.success("🧬 Decoding sequence execution successful!")
                
                # Concrete download hook referencing active memory allocations
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
