from rest_framework import serializers

from courses.models import Course, Lesson, Payment


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lesson = LessonSerializer(many=True, read_only=True)
    owner = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Course
        fields = '__all__'

    def get_lesson_count(self, obj):
        return Lesson.objects.filter(course=obj).count()

    def save(self, **kwargs):
        if self.instance is None:
            kwargs['owner'] = self.fields['owner'].get_default()
        return super().save(**kwargs)


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'

