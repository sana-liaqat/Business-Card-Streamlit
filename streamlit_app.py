import streamlit as st
import base64
import json
from PIL import Image
import io
from openai import OpenAI

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="AI Business Card Scanner",
    layout="centered"
)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("📇 AI Business Card Scanner")
st.caption("Powered by GPT-4o Vision")

st.divider()

# ---------------- HELPER ----------------
def image_to_base64(image: Image.Image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

import re
import json

def safe_json_parse(content: str):
    # Remove ```json and ``` wrappers if present
    match = re.search(r"\{.*\}", content, re.DOTALL)
    if not match:
        return {}

    try:
        return json.loads(match.group())
    except json.JSONDecodeError:
        return {}


def extract_business_card_data(image: Image.Image):
    image_base64 = image_to_base64(image)

    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI that extracts structured business card data. "
                    "The card may be in English, Arabic, or both.\n\n"
                    "Return ONLY valid JSON in the following format:\n"
                    "{\n"
                    "  \"First Name\": \"\",\n"
                    "  \"Last Name\": \"\",\n"
                    "  \"Designation\": \"\",\n"
                    "  \"Company Name\": \"\",\n"
                    "  \"Email\": \"\",\n"
                    "  \"Contact Number\": \"\",\n"
                    "  \"Fax Number\": \"\",\n"
                    "  \"Website\": \"\",\n"
                    "  \"Address\": \"\",\n"
                    "  \"Social Media Handle\": \"\"\n"
                    "}"
                )
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract structured information from this business card."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_base64}"
                        }
                    }
                ]
            }
        ],
    )

    content = response.choices[0].message.content
    print(content)  # For debugging purposes

    return safe_json_parse(content)

# ---------------- UI ----------------
uploaded_file = st.file_uploader(
    "Upload a business card image",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Business Card", width=300)

    if st.button("🚀 Scan Business Card"):
        with st.spinner("Understanding card content..."):
            data = extract_business_card_data(image)

        if not data:
            st.error("Extraction failed.")
        else:
            st.success("Business card scanned successfully")

            st.subheader("🧾 Extracted Information")

            col1, col2 = st.columns(2)

            with col1:
                st.text_input("First Name", data.get("First Name", ""), disabled=True)
                st.text_input("Last Name", data.get("Last Name", ""), disabled=True)
                st.text_input("Designation", data.get("Designation", ""), disabled=True)

            with col2:
                st.text_input("Company Name", data.get("Company Name", ""), disabled=True)
                st.text_input("Website", data.get("Website", ""), disabled=True)

            st.subheader("📞 Contact Details")
            col3, col4 = st.columns(2)

            with col3:
                st.text_input("Email", data.get("Email", ""), disabled=True)
                st.text_input("Contact Number", data.get("Contact Number", ""), disabled=True)

            with col4:
                st.text_input("Fax Number", data.get("Fax Number", ""), disabled=True)
                st.text_input("Social Media", data.get("Social Media Handle", ""), disabled=True)

            st.subheader("📍 Address")
            st.text_area("Address", data.get("Address", ""), height=80, disabled=True)

