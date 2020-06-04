from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, ListView,
                                  UpdateView, TemplateView)
from django.contrib.auth.mixins import LoginRequiredMixin
from coupons.decorators import user_role_less_than_required
from coupons.models import User, Vendor, Coupons
from django.contrib.auth.models import AbstractUser
from coupons.forms import InterviewerUpdateForm, InterviewerSignUpForm



class HomePageView(TemplateView):
    template_name = 'templates/vendor/dashboard.html'


@login_required
@user_role_less_than_required(role_less_than=10)
def manage_dashboard(request):
    return render(request, 'vendor/dashboard.html')



@method_decorator([login_required, user_role_less_than_required(role_less_than=3)], name='dispatch')
class UserManagementListView(ListView):

    model = User
    ordering = ('first_name')
    context_object_name = 'consumers'
    template_name = 'vendor/user_management_list.html'

    def get_queryset(self):
        # return redirect('vendor:user_management_list')
        if self.request.user.user_type == 1:
            # queryset = User.objects.exclude(user_type=10)
            queryset = User.objects.order_by('first_name')
        # elif self.request.user.user_type == 2:
        #     queryset = User.objects.filter(
        #         working_organization__company__id=Interviewer.objects.filter(user=self.request.user.id).values()[0][
        #             'company_id']).exclude(user_type=10)
        else:
            queryset = User.objects.none()
        return queryset


@method_decorator([login_required, user_role_less_than_required(role_less_than=3)], name='dispatch')
class InterviewerSignUpView(LoginRequiredMixin, CreateView):
    model = User
    form_class = InterviewerSignUpForm
    template_name = 'vendor/user_management_create.html'



    # def post(self, request, *args, **kwargs):
    #     print("=================================================================================")
    #     print(request.POST['company_name'])




    def form_valid(self, form):

        #print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

        # if 'company_name' not in self.request.POST:
        #     company_id = Interviewer.objects.filter(user=self.request.user.id).values()[0]['company_id']
        #     #print("company_id: "+str(company_id))
        #     #return HttpResponse(str(company_id)) //// Exit Statement
        # else:
        #     company_id = self.request.POST['company_name']


        create_user_type = self.request.POST['user_type']


        comp = Company.objects.get(id=company_id)
        total_user = User.objects.filter(working_organization__company__id=company_id).exclude(user_type=10).count()

        #print("Licenses: "+str(comp.subscription.licenses))
        #print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        #print("Total user: "+str(total_user))

        #print(create_user_type)

        if int(create_user_type) == 1:
            if self.request.user.user_type == 1:
                user = form.save(user_obj=self.request.user)
                messages.success(self.request, 'User was added successfully')
                return redirect('vendor:user_management_list')
            elif self.request.user.user_type == 2 \
                    and "user_type=1" not in str(self.request.body):
                user = form.save(user_obj=self.request.user)
                messages.success(self.request, 'User was added successfully')
                return redirect('vendor:user_management_list')
            messages.error(
                self.request, 'You need permission to perform this action')
            return redirect('vendor:user_management_add')
        else:
            if int(total_user) < int(comp.subscription.licenses):
                if self.request.user.user_type == 1:
                    user = form.save(user_obj=self.request.user)
                    messages.success(self.request, 'User was added successfully')
                    return redirect('vendor:user_management_list')
                elif self.request.user.user_type == 2 \
                        and "user_type=1" not in str(self.request.body):
                    user = form.save(user_obj=self.request.user)
                    messages.success(self.request, 'User was added successfully')
                    return redirect('vendor:user_management_list')
                messages.error(
                    self.request, 'You need permission to perform this action')
                return redirect('vendor:user_management_add')
            else:
                messages.error(self.request, 'You have reached to the total users for your plan, Please updrade your plan to add more users.')
                return redirect('vendor:user_management_add')




    def get_context_data(self, **kwargs):
        context = super(InterviewerSignUpView, self).get_context_data(**kwargs)
        if self.request.user.user_type < 3:
            context['form'].fields['user_type'].choices = [(index, value) for index, value in
                                                           [(index, value) for index, value in
                                                            context['form'].fields['user_type'].choices if
                                                            type(index) == int] if
                                                           (self.request.user.user_type <= index < 10)]
        else:
            context = {}
        return context
#

@method_decorator([login_required, user_role_less_than_required(role_less_than=10)], name='dispatch')
class InterviewerUpdateView(UpdateView):
    model = User
    template_name = 'vendor/user_management_edit.html'
    context_object_name = 'consumer'
    form_class = InterviewerUpdateForm

    def get_success_url(self):
        return reverse('vendor:user_management_edit', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        if self.request.user.user_type == 1:
            company = form.save()
            user = form.save(user_obj=self.request.user)
            messages.success(self.request, 'User was updated successfully')
            return redirect('vendor:user_management_edit', pk=self.object.pk)
        elif self.request.user.user_type == 2 \
                and "user_type=1" not in str(self.request.body) \
                and Interviewer.objects.filter(user=self.request.user.id).values()[0]['company_id'] == \
                Interviewer.objects.filter(user=User.objects.filter(username=[para for para in
                                                                              self.request.body.decode("utf-8").split(
                                                                                  "&") if para.startswith("email=")][0].replace(
                    "%40", "@").split("=")[-1])[0].id).values()[0]['company_id']:
            user = form.save(user_obj=self.request.user)
            messages.success(self.request, 'User was updated successfully')
            return redirect('vendor:user_management_edit', pk=self.object.pk)
        messages.error(
            self.request, 'You need permission to perform this action')
        return redirect('vendor:user_management_edit', pk=self.object.pk)

    def get_context_data(self, **kwargs):
        context = super(InterviewerUpdateView, self).get_context_data(**kwargs)
        if self.request.user.user_type < 3:
            context['form'].fields['user_type'].choices = [(index, value)
                                                           for index, value in [(index, value)
                                                                                for index, value in
                                                                                context['form'].fields['user_type'].choices
                                                                                if type(index) == int]
                                                           if (self.request.user.user_type <= index < 10)]
        else:
            context = {}
        return context

    def get_queryset(self):
        if self.request.user.user_type == 1:
            queryset = User.objects.exclude(user_type=10)
        elif self.request.user.user_type == 2:
            queryset = User.objects.filter(
                working_organization__company__id=Interviewer.objects.filter(user=self.request.user.id).values()[0][
                    'company_id']).exclude(user_type=10)
        else:
            queryset = User.objects.none()
        return queryset


@method_decorator([login_required, user_role_less_than_required(role_less_than=3)], name='dispatch')
class InterviewerDeleteView(DeleteView):
    model = User
    template_name = 'vendor/user_management_delete.html'
    success_url = reverse_lazy('vendor:user_management_list')
    context_object_name = "consumer"

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        messages.success(
            request, 'The user %s was deleted with success!' % user.email)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.user.user_type == 1:
            queryset = User.objects.all()
        #     queryset = User.objects.exclude(user_type=10)
        # elif self.request.user.user_type == 2:
        #     queryset = User.objects.filter(
        #         working_organization__company__id=Interviewer.objects.filter(user=self.request.user.id).values()[0][
        #             'company_id']).exclude(user_type=10)
        else:
            queryset = User.objects.none()
        return queryset
