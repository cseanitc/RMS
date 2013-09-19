from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from django.contrib.auth.models import User
from dashboard.models import UserProfile
from dajax.core import Dajax
from datetime import datetime
from datetime import time
from datetime import date
from resource.models import *
import jsonpickle
from django.db.models import Q
import threading

@dajaxice_register()
def updatecombo(request,option):
    dajax = Dajax()
    out = ["<option value='0'>Select Resource...</option>"]
    if option != '0':
        re=Resource.objects.filter(type=option).values('name','id')
        res=re.filter(availability='true')
        dajax.remove_css_class('#combo2s', 'hide')
        for r in res:
            out.append("<option value='%s'>%s</option>" % (r['id'],r['name']))
    else:
        dajax.add_css_class('#combo2s', 'hide')
    dajax.assign('#combo2', 'innerHTML',''.join(out))
    
    dajax.clear('#status', 'innerHTML')
    dajax.add_css_class('#options', 'hide')
    dajax.add_css_class('.alert-error', 'hide')
    dajax.clear('#errorList .showMessage','innerHTML')
    dajax.add_css_class('#mul_date','hide')
    dajax.add_css_class('#sel_date','hide')
    dajax.add_css_class('#infos', 'hide')
    dajax.add_css_class('#st_time', 'hide')
    dajax.add_css_class('#en_time', 'hide')
    dajax.add_data('','$("input[name=optionsRadios]:checked").val')
    dajax.add_data('checked','$("input[name=optionsRadios]:checked").removeAttr')
    return dajax.json()

@dajaxice_register()
def updateprofile(request,fname,lname,email,cno):
    dajax = Dajax()
    u=User.objects.get(id=request.user.id)
    user_cno=UserProfile.objects.get(id=u.id)
    if fname =='':
         dajax.add_data('First name can not be left blank','bootbox.alert')
    elif lname =='':
         dajax.add_data('Last name can not be left blank','bootbox.alert')
    elif email=='':
         dajax.add_data('Email can not be left blank','bootbox.alert')
    elif cno=='':
         dajax.add_data('Contact number can not be left blank','bootbox.alert')
    else:
         u.first_name=fname
         u.last_name=lname
         u.email=email
         user_cno.contact_no=int(cno)
         u.save()
         user_cno.save()
         dajax.add_data({'message':'Your profile has been successfully updated','location':'/profile/'}, 'bootbox_alert')
    return dajax.json()

    
@dajaxice_register()
def updateinfo(request,option):
    dajax = Dajax()
    if option !='0' and option != None:
        infor=Resource.objects.get(id=option)
        dajax.assign('#info', 'innerHTML',infor.Add_information)
        dajax.assign('#location', 'innerHTML',infor.location)
        dajax.remove_css_class('#options', 'hide')
        dajax.remove_css_class('#infos', 'hide')
    else:
        dajax.add_css_class('#infos', 'hide')
        dajax.add_css_class('#options', 'hide')
        dajax.add_css_class('#infos', 'hide')
        dajax.add_css_class('#options', 'hide')
        dajax.add_css_class('#options', 'hide')
        dajax.add_css_class('.alert-error', 'hide')
        dajax.clear('#errorList .showMessage','innerHTML')
        dajax.add_css_class('#mul_date','hide')
        dajax.add_css_class('#sel_date','hide')
        dajax.add_css_class('#infos', 'hide')
        dajax.add_css_class('#st_time', 'hide')
        dajax.add_css_class('#en_time', 'hide')
        dajax.add_data('','$("input[name=optionsRadios]:checked").val')
        dajax.add_data('checked','$("input[name=optionsRadios]:checked").removeAttr')
        dajax.clear('#status', 'innerHTML')
    return dajax.json()


@dajaxice_register()
def cancel_booking(request,option):
    dajax = Dajax()
    booking=Booked_resource.objects.get(id=option)
    booking.delete()
    dajax.add_data('Your booking has been cancelled','bootbox.alert')
    dajax.redirect('/dashboard/', delay=3000)
    return dajax.json()


@dajaxice_register()
def eInfo(request,option):
    dajax = Dajax()
    now=datetime.now().date()
    booking=Booked_resource.objects.get(id=option).filter(Q(start_date__gte=now)|Q(end_date__gte=now))
    input =[];
    input.append('<table class="table table-striped"><thead></thead><tr><th>Event Name</th><th>Resource Name</th><th>Resource Type</th><th>Booked By</th><th>Additional Information</th></tr><tr><td>'+booking.Event_name+'</td><td>'+booking.resource_name+'</td><td>'+booking.resource_type+'</td><td>'+booking.Booked_by+'</td><td>'+booking.Purpose_of_booking+'</td></tr><tbody></tbody></table>')
    dajax.assign('.modal-body1', 'innerHTML',''.join(input))
    return dajax.json()


@dajaxice_register()    
def day_check(request,option):
    dajax=Dajax()
    dajax.alert(option)
    return dajax.json()


    
