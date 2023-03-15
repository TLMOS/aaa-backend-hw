import os
import io
import configparser
import logging
from logging.handlers import RotatingFileHandler

import requests
from flask import Flask, request

from models.plate_reader import PlateReader, InvalidImage


config_path = os.environ.get('CONFIG_PATH', './config.ini')
log_dir = os.environ.get('LOG_DIR', './logs')
model_weights_dir = os.environ.get('MODEL_WEIGHTS_DIR', './model_weights')
log_path = os.path.join(log_dir, 'app.log')


cfg = configparser.ConfigParser()
cfg.read('./config.ini')
name = cfg['App']['name']
debug = cfg['Run'].getboolean('debug')
image_host = cfg['Image Server']['host']
model_weights = cfg['Model']['model_weights']


app = Flask(name)
app.config['JSON_AS_ASCII'] = False
weights_path = os.path.join(model_weights_dir, model_weights)
plate_reader = PlateReader.load_from_file(weights_path)


def get_plate_number_by_id(img_id):
    try:
        response = requests.get(f'{image_host}/images/{img_id}')
        img = io.BytesIO(response.content)
        plate_number = plate_reader.read_text(img)
    except requests.exceptions.ConnectionError:
        return 'Connection error', 500
    except requests.exceptions.Timeout:
        return 'Timeout error', 500
    except requests.exceptions.RequestException:
        return 'Unknown error while getting image', 500
    except InvalidImage:
        return 'Invalid image', 400
    except RuntimeError as e:
        if e.args[0] == 'CUDA out of memory.':
            return 'CUDA out of memory', 500
        elif 'The size of tensor a' in e.args[0]:
            return 'Expected grayscale image', 400
        return 'Runtime error', 500
    except Exception as e:
        logging.error(e)
        return 'Unknown error', 500
    return plate_number, 200


@app.route('/read-plate-number')
def read_plate_number():
    img_id = request.args.get('img_id')
    res, status_code = get_plate_number_by_id(img_id)
    if status_code != 200:
        return {'error': res}, status_code
    return {'plate_number': res}


@app.route('/read-plate-numbers')
def read_plate_numbers():
    ids = request.args.get('img_ids')
    if not ids:
        return {'error': 'No ids provided'}, 400
    ids = ids.split(',')
    plate_numbers = {}
    for img_id in ids:
        res, status_code = get_plate_number_by_id(img_id)
        if status_code != 200:
            return {'error': res, 'img_id': img_id}, status_code
        plate_numbers[img_id] = res
    return {'plate_numbers': plate_numbers}


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)-7.7s]  %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            RotatingFileHandler(log_path, maxBytes=1024),
            logging.StreamHandler()
        ]
    )

    app.run(host='0.0.0.0', port=8080, debug=debug)
