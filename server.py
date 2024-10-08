from flask import Flask, request, jsonify, send_file, url_for
import os
import subprocess
import logging
import time

# 配置日志，只输出到控制台
logging.basicConfig(
    level=logging.DEBUG,  # 设置日志级别，显示 DEBUG 及以上级别的日志
    format='%(asctime)s - %(levelname)s - %(message)s',  # 日志格式
    handlers=[logging.StreamHandler()]  # 只输出到控制台
)

app = Flask(__name__)

# 定义文件上传保存的目录
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 配置应用的上传文件路径
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 定义文件保存的目录为 'download_video'
DOWNLOAD_FOLDER = 'download_video'

# 如果文件夹不存在，则创建文件夹
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

@app.route('/')
def home():
    return "Welcome to the Flask server!"


@app.route('/favicon.ico')
def favicon():
    return '', 204  # 返回一个空响应


import os
import mimetypes
from flask import send_file


def debug_file_send(file_path):
    logging.info(f"Debugging file send for: {file_path}")

    # 检查文件是否存在
    if not os.path.exists(file_path):
        logging.info(f"Error: File does not exist at {file_path}")
        return

    # 检查文件大小
    file_size = os.path.getsize(file_path)
    logging.info(f"File size: {file_size} bytes")

    # 检查文件权限
    permissions = oct(os.stat(file_path).st_mode)[-3:]
    logging.info(f"File permissions: {permissions}")

    # 检查MIME类型
    mime_type, _ = mimetypes.guess_type(file_path)
    logging.info(f"MIME type: {mime_type}")

    # 尝试打开并读取文件
    try:
        with open(file_path, 'rb') as f:
            content = f.read(1024)  # 读取前1KB
        logging.info(f"Successfully read {len(content)} bytes from the file")
    except Exception as e:
        logging.info(f"Error reading file: {str(e)}")

    # 尝试使用send_file
    try:
        response = send_file(file_path, as_attachment=True, download_name='output.mp4')
        logging.info(f"send_file response: {response}")
    except Exception as e:
        logging.info(f"Error in send_file: {str(e)}")


@app.route('/upload', methods=['POST'])
def upload_file():
    # 检查请求中是否包含文件
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    # 检查文件是否有文件名
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # 如果文件存在，保存文件到指定路径
    if file:
        # 定义上传后的视频路径
        uploaded_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'received_video.mp4')
        output_file_path = os.path.join(app.config['DOWNLOAD_FOLDER'], 'output.mp4')

        # 如果文件已存在，先删除旧文件
        if os.path.exists(uploaded_file_path):
            os.remove(uploaded_file_path)

        # 保存上传的文件
        file.save(uploaded_file_path)

        # 调用 infer_on_video.py 处理视频
        try:
            # 构建命令及参数
            command = [
                'python', 'TrackNet/infer_on_video.py',
                '--video_path', 'uploads/received_video.mp4',
                '--video_out_path', 'download_video/output.mp4',
                '--model_path', 'TrackNet/model_best.pt'
            ]

            # python TrackNet/infer_on_video.py --video_path uploads/received_video.mp4 --video_out_path uploads/output.mp4 --model_path TrackNet/model_best.pt

            # 使用 subprocess.run 执行命令
            subprocess.run(command, capture_output=True, text=True)
            logging.info("完成模型推理了")

            # subprocess.run(['python', 'infer_on_video.py', '--input', "uploads/"+uploaded_file_path, '--output', "uploads/"+output_file_path], check=True)

            debug_file_send(output_file_path)

            # 检查处理后的输出文件是否存在
            if os.path.exists(output_file_path):
                time.sleep(1)
                logging.warning('文件存在')
                # 返回处理后的文件
                # return send_file(output_file_path, as_attachment=True, download_name='output.mp4')

                # response_data = {
                #     "status": "success",
                #     "video_url": url_for('upload_file', filename="output.mp4", _external=True)
                # }
                #
                # return jsonify(response_data)

                video_url = url_for('get_video', filename="output.mp4",  _external=True)
                return jsonify({'video_url': video_url}), 200

            else:
                logging.error("直接跳过了")
                return jsonify({'error': 'Processing failed, output file not found'}), 500

            # return send_file(output_file_path, as_attachment=True, download_name='output.mp4')

        except subprocess.CalledProcessError as e:
            return jsonify({'error': 'Error during video processing', 'details': str(e)}), 500
@app.route('/download_video/<filename>', methods=['GET'])
def get_video(filename):
    filepath = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
    logging.info(filepath)
    if os.path.exists(filepath):
        return send_file(filepath, mimetype='video/mp4')
    else:
        return jsonify({"error": "File not found"}), 404


if __name__ == '__main__':
    # 使用 HTTP 运行 Flask 服务器，不使用 HTTPS
    app.run(host='0.0.0.0', port=5000)