@dajaxice_register()    
def date_check(request,option):
    dajax = Dajax()
    now=datetime.now().date()
    status = []
    sel_date = datetime.strptime(option,"%Y-%m-%d").date()
    if sel_date > now:
         status.append('<button onclick="Dajaxice.dashboard.single_booking_check(Dajax.process, {\'end_min\':document.getElementById(\'emin\').value,\'end_hour\':document.getElementById(\'ehr\').value,\'start_hour\':document.getElementById(\'shr\').value,\'start_min\':document.getElementById(\'smin\').value,\'option\':document.getElementById(\'datepicker\').value,\'res_id\':document.getElementById(\'combo2\').value})" type="button"  >Click here to check status</button>')
         dajax.assign('#status', 'innerHTML',''.join(status))
         dajax.add_css_class('#errorList', 'hide')
         dajax.add_css_class('.alert-error', 'hide')
    else:
         dajax.assign('#errorList .showMessage','innerHTML','You cannot book for the past or today. Kindly select some other date')
         dajax.clear('#status', 'innerHTML')
         dajax.add_css_class('#startt-error', 'hide')
         dajax.add_css_class('#endt-error', 'hide')
         dajax.remove_css_class('#errorList', 'hide') 
         dajax.remove_css_class('#seld-error', 'hide')   
    return dajax.json()



##########################fixed    
@dajaxice_register()    
def date_check_new(request,option,end_hour,end_min,start_hour,start_min):
    dajax = Dajax()
    end_hour=int(end_hour)
    end_min=int(end_min)
    start_hour = int(start_hour)
    start_min = int(start_min)
    now=datetime.now().date()
    date = datetime.strptime(option,"%Y-%m-%d").date()
    status = []
    if now < date:
        dajax.add_css_class('#seld-error', 'hide')
        dajax.add_css_class('#errorList', 'hide')
        if start_hour!=0  and end_hour!=0 and end_min!=60 and start_min!=60:
            status.append('<button onclick="Dajaxice.dashboard.single_booking_check(Dajax.process, {\'end_min\':document.getElementById(\'emin\').value,\'end_hour\':document.getElementById(\'ehr\').value,\'start_hour\':document.getElementById(\'shr\').value,\'start_min\':document.getElementById(\'smin\').value,\'option\':document.getElementById(\'datepicker\').value,\'res_id\':document.getElementById(\'combo2\').value})" type="button"  >Click here to check status</button>')
            dajax.assign('#status', 'innerHTML',''.join(status))
            dajax.add_css_class('#errorList', 'hide')
            dajax.add_css_class('.alert-error', 'hide')
        else:
            dajax.clear('#status','innerHTML')
            if start_hour==0 or start_min==60:
                dajax.remove_css_class('#startt-error', 'hide')
            else:
                dajax.remove_css_class('#endt-error', 'hide')
                dajax.add_css_class('#startt-error', 'hide')

    else:
        dajax.assign('#errorList .showMessage','innerHTML','You can not book for the past or today. Kindly select some other date')
        dajax.clear('#status','innerHTML')
        dajax.remove_css_class('#errorList', 'hide')
        dajax.remove_css_class('#seld-error', 'hide')
    return dajax.json()




@dajaxice_register()    
def time_check(request,end_hour,end_min,start_hour,start_min,option):
    dajax=Dajax()
    end_hour=int(end_hour)
    end_min=int(end_min)
    start_hour=int(start_hour)
    start_min=int(start_min)
    status=[]
    if start_hour!=0  and end_hour!=0 and end_min!=60 and start_min!=60:
        end_time=time(int(end_hour),int(end_min))
        start_time = time(int(start_hour),int(start_min))
        dajax.add_css_class('#startt-error', 'hide')
        dajax.add_css_class('#endt-error', 'hide')
        if(end_time<=start_time):
            dajax.clear('#status', 'innerHTML')
            dajax.assign('#errorList .showMessage','innerHTML','End time cannot be less than or equal to start time')
            dajax.remove_css_class('#errorList', 'hide')
            dajax.remove_css_class('#endt-error', 'hide')
        else:
            now=datetime.now().date()
            date = datetime.strptime(option,"%Y-%m-%d").date()
            if now<date:
                status.append('<button onclick="Dajaxice.dashboard.single_booking_check(Dajax.process, {\'end_min\':document.getElementById(\'emin\').value,\'end_hour\':document.getElementById(\'ehr\').value,\'start_hour\':document.getElementById(\'shr\').value,\'start_min\':document.getElementById(\'smin\').value,\'option\':document.getElementById(\'datepicker\').value,\'res_id\':document.getElementById(\'combo2\').value})" type="button"  >Click here to check status</button>')
                dajax.assign('#status', 'innerHTML',''.join(status))
                dajax.add_css_class('#errorList', 'hide')
                dajax.add_css_class('.alert-error', 'hide')
            else:
                dajax.assign('#errorList .showMessage','innerHTML','You can not book for the past or today. Kindly select some other date')
                dajax.clear('#status','innerHTML')
                dajax.remove_css_class('#errorList', 'hide')
                dajax.remove_css_class('#seld-error', 'hide')
    else:
        dajax.clear('#status','innerHTML')
        if start_hour==0 or start_min==60:
            dajax.remove_css_class('#startt-error', 'hide')
        else:
            dajax.remove_css_class('#endt-error', 'hide')
            dajax.add_css_class('#startt-error', 'hide')
    return dajax.json()

