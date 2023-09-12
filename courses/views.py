from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from courses.paginators import CourseAndLessonPaginator
from courses.permissions import IsModerator, IsOwner, CoursesPermissions, IsModeratorOrIsOwner

from courses.models import Course, Lesson, Payment, Subscription
from courses.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionSerializer


class CoursesViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [CoursesPermissions]
    pagination_class = CourseAndLessonPaginator

    @action(detail=True, methods=['POST'], serializer_class=SubscriptionSerializer)
    def subscribe(self, request, pk=None):
        course = self.get_object()
        serializer = SubscriptionSerializer(data={'user': request.user.id, 'course': course.id})

        if serializer.is_valid():
            subscription_exists = Subscription.objects.filter(user=request.user, course=course).exists()

            if subscription_exists:
                return Response({'detail': 'Пользователь уже подписан на этот курс'}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response({'detail': 'Подписка установлена успешно'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['DELETE'])
    def unsubscribe(self, request, pk=None):
        course = self.get_object()

        subscription_exists = Subscription.objects.filter(user=request.user, course=course).exists()

        if not subscription_exists:
            return Response({'detail': 'Пользователь не был подписан на этот курс.'},
                            status=status.HTTP_400_BAD_REQUEST)

        Subscription.objects.filter(user=request.user, course=course).delete()

        return Response({'detail': 'Подписка успешно удалена.'}, status=status.HTTP_204_NO_CONTENT)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CourseAndLessonPaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModeratorOrIsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('payed_course', 'payed_lesson', 'payment_method')
    ordering_fields = ('payment_date',)
    permission_classes = [IsModerator]
