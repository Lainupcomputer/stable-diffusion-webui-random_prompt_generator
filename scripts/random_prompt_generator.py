from typing import Union, Any

import gradio as gr
import modules
from modules import script_callbacks
import glob
import random


class Swap:

    def __init__(self):
        self.data = ""


swap = Swap()


def get_prompts():
    prompt_lists = []
    final_prompts = []
    prompt_str = ""
    script_path = "./extensions/stable-diffusion-webui-random_prompt_generator"
    static_prompts = open_file(script_path + "./static.txt")
    prompt_folder = "/Prompts/*.txt"
    file_paths = glob.glob(script_path + prompt_folder)

    for static in static_prompts:
        prompt_str = prompt_str + static + ", "

    for path in file_paths:
        prompt_lists.append(open_file(path))

    for prompt_list in prompt_lists:
        final_prompts.append(random.choice(prompt_list))

    for prompt in final_prompts:
        prompt_str = prompt_str + prompt + ", "

    return prompt_str


def open_file(filename):
    # open a file from fs and read data to type:list[]
    data_output = []
    with open(filename, "r")as f:
        lines = f.readlines()
        for line in lines:
            sl = line.split("\n")
            data_output.append(sl[0])
        return data_output


def add_to_prompt():
    return swap.data


def on_ui_tabs():
    txt2img_prompt = modules.ui.txt2img_paste_fields[0][0]

    with gr.Blocks(analytics_enabled=False) as prompt_generator:
        with gr.Column():
            with gr.Row():
                gen_btn = gr.Button(value="Generate", elem_id="generate_button")

        with gr.Column(visible=False) as results_col:
            results = gr.Text(label="Results", elem_id="Results_textBox", interactive=False)
        with gr.Column():
            warning = gr.HTML(value="Send the first generated prompt to:", visible=False)
            with gr.Row():
                send_to_txt2img = gr.Button('Send to txt2img', visible=False)

        def generate_prompts():
            swap.data = get_prompts()
            return {results: swap.data,
                    send_to_txt2img: gr.update(visible=True),
                    results_col: gr.update(visible=True),
                    warning: gr.update(visible=True)
                    }

        # events
        gen_btn.click(fn=generate_prompts, outputs=[results, send_to_txt2img, results_col, warning])
        send_to_txt2img.click(add_to_prompt, outputs=[txt2img_prompt])
        send_to_txt2img.click(None, _js='switch_to_txt2img', inputs=None, outputs=None)
    return (prompt_generator, "Random-Prompt-Gen", "Random-Prompt-Gen"),


script_callbacks.on_ui_tabs(on_ui_tabs)