@dajaxice_register()    
def time_check_new(request,end_hour,end_min,start_hour,start_min,option):
    dajax=Dajax()
    end_hour=int(end_hour)
    end_min=int(end_min)
    start_hour=int(start_hour)
    start_min=int(start_min)
    status=[]
    if start_hour!=0  and end_hour!=0 and end_min!=60 and start_min!=60:
        end_time=time(int(end_hour),int(end_min))
        start_time = time(int(start_hour),int(start_min))
        if(end_time<=start_time):
            dajax.assign('#errorList .showMessage','innerHTML','End time must be greater than Start time')
            dajax.clear('#status','innerHTML')
            dajax.remove_css_class('#errorList', 'hide')
            dajax.remove_css_class('#endt-error', 'hide')
        else:
            now=datetime.now().date()
            date = datetime.strptime(option,"%Y-%m-%d").date()
            if now<date:
                status.append('<button onclick="Dajaxice.dashboard.single_booking_check(Dajax.process, {\'end_min\':document.getElementById(\'emin\').value,\'end_hour\':document.getElementById(\'ehr\').value,\'start_hour\':document.getElementById(\'shr\').value,\'start_min\':document.getElementById(\'smin\').value,\'option\':document.getElementById(\'datepicker\').value,\'res_id\':document.getElementById(\'combo2\').value})" type="button"  >Click here to check status</button>')
                dajax.assign('#status', 'innerHTML',''.join(status))
                dajax.add_css_class('#errorList', 'hide')
                dajax.add_css_class('.alert-error', 'hide')
            else:
                dajax.assign('#errorList .showMessage','innerHTML','You can not book for the past or today, Kindly select some other date')
                dajax.clear('#status', 'innerHTML')
                dajax.remove_css_class('#errorList', 'hide')
                dajax.remove_css_class('#seld-error', 'hide')
    else:
        dajax.clear('#status','innerHTML')
        if start_hour==0 or start_min==60:
            dajax.remove_css_class('#startt-error', 'hide')
        else:
            dajax.remove_css_class('#endt-error', 'hide')
            dajax.add_css_class('#startt-error', 'hide')
    
    return dajax.json()



##########################fixed       
@dajaxice_register()    
def start_date_check(request,start_date):
    dajax = Dajax()
    now=datetime.now().date()
    st = []
    start_date = datetime.strptime(start_date,"%Y-%m-%d").date()
    if now<start_date:
        dajax.add_css_class('#startd-error', 'hide')
        dajax.remove_css_class('#endd-error', 'hide')
        dajax.assign('#errorList .showMessage','innerHTML','Kindly choose end date')
        dajax.clear('#status','innerHTML')
    else:
        dajax.assign('#errorList .showMessage','innerHTML','You can not book for the past or today, Kindly select some other start date')
        dajax.clear('#status','innerHTML')
        dajax.remove_css_class('#startd-error', 'hide')
    
    dajax.remove_css_class('#errorList', 'hide')
    return dajax.json()


##########################fixed  
@dajaxice_register()    
def end_date_check(request,end_date):
    dajax = Dajax()
    now=datetime.now().date()
    st = []
    end_date = datetime.strptime(end_date,"%Y-%m-%d").date()
    if now<end_date:
        dajax.add_css_class('#endd-error', 'hide')
        dajax.remove_css_class('#startd-error', 'hide')
        dajax.assign('#errorList .showMessage','innerHTML','Kindly choose start date')
        dajax.clear('#status','innerHTML')
    else:
        dajax.assign('#errorList .showMessage','innerHTML','You can not book for the past or today, Kindly select some other end date')
        dajax.clear('#status','innerHTML')
        dajax.remove_css_class('#endd-error', 'hide')
    
    dajax.remove_css_class('#errorList', 'hide')
    return dajax.json()

@dajaxice_register()
def both_date_check(request,start_date,end_date):
    dajax = Dajax()
    now=datetime.now().date()
    st = []
    start_date = datetime.strptime(start_date,"%Y-%m-%d").date()
    end_date = datetime.strptime(end_date,"%Y-%m-%d").date()
    if now<end_date:
        if now<start_date:
            dajax.add_css_class('#startd-error', 'hide')
            if start_date<end_date:
                st.append('<button onclick="Dajaxice.dashboard.multiple_booking_check(Dajax.process, {\'option\':this.value,\'start_date\':document.getElementById(\'datepicker1\').value,\'end_date\':document.getElementById(\'datepicker2\').value,\'res_id\':document.getElementById(\'combo2\').value})" type="button"  >Click here to check status</button>')
                dajax.assign('#status', 'innerHTML',''.join(st))
                dajax.add_css_class('#errorList', 'hide')
                dajax.add_css_class('.alert-error', 'hide')
            else:
                dajax.assign('#errorList .showMessage','innerHTML','Kindly choose end date greater than start date')
                dajax.clear('#status','innerHTML')
                dajax.remove_css_class('#endd-error', 'hide')
                dajax.remove_css_class('#errorList', 'hide')
        else:
            dajax.assign('#errorList .showMessage','innerHTML','You can not book for the past or today. Kindly select some other start date')
            dajax.clear('#status','innerHTML')
            dajax.remove_css_class('#startd-error', 'hide')
            dajax.remove_css_class('#errorList', 'hide')
    else:
        dajax.assign('#errorList .showMessage','innerHTML','You can not book for the past or today. Kindly select some other end date')
        dajax.clear('#status','innerHTML')
        dajax.remove_css_class('#endd-error', 'hide')
        dajax.remove_css_class('#errorList', 'hide')
    return dajax.json()


