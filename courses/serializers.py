from rest_framework import serializers

from courses.models import Course, Lesson, Payment


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lesson = LessonSerializer(many=True)

    class Meta:
        model = Course
        fields = '__all__'

    def get_lesson_count(self, obj):
        return Lesson.objects.filter(course=obj).count()


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'

