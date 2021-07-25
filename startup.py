#!/usr/bin/python3

import os
import time

V1_BASE_URL = 'https://www.googleapis.com/compute/v1/projects/mbexam-5'
google_key_file = "mbexam-5-d37beb826749.p12"
client_email = 'mb-exam-5@mbexam-5.iam.gserviceaccount.com'
base_image_name = V1_BASE_URL + '/global/images/cnc-image-4'


def get_access_credentials():
    from oauth2client.service_account import ServiceAccountCredentials

    credentials = ServiceAccountCredentials.from_p12_keyfile(client_email, google_key_file,
                                                             scopes=['https://www.googleapis.com/auth/compute'])

    return credentials


def create_instance(instance_name, image_name, size, rc='europe-west1-b'):
    import json, requests

    url = V1_BASE_URL + '/zones/%s/instances' % rc
    token = get_access_credentials().get_access_token().access_token
    headers = {'Authorization': 'Bearer %s' % token, 'content-type': "application/json"}
    params = {
        'name': instance_name,
        'machineType': "zones/%s/machineTypes/%s" % (rc, size),
        'disks': [
            {
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': image_name,
                }
            },
        ],
        'networkInterfaces': [{
            'network': 'global/networks/default',
            'accessConfigs': [
                {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
            ]
        }],
        'scheduling': {'preemptible': False},
    }

    r = requests.post(url, data=json.dumps(params), headers=headers)
    if int(r.status_code) != 200:
        raise Exception("Google: Unable to create instance in %s. %s" % (str(rc), str(r.__dict__)))

    res = r.json()
    return res


def list_instances():
    import requests
    url = V1_BASE_URL + '/aggregated/instances'
    token = get_access_credentials().get_access_token().access_token
    headers = {'Authorization': 'Bearer %s' % token, 'content-type': "application/json"}

    r = requests.get(url, headers=headers, params={})
    if int(r.status_code) != 200:
        raise Exception("Google: Unable to list instances. %s" % str(r.__dict__))
    res = r.json()

    instances = []
    for zone, data in res['items'].items():
        if 'instances' in data:
            for i in data['instances']:
                instances.append(i)

    return instances


if __name__ == '__main__':
    print('Creating instance, please wait..')
    response = create_instance(instance_name='cnc-server', image_name=base_image_name, size='n1-highcpu-2')
    instance_id = response['targetId']

    grace_period_in_seconds = 5
    time.sleep(grace_period_in_seconds)

    instance_list = list_instances()
    for instance in instance_list:
        if instance['id'] == instance_id:
            extended_grace_period_in_seconds = grace_period_in_seconds * 4
            print('Giving the server a grace period of {} seconds..'.format(extended_grace_period_in_seconds))
            time.sleep(extended_grace_period_in_seconds)
            instance_external_ip = instance['networkInterfaces'][0]['accessConfigs'][0]['natIP']
            print('Command&Control server is ready! Please navigate to http://' + instance_external_ip
                  + ":8000/instances/")
            break