@dajaxice_register()    
def update_check_new(request,val,resource,end_hour,end_min,start_hour,start_min,start_date,end_date,sel_date):
    dajax = Dajax()
    if resource !='0' and resource != None:
        infor=Resource.objects.get(id=resource)
        dajax.assign('#info', 'innerHTML',infor.Add_information)
        dajax.assign('#location', 'innerHTML',infor.location)
        dajax.remove_css_class('#options', 'hide')
        dajax.remove_css_class('#infos', 'hide')
    else:
        dajax.add_css_class('#infos', 'hide')
        dajax.add_css_class('#options', 'hide')
        dajax.add_css_class('#options', 'hide')
        dajax.add_css_class('.alert-error', 'hide')
        dajax.clear('#errorList .showMessage','innerHTML')
        dajax.add_css_class('#mul_date','hide')
        dajax.add_css_class('#sel_date','hide')
        dajax.add_css_class('#infos', 'hide')
        dajax.add_css_class('#st_time', 'hide')
        dajax.add_css_class('#en_time', 'hide')
        dajax.add_data('','$("input[name=optionsRadios]:checked").val')
        dajax.add_data('checked','$("input[name=optionsRadios]:checked").removeAttr')
    dajax.clear('#status', 'innerHTML')
    val = int(val)
    d = dajax.json()
    s=None
    if val==1:
        if sel_date != '':
            s=time_check_new(request,end_hour,end_min,start_hour,start_min,sel_date)
            d = d[0:-1]+', '+s[1:]
    if val==2:
        if sel_date != '':
            s = date_check(request,sel_date)
            d = d[0:-1]+', '+s[1:]
    if val==3:
        if start_date != '' and end_date!= '':
            s = both_date_check(request,start_date,end_date)
        elif start_date!= '':
            s = start_date_check(request,start_date)
        elif end_date != '':
            s = end_date_check(request,end_date)
        if s:
            d = d[0:-1]+', '+s[1:]
    return d

 
#fixed------------------------------------  
@dajaxice_register()
def multiple_booking_check(request,option,start_date,end_date,res_id):
    dajax=Dajax()
    overwrite_list = []
    overwrite = True
    book = True
    resource_name=Resource.objects.get(id=res_id).name
    try:
        start_date = datetime.strptime(start_date,"%Y-%m-%d").date()
        end_date = datetime.strptime(end_date,"%Y-%m-%d").date()
    except:
        dajax.add_data("Dates not choosen",'bootbox.alert')
        return dajax.json()
    now = datetime.now().date()
    allocation_policy=Resource.objects.get(id=res_id).allocation_policy # This query fetches the allocation policy of the selected resource
    user_desg=UserProfile.objects.get(id=request.user.id) # This query gets the user designation
    user_priority=Priority_table.objects.get(Designation=user_desg.designation).Priority_num # This query gets the priority number of user
    booking_list=Booked_resource.objects.filter(resource_id=res_id).filter(Q(start_date__gte=now)|Q(end_date__gte=now))

    if start_date>end_date:
        dajax.add_data("End Date must be greater than start date",'bootbox.alert')
    elif start_date <= now or end_date <= now:
        dajax.add_data("You cannot book for past.",'bootbox.alert')
    else:
        # Check for resources to "free" or "need to be overwritten"
        for r in booking_list:
            u=User.objects.get(username=r.Booked_by)
            profile=UserProfile.objects.get(id=u.id)
            booked_priority=Priority_table.objects.get(Designation=profile.designation).Priority_num
            if (start_date >= r.start_date and start_date <=r.end_date) or (end_date >= r.start_date and end_date <= r.end_date):
                if allocation_policy == 'PRIOR':
                    if user_priority < booked_priority:
                        overwrite = False
                        break
                    else:
                        overwrite_list.append(r)
                elif allocation_policy == 'FCFS':
                    book = False
                    break
        # Return based on check done
        if allocation_policy == 'PRIOR':
            if overwrite:
                if overwrite_list:
                    status = '<p>You are going to overwrite following Bookings:</br><table class="zebra-striped">'
                    mapping={0:"No",1:"Single",2:"Multiple"}
                    for r in overwrite_list:
                        starts = r.start_date.strftime("%b %d, %Y") + ', ' + r.start_time.strftime("%H,%M")
                        ends = r.end_date.strftime("%b %d, %Y") + ', ' + r.end_time.strftime("%H,%M")
                        status=status+"<tr> <td>"+r.Event_name+"</td> <td>"+r.Booked_by+"</td> <td>"+mapping[r.all_day_event]+"<td> <td>"+starts+"</td> <td>"+ends+"</td> <td>"+r.Purpose_of_booking+"</td> </tr>"
                    status=status+"</table></br> Do you want to proceed booking the "+resource_name+"?</p>"
                    pickled_overwrite=jsonpickle.encode(overwrite_list)
                    dajax.add_data({'message': status, 'type':'multiple', 'pickled_overwrite':pickled_overwrite}, 'book_resource')
                else:
                    dajax.add_data({'message': '{0} is free. Do you want to proceed booking?'.format(resource_name), 'type':'multiple'}, 'book_resource')
        elif allocation_policy == 'FCFS':
            if book:
                dajax.add_data({'message':'{0} is free. Do you want to proceed booking?'.format(resource_name), 'type':'multiple'}, 'book_resource')
            else:
                dajax.add_data("Sorry {0} is not free. Kindly choose some other date/time/resource".format(resource_name),'bootbox.alert')
    return dajax.json() 


