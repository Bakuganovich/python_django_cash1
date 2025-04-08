from django.core.management.base import BaseCommand
from django.urls import get_resolver

class Command(BaseCommand):
    help = "Вывести все зарегистрированные URL"

    def handle(self, *args, **kwargs):
        resolver = get_resolver()
        all_urls = self.get_urls(resolver.url_patterns)

        for url in all_urls:
            self.stdout.write(url)

    def get_urls(self, patterns, base=''):
        """Рекурсивно собираем все URL"""
        urls = []
        for pattern in patterns:
            if hasattr(pattern, 'url_patterns'):  # Это include()
                urls += self.get_urls(pattern.url_patterns, base + str(pattern.pattern))
            else:  # Это конкретный маршрут
                urls.append(base + str(pattern.pattern))
        return urls

# user/login/
# user/registration/
# user/profile/
# user/logout/
# user/profile_student/
# user/approvall/
# schedule/
# scheduledit/
# scheduledit/timetable_add/
# scheduledit/timetable_delete/
# scheduledit/detailed/