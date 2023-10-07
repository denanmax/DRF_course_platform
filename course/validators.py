from rest_framework.exceptions import ValidationError


class LinkValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_value = dict(value).get(self.field)
        if tmp_value and not 'youtube.com' in tmp_value:
            raise ValidationError('Тут должна быть ссылка на юупуп')