#fixed------------------------------------
@dajaxice_register()
def single_booking_check(request,end_hour,end_min,start_hour,start_min,option,res_id):
    dajax=Dajax()
    end_hour=int(end_hour)
    end_min=int(end_min)
    start_hour=int(start_hour)
    start_min=int(start_min)
    overwrite_list = []
    overwrite = True
    book = True
    resource_name=Resource.objects.get(id=res_id).name
    now = datetime.now().date()
    sel_date,start_time,end_time = None,None,None 
    try:
        sel_date = datetime.strptime(option,"%Y-%m-%d").date()
    except:
        dajax.add_data("Date not choosen",'bootbox.alert')
        return dajax.json()
    try:
        end_time=time(int(end_hour),int(end_min))
        start_time = time(int(start_hour),int(start_min))
    except:
        dajax.add_data("Please select correct time",'bootbox.alert') 
        return dajax.json() 
    allocation_policy=Resource.objects.get(id=res_id).allocation_policy # This query fetches the allocation policy of the selected resource
    user_desg=UserProfile.objects.get(id=request.user.id) # This query gets the user designation
    user_priority=Priority_table.objects.get(Designation=user_desg.designation).Priority_num # This query gets the priority number of user
    booking_list=Booked_resource.objects.filter(resource_id=res_id).filter(Q(start_date__gte=now)|Q(end_date__gte=now))
    if start_hour==0  or end_hour==0 or end_min==60 or start_min==60:
        dajax.add_data('All the fields must be filled','bootbox.alert') 
    elif end_hour==start_hour and end_min<=start_min:
        dajax.add_data('End time cannot be less than or equals to start time','bootbox.alert')  
    elif end_hour<start_hour:
        dajax.add_data('End time cannot be less than start time','bootbox.alert')
    elif sel_date < now:
        dajax.add_data('End time cannot be less than start time','bootbox.alert')
    else:
        for r in booking_list:
            u=User.objects.get(username=r.Booked_by)
            profile=UserProfile.objects.get(id=u.id)
            booked_priority=Priority_table.objects.get(Designation=profile.designation).Priority_num
            if  r.start_date != r.end_date:
                if (sel_date >= r.start_date and sel_date <=r.end_date):
                    if allocation_policy == 'PRIOR':
                        if user_priority < booked_priority:
                            overwrite = False
                            break
                        else:
                            overwrite_list.append(r)
                    elif allocation_policy == 'FCFS':
                        book = False
                        break
            elif r.start_date == r.end_date:
                if sel_date == r.start_date:  
                    if r.all_day_event:   
                        if allocation_policy == 'PRIOR':
                            if user_priority < booked_priority:
                                overwrite = False
                                break
                            else:
                                overwrite_list.append(r)
                        elif allocation_policy == 'FCFS':
                            book = False
                            break
                    elif (start_time >= r.start_time and start_time <=r.end_time) or (end_time >= r.start_time and end_time <= r.end_time):
                        if allocation_policy == 'PRIOR':
                            if user_priority < booked_priority:
                                overwrite = False
                                break
                            else:
                                overwrite_list.append(r)
                        elif allocation_policy == 'FCFS':
                            book = False
                            break

        # Return based on check done
        if allocation_policy == 'PRIOR':
            if overwrite:
                if overwrite_list:
                    status = '<p>You are going to overwrite following Bookings:</br><table class="zebra-striped">'
                    mapping={0:"No",1:"Single",2:"Multiple"}
                    for r in overwrite_list:
                        starts = r.start_date.strftime("%b %d, %Y") + ', ' + r.start_time.strftime("%H,%M")
                        ends = r.end_date.strftime("%b %d, %Y") + ', ' + r.end_time.strftime("%H,%M")
                        status=status+"<tr> <td>"+r.Event_name+"</td> <td>"+r.Booked_by+"</td> <td>"+mapping[r.all_day_event]+"<td> <td>"+starts+"</td> <td>"+ends+"</td> <td>"+r.Purpose_of_booking+"</td> </tr>"
                    status=status+"</table></br> Do you want to proceed booking the "+resource_name+"?</p>"
                    pickled_overwrite=jsonpickle.encode(overwrite_list)
                    dajax.add_data({'message': status, 'type':'single', 'pickled_overwrite':pickled_overwrite}, 'book_resource')
                else:
                    dajax.add_data({'message': '{0} is free. Do you want to proceed booking?'.format(resource_name), 'type':'single'}, 'book_resource')
            else:
                dajax.add_data("Sorry overwriting booked {0} is not possible. <br/> Kindly choose some other date/time/resource".format(resource_name),'bootbox.alert')    
        elif allocation_policy == 'FCFS':
            if book:
                dajax.add_data({'message':'{0} is free. Do you want to proceed booking?'.format(resource_name), 'type':'single'}, 'book_resource')
            else:
                dajax.add_data("Sorry {0} is not free. Kindly choose some other date/time/resource".format(resource_name),'bootbox.alert')
    return dajax.json()
