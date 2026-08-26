import streamlit as st
import base64

# --- 1. SET PAGE CONFIGURATION ---
st.set_page_config(page_title="DNA Storage Simulator Pro", page_icon="🧬", layout="wide")

# --- 2. PERSISTENT MEMORY STORAGE ---
if "dna_strand" not in st.session_state:
    st.session_state.dna_strand = ""
if "filename" not in st.session_state:
    st.session_state.filename = "downloaded_file.pdf"
if "decoded_bytes" not in st.session_state:
    st.session_state.decoded_bytes = None

# --- 3. BIOLOGICAL SIMULATOR CORES ---
def encode_bytes_to_dna(data_bytes):
    """Dynamically converts raw uploaded file bytes into continuous A,C,G,T strands."""
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
    """Dynamically reconstructs clean binary letters back into raw file byte arrays."""
    mapping = {"A": "00", "C": "01", "G": "10", "T": "11"}
    clean_dna = [base for base in dna_string.upper() if base in mapping]
    binary_string = "".join(mapping[base] for base in clean_dna)
    byte_aligned_length = (len(binary_string) // 8) * 8
    binary_string = binary_string[:byte_aligned_length]
    byte_arr = bytearray()
    for i in range(0, len(binary_string), 8):
        byte_arr.append(int(binary_string[i:i+8], 2))
    return bytes(byte_arr)

# --- 4. DYNAMIC VIEW COMPONENT ---
def display_file_preview(file_bytes, file_name):
    """Bypasses browser blockades to show real-time image, pdf, or text previews."""
    if not file_bytes:
        return
        
    ext = file_name.split(".")[-1].lower()
    st.markdown("### 👁️ Dynamic File Content View")
    
    if ext in ["png", "jpg", "jpeg"]:
        st.image(file_bytes, caption=f"Active View: {file_name}", use_container_width=True)
        
    elif ext == "pdf":
        st.info("📄 Generating Document Sandbox View...")
        # High compatibility iframe delivery system for cross-browser stability
        try:
            base64_pdf = base64.b64encode(file_bytes).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
        except Exception:
            st.warning("Your browser is blocking the inline PDF frame. Use the download module below to verify.")
            
    elif ext in ["txt", "csv", "log"]:
        st.text_area("File Text Output", value=file_bytes.decode("utf-8", errors="ignore"), height=250)
    else:
        st.warning(f"Preview engine unassigned for .{ext} files. The compiled payload remains completely safe.")

# --- 5. SYSTEM LAYOUT GRAPHICS ---
st.title("🧬 DNA Storage Simulator Pro")
st.caption("Upload production files, encode them to biological sequences, and monitor chemical density profiles.")

tab1, tab2 = st.tabs(["📤 Upload & Encode Files", "📥 Read & Decode DNA"])

# --- TAB 1: AUTOMATED ENCODER ---
with tab1:
    st.subheader("Encode Any File")
    uploaded_file = st.file_uploader("Choose a small file (Text, Image, PDF up to 50KB):", type=["pdf", "png", "jpg", "txt"])
    
    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        
        if len(file_bytes) > 150000:
            st.error("File size limits exceeded. Please process a file beneath 50KB.")
        else:
            # Automate mapping process immediately
            dna_sequence, bit_count = encode_bytes_to_dna(file_bytes)
            
            # Map values permanently to memory states
            st.session_state.dna_strand = dna_sequence
            st.session_state.filename = uploaded_file.name
            
            # Metrics Dashboards
            c1, c2, c3 = st.columns(3)
            c1.metric("File Weight", f"{len(file_bytes) / 1024:.2f} KB")
            c2.metric("Binary Size", f"{len(file_bytes)} Bytes")
            c3.metric("Synthesized Strand Length", f"{len(dna_sequence)} Bases")
            
            st.markdown("### 🔬 Real-World Biological Storage Scale")
            nanograms = (len(dna_sequence) * 650) / 1e9
            st.info(f"⚖️ **Physical DNA Weight:** This file weighs **{nanograms:.6f} nanograms** as a physical molecule.")
            st.success("⏳ **Format Lifespan:** Kept dry in cold capsules, this physical file will last for thousands of years without corruption.")
            
            st.markdown("### Generated Genetic Strand Code:")
            st.text_area("Full Untruncated Sequence Stream", value=dna_sequence, height=150, disabled=True)
            
            # Show live file preview immediately on upload
            display_file_preview(file_bytes, uploaded_file.name)

# --- TAB 2: AUTOMATED DECODER ---
with tab2:
    st.subheader("Decode DNA Strands Back to Files")
    
    # HANDSHAKE: Reads directly from state to remove manual typing errors
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
            # Reconstruct byte objects dynamically
            reconstructed_bytes = decode_dna_to_bytes(dna_input)
            st.session_state.decoded_bytes = reconstructed_bytes
            
            if len(reconstructed_bytes) > 0:
                st.success("🧬 Decoding sequence execution successful!")
                
                # Active non-zero memory download asset link
                st.download_button(
                    label="📥 Download Restored Asset",
                    data=reconstructed_bytes,
                    file_name=output_name,
                    mime="application/octet-stream"
                )
                
                # Show dynamic file view inside decoder window instantly
                display_file_preview(reconstructed_bytes, output_name)
            else:
                st.error("The sequence string entered generated 0 bytes of readable digital data.")
        except Exception as e:
            st.error(f"Processing error during biological strand tracking: {str(e)}")
