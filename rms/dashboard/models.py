from django.contrib.auth.models import User
from django.db import models
class UserProfile(models.Model):
    # This field is required.
   user = models.OneToOneField(User)

    # Other fields here
   HOD = 'HOD'
   STUDENT = 'STU'
   STAFF = 'STF'
   FACULTY = 'FAC'
   PROFESSOR = 'PRO'
   ASSOCIATEPROF ='ASSOP'
   ASSISTANTPROF ='ASSIP'
   ADHOC = 'ADH'
	
	
   USER_TYPE_CHOICES = (
   (STUDENT, 'Student'),
   (STAFF, 'Staff'),
   (FACULTY, 'Faculty'),
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
	
   contact_no = models.BigIntegerField()
   
   designation = models.CharField(max_length=6,choices=DESG_TYPE_CHOICES,default=STUDENT)
									  
   user_type = models.CharField(max_length=3,choices=USER_TYPE_CHOICES,default=STUDENT)
