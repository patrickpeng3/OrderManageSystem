from django import template
from accounts.models import User
from users.models import department_Mode

register = template.Library()


@register.filter(name='message')
def message(user):
    user_info = User.objects.get(username=user)
    try:
        user_group = department_Mode.objects.get(pk=user_info.department_id)
        if user_group.desc_gid == 1001:
            print("1")
    except Exception as e:
        print("error")
