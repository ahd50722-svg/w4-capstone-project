# RoomCraft AI 🏠

**RoomCraft AI** is a multimodal interior-design assistant created by **Ahad Dera** for the Najran University Generative AI Summer Bootcamp capstone.

## What it does

The user uploads a room photo, chooses a preferred style and budget, and receives recommendations for:

- Color palette
- Furniture and layout
- Lighting
- Curtains and textiles
- Décor details
- Three priority actions

The application can produce the report in Arabic or English.

## AI models

- `Salesforce/blip-image-captioning-base` for image captioning
- `Salesforce/blip-vqa-base` for visual question answering
- `Qwen/Qwen2.5-1.5B-Instruct` for personalized design recommendations

## Run in Google Colab

1. Open `RoomCraft_AI_Capstone_Ahad_Dera.ipynb` in Google Colab.
2. Enable a **T4 GPU**.
3. Run all cells in order.
4. Upload a room image in the Gradio interface.

## Limitations and responsible use

The system may misunderstand visual details and does not measure dimensions or assess structural safety. Its suggestions are for inspiration only. Structural, electrical, and construction changes must be reviewed by qualified professionals.
