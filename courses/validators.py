from rest_framework.serializers import ValidationError


class UrlValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_value = dict(value).get(self.field)
        if tmp_value is not None and 'youtube.com' not in tmp_value:
            raise ValidationError('Некорректная ссылка.')

