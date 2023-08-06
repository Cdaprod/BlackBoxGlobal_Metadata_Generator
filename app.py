from flask import Flask, request, jsonify
import os
import gradio as gr
import metadata_generator

app = Flask(__name__)

@app.route('/api/generate', methods=['POST'])
def generate_api():
    data = request.get_json()

    xlsx_file = data.get('xlsx_file')
    videos_folder = data.get('videos_folder')

    if not xlsx_file or not videos_folder:
        return jsonify({'error': 'xlsx_file and videos_folder are required'}), 400

    if not os.path.isfile(xlsx_file):
        return jsonify({'error': f'{xlsx_file} is not a valid xlsx file'}), 400

    if not os.path.isdir(videos_folder):
        return jsonify({'error': f'{videos_folder} is not a valid folder'}), 400

    try:
        metadata_generator.generate_metadata(xlsx_file, videos_folder)
        return jsonify({'message': 'Metadata generated successfully'})

    except Exception as e:
        app.logger.error(f"Metadata generation failed: {e}")
        return jsonify({'error': 'Metadata generation failed'}), 500


def generate_metadata_ui(xlsx_file, videos_folder):
    if not xlsx_file or not videos_folder:
        return 'xlsx_file and videos_folder are required'

    try:
        metadata_generator.generate_metadata(xlsx_file.name, videos_folder.name)
        return "Metadata generated successfully!"
    except Exception as e:
        return str(e)


gr.Interface(
    fn=generate_metadata_ui,
    inputs=[
        gr.inputs.File(label="Excel File"),
        gr.inputs.Directory(label="Videos Folder")
    ],
    outputs="text",
    server_name="localhost",
    server_port=5000
).launch()


if __name__ == '__main__':
    app.run(port=5000)
