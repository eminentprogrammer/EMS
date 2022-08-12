from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Exeat, Account, Student
from django.contrib.auth.decorators import login_required
from .forms import ExeatAPPLYForm




def approve(request, id):
    user = Account.objects.get(slug=request.user.slug)
    exeat = Exeat.objects.get(id=id)

    if user.is_dsa:
        exeat.is_approved_DSA = True
        exeat.save()
    if user.is_female_porter:
        exeat.is_approved_by_hall_admin = True
        exeat.save()
    if user.is_male_porter:
        exeat.is_approved_by_hall_admin = True
        exeat.save()
    return redirect("list_of_approved_exeat")


class apply_for_exeat(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("login")
        return render(request, "exeat/exeat_form.html", locals())

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect("login")
        title = request.POST['title']
        reason = request.POST['reason']
        leave_on = request.POST['leave_on']
        return_on = request.POST['return_on']
        instance = Exeat.objects.create(student=Student.objects.get(user=request.user), title=title, reason=reason, leave_on=leave_on, return_on=return_on)
        # Send Hall of Admin and DSA a notification and email
        return redirect("pending_approved")


@login_required()
def list_of_approved_exeat(request):
    user = Account.objects.get(slug=request.user.slug)
    if user.is_student:
        list_of_exeats = Exeat.objects.filter(student=Student.objects.get(user=request.user), is_approved_DSA=True)

    if user.is_female_porter:
        list_of_exeats = Exeat.objects.filter(residence='Assumption Hall', is_approved_by_hall_admin=True)

    if user.is_male_porter:
        list_of_exeats = Exeat.objects.filter(residence='Divine Mercy Hall', is_approved_by_hall_admin=True)

    if user.is_dsa:
        list_of_exeats = Exeat.objects.filter(is_approved_DSA=True)
    return render(request, "exeat/list_of_approved_exeat.html", locals())


@login_required()
def pending_approved(request):
    user = Account.objects.get(slug=request.user.slug)
    
    if user.is_student:
        list_of_exeats = Exeat.objects.filter(student=Student.objects.get(user=request.user), is_approved_DSA=False)
    
    if user.is_female_porter:
        list_of_exeats = Exeat.objects.filter(residence='Assumption Hall', is_approved_by_hall_admin=False)

    if user.is_male_porter:
        list_of_exeats = Exeat.objects.filter(residence='Divine Mercy Hall', is_approved_by_hall_admin=False)

    if user.is_dsa:
        list_of_exeats = Exeat.objects.filter(is_approved_by_hall_admin=True, is_approved_DSA=False)
    return render(request, "exeat/pending_approval.html", locals())
