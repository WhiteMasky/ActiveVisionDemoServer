# from flask import Flask, request
#
# app = Flask(__name__)
#
# # 定义根路径的路由
# @app.route('/')
# def home():
#     return "Welcome to the Flask server!"
#
# @app.route('/favicon.ico')
# def favicon():
#     return '', 204  # 返回一个空响应
#
# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return 'No file part', 400
#     file = request.files['file']
#     if file.filename == '':
#         return 'No selected file', 400
#     if file:
#         file.save("received_video.mp4")
#         return 'File successfully uploaded', 200
#
# if __name__ == '__main__':
#     # 启用 HTTPS，使用生成的证书
#     app.run('0.0.0.0', port=5000)


# from flask import Flask, request, jsonify
# import os
#
# app = Flask(__name__)
#
# # 定义文件上传保存的目录
# UPLOAD_FOLDER = 'uploads'
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)
#
# # 配置应用的上传文件路径
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#
#
# @app.route('/')
# def home():
#     return "Welcome to the Flask server!"
#
#
# @app.route('/favicon.ico')
# def favicon():
#     return '', 204  # 返回一个空响应
#
#
# @app.route('/upload', methods=['POST'])
# def upload_file():
#     # 检查请求中是否包含文件
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part'}), 400
#
#     file = request.files['file']
#
#     # 检查文件是否有文件名
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400
#
#     # 如果文件存在，保存文件到指定路径
#     if file:
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'received_video.mp4')
#         file.save(file_path)
#         return jsonify({'message': 'File successfully uploaded', 'file_path': file_path}), 200
#
#
# if __name__ == '__main__':
#     # 使用 HTTP 运行 Flask 服务器，不使用 HTTPS
#     app.run(host='0.0.0.0', port=5000)


# from flask import Flask, request, jsonify, send_file
# import os
#
# app = Flask(__name__)
#
# # 定义文件上传保存的目录
# UPLOAD_FOLDER = 'uploads'
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)
#
# # 配置应用的上传文件路径
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#
#
# @app.route('/')
# def home():
#     return "Welcome to the Flask server!"
#
#
# @app.route('/favicon.ico')
# def favicon():
#     return '', 204  # 返回一个空响应
#
#
# @app.route('/upload', methods=['POST'])
# def upload_file():
#     # 检查请求中是否包含文件
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part'}), 400
#
#     file = request.files['file']
#
#     # 检查文件是否有文件名
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400
#
#     # 如果文件存在，保存文件到指定路径
#     if file:
#         # 定义上传后的视频路径
#         uploaded_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'received_video.mp4')
#         output_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.mp4')
#
#         # 保存上传的文件
#         file.save(uploaded_file_path)
#
#         # 将文件重命名为 output.mp4
#         os.rename(uploaded_file_path, output_file_path)
#
#         # 返回文件给客户端，使用新的参数 download_name
#         return send_file(output_file_path, as_attachment=True, download_name='output.mp4')
#
#
# if __name__ == '__main__':
#     # 使用 HTTP 运行 Flask 服务器，不使用 HTTPS
#     app.run(host='0.0.0.0', port=5000)




# from flask import Flask, request, jsonify, send_file
# import os
#
# app = Flask(__name__)
#
# # 定义文件上传保存的目录
# UPLOAD_FOLDER = 'uploads'
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)
#
# # 配置应用的上传文件路径
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#
#
# @app.route('/')
# def home():
#     return "Welcome to the Flask server!"
#
#
# @app.route('/favicon.ico')
# def favicon():
#     return '', 204  # 返回一个空响应
#
#
# @app.route('/upload', methods=['POST'])
# def upload_file():
#     # 检查请求中是否包含文件
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part'}), 400
#
#     file = request.files['file']
#
#     # 检查文件是否有文件名
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400
#
#     # 如果文件存在，保存文件到指定路径
#     if file:
#         # 定义上传后的视频路径
#         uploaded_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'received_video.mp4')
#         output_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.mp4')
#
#         # 如果文件已存在，先删除旧文件
#         if os.path.exists(uploaded_file_path):
#             os.remove(uploaded_file_path)
#
#         # 保存上传的文件
#         file.save(uploaded_file_path)
#
#         # 将文件重命名为 output.mp4
#         if os.path.exists(output_file_path):
#             os.remove(output_file_path)
#         os.rename(uploaded_file_path, output_file_path)
#
#         # 返回文件给客户端，使用新的参数 download_name
#         return send_file(output_file_path, as_attachment=True, download_name='output.mp4')
#
#
# if __name__ == '__main__':
#     # 使用 HTTP 运行 Flask 服务器，不使用 HTTPS
#     app.run(host='0.0.0.0', port=5000)




from flask import Flask, request, jsonify, send_file
import os
import subprocess

app = Flask(__name__)

# 定义文件上传保存的目录
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 配置应用的上传文件路径
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def home():
    return "Welcome to the Flask server!"


@app.route('/favicon.ico')
def favicon():
    return '', 204  # 返回一个空响应


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
        output_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.mp4')

        # 如果文件已存在，先删除旧文件
        if os.path.exists(uploaded_file_path):
            os.remove(uploaded_file_path)

        # 保存上传的文件
        file.save(uploaded_file_path)

        # 调用 infer_on_video.py 处理视频
        try:
            subprocess.run(['python', 'infer_on_video.py', '--input', "uploads/"+uploaded_file_path, '--output', "uploads/"+output_file_path], check=True)

            # 检查处理后的输出文件是否存在
            if os.path.exists(output_file_path):
                # 返回处理后的文件
                return send_file(output_file_path, as_attachment=True, download_name='output.mp4')
            else:
                return jsonify({'error': 'Processing failed, output file not found'}), 500

        except subprocess.CalledProcessError as e:
            return jsonify({'error': 'Error during video processing', 'details': str(e)}), 500


if __name__ == '__main__':
    # 使用 HTTP 运行 Flask 服务器，不使用 HTTPS
    app.run(host='0.0.0.0', port=5000)
