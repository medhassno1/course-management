from course_management.views.base import render_with_default
from course_management.forms import RegistrationForm
from course_management.models.student import Student


def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            userdata = form.cleaned_data
            Student.create(email=userdata['email'],
                           password=userdata['password'],
                           first_name=userdata['first_name'],
                           last_name=userdata['family_name'],
                           s_number=userdata['s_number'])
            print("YES")

        else:
            print("NO")
    else:
        form = RegistrationForm()
        return render_with_default(request, 'register.html', {'title': 'Registration | iFSR Course Management',
                                                              'form': form})
