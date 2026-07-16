# RoomCraft AI — One-Page Project Write-up

**Student:** Ahad Dera  
**Program:** Generative AI Summer Bootcamp, Najran University  
**Track:** Multimodal Generative AI

## Problem

Choosing suitable colors, furniture, lighting, curtains, and décor for a room can be difficult for non-specialists. Professional consultations may not always be immediately available, and users often need a quick starting point before making design decisions.

## Solution

RoomCraft AI is a multimodal interior-design assistant. A user uploads a room photo, chooses a preferred design style and budget level, asks an optional question, and selects Arabic or English. The application analyzes the image and returns an organized design report with a room analysis, color palette, furniture and layout recommendations, lighting, curtains and textiles, décor details, and three priority actions.

## Generative AI pipeline

The application combines three open models. BLIP Image Captioning creates a description of the image. BLIP Visual Question Answering answers the user's visual question. Qwen2.5-1.5B-Instruct receives these observations together with the selected style and budget, then generates personalized interior-design recommendations. A Gradio interface connects the full pipeline into a simple web application.

## Value and uniqueness

RoomCraft AI makes basic design guidance accessible to Arabic-speaking users and includes a Saudi Contemporary style option. The project connects my interest in interior design with practical generative AI skills learned during the bootcamp.

## Limitations and responsible use

The model can misunderstand images and cannot confirm measurements, materials, electrical safety, or structural conditions. The recommendations are inspirational rather than professional plans. Users are clearly advised to consult qualified professionals before structural, electrical, or construction work.

## Future improvements

Future versions could generate a matching color-palette image, support before-and-after visualization, recognize room dimensions, save design reports, and connect recommendations to locally available furniture products.