#fixed------------------------------------

    
@dajaxice_register()    
def book_m(request,event,add_info,start_date,end_date,start_hour,start_min,end_hour,end_min,res_id,verify_list):
    dajax=Dajax()
    overwrite_list = []
    overwrite = True
    book = True
    start_time,end_time = None,None
    resource_name=Resource.objects.get(id=res_id).name
    try:
        start_date = datetime.strptime(start_date,"%Y-%m-%d").date()
        end_date = datetime.strptime(end_date,"%Y-%m-%d").date()
    except:
        dajax.add_data("Dates not choosen",'bootbox.alert')
        return dajax.json()
    try:
        end_time=time(int(end_hour),int(end_min))
        start_time = time(int(start_hour),int(start_min))
    except:
        dajax.add_data("Invalid input",'bootbox.alert')
        return dajax.json()
    now = datetime.now().date()
    allocation_policy=Resource.objects.get(id=res_id).allocation_policy # This query fetches the allocation policy of the selected resource
    user_desg=UserProfile.objects.get(id=request.user.id) # This query gets the user designation
    user_priority=Priority_table.objects.get(Designation=user_desg.designation).Priority_num # This query gets the priority number of user

    if start_date>end_date:
        dajax.add_data("End Date must be greater than start date",'bootbox.alert')
    elif start_date <= now or end_date <= now:
        dajax.add_data("You cannot book for past.",'bootbox.alert')
    elif event == "":
         dajax.add_data('Please enter Event name!!','bootbox.alert')
    elif add_info == "":
         dajax.add_data('Please enter additional information!!','bootbox.alert')
    else:
        # Check for resources to "free" or "need to be overwritten"
        dajax.add_data('#myModal_multiple','hide_modal')
        lock = threading.Lock()
        with lock:
            booking_list=Booked_resource.objects.filter(resource_id=res_id).filter(Q(start_date__gte=now)|Q(end_date__gte=now))
            for r in booking_list:
                u=User.objects.get(username=r.Booked_by)
                profile=UserProfile.objects.get(id=u.id)
                booked_priority=Priority_table.objects.get(Designation=profile.designation).Priority_num
                if (start_date >= r.start_date and start_date <=r.end_date) or (end_date >= r.start_date and end_date <= r.end_date):
                    if allocation_policy == 'PRIOR':
                        if user_priority < booked_priority:
                            overwrite = False
                            break
                        else:
                            overwrite_list.append(r)
                    elif allocation_policy == 'FCFS':
                        book = False
                        break
            # Return based on check done
            resource_details=Resource.objects.get(id=res_id)
            if allocation_policy == 'PRIOR':
                if overwrite:
                    if overwrite_list:
                        for r in overwrite_list:
                            booking_del=Booked_resource.objects.get(id=r.id)
                            booking_del.delete()
                        booking=Booked_resource.objects.create(Booked_by=request.user.username,Event_name=event,Purpose_of_booking=add_info,all_day_event=2,start_date=start_date,start_time=start_time.strftime("%H:%M"),end_date=end_date,end_time=end_time.strftime("%H:%M"),resource_id=res_id,resource_name=resource_details.name,resource_type=resource_details.type)
                        booking.save()
                        dajax.add_data({ 'message':'{0} has been booked by overwriting successfully'.format(resource_name),'location':'/booking/'},'bootbox_alert')
                    else:
                        booking=Booked_resource.objects.create(Booked_by=request.user.username,Event_name=event,Purpose_of_booking=add_info,all_day_event=2,start_date=start_date,start_time=start_time.strftime("%H:%M"),end_date=end_date,end_time=end_time.strftime("%H:%M"),resource_id=res_id,resource_name=resource_details.name,resource_type=resource_details.type)
                        booking.save()
                        dajax.add_data({ 'message':'{0} has been booked successfully'.format(resource_name), 'location':'/booking/'},'bootbox_alert')
                else:
                    dajax.add_data("Sorry overwriting booked {0} is not possible. Kindly choose some other date/time/resource".format(resource_name),'bootbox.alert')
            elif allocation_policy == 'FCFS':
                if book:
                    booking=Booked_resource.objects.create(Booked_by=request.user.username,Event_name=event,Purpose_of_booking=add_info,all_day_event=2,start_date=start_date,start_time=start_time.strftime("%H:%M"),end_date=end_date,end_time=end_time.strftime("%H:%M"),resource_id=res_id,resource_name=resource_details.name,resource_type=resource_details.type)
                    booking.save()
                    dajax.add_data({'message':'{0} has been booked successfully'.format(resource_name),'location':'/booking/'}, 'bootbox_alert')
                else:
                    dajax.add_data("Sorry {0} is not free. Kindly choose some other date/time/resource".format(resource_name),'bootbox.alert')
    return dajax.json()

