from django.shortcuts import render
from django.views.generic import View
from django_project.settings import MEDIA_URL
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.db.models import Q

from .models import CourseOrg, CityDict, Teacher
from .forms import UserAskForm
from courses.models import Course
from operations.models import UserFavorite

# Create your views here.
class OrgView(View):
    """
    课程机构列表
    """
    def get(self, request):
        city_id = request.GET.get('city', '')
        category = request.GET.get('ct', '')
        sort = request.GET.get('sort', '')
        all_orgs = CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by("-click_nums")[:3]

        #机构搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) |
                                       Q(desc__icontains=search_keywords)
                                       )

        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))
        if category:
            all_orgs = all_orgs.filter(catgory=category)
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("course_nums")

        org_nums = all_orgs.count()
        all_citys = CityDict.objects.all()

        #分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        #第二个的参数为每页显示多少数量
        p = Paginator(all_orgs, 10, request=request)
        orgs = p.page(page)

        return render(request, "org-list.html", {
            "all_orgs": orgs,
            "all_citys": all_citys,
            "org_nums": org_nums,
            "MEDIA_URL": MEDIA_URL,
            "city_id": city_id,
            "category": category,
            "hot_orgs": hot_orgs,
            "sort": sort,
        })


class AddUserAskView(View):
    """
    用户咨询
    """
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            #userask_form = userask_form.save(commit=True)
            userask_form.save(commit=True)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'fail', 'msg': '添加出错'})


class OrgHomeView(View):
    """
    机构首页
    """
    def get(self, request, org_id):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))
        #判断用户是否收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_coures = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {
            'all_coures': all_coures,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })


class OrgCourseView(View):
    """
    机构课程列表页
    """
    def get(self, request, org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()
        all_coures = course_org.course_set.all()
        #判断用户是否收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-course.html', {
            'all_coures': all_coures,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })


class OrgDescView(View):
    """
    机构介绍页
    """
    def get(self, request, org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))
        #判断用户是否收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })


class OrgTeacherView(View):
    """
    教师列表页
    """
    def get(self, request, org_id):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teacher = course_org.teacher_set.all()
        #判断用户是否收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=3):
                has_fav = True
        return render(request, 'org-detail-teachers.html', {
            'all_teacher': all_teacher,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })


class AddFavView(View):
    """
    用户收藏以及取消
    """
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        #判断用户是否登录
        if not request.user.is_authenticated():
            return JsonResponse({'status': 'fail', 'msg': '用户未登录'})

        #判断收藏记录是否存在
        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            exist_records.delete()
            # fav_nums 自减
            if int(fav_type) == 1:
                temp_object = Course.objects.filter(id=int(fav_id))
            elif int(fav_type) == 2:
                temp_object = CourseOrg.objects.filter(id=int(fav_id))
            elif int(fav_type) == 3:
                temp_object = Teacher.objects.filter(id=int(fav_id))
            temp_object.fav_nums -= 1
            if temp_object.fav_nums < 0:
                temp_object.fav_nums = 0
            temp_object.save()

            return JsonResponse({'status': 'fail', 'msg': '收藏'})
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_id) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                # fav_nums 自增
                if int(fav_type) == 1:
                    temp_object = Course.objects.filter(id=int(fav_id))
                elif int(fav_type) == 2:
                    temp_object = CourseOrg.objects.filter(id=int(fav_id))
                elif int(fav_type) == 3:
                    temp_object = Teacher.objects.filter(id=int(fav_id))
                temp_object.fav_nums += 1
                temp_object.save()
                return JsonResponse({'status': 'success', 'msg': '收藏成功'})
            else:
                return JsonResponse({'status': 'fail', 'msg': '收藏出错'})


class TeacherListView(View):
    """
    课程讲师列表页
    """
    def get(self, request):
        all_teachers = Teacher.objects.all()

        #讲师搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_teachers = all_teachers.filter(Q(name__icontains=search_keywords) |
                                               Q(work_company__icontains=search_keywords) |
                                               Q(work_position__icontains=search_keywords))

        sort = request.GET.get('sort', "")
        if sort:
            if sort == "hot":
                all_teachers = all_teachers.order_by("-click_nums")

        sorted_teacher = Teacher.objects.all().order_by("-click_nums")[:3]

        #分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        #第二个的参数为每页显示多少数量
        p = Paginator(all_teachers, 10, request=request)
        teachers = p.page(page)

        return render(request, 'teachers-list.html', {
            'all_teachers': teachers,
            'sort': sort,
            'sorted_teacher': sorted_teacher
        })


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        all_courses = Course.objects.filter(teacher=teacher)
        teacher.click_nums += 1
        teacher.save()

        has_teacher_faved = False
        if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
            has_teacher_faved = True

        has_org_faved = False
        if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
            has_org_faved = True

        sorted_teacher = Teacher.objects.all().order_by("-click_nums")[:3]
        return render(request, 'teacher-detail.html', {
            'teacher': teacher,
            'all_courses': all_courses,
            'sorted_teacher': sorted_teacher,
            'has_teacher_faved': has_teacher_faved,
            'has_org_faved': has_org_faved
        })