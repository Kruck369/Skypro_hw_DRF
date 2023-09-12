from rest_framework.pagination import PageNumberPagination


class CourseAndLessonPaginator(PageNumberPagination):
    page_size = 10