@dajaxice_register()
def book_s(request,event,add_info,start_date,end_date,start_hour,start_min,end_hour,end_min,res_id,verify_list):
    dajax=Dajax()
    end_hour=int(end_hour)
    end_min=int(end_min)
    start_hour=int(start_hour)
    start_min=int(start_min)
    overwrite_list = []
    overwrite = True
    book = True
    resource_name=Resource.objects.get(id=res_id).name
    now = datetime.now().date()
    sel_date,start_time,end_time = None,None,None 
    try:
        sel_date = datetime.strptime(start_date,"%Y-%m-%d").date()
    except:
        dajax.add_data("Date not choosen",'bootbox.alert')
        return dajax.json()
    try:
        end_time=time(int(end_hour),int(end_min))
        start_time = time(int(start_hour),int(start_min))
    except:
        dajax.add_data("Please select correct time",'bootbox.alert') 
        return dajax.json() 
    allocation_policy=Resource.objects.get(id=res_id).allocation_policy # This query fetches the allocation policy of the selected resource
    user_desg=UserProfile.objects.get(id=request.user.id) # This query gets the user designation
    user_priority=Priority_table.objects.get(Designation=user_desg.designation).Priority_num # This query gets the priority number of user

    if sel_date<now:
        dajax.add_data('You cannot book for past','bootbox.alert')
    elif event == "":
        dajax.add_data('Please enter Event name!!','bootbox.alert')
    elif add_info == "":
        dajax.add_data('Please enter additional information!!','bootbox.alert')
    else:
        dajax.add_data('#myModal','hide_modal')
        lock = threading.Lock()
        with lock:
            booking_list=Booked_resource.objects.filter(resource_id=res_id).filter(Q(start_date__gte=now)|Q(end_date__gte=now))
            for r in booking_list:
                u=User.objects.get(username=r.Booked_by)
                profile=UserProfile.objects.get(id=u.id)
                booked_priority=Priority_table.objects.get(Designation=profile.designation).Priority_num
                if  r.start_date != r.end_date:
                    if sel_date >= r.start_date and sel_date <=r.end_date:
                        if allocation_policy == 'PRIOR':
                            if user_priority < booked_priority:
                                overwrite = False
                                break
                            else:
                                overwrite_list.append(r)
                        elif allocation_policy == 'FCFS':
                            book = False
                            break
                elif r.start_date == r.end_date:
                    if sel_date == r.start_date:  
                        if r.all_day_event:   
                            if allocation_policy == 'PRIOR':
                                if user_priority < booked_priority:
                                    overwrite = False
                                    break
                                else:
                                    overwrite_list.append(r)
                            elif allocation_policy == 'FCFS':
                                book = False
                                break
                        elif (start_time >= r.start_time and start_time <=r.end_time) or (end_time >= r.start_time and end_time <= r.end_time):
                            if allocation_policy == 'PRIOR':
                                if user_priority < booked_priority:
                                    overwrite = False
                                    break
                                else:
                                    overwrite_list.append(r)
                            elif allocation_policy == 'FCFS':
                                book = False
                                break
            resource_details=Resource.objects.get(id=res_id)
            if allocation_policy == 'PRIOR':
                if overwrite:
                    if overwrite_list:
                        for r in overwrite_list:
                            booking_del=Booked_resource.objects.get(id=r.id)
                            booking_del.delete()
                        booking=Booked_resource.objects.create(Booked_by=request.user.username,Event_name=event,Purpose_of_booking=add_info,all_day_event=0,start_date=start_date,start_time=start_time.strftime("%H:%M"),end_date=end_date,end_time=end_time.strftime("%H:%M"),resource_id=res_id,resource_name=resource_details.name,resource_type=resource_details.type)
                        booking.save()
                        dajax.add_data({ 'message':'{0} has been booked by overwriting successfully'.format(resource_name),'location':'/booking/'},'bootbox_alert')
                    else:
                        booking=Booked_resource.objects.create(Booked_by=request.user.username,Event_name=event,Purpose_of_booking=add_info,all_day_event=0,start_date=start_date,start_time=start_time.strftime("%H:%M"),end_date=end_date,end_time=end_time.strftime("%H:%M"),resource_id=res_id,resource_name=resource_details.name,resource_type=resource_details.type)
                        booking.save()
                        dajax.add_data({ 'message':'{0} has been booked successfully'.format(resource_name), 'location':'/booking/'},'bootbox_alert')
                else:
                    dajax.add_data("Sorry overwriting booked {0} is not possible. Kindly choose some other date/time/resource".format(resource_name),'bootbox.alert')
            elif allocation_policy == 'FCFS':
                if book:
                    booking=Booked_resource.objects.create(Booked_by=request.user.username,Event_name=event,Purpose_of_booking=add_info,all_day_event=0,start_date=start_date,start_time=start_time.strftime("%H:%M"),end_date=end_date,end_time=end_time.strftime("%H:%M"),resource_id=res_id,resource_name=resource_details.name,resource_type=resource_details.type)
                    booking.save()
                    dajax.add_data({'message':'{0} has been booked successfully'.format(resource_name), 'location':'/booking/'}, 'bootbox_alert')
                else:
                    dajax.add_data("Sorry {0} is not free. Kindly choose some other date/time/resource".format(resource_name),'bootbox.alert')
    return dajax.json()


