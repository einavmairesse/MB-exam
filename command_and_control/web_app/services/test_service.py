import json
import ast
from datetime import datetime
from .google_cloud_helper import run_gcp_command

import requests
from ..models import InstancesTests, Tests


class InstanceNumberTooLow(Exception):
    pass


def get_ips_by_hostnames():
    output = run_gcp_command('list')

    if output[0] is False:
        print('An error occurred while fetching running instances')

    instance_list = str(output[1]).split('List:\\n\\n')[1].replace('\'', '"')
    instances = instance_list.split('\\n\\n\\n')[:-1]

    hostname_to_ip = {}
    for instance in instances:
        instance_details = ast.literal_eval(json.loads(json.dumps(str(instance).replace('\\n', ''))))
        instance_ip = instance_details.get("networkInterfaces")[0].get("accessConfigs")[0].get('natIP')
        instance_name = instance_details.get("name")
        hostname_to_ip[instance_name] = instance_ip

    return hostname_to_ip


def start_test(test_name, instance_names, command_to_execute):
    if len(instance_names) < 1:
        raise InstanceNumberTooLow

    print('Getting IPs')
    hostname_to_ip = get_ips_by_hostnames()
    print("Instance names: " + str(instance_names))
    for instance_name, instance_ip in hostname_to_ip.items():
        if instance_name not in instance_names:
            continue

        data = {
            'test_name': test_name,
            'command': command_to_execute
        }

        print('Sending request')
        response = requests.post('http://' + str(instance_ip) + ':8000/start/', data=json.dumps(data))

        if response.status_code != 200:
            print("Error while starting a test: ", response.reason)

        print('Status code: ', response.status_code)
        process_id = response.json()['process_id']
        InstancesTests.objects.filter(test_name=test_name, instance_name=instance_name).update(process_id=process_id)


def stop_tests(test_names):
    hostname_to_ip = get_ips_by_hostnames()

    for test_name in test_names:
        list_of_instances = InstancesTests.objects.filter(test_name=test_name).values('instance_name', 'process_id').values()

        for instance in list_of_instances:
            instance_name = instance.get('instance_name')
            process_id = instance.get('process_id')
            data = {'process_id': process_id}

            instance_ip = hostname_to_ip.get(instance_name)
            response = requests.post('http://' + str(instance_ip) + ':8000/stop/', data=data)

            if response.status_code != 200:
                print("Error while stoping test: ", response.reason)
            else:
                print('Successfully stopped the attack for instance ' + instance_name)

            Tests.objects.filter(name=test_name).update(status="Done")
            InstancesTests.objects.filter(test_name=test_name).delete()


def create_instances_tests_in_db(instance_names, test_name):
    for instance_name in instance_names:
        InstancesTests(instance_name=instance_name, test_name=test_name).save()


def create_test_in_db(instance_names, test_name):
    Tests(name=test_name, status="In Progress", number_of_instances=len(instance_names),
          created_at=datetime.now()).save()
