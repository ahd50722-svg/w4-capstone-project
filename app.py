import gradio as gr
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BlipProcessor,
    BlipForConditionalGeneration,
    BlipForQuestionAnswering,
)

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
LLM_ID = "Qwen/Qwen2.5-1.5B-Instruct"

# Models are loaded once when the app starts.
tokenizer = AutoTokenizer.from_pretrained(LLM_ID)
llm = AutoModelForCausalLM.from_pretrained(
    LLM_ID,
    torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32,
    device_map="auto",
)
caption_proc = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
caption_model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
).to(DEVICE)
vqa_proc = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")
vqa_model = BlipForQuestionAnswering.from_pretrained(
    "Salesforce/blip-vqa-base"
).to(DEVICE)

STYLE_GUIDES = {
    "Modern": "clean lines, practical furniture, neutral colors, and uncluttered styling",
    "Luxury": "elegant materials, refined lighting, layered textures, and a premium appearance",
    "Classic": "balanced furniture, timeless details, warm woods, and formal symmetry",
    "Minimal": "simple forms, fewer objects, functional storage, and calm colors",
    "Saudi Contemporary": "modern comfort with tasteful Saudi and Najrani-inspired details",
}
BUDGET_GUIDES = {
    "Low": "Prioritize paint, rearranging existing furniture, textiles, and affordable accessories.",
    "Medium": "Allow selected furniture replacement, improved lighting, curtains, and feature decor.",
    "High": "Allow custom furniture, premium finishes, architectural lighting, and full styling.",
}


def chat(prompt, system=None, max_new_tokens=420, **gen_kwargs):
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    inputs = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True, return_tensors="pt", return_dict=False
    ).to(llm.device)
    output = llm.generate(
        inputs,
        max_new_tokens=max_new_tokens,
        pad_token_id=tokenizer.eos_token_id,
        **gen_kwargs,
    )
    return tokenizer.decode(
        output[0][inputs.shape[1]:], skip_special_tokens=True
    ).strip()


def caption_image(image):
    inputs = caption_proc(image.convert("RGB"), return_tensors="pt").to(DEVICE)
    output = caption_model.generate(**inputs, max_new_tokens=45)
    return caption_proc.decode(output[0], skip_special_tokens=True)


def ask_image(image, question):
    inputs = vqa_proc(image.convert("RGB"), question, return_tensors="pt").to(DEVICE)
    output = vqa_model.generate(**inputs, max_new_tokens=30)
    return vqa_proc.decode(output[0], skip_special_tokens=True)


def design_room(image, style, budget, question, language):
    if image is None:
        return "Please upload a room image first. / الرجاء رفع صورة للغرفة أولًا."
    question = (question or "What type of room is this?").strip()
    caption = caption_image(image)
    visual_answer = ask_image(image, question)
    output_rule = (
        "Write the complete answer in clear Arabic. Keep the project title in English."
        if language == "Arabic"
        else "Write the complete answer in clear professional English."
    )
    prompt = f"""
You are RoomCraft AI, a careful interior-design assistant created by Ahad Dera.
Use only these visual observations. Do not invent dimensions or hidden features.
Image caption: {caption}
Question: {question}
Visual answer: {visual_answer}
Style: {style} — {STYLE_GUIDES[style]}
Budget: {budget} — {BUDGET_GUIDES[budget]}
Create a concise report with: Room Analysis, Color Palette, Furniture and Layout,
Lighting, Curtains and Textiles, Decor Details, Three Priority Actions, Important Note.
The note must say that structural/electrical work requires a qualified professional.
{output_rule}
"""
    report = chat(
        prompt,
        system="Give tasteful, realistic and practical interior-design advice.",
        do_sample=True,
        temperature=0.65,
        top_p=0.9,
        repetition_penalty=1.08,
    )
    return (
        f"**Project:** RoomCraft AI  \n**Created by:** Ahad Dera  \n"
        f"**Vision caption:** {caption}  \n**Visual Q&A:** {visual_answer}  \n\n{report}"
    )


with gr.Blocks(title="RoomCraft AI") as demo:
    gr.Markdown("# 🏠 RoomCraft AI\n### Interior Design Assistant by Ahad Dera")
    with gr.Row():
        with gr.Column():
            image_input = gr.Image(type="pil", label="Upload a room image")
            style_input = gr.Dropdown(list(STYLE_GUIDES), value="Modern", label="Style")
            budget_input = gr.Radio(list(BUDGET_GUIDES), value="Medium", label="Budget")
            question_input = gr.Textbox(
                value="What type of room is this and what are its main visible features?",
                label="Question about the image",
            )
            language_input = gr.Radio(["Arabic", "English"], value="Arabic", label="Language")
            button = gr.Button("Design My Room", variant="primary")
        with gr.Column():
            output = gr.Markdown()
    button.click(
        design_room,
        [image_input, style_input, budget_input, question_input, language_input],
        output,
    )
    gr.Markdown("*AI suggestions are for inspiration. Consult professionals before structural or electrical changes.*")

if __name__ == "__main__":
    demo.launch()
