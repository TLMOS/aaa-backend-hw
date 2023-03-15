from typing import List

import requests


class PlateReaderClient:
    """Client for plate reader API."""

    def __init__(self, host: str):
        self.host = host

    def read_plate_number(self, img_id: int) -> str:
        """
        Read plate number from image with given id.

        :param img_id: id of image
        """
        res = requests.get(
            f'{self.host}/read-plate-number',
            params={'img_id': img_id}
        )
        if res.status_code != 200:
            raise Exception(res.json()['error'])
        return res.json()['plate_number']

    def read_plate_numbers(self, img_ids: List[int]) -> dict:
        """
        Read plate numbers from images with given ids.

        :param img_ids: ids of images
        """
        res = requests.get(
            f'{self.host}/read-plate-numbers',
            params={'img_ids': ','.join(map(str, img_ids))}
        )
        if res.status_code != 200:
            raise Exception(res.json()['error'])
        return res.json()['plate_numbers']


if __name__ == '__main__':
    client = PlateReaderClient('http://localhost:8080')
    plate_number = client.read_plate_number(10022)
    plate_numbers = client.read_plate_numbers([10022, 9965])
    print(f'Plate number: {plate_number}')
    print('Plate numbers:')
    for img_id, numer in plate_numbers.items():
        print(f'  {img_id}: {numer}')
