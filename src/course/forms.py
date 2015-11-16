from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from course.models.schedule import WEEKDAYS, TIMESLOTS, Schedule
from course.models.subject import Subject

location_validator = RegexValidator(
    r'^.*$', # does absolutely nothing yet
    message='Invalid location name.'
)


SUBJECT_DISALLOWED_NAMES = ['new', 'overview']


subject_name_validator = RegexValidator(
    r'^\w(\w|[0-9_ -])+$',
    message='Invalid subject name.'
)


def username_exists_validator(value):
    try:
        User.objects.get(username=value)

    except User.DoesNotExist:
        raise ValidationError('This username does not exist')


class EditCourseForm(forms.Form):
    description = forms.CharField(widget=forms.Textarea)
    max_participants = forms.DecimalField(
        min_value=1,
        label="Maximum number of allowed participants",
        help_text='Set a new limit for how many people can join the course. '
                  'This does not unenroll any students.'
                  'If the new limit is below the number of currently enrolled '
                  'students it simply disables the option for joining the course.'
    )


class AddDateForm(forms.Form):
    date = forms.DateTimeField()
    location = forms.CharField(validators=[location_validator])


class AddWeeklySlotForm(forms.Form):
    weekday = forms.ChoiceField(WEEKDAYS)
    timeslot = forms.ChoiceField(TIMESLOTS)
    location = forms.CharField(validators=[location_validator])


class CreateCourseForm(forms.Form):
    subject = forms.ChoiceField(
        lambda: map(lambda s: (s.id, s.name), Subject.objects.all()),
        help_text='Choose a subject for your course. '
                  'Beware that this choice may not be changed later'
    )
    schedule = forms.ChoiceField(Schedule.TYPES)
    active = forms.BooleanField(
        initial=False,
        required=False,
        help_text='Choose whether people should be able to join this course right now.'
    )
    description = forms.CharField(
        widget=forms.Textarea,
        help_text='A good description is half the battle. You can use markdown for formatting.',
        initial='# My course\n\nWe will explore the universe.\n\n## Materials\n\n- a spaceship\n- lots of courage'
    )
    max_participants = forms.DecimalField(
        min_value=1,
        initial=30,
        label='Max nr. of participants',
        help_text='How many people can join your course. (Can be changed later)'
    )


class AddTeacherForm(forms.Form):
    username = forms.CharField(
        help_text='Username of the person you want to be a teacher for this course',
        validators=[username_exists_validator]
    )


class NotifyCourseForm(forms.Form):
    subject = forms.CharField(
        min_length=1,
        help_text='This will become the subject field of the resulting email.'
    )
    content = forms.CharField(
        widget=forms.Textarea,
        help_text='This will be the content of the email. HTML is not allowed and any html tags will be removed.'
    )
    show_sender = forms.BooleanField(
        initial=False,
        required=False,
        help_text='Whether to set the email sender to your email address or not.'
    )


class CreateSubjectForm(forms.Form):
    name = forms.CharField(
        min_length=1,
        help_text='Name of the subject, also decides its url. '
                  'Allowed characters are word characters, numbers, spaces, '
                  '\'-\' and \'_\' and it cannot be \'new\'.',
        validators=[subject_name_validator, lambda a: a not in SUBJECT_DISALLOWED_NAMES]
    )
    description = forms.CharField(
        min_length=1,
        widget=forms.Textarea
    )
