from ..models import Tests


def validate_instance_count(instance_count):
    try:
        instance_count = int(instance_count)
        return instance_count > 0
    except ValueError:
        return False


def is_test_name_exists(test_name):
    count_tests_with_same_name = Tests.objects.filter(name=test_name).count()
    if count_tests_with_same_name > 0:
        return True
    return False
