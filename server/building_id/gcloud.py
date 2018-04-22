import os

import googleapiclient.discovery
import numpy as np


buildings = ['Parks Library', 'Beardshear Hall', 'Atanasoff hall', 'Catt Hall', 'Gilman Hall', 'Memorial Union', 'Mackay Hall']
ind_to_building = {i:buildings[i] for i in range(len(buildings))}


def predict(X, project='nimble-sight-187200', model='ser', version='pepe'):


    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'Alpha-d072426f34cd.json'

    service = googleapiclient.discovery.build('ml', 'v1')
    name = 'projects/{}/models/{}/versions/{}'.format(project, model, version)

    request_dict = {'instances': [{"images": X}]}

    response = service.projects().predict(
        name=name,
        body=request_dict
    ).execute()

    class_scores = response['predictions'][0]['scores']
    building = ind_to_building[ np.argmax(class_scores) ]

    return building

