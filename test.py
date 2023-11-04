from connect_models import *
# Application logic
first_user = User.objects.all()[0]

print(first_user.name)
print(first_user.email)