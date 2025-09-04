import gradio as gr

from src.vad_service import get_vad_timestamps

input_audio = gr.Audio(
    sources=["microphone"],
    waveform_options=gr.WaveformOptions(
        waveform_color="#01C6FF",
        waveform_progress_color="#0066B4",
        skip_length=2,
        show_controls=False,
    ),
)

output_text = gr.Textbox(label="VAD Timestamps", lines=10)

client = gr.Interface(
    fn=get_vad_timestamps,
    inputs=input_audio,
    outputs=output_text,
    title="Voice Activity Detection (VAD) Service",
    description="Upload an audio file or record your voice to get VAD timestamps.",
    allow_flagging="never",
)
client.launch(share=True)
