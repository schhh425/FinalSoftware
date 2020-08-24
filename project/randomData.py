#!/usr/bin/python3

from project.common import PATH
from random import choice, randint, shuffle

# value range and target path value
__targetRangeBegin__ = 50
__targetRangeEnd__ = 650

# difficult
__targetMaxEnd1__ = 660
# easy
__targetMaxEnd2__ = 1200


def get_random_target_data():
    """
    Randomly generated data. There are 12 data sets in total.
    A path is randomly selected as the target in each data set. choice()
    Target is assigned to targetMaxEnd1 or targetMaxEnd2.
    The set of data to which target is assigned to targetMaxEnd1 is considered a DIFFICULT.
    The set of data to which target is assigned to targetMaxEnd2 is considered a EASY.
    Paths other than target is assigned a value of a random number between targetRangeBegin and targetRangeEnd.
    :return:
    """
    data = []
    for _ in range(12):
        targetName = choice(PATH)
        if _ % 2 == 0:
            targetValue = __targetMaxEnd1__
        else:
            targetValue = __targetMaxEnd2__
        # Paths other than the target path
        easyPath = []
        difficultPath = []
        for item in PATH:
            easy = {}
            difficult = {}
            if item != targetName:
                # easy data
                easy['name'] = item
                easy['value'] = randint(__targetRangeBegin__, __targetRangeEnd__)
                easyPath.append(easy)
            else:
                # difficult data
                difficult['name'] = targetName
                difficult['value'] = targetValue
                difficultPath.append(difficult)

        d = {
            'target_name': targetName,
            'target_value': targetValue,
            'easy': easyPath,
            'difficult': difficultPath
        }
        typeAndColor(_, d)
        data.append(d)

    return data


def typeAndColor(index, data):
    """
    Each group of data is set with a different chart type and color setting.
    :param index:
    :param data:
    :return:
    """
    if index == 0:
        data['image_type'] = 'column'
        data['color'] = 'text'
    if index == 1:
        data['image_type'] = 'column'
        data['color'] = 'text'
    if index == 2:
        data['image_type'] = 'column'
        data['color'] = 'color'
    if index == 3:
        data['image_type'] = 'column'
        data['color'] = 'color'
    if index == 4:
        data['image_type'] = 'bar'
        data['color'] = 'text'
    if index == 5:
        data['image_type'] = 'bar'
        data['color'] = 'text'
    if index == 6:
        data['image_type'] = 'bar'
        data['color'] = 'color'
    if index == 7:
        data['image_type'] = 'bar'
        data['color'] = 'color'
    if index == 8:
        data['image_type'] = 'pie'
        data['color'] = 'color'
    if index == 9:
        data['image_type'] = 'pie'
        data['color'] = 'color'
    if index == 10:
        data['image_type'] = 'pie'
        data['color'] = 'none'
    if index == 11:
        data['image_type'] = 'pie'
        data['color'] = 'none'


def get_data():
    """
    Get details of the structured data items to be displayed and disrupt the data order.   shuffle()
    :return:
    """
    serializeData = []
    targetData = get_random_target_data()

    for item in targetData:
        data_list = item.get('easy') + item.get('difficult')
        shuffle(data_list)
        _data = {
            'data_type': 'easy' if item.get('target_value') == __targetMaxEnd2__ else 'difficult',
            'target_name': item.get('target_name'),
            'target_value': item.get('target_value'),
            'image_type': item.get('image_type'),
            'color': item.get('color'),
            'data': data_list
        }
        serializeData.append(_data)

    shuffle(serializeData)

    return serializeData
