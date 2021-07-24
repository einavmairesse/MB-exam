from datetime import datetime

from .google_cloud_helper import run_gcp_command
from ..models import Instances


def create_instances(number_of_instances):
    for i in range(number_of_instances):
        result = run_gcp_command('create')

        if result[0] is False:
            print("Failed creating a new instance: " + str(result[1]))
            return False, result[1]
        else:
            print("Created an instance successfully")
            instance_name = str(result[1]).split('\\r\\n')[0].split(' ')[1]
            Instances(name=instance_name, status='Running', created_at=datetime.now()).save()

    return True, ''


def terminate_selected(instance_list):
    for instance in instance_list:
        run_gcp_command('delete', '-i', instance)
        Instances.objects.filter(name=instance).delete()
    return