@dajaxice_register()    
def book_all_day_event(request,event,add_info,start_date,end_date,start_hour,start_min,end_hour,end_min,res_id,verify_list):
    dajax=Dajax()
    end_hour=int(end_hour)
    end_min=int(end_min)
    start_hour=int(start_hour)
    start_min=int(start_min)
    overwrite_list = []
    overwrite = True
    book = True
    resource_name=Resource.objects.get(id=res_id).name
    now = datetime.now().date()
    sel_date,start_time,end_time = None,None,None 
    try:
        sel_date = datetime.strptime(start_date,"%Y-%m-%d").date()
    except:
        dajax.add_data("Date not choosen",'bootbox.alert')
        return dajax.json()
    try:
        end_time=time(int(end_hour),int(end_min))
        start_time = time(int(start_hour),int(start_min))
    except:
        dajax.add_data("Please select correct time",'bootbox.alert') 
        return dajax.json() 
    allocation_policy=Resource.objects.get(id=res_id).allocation_policy # This query fetches the allocation policy of the selected resource
    user_desg=UserProfile.objects.get(id=request.user.id) # This query gets the user designation
    user_priority=Priority_table.objects.get(Designation=user_desg.designation).Priority_num # This query gets the priority number of user
    if sel_date <= now:
        dajax.add_data("You cannot book for past.",'bootbox.alert')
    elif end_time<=start_time:
        dajax.add_data('Incorrect time input','bootbox.alert')
    elif event == "":
        dajax.add_data('Please enter Event name!!','bootbox.alert')
    elif add_info == "":
        dajax.add_data('Please enter additional information!!','bootbox.alert')
    else:
        dajax.add_data('#myModal','hide_modal')
        lock = threading.Lock()
        with lock:
            booking_list=Booked_resource.objects.filter(resource_id=res_id).filter(Q(start_date__gte=now)|Q(end_date__gte=now))
            for r in booking_list:
                u=User.objects.get(username=r.Booked_by)
                profile=UserProfile.objects.get(id=u.id)
                booked_priority=Priority_table.objects.get(Designation=profile.designation).Priority_num

                if  r.start_date != r.end_date:
                    #dajax.alert('Multiple date')
                    if (sel_date >= r.start_date and sel_date <=r.end_date):
                        #dajax.alert('M overlap')
                        if(allocation_policy == 'PRIOR'):
                            overwrite_list.append(r)
                            if user_priority < booked_priority:
                                overwrite = False
                                break
                        else:
                            book = False
                            break
                elif r.start_date == r.end_date:
                    if sel_date == r.start_date:     
                        if(allocation_policy == 'PRIOR'):
                            overwrite_list.append(r)
                            if user_priority < booked_priority:
                                overwrite = False
                        elif allocation_policy == 'FCFS':
                            book = False
                            break
            resource_details=Resource.objects.get(id=res_id)
            if allocation_policy == 'PRIOR':
                if overwrite:
                    if overwrite_list:
                        for r in overwrite_list:
                            booking_del=Booked_resource.objects.get(id=r.id)
                            booking_del.delete()
                        booking=Booked_resource.objects.create(Booked_by=request.user.username,Event_name=event,Purpose_of_booking=add_info,all_day_event=1,start_date=start_date,start_time=start_time.strftime("%H:%M"),end_date=end_date,end_time=end_time.strftime("%H:%M"),resource_id=res_id,resource_name=resource_details.name,resource_type=resource_details.type)
                        booking.save()
                        dajax.add_data({ 'message':'{0} has been booked by overwriting successfully'.format(resource_name),'location':'/booking/'},'bootbox_alert')
                    else:
                        booking=Booked_resource.objects.create(Booked_by=request.user.username,Event_name=event,Purpose_of_booking=add_info,all_day_event=1,start_date=start_date,start_time=start_time.strftime("%H:%M"),end_date=end_date,end_time=end_time.strftime("%H:%M"),resource_id=res_id,resource_name=resource_details.name,resource_type=resource_details.type)
                        booking.save()
                        dajax.add_data({ 'message':'{0} has been booked successfully'.format(resource_name), 'location':'/booking/'},'bootbox_alert')
                else:
                    dajax.add_data("Sorry overwriting booked {0} is not possible. Kindly choose some other date/time/resource".format(resource_name),'bootbox.alert')
            elif allocation_policy == 'FCFS':
                if book:
                    booking=Booked_resource.objects.create(Booked_by=request.user.username,Event_name=event,Purpose_of_booking=add_info,all_day_event=1,start_date=start_date,start_time=start_time.strftime("%H:%M"),end_date=end_date,end_time=end_time.strftime("%H:%M"),resource_id=res_id,resource_name=resource_details.name,resource_type=resource_details.type)
                    booking.save()
                    dajax.add_data({'message':'{0} has been booked successfully'.format(resource_name), 'location':'/booking/'}, 'bootbox_alert')
                else:
                    dajax.add_data("Sorry {0} is not free. Kindly choose some other date/time/resource".format(resource_name),'bootbox.alert')
    return dajax.json()