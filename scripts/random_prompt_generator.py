import gradio as gr
import modules
from modules import script_callbacks
import glob
import random


class Swap:

    def __init__(self):
        # extension folder
        self.script_path = "./extensions/stable-diffusion-webui-random_prompt_generator"
        self.static_path = "./static.txt"
        self.prompt_path = "/Prompts/"
        # variable to store generated prompts
        self.prompt_output = ""
        self.file_list = []
        self.choose_prompts = []

    @staticmethod
    def load_from_fs(filename):
        """
        open a data file from Folder and return a list without new line
        :param filename: path for file to read
        :return: list of read data
        """
        output = []
        with open(filename, "r") as f:
            lines = f.readlines()
            for line in lines:
                # remove new line
                sl = line.split("\n")
                output.append(sl[0])
            return output

    def reset(self):
        self.prompt_output = ""
        self.file_list = []
        self.choose_prompts = []

    def add_static_prompts(self):
        for line in self.load_from_fs(self.script_path + self.static_path):
            self.prompt_output = self.prompt_output + line + ","

    def get_folder_prompts(self):
        for file_path in glob.glob(self.script_path + self.prompt_path + "*.txt"):
            self.file_list.append(self.load_from_fs(file_path))

    def choose_prompt(self):
        for prompts in self.file_list:
            self.choose_prompts.append(random.choice(prompts))

    def format_prompts(self):
        for prompt in self.choose_prompts:
            self.prompt_output = self.prompt_output + prompt + ","

        self.prompt_output = self.prompt_output[:-1]

    def run(self):
        self.reset()
        self.add_static_prompts()
        self.get_folder_prompts()
        self.choose_prompt()
        self.format_prompts()


swap = Swap()


def add_to_prompt():
    return swap.prompt_output


def on_ui_tabs():
    txt2img_prompt = modules.ui.txt2img_paste_fields[0][0]

    with gr.Blocks(analytics_enabled=False) as prompt_generator:
        with gr.Tabs():
            with gr.TabItem("Generator"):
                with gr.Column():
                    gen_btn = gr.Button(value="Generate", elem_id="generate_button")
                with gr.Column(visible=False) as results_col:
                    results = gr.Text(label="Results", elem_id="Results_textBox", interactive=False)
                with gr.Column():
                    warning = gr.HTML(value="Send the first generated prompt to:", visible=False)
                    with gr.Row():
                        send_to_txt2img = gr.Button('Send to txt2img', visible=False)
            with gr.TabItem("Configuration"):
                gr.Markdown("this is a demo")

        def generate_prompts():
            swap.run()
            return {results: swap.prompt_output,
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
