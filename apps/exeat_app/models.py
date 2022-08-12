from tabnanny import verbose
from turtle import title
from django.db import models
from account.models import Account, Student


class Exeat(models.Model):
    student                     = models.ForeignKey(Student, on_delete=models.CASCADE)

    title                       = models.CharField(max_length=500, null=True, blank=True)
    reason                      = models.TextField(help_text="Reasons for applying for exeat")
    
    leave_on                    = models.DateField(null=True, blank=True)
    return_on                   = models.DateField(null=True, blank=True)

    date_submitted              = models.DateTimeField(auto_now_add=True)
    
    residence                   = models.CharField(max_length=500, blank=True, null=True)

    is_approved_DSA             = models.BooleanField(default=False)
    is_approved_by_hall_admin   = models.BooleanField(default=False)

    def __str__(self):
        return self.student.user.email
    
    class Meta:
        verbose_name_plural = "Exeat Form"

    def save(self, *args, **kwargs):
        self.residence = self.student.hall_of_residence
        super().save(*args, **kwargs)