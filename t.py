from django.contrib.auth.models import User, Group

user = User.objects.get(username="john")
group = Group.objects.get(name="Field Engineer")
user.groups.add(group)
user.save()
