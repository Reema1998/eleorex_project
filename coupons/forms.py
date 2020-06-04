from django import forms
import datetime
from django.db import transaction
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordResetForm, PasswordChangeForm
from coupons.models import User, Vendor, Coupons
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget




class UserAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(UserAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {'required': True,
                                                'class': 'form-control',
                                                'placeholder': 'Username',
                                                'id': 'username',
                                                'name': 'username',
                                                'type': 'text',
                                                'value': '',
                                                }
        self.fields['password'].widget.attrs = {'required': True,
                                                'class': 'form-control',
                                                'placeholder': 'Password',
                                                'id': 'password',
                                                'name': 'password',
                                                'type': 'password',
                                                'value': '',
                                                }

class AdminAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(AdminAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {'required': True,
                                                'class': 'EmailAdd',
                                                'placeholder': 'Email',
                                                'id': 'email',
                                                'name': 'email',
                                                'type': 'text',
                                                'value': '',
                                                }
        self.fields['password'].widget.attrs = {'required': True,
                                                'class': 'PassAdd',
                                                'placeholder': 'Password',
                                                'id': 'password',
                                                'name': 'password',
                                                'type': 'password',
                                                'value': '',
                                                }


class CaptchaPasswordResetForm(PasswordResetForm):
    captcha = ReCaptchaField(widget=ReCaptchaWidget())


class InterviewerSignUpForm(UserCreationForm):

    # def formCreation(forms.ModelForms):
    #

    def __init__(self, *args, **kwargs):
        super(InterviewerSignUpForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs = {"type": "text",
                                                  "name": "firstName",
                                                  "class": "form-control",
                                                  "required": True,
                                                  "placeholder": "Enter Firstname"
                                                  }
        self.fields['last_name'].widget.attrs = {"type": "text",
                                                 "name": "lastName",
                                                 "class": "form-control",
                                                 "required": True,
                                                 "placeholder": "Enter Lastname"
                                                 }
        self.fields['email'].widget.attrs = {"type": "email",
                                             "name": "email",
                                             "class": "form-control",
                                             "required": True,
                                             "onchange": "checkEmail(this)",
                                             "placeholder": "Enter email"
                                             }
        self.fields['password1'].widget.attrs = {"type": "password",
                                                 "name": "pass",
                                                 "class": "form-control",
                                                 "required": True,
                                                 "id=": "pass",
                                                 "placeholder": "Enter password"
                                                 }
        self.fields['password2'].widget.attrs = {"type": "password",
                                                 "name": "confirm_pass",
                                                 "class": "form-control",
                                                 "id": "confirm_pass",
                                                 "required": True,
                                                 "onchange": "confirmPassword()",
                                                 "placeholder": "Enter Confirm password"
                                                 }
        self.fields['user_type'].widget.attrs = {"class": "selectBox",
                                                 'required': True,
                                                 }


        # self.fields['company_name'].choices = [(tempDict['id'], tempDict['name']) for tempDict in
        #                                        Company.objects.values()]
        # self.fields['company_name'].widget.attrs = {'required': False,
        #                                             "class": "selectBox",
        #                                             "selected": "selected",
        #                                             "value": "1",
        #                                             }
        self.fields['user_type'].choices = [(index, value)
                                            for index, value in [(index, value)
                                                                 for index, value in self.fields['user_type'].choices
                                                                 if type(index) == int]
                                            if index < 3]

    # company_name = forms.ModelChoiceField(
    #     queryset=Company.objects.all(),
    #     required=False,
    #     initial=ADMIN_COMPANY_NAME
    # )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email',
                   'user_type')

    @transaction.atomic
    def save(self, user_obj=""):

        user = super().save(commit=False)
        user.username = user.email
        user.save()
        if user_obj.user_type == 1:
            company_detail = self.cleaned_data.get('company_name')
        else:
            company_detail = user_obj.working_organization.company
        interviewer = Interviewer.objects.create(
            user=user,
            company=company_detail)
        return user

    def clean_email(self):
        # Get the email
        email = self.cleaned_data.get('email')
        # Check to see if any users already exist with this email as a username.
        try:
            match = User.objects.get(email=email)
            print("-------in try------")
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            print("-------in except------")
            return email

        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('This email address is already in use.')


class InterviewerUpdateForm(UserChangeForm):

    def __init__(self, *args, **kwargs):
        super(InterviewerUpdateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs = {"type": "text",
                                                  "name": "firstName",
                                                  "class": "form-control",
                                                  "required": True,
                                                  "placeholder": "Enter Firstname"
                                                  }
        self.fields['last_name'].widget.attrs = {"type": "text",
                                                 "name": "lastName",
                                                 "class": "form-control",
                                                 "required": True,
                                                 "placeholder": "Enter Lastname"
                                                 }
        self.fields['email'].widget.attrs = {"type": "email",
                                             "name": "email",
                                             "class": "form-control",
                                             "onchange": "checkEmail(this)",
                                             "placeholder": "Enter email",
                                             'readonly': "readonly",
                                             }
        self.fields['user_type'].widget.attrs = {"class": "selectBox",
                                                 'required': True,
                                                 }
        self.fields['user_type'].choices = [(index, value)
                                            for index, value in [(index, value)
                                                                 for index, value in self.fields['user_type'].choices
                                                                 if type(index) == int]
                                            if index < 10]

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'user_type')

    @transaction.atomic
    def save(self, user_obj=""):
        user = super().save(commit=True)
        user.save()
        return user



class MyPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super(MyPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs = {'required': True,
                                                    'class': 'EmailAdd',
                                                    'placeholder': 'Old Password',
                                                    'id': 'old_password',
                                                    'name': 'old_password',
                                                    'type': 'text',
                                                    'value': '',
                                                    }
        self.fields['new_password1'].widget.attrs = {'required': True,
                                                     'class': 'PassAdd',
                                                     'placeholder': 'New Password',
                                                     'id': 'new_password1',
                                                     'name': 'new_password1',
                                                     'type': 'password',
                                                     'value': '',
                                                     }
        self.fields['new_password2'].widget.attrs = {'required': True,
                                                     'class': 'PassAdd',
                                                     'placeholder': 'Confirm New Password',
                                                     'id': 'new_password2',
                                                     'name': 'new_password2',
                                                     'type': 'password',
                                                     'value': '',
                                                     }
