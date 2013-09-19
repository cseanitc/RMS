from django.db import models

# Create your models here.
from django.db import models

FCFS = 'FCFS'
PRIORITY = 'PRIOR'

STUDENT = 'STU'
STAFF = 'STF'
FACULTY = 'FAC'
PROFESSOR = 'PRO'
ASSOCIATEPROF ='ASSOP'
ASSISTANTPROF ='ASSIP'
ADHOC = 'ADH'
HOD = 'HOD'

   
	
POLICY_CHOICES = (
(FCFS, 'First come first serve'),
(PRIORITY, 'Priority'),
)

DESG_TYPE_CHOICES = (
 (HOD,'hod'),
(PROFESSOR, 'Professor'),
(ASSOCIATEPROF, 'Associate Professor'),
(ASSISTANTPROF, 'Assistant Professor'),
(ADHOC, 'Ad- hoc faculty'),
(STAFF, 'Staff'),
(STUDENT, 'Student'),
)   

class Resource(models.Model):
		name = models.CharField(max_length=100)
		type = models.CharField(max_length=100)
		location = models.CharField(max_length=300,blank=True, null=True)
		owning_dep = models.CharField(max_length=50) 
		availability = models.BooleanField()
		Add_information = models.CharField(max_length=500)
		allocation_policy = models.CharField(max_length=6,choices=POLICY_CHOICES)


class Booked_resource(models.Model):
       Booked_by = models.CharField(max_length=100)
       Event_name = models.CharField(max_length=400)
       Purpose_of_booking = models.CharField(max_length=500)
       all_day_event = models.IntegerField()
       start_date = models.DateField()
       start_time = models.TimeField()
       end_date = models.DateField()
       end_time = models.TimeField()
       resource_id = models.IntegerField()
       resource_name = models.CharField(max_length=100)
       resource_type = models.CharField(max_length=100)
	   
	   
class Priority_table(models.Model):
      Designation= models.CharField(max_length=100,choices=DESG_TYPE_CHOICES)
      Priority_num = models.IntegerField()