from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import(
	Volunteer,
	Student,
	Schedule,
	Volunteer_schedule,
	Student_schedule,
	Cw_hw,
	Calendar,
	Volunteer_attended_on,
	Student_attended_on,
)
from django.http import HttpResponse
from datetime import datetime, date

# Create your views here.
def index(request):
	if request.user.is_authenticated:
		return redirect('dashboard')
	return render(request, 'home/index.html')

def dashboard(request):
	if request.user.is_authenticated:
		email = request.user

		if not Volunteer.objects.filter(email=email).exists():
			return redirect('set_profile')

		volun = Volunteer.objects.get(email=email)
		
		if request.method == 'POST':
			if request.POST.get('submit') == 'class-info':
				class_info_date_str		= request.POST['class-info-date']
				class_info_section		= request.POST['class-info-section']
				
				class_info_date = datetime.strptime(class_info_date_str, '%Y-%m-%d').date()
				class_info_day = class_info_date.strftime("%A")

				calendar = Calendar.objects.filter(date = class_info_date)
				if calendar.exists():
					if calendar[0].class_scheduled is True:
						schedule = Schedule.objects.filter(day = class_info_day, section = class_info_section)
						if schedule.exists():
							if class_info_date > date.today():
								students_attended = "Class not yet scheduled!"
								vol_volunteered = "Class not yet scheduled!"
							else:
								students_attended = Student_attended_on.objects.filter(date = calendar[0])
								vol_volunteered = Volunteer_attended_on.objects.filter(date = calendar[0])

								if class_info_date == date.today() and not students_attended.exists():
									students_attended = "Not yet updated!"
								elif not students_attended.exists():
									students_attended = "No student present."

								if class_info_date == date.today() and not vol_volunteered.exists():
									vol_volunteered = "Not yet updated!"
								elif not vol_volunteered.exists():
									vol_volunteered = "No volunteers were present."

							cw_hw = Cw_hw.objects.filter(date = class_info_date, section = schedule[0])
							if cw_hw.exists():
								context = {
									#dash-main
									'schedule' : schedule,
									'students_attended' : students_attended,
									'vol_volunteered' : vol_volunteered,
									'cw_hw' : cw_hw[0],
									'selected_date' : class_info_date,
									'selected_schedule' : class_info_section,
									'choices': Schedule.SECTION,

									#dash-update
									'last_4_year': datetime.now().year - 4,

									#dash-schedule
									'day': Schedule.DAY,
									'section': Schedule.SECTION,

									#dash-vol-att
									'today_date' : date.today(),
									'today_volun' : Volunteer_schedule.objects.filter(day=date.today().strftime("%A")),

									#dash-atu-att
									'today_stu' : Student_schedule.objects.filter(day=date.today().strftime("%A")),
								}
								return render(request, 'home/dashboard.html', context)
							else:
								context = {
									#dash-main
									'schedule' : schedule,
									'students_attended' : students_attended,
									'vol_volunteered' : vol_volunteered,
									'cw_hw' : {
										'cw' : "Not yet updated!",
										'hw' : "Not yet updated!",
									},
									'selected_date' : class_info_date,
									'selected_schedule' : class_info_section,
									'choices': Schedule.SECTION,

									#dash-update
									'last_4_year': datetime.now().year - 4,

									#dash-schedule
									'day': Schedule.DAY,
									'section': Schedule.SECTION,

									#dash-vol-att
									'today_date' : date.today(),
									'today_volun' : Volunteer_schedule.objects.filter(day=date.today().strftime("%A")),

									#dash-atu-att
									'today_stu' : Student_schedule.objects.filter(day=date.today().strftime("%A")),
								}
								return render(request, 'home/dashboard.html', context)
						else:
							context = {
								#dash-main
								'no_schedule_found' : "yup!",
								'selected_date' : class_info_date,
								'selected_schedule' : class_info_section,
								'choices': Schedule.SECTION,

								#dash-update
								'last_4_year': datetime.now().year - 4,

								#dash-schedule
								'day': Schedule.DAY,
								'section': Schedule.SECTION,

								#dash-vol-att
								'today_date' : date.today(),
								'today_volun' : Volunteer_schedule.objects.filter(day=date.today().strftime("%A")),

								#dash-atu-att
								'today_stu' : Student_schedule.objects.filter(day=date.today().strftime("%A")),
							}
							return render(request, 'home/dashboard.html', context)  # The chosen section is not taught on the chosen day
					else:
						context = {
							#dash-main
							'calendar' : calendar[0],
							'no_class_scheduled' : "haan",
							'selected_date' : class_info_date,
							'selected_schedule' : class_info_section,
							'choices': Schedule.SECTION,

							#dash-update
							'last_4_year': datetime.now().year - 4,

							#dash-schedule
							'day': Schedule.DAY,
							'section': Schedule.SECTION,

							#dash-vol-att
							'today_date' : date.today(),
							'today_volun' : Volunteer_schedule.objects.filter(day=date.today().strftime("%A")),

							#dash-atu-att
							'today_stu' : Student_schedule.objects.filter(day=date.today().strftime("%A")),
						}
						return render(request, 'home/dashboard.html', context)
				else:
					context = {
						#dash-main
						'no_class_found' : "bilkul_nhi",
						'selected_date' : class_info_date,
						'selected_schedule' : class_info_section,
						'choices': Schedule.SECTION,

						#dash-update
						'last_4_year': datetime.now().year - 4,

						#dash-schedule
						'day': Schedule.DAY,
						'section': Schedule.SECTION,

						#dash-vol-att
						'today_date' : date.today(),
						'today_volun' : Volunteer_schedule.objects.filter(day=date.today().strftime("%A")),

						#dash-atu-att
						'today_stu' : Student_schedule.objects.filter(day=date.today().strftime("%A")),
					}
					return render(request, 'home/dashboard.html', context)
			elif request.POST.get('submit') == 'update-profile':
				roll_no         = request.POST['roll_no']
				first_name      = request.POST['first_name']
				last_name       = request.POST['last_name']
				gender          = request.POST['gender']
				alt_email       = request.POST['alt_email']
				batch           = request.POST['batch']
				programme       = request.POST['programme']
				street_address1 = request.POST['street_address1']
				street_address2 = request.POST['street_address2']
				pincode         = request.POST['pincode']
				city            = request.POST['city']
				state           = request.POST['state']
				dob             = request.POST['dob']
				contact_no      = request.POST['contact_no']

				update_error = ""
				toast = ""
				if roll_no:
					if volun.roll_no != roll_no:
						duplicate_roll_check = Volunteer.objects.filter(roll_no = roll_no)
						if duplicate_roll_check.exists():
							update_error = "A volunteer with entered roll no. already exists."
							toast = "Profile update failed!"
						else:
							volun.roll_no = roll_no
				if first_name:
					volun.first_name = first_name
				if last_name:
					volun.last_name = last_name
				volun.gender = gender
				volun.batch = batch
				volun.programme = programme
				volun.dob = dob
				if contact_no:
					volun.contact_no = contact_no
				if alt_email:
					volun.alt_email = alt_email
				if street_address1:
					volun.street_address1 = street_address1
				if street_address2:
					volun.street_address2 = street_address2
				if city:
					volun.city = city
				if state:
					volun.state = state
				if pincode:
					volun.pincode = pincode

				if update_error == "":
					volun.save()
					toast = "Profile updated Successfully!"


				context = {
					#dash-main
					'class_info_submitted' : "nooooo!",
					'choices': Schedule.SECTION,

					#dash-update
					'update_error' : update_error,
					'last_4_year': datetime.now().year - 4,
					'toast': toast,

					#dash-schedule
					'day': Schedule.DAY,
					'section': Schedule.SECTION,

					#dash-vol-att
					'today_date' : date.today(),
					'today_volun' : Volunteer_schedule.objects.filter(day=date.today().strftime("%A")),

					#dash-atu-att
					'today_stu' : Student_schedule.objects.filter(day=date.today().strftime("%A")),
				}
				return render(request, 'home/dashboard.html', context)
			elif request.POST.get('submit') == 'update-schedule':
				day			= request.POST['day']
				section		= request.POST['section']

				schedules = Schedule.objects.filter(day = day, section = section)

				if schedules.exists():
					volun_schedules = Volunteer_schedule.objects.filter(roll_no = volun)
					if volun_schedules.exists():
						volun_schedule = volun_schedules[0]
						volun_schedule.schedule = schedules[0]
					else:
						volun_schedule = Volunteer_schedule(roll_no = volun, schedule = schedules[0])
					volun_schedule.save()

					context = {
						#dash-main
						'class_info_submitted' : "nopes",
						'choices': Schedule.SECTION,

						#dash-update
						'last_4_year': datetime.now().year - 4,

						#dash-schedule
						'toast' : "Schedule updated successfully!",
						'day': Schedule.DAY,
						'section': Schedule.SECTION,
					}
					return render(request, 'home/dashboard.html', context)

				else:
					context = {
						#dash-main
						'class_info_submitted' : "nopes",
						'choices': Schedule.SECTION,

						#dash-update
						'last_4_year': datetime.now().year - 4,

						#dash-schedule
						'sch_error' : "Selected schedule doesn't exists. Kindly refer to the Schedule.",
						'toast' : "Failed to update schedule!",
						'day': Schedule.DAY,
						'section': Schedule.SECTION,
					}
					return render(request, 'home/dashboard.html', context)
			elif request.POST.get('submit') == 'cwhw-date':
				cwhw_date_str = request.POST['date']

				cwhw_date = datetime.strptime(cwhw_date_str, '%Y-%m-%d').date()
				cwhw_day = cwhw_date.strftime("%A")

				calendar_date = Calendar.objects.filter(date = cwhw_date)

				if calendar_date.exists():
					context = {
						#dash-main
						'class_info_submitted' : "nopes",
						'choices': Schedule.SECTION,

						#dash-update
						'last_4_year': datetime.now().year - 4,

						#dash-cwhw
						'cwhw_selected_date' : cwhw_date,
						'cwhw_section': Schedule.objects.filter(day=cwhw_day),

						#dash-vol-att
						'today_date' : date.today(),
						'today_volun' : Volunteer_schedule.objects.filter(day=date.today().strftime("%A")),

						#dash-atu-att
						'today_stu' : Student_schedule.objects.filter(day=date.today().strftime("%A")),
					}
					return render(request, 'home/dashboard.html', context)
				else:
					context = {
						#dash-main
						'class_info_submitted' : "nopes",
						'choices': Schedule.SECTION,

						#dash-update
						'last_4_year': datetime.now().year - 4,

						#dash-cwhw
						'cwhw_selected_date' : cwhw_date,
						'cwhw_error' : "The chosen day is not yet updated in the Calender.",

						#dash-vol-att
						'today_date' : date.today(),
						'today_volun' : Volunteer_schedule.objects.filter(day=date.today().strftime("%A")),

						#dash-atu-att
						'today_stu' : Student_schedule.objects.filter(day=date.today().strftime("%A")),
					}
					return render(request, 'home/dashboard.html', context)
			elif request.POST.get('submit') == 'update-cwhw':
				cwhw_date_str			= request.POST['date']
				cwhw_selected_date_str	= request.POST['selected-date']
				cwhw_section			= request.POST['section']
				cw						= request.POST['cw']
				hw						= request.POST['hw']

				cwhw_date = datetime.strptime(cwhw_date_str, '%Y-%m-%d').date()
				cwhw_day = cwhw_date.strftime("%A")

				cwhw_selected_date = datetime.strptime(cwhw_selected_date_str, '%Y-%m-%d').date()

				if cwhw_selected_date == cwhw_date:
					cal_date = Calendar.objects.get(date = cwhw_date)
					sch_section = Schedule.objects.get(day=cwhw_day, section=cwhw_section)

					if Cw_hw.objects.filter(date=cal_date, section=sch_section).exists():
						cw_hw = Cw_hw.objects.get(date=cal_date, section=sch_section)
						if cw:
							cw_hw.cw = cw
						if hw:
							cw_hw.hw = hw
						cw_hw.save()
					else:
						cw_hw = Cw_hw(date=cal_date, section=sch_section, cw=cw, hw=hw)
						cw_hw.save()

					context = {
						#dash-main
						'class_info_submitted' : "nopes",
						'choices': Schedule.SECTION,

						#dash-update
						'last_4_year': datetime.now().year - 4,

						#dash-cwhw
						'toast' : "CW_HW update successful!",

						#dash-vol-att
						'today_date' : date.today(),
						'today_volun' : Volunteer_schedule.objects.filter(day=date.today().strftime("%A")),

						#dash-atu-att
						'today_stu' : Student_schedule.objects.filter(day=date.today().strftime("%A")),
					}
					return render(request, 'home/dashboard.html', context)
				else:
					context = {
						#dash-main
						'class_info_submitted' : "nopes",
						'choices': Schedule.SECTION,

						#dash-update
						'last_4_year': datetime.now().year - 4,

						#dash-cwhw
						'cwhw_selected_date' : cwhw_date,
						'cwhw_error' : "You've changed the date! Kindly submit the chosen date before updating.",
						'toast' : "CW_HW update failed!",

						#dash-vol-att
						'today_date' : date.today(),
						'today_volun' : Volunteer_schedule.objects.filter(day=date.today().strftime("%A")),

						#dash-atu-att
						'today_stu' : Student_schedule.objects.filter(day=date.today().strftime("%A")),
					}
					return render(request, 'home/dashboard.html', context)
			elif request.POST.get('submit') == 'vol-att':
				today_date = Calendar.objects.get(date=date.today())
				vol_array = request.POST.getlist('volunteered')
				for i in vol_array:
					roll_no = Volunteer.objects.get(roll_no=i) #i is first column of volun_array
					vol_attendance = Volunteer_attended_on(roll_no = roll_no, date = today_date)
					vol_attendance.save()
				
				context = {
					#dash-main
					'class_info_submitted' : "nopes",
					'choices': Schedule.SECTION,

					#dash-update
					'last_4_year': datetime.now().year - 4,

					#dash-vol-att
					'today_date' : date.today(),
					'today_volun' : Volunteer_schedule.objects.filter(day=date.today().strftime("%A")),
					'toast' : "Attendence marked successfully!",

					#dash-atu-att
					'today_stu' : Student_schedule.objects.filter(day=date.today().strftime("%A")),
				}
				return render(request, 'home/dashboard.html', context)
			elif request.POST.get('submit') == 'stu-att':
					today_date = Calendar.objects.get(date=date.today())
					stu_array = request.POST.getlist('attended')
					for sid in stu_array:
						stu = Student.objects.get(id=sid)
						stu_attendance = Student_attended_on(sid = stu, date = today_date)
						stu_attendance.save()
					
					context = {
						#dash-main
						'class_info_submitted' : "nopes",
						'choices': Schedule.SECTION,

						#dash-update
						'last_4_year': datetime.now().year - 4,

						#dash-vol-att
						'today_date' : date.today(),
						'today_volun' : Volunteer_schedule.objects.filter(day=date.today().strftime("%A")),

						#dash-atu-att
						'today_stu' : Student_schedule.objects.filter(day=date.today().strftime("%A")),
						'toast' : "Attendence marked successfully!",

					}
					return render(request, 'home/dashboard.html', context)

		else:
			context = {
				#dash-main
				'class_info_submitted' : "nopes",
				'choices': Schedule.SECTION,

				#dash-update
				'last_4_year': datetime.now().year - 4,

				#dash-schedule
				'day': Schedule.DAY,
				'section': Schedule.SECTION,

				#dash-vol-att
				'today_date' : date.today(),
				'today_volun' : Volunteer_schedule.objects.filter(day=date.today().strftime("%A")),

				#dash-atu-att
				'today_stu' : Student_schedule.objects.filter(day=date.today().strftime("%A")),
			}
			return render(request, 'home/dashboard.html', context)
	return redirect('home')

def volunteerInformation(request):
	if request.user.is_authenticated:
		schedules = Schedule.objects.all()
		email = request.user
		if Volunteer.objects.filter(email=email).exists():
			return redirect('dashboard')
		if request.method == 'POST':
			# roll = str(email)
			# rollnum = roll.split('@')[0]
			roll_no         = request.POST['roll_no']
			first_name      = request.POST['first_name']
			last_name       = request.POST['last_name']
			gender          = request.POST['gender']
			alt_email       = request.POST['alt_email']
			batch           = request.POST['batch']
			programme       = request.POST['programme']
			street_address1 = request.POST['street_address1']
			street_address2 = request.POST['street_address2']
			pincode         = request.POST['pincode']
			city            = request.POST['city']
			state           = request.POST['state']
			dob             = request.POST['dob']
			contact_no      = request.POST['contact_no']
			# sch_id          = request.POST['schedule']
			# sch_day         = Schedule.objects.get(id = sch_id).day
			vol_obj = Volunteer(
				email           = email,
				roll_no         = roll_no,
				first_name      = first_name,
				last_name       = last_name,
				gender          = gender,
				city            = city,
				state           = state,
				dob             = dob,
				contact_no      = contact_no,
				pincode         = pincode,
				programme       = programme,
				batch           = batch,
				alt_email       = alt_email,     
				street_address1 = street_address1,
				street_address2 = street_address2,
			)
			vol_obj.save()
			# sch_obj = Volunteer_schedule(
			# 	roll_no         = Volunteer.objects.get(roll_no = roll_no),
			# 	day             = sch_day,
			# 	schedule        = Schedule.objects.get(id = sch_id),
			# )
			
			# sch_obj.save()
			
			return redirect('dashboard')
		
		return render(request, 'home/set_profile.html', {
			'cur_year': datetime.now().year - 4,
			# 'schedule': schedules,
			})
	else:
		return redirect('login_signup')

		