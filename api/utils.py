from collections import defaultdict

import requests
import urllib3
from rest_framework import serializers

urllib3.disable_warnings()


def get_order(number: str, passenger_id: str) -> dict:
    """
    :param number: номер брони
    :param passenger_id: фамилия пассажира
    :return: Данные заказа
    """
    url = "??/orders"
    querystring = {"number": number, "passengerId": passenger_id}
    payload = ""
    headers = {}
    response = requests.get(url, data=payload, headers=headers, params=querystring)
    response.raise_for_status()
    return response.json()


def extract_ski_data(data: dict) -> dict:
    """Возвращает из данных все passengerId, все routeId, baggageIds с equipmentType == ski
    Args:
        data: данные заказа
    Returns:
        Все passengerId, все routeId, baggageIds с equipmentType == ski
    """
    raw_result = defaultdict(list)

    for ancillaries_pricing in data['ancillariesPricings']:
        for baggage_pricing in ancillaries_pricing['baggagePricings']:
            passenger_ids = baggage_pricing['passengerIds']
            route_id = baggage_pricing['routeId']
            for baggage in baggage_pricing['baggages']:
                if 'equipmentType' in baggage and baggage['equipmentType'] == 'ski':
                    for passenger_id in passenger_ids:
                        raw_result[(passenger_id, route_id)].append(baggage['id'])

    return {
        'baggageSelections': [{
            'passengerId': key[0],
            'routeId': key[1],
            'baggageIds': baggage_ids,
            'redemption': False
        } for key, baggage_ids in raw_result.items()]
    }


def make_order(data):
    url = "??/bags"
    querystring = ""
    payload = data
    headers = {}
    response = requests.put(url, data=payload, headers=headers, params=querystring)
    response.raise_for_status()


def validate_data(data, serializer_class: serializers.Serializer()):
    return serializer_class(data=data).is_valid()
