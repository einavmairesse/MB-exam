import ast

from django.http import HttpResponse
from django.template import loader

from django.views.decorators.csrf import csrf_exempt
from .models import Instances, Tests
from .services.instance_service import create_instances, terminate_selected
from .services.validator import validate_instance_count, is_test_name_exists
from .services.test_service import create_instances_tests_in_db, create_test_in_db, start_test, stop_tests, \
    InstanceNumberTooLow


@csrf_exempt
def create_instances_view(request):
    count = request.POST.get('instanceCount')
    if not validate_instance_count(count):
        return HttpResponse('Number of instances to launch must be a positive integer.', status=400)

    count = int(count)
    create_instances(count)

    instances = Instances.objects.all()
    # print(len(instances))
    template = loader.get_template('web_app/instances.html')
    context = {'instance_list': instances}
    return HttpResponse(template.render(context, request))


@csrf_exempt
def stop(request):
    tests_to_stop = request.POST.getlist('testNames')
    stop_tests(tests_to_stop)

    tests = Tests.objects.all()
    template = loader.get_template('web_app/running_tests.html')
    context = {'test_list': tests}
    return HttpResponse(template.render(context, request))


def instances_page(request):
    # todo: Define what to do when there no instances in the table
    instances = Instances.objects.all()
    template = loader.get_template('web_app/instances.html')
    context = {'instance_list': instances}
    return HttpResponse(template.render(context, request))


@csrf_exempt
def start_test_page(request):
    template = loader.get_template('web_app/start_test.html')
    context = {'instance_list': request.POST.getlist('instanceNames')}
    return HttpResponse(template.render(context, request))


@csrf_exempt
def running_tests_page(request):
    instance_names = ast.literal_eval(request.POST.get('instanceNames'))
    test_name = request.POST.get('testName')
    command_to_execute = request.POST.get('command')

    if is_test_name_exists(test_name):
        return start_test_page(request)

    create_instances_tests_in_db(instance_names, test_name)
    create_test_in_db(instance_names, test_name)

    try:
        start_test(test_name, instance_names, command_to_execute)
    except InstanceNumberTooLow:
        return instances_page(request)

    tests = Tests.objects.all()
    template = loader.get_template('web_app/running_tests.html')
    context = {'test_list': tests}
    return HttpResponse(template.render(context, request))


@csrf_exempt
def update(request):
    instance_names = request.POST.getlist('instanceNames')
    operation = request.POST.get('operation')

    if operation == "Start Test":
        template = loader.get_template('web_app/start_test.html')
        context = {'instance_list': instance_names}
    elif operation == "Terminate Selected":
        terminate_selected(instance_names)
        return instances_page(request)

    return HttpResponse(template.render(context, request))
