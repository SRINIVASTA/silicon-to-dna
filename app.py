import streamlit as st
import base64

# --- 1. CONFIGURATION & STATE SYSTEM ---
st.set_page_config(page_title="DNA Storage Simulator Pro", page_icon="🧬", layout="wide")

# Initialize persistent memory across app interactions
if "dna_strand" not in st.session_state:
    st.session_state.dna_strand = ""
if "filename" not in st.session_state:
    st.session_state.filename = ""
if "file_bytes" not in st.session_state:
    st.session_state.file_bytes = None
if "mime_type" not in st.session_state:
    st.session_state.mime_type = ""

# --- 2. BIOLOGICAL CORE ENGINE FUNCTIONS ---
def encode_bytes_to_dna(data_bytes):
    """Converts raw uploaded file bytes into continuous A, C, G, T strands."""
    binary_string = "".join(f"{b:08b}" for b in data_bytes)
    mapping = {"00": "A", "01": "C", "10": "G", "11": "T"}
    dna_list = []
    for i in range(0, len(binary_string), 2):
        chunk = binary_string[i:i+2]
        if len(chunk) == 2:
            dna_list.append(mapping[chunk])
        else:
            dna_list.append("A" if chunk == "0" else "C")
    return "".join(dna_list), len(binary_string)

def decode_dna_to_bytes(dna_string):
    """Reconstructs clean binary streams back into original raw file bytes."""
    mapping = {"A": "00", "C": "01", "G": "10", "T": "11"}
    clean_dna = [base for base in dna_string.upper() if base in mapping]
    binary_chunks = [mapping[base] for base in clean_dna]
    binary_string = "".join(binary_chunks)
    byte_aligned_length = (len(binary_string) // 8) * 8
    binary_string = binary_string[:byte_aligned_length]
    byte_arr = bytearray()
    for i in range(0, len(binary_string), 8):
        byte_arr.append(int(binary_string[i:i+8], 2))
    return bytes(byte_arr)

def render_file_preview(file_bytes, filename, mime):
    """Handles inline visual rendering directly inside the dashboard layer."""
    if not file_bytes:
        return
    
    st.markdown("### 🖼️ Active File Document View")
    ext = filename.split(".")[-1].lower()
    
    if ext in ["png", "jpg", "jpeg"]:
        st.image(file_bytes, caption=filename, use_container_width=True)
    elif ext == "pdf":
        base64_pdf = base64.b64encode(file_bytes).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
    elif ext in ["txt", "csv", "log"]:
        try:
            text_content = file_bytes.decode("utf-8")
            st.text_area("Plain Text Content View", value=text_content, height=250, disabled=True)
        except Exception:
            st.warning("Unable to parse text file as clean UTF-8 string encoding.")
    else:
        st.info(f"📂 Inline viewing not supported for .{ext} format files. The file tracking pointer is secure.")

# --- 3. DASHBOARD USER INTERFACE ---
st.title("🧬 DNA Storage Simulator Pro")
st.caption("Upload production files, encode them to biological sequences, and monitor chemical density profiles.")

tab1, tab2 = st.tabs(["📤 Upload & Encode Files", "📥 Read & Decode DNA"])

# --- TAB 1: DYNAMIC ENCODING PROCESS ---
with tab1:
    st.subheader("Encode Any File")
    uploaded_file = st.file_uploader("Choose a small file (Text, Image, PDF up to 50KB):", type=["pdf", "png", "jpg", "jpeg", "txt"])
    
    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        file_size_bytes = len(file_bytes)
        
        if file_size_bytes > 150000:
            st.error(f"File too large ({file_size_bytes / 1024:.2f} KB). Please upload a file smaller than 50KB.")
        else:
            dna_sequence, bit_count = encode_bytes_to_dna(file_bytes)
            
            # Save states globally inside session pipeline
            st.session_state.dna_strand = dna_sequence
            st.session_state.filename = uploaded_file.name
            st.session_state.file_bytes = file_bytes
            st.session_state.mime_type = uploaded_file.type
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("File Weight", f"{file_size_bytes / 1024:.1f} KB")
            with col2:
                st.metric("Binary Size", f"{file_size_bytes} Bytes")
            with col3:
                st.metric("Synthesized Strand Length", f"{len(dna_sequence)} Bases")
                
            st.markdown("### 🔬 Real-World Biological Storage Scale")
            nanograms = (len(dna_sequence) * 650) / 1e9
            st.info(f"⚖️ **Physical DNA Weight:** This file weighs **{nanograms:.6f} nanograms** as a physical molecule.")
            st.success("⏳ **Format Lifespan:** Kept dry in cold capsules, this physical file will last for thousands of years without corruption.")
            
            st.markdown("### Generated Genetic Strand Code:")
            st.text_area("Live Data Stream", value=dna_sequence, height=150, disabled=True)
            
            # Chemical Analysis
            gc_count = dna_sequence.count("G") + dna_sequence.count("C")
            gc_ratio = (gc_count / len(dna_sequence)) * 100 if dna_sequence else 0
            st.markdown("### 📊 Interactive Molecular Density Profile")
            st.metric("Total GC-Content Ratio", f"{gc_ratio:.1f}%")
            if 40 <= gc_ratio <= 60:
                st.success("✅ Excellent chemical stability target calculated for physical manufacturing.")
            else:
                st.warning("⚠️ Warning: Extreme GC balance variation could complicate synthesis loop profiles.")
            
            # SHOW LIVE UPLOADED VIEW
            render_file_preview(st.session_state.file_bytes, st.session_state.filename, st.session_state.mime_type)

# --- TAB 2: DYNAMIC DECODING PROCESS ---
with tab2:
    st.subheader("Decode DNA Strands Back to Files")
    
    # Auto-fills with zero truncation loss
    dna_input = st.text_area(
        "Input continuous raw DNA base sequence (A, C, G, T):", 
        value=st.session_state.dna_strand,
        height=150
    )
    
    output_name = st.text_input(
        "Saved output name with original extension:", 
        value=f"decoded_{st.session_state.filename}" if st.session_state.filename else "downloaded_file.pdf"
    )
    
    if dna_input:
        try:
            reconstructed_bytes = decode_dna_to_bytes(dna_input)
            
            if len(reconstructed_bytes) > 0:
                st.success("🧬 Decoding sequence execution successful!")
                
                # Active non-zero byte stream download anchor point
                st.download_button(
                    label="📥 Download Restored Asset",
                    data=reconstructed_bytes,
                    file_name=output_name,
                    mime="application/octet-stream"
                )
                
                # SHOW LIVE DECODED VIEW
                render_file_preview(reconstructed_bytes, output_name, "application/octet-stream")
            else:
                st.error("The sequence string entered generated 0 bytes of readable digital data.")
        except Exception as e:
            st.error(f"Processing error during biological strand tracking: {str(e)}")
