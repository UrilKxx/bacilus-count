from io import BytesIO

from PIL import Image
from flask import Flask, request, jsonify, send_file, Response
from flask_api import status

from Embedding import Embedding
from domain import Status
from storage import HDF5ImageStorage

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB


def _send_image(image: Image):
    img = Image.fromarray(image.image)
    # Сохраняем изображение в объект BytesIO
    img_io = BytesIO()
    img.save(img_io, 'PNG')  # Сохраняем как PNG
    img_io.seek(0)  # Возвращаемся в начало объекта BytesIO
    # Отправляем изображение как файл для скачивания
    return send_file(img_io, mimetype='image/png', as_attachment=True, download_name=f'{image.uuid}.png')


def create_app():
    storage = HDF5ImageStorage()
    embedding = Embedding(storage)

    @app.route('/images/upload', methods=['POST'])
    def upload_image():
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), status.HTTP_400_BAD_REQUEST

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), status.HTTP_400_BAD_REQUEST
        try:
            embedding.add_image(file)
        except ValueError as v:
            return jsonify({'error': v.args[0]}), status.HTTP_409_CONFLICT
        except Exception as e:
            return jsonify({'error': str(e)}), status.HTTP_500_INTERNAL_SERVER_ERROR
        return Response(status=status.HTTP_200_OK)

    @app.route('/images/<string:image_id>/download', methods=['GET'])
    def get_image(image_id):
        try:
            return _send_image(embedding.get_processed_image(image_id))
        except ValueError:
            return jsonify({'error': 'Image not found'}), status.HTTP_404_NOT_FOUND
        except Exception as e:
            return jsonify({'error': str(e)}), status.HTTP_500_INTERNAL_SERVER_ERROR

    @app.route('/images/<string:image_id>/count', methods=['POST'])
    def start_counting(image_id: str):
        try:
            embedding.handle_algorithm(image_id)
            return Response(status=status.HTTP_202_ACCEPTED)
        except ValueError:
            return jsonify({'error': 'Image not found'}), status.HTTP_404_NOT_FOUND
        except Exception as e:
            return jsonify({'error': str(e)}), status.HTTP_500_INTERNAL_SERVER_ERROR

    @app.route('/counts/<string:job_id>', methods=['GET'])
    def get_job_status(job_id):
        try:
            job = embedding.get_job_by_uuid(job_id)

            return jsonify(job.to_dict())
        except ValueError:
            return jsonify({'error': 'Job not found'}), status.HTTP_404_NOT_FOUND

    @app.route('/counts', methods=['GET'])
    def get_job_list():
        try:
            return jsonify([job.to_dict() for job in embedding.get_jobs()])
        except Exception as e:
            return jsonify({'error': str(e)}), status.HTTP_500_INTERNAL_SERVER_ERROR

    @app.route('/counts/<string:job_id>/image/download', methods=['GET'])
    def get_segmented_image(job_id):
        try:
            job = embedding.get_job_by_uuid(job_id)
            if job.status == Status.COMPLETED:
                return _send_image(job.image)
            return jsonify({'error': 'Job not completed'}), status.HTTP_404_NOT_FOUND
        except ValueError:
            return jsonify({'error': 'Image not found'}), status.HTTP_404_NOT_FOUND
        except Exception as e:
            return jsonify({'error': str(e)}), status.HTTP_500_INTERNAL_SERVER_ERROR

    @app.route('/images', methods=['GET'])
    def get_image_list():
        # page = request.args.get('page', 1, type=int)
        # per_page = request.args.get('per_page', 10, type=int)
        # start = (page - 1) * per_page
        # end = start + per_page
        # jsonify(image_list[start:end])
        images = jsonify({'images': embedding.get_list_unprocessed_images(),
                          'processed_images': embedding.get_list_processed_images()})
        return images

    @app.route('/algorithms', methods=['GET'])
    def get_algorithm_list():
        return jsonify("Canny")

    return app
