from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.db.models import Q

from .models import Course, CourseResource
from operations.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by("-add_time")
        hot_courses = Course.objects.all().order_by("-click_nums")[:3]

        #课程搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords) |
                                             Q(desc__icontains=search_keywords) |
                                             Q(detail__icontains=search_keywords))

        #排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")
        #分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        #第二个的参数为每页显示多少数量
        p = Paginator(all_courses, 6, request=request)
        courses = p.page(page)

        return render(request, 'course-list.html', {
            'all_courses': courses,
            'sort': sort,
            'hot_courses': hot_courses,
        })


class CourseDetailView(View):
    """
    课程详情页
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        has_fav_course = False
        has_fav_org = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        #相关课程推荐
        tag = course.tag
        if tag:
            relate_coures = Course.objects.filter(tag=tag)[:1]
        else:
            relate_coures = []

        return render(request, "course-detail.html", {
            'course': course,
            'relate_coures': relate_coures,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org
        })


class CourseInfoView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()
        all_resources = CourseResource.objects.filter(course=course)

        #查询用户是否已经关联该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_courses = UserCourse(user=request.user, course=course)
            user_courses.save()

        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]    #跟该课程有关的用户
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)   #这些用户涉及到的课程
        # 取出课程id(并排除当前id)
        course_ids = []
        for user_course in all_user_courses:
            if user_course.course.id != int(course_id):
                course_ids.append(user_course.course.id)

        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]   #取出相关课程
        return render(request, "course-video.html", {
            'course': course,
            "course_resources": all_resources,
            'relate_courses': relate_courses
        })


class CommentsView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.filter(course=course)

        #查询用户是否已经关联该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_courses = UserCourse(user=request.user, course=course)
            user_courses.save()

        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]    #跟该课程有关的用户
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)   #这些用户涉及到的课程
        # 取出课程id(并排除当前id)
        course_ids = []
        for user_course in all_user_courses:
            if user_course.course.id != int(course_id):
                course_ids.append(user_course.course.id)

        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]   #取出相关课程

        return render(request, "course-comment.html", {
            'course': course,
            'course_resources': all_resources,
            'all_comments': all_comments,
            'relate_courses': relate_courses
        })


class AddComentsView(View):
    """
    添加评论
    """
    def post(self, request):
        if not request.user.is_authenticated():
            return JsonResponse({"status": "fail", "msg": "用户未登录"})

        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "")
        if int(course_id) > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return JsonResponse({"status": "success", "msg": "添加成功"})
        else:
            return JsonResponse({"status": "fail", "msg": "添加失败"})
