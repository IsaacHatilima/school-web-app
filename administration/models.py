from django.db import models
import uuid
from django.urls import reverse
from authentication.models import StaffProfile


class Department (models.Model):
    public_key = models.UUIDField(default=uuid.uuid4, editable=False,
                                  null=False, unique=True)
    created_by = models.ForeignKey(StaffProfile, null=False, editable=False,
                                   on_delete=models.PROTECT)
    department = models.CharField(max_length=50, null=False, unique=True)
    members = models.IntegerField(default=0, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        db_table = 'departments'
        ordering = ['-id']

    def get_absolute_url(self):
        return reverse('admin_dept_details',
                       kwargs={'public_key': self.public_key})

    def __str__(self):
        return self.department
