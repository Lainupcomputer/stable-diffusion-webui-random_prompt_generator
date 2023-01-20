import gradio as gr
import modules
from modules import script_callbacks
from scripts.generator import Generator

try:
    from ez_storage.ez_storage import Ez_Storage
except ModuleNotFoundError:
    print("ez_storage module is missing (pip install ez-storage==1.3.3)")

default = Ez_Storage("./extensions/stable-diffusion-webui-random_prompt_generator/default.ezs")
generator = Generator(default)


# UI
def on_ui_tabs():

    txt2img_prompt = modules.ui.txt2img_paste_fields[0][0]
    txt2img_negative_prompt = modules.ui.txt2img_paste_fields[1][0]

    with gr.Blocks(analytics_enabled=False) as prompt_generator:
        with gr.Tabs():
            with gr.TabItem("Generator"):
                # headline
                with gr.Column():
                    try:
                        prefixes = default.get_storage(mode="l", obj="prefix_index")
                    except KeyError:
                        prefixes = ['configure extension']

                    with gr.Row():
                        prefix_dd = gr.Dropdown(prefixes)
                        gen_btn = gr.Button(value="Generate")

                with gr.Column(visible=False) as results_col:
                    with gr.Row():
                        results = gr.Text(label="Results", elem_id="Results_textBox", interactive=False)
                        send_btn = gr.Button('Send to txt2img', visible=False)

            with gr.TabItem("Settings"):
                pass

        def generate_prompts(prefix_dd):
            print(prefix_dd)
            generator.run(prefix=prefix_dd, check_for_duplicates=True)
            return {results: generator.chosen_prompts,
                    send_btn: gr.update(visible=True),
                    results_col: gr.update(visible=True)
                    }

        def get_positive_prompt():
            return generator.positive_str_output

        def get_negative_prompt():
            return generator.negative_str_output

        # events
        gen_btn.click(fn=generate_prompts, outputs=[results, send_btn, results_col], inputs=[prefix_dd])
        send_btn.click(get_positive_prompt, outputs=[txt2img_prompt])
        send_btn.click(get_negative_prompt, outputs=[txt2img_negative_prompt])
        send_btn.click(None, _js='switch_to_txt2img', inputs=None, outputs=None)
    return (prompt_generator, "Prompt-Generator", "Prompt-Generato"),


script_callbacks.on_ui_tabs(on_ui_tabs)
