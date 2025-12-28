from django.core.management.base import BaseCommand
from products.models import Category

DEFAULT_CATEGORIES = [
    ('دیجیتالی', 'لوازم الکترونیکی و دیجیتال'),
    ('غذا', 'مواد غذایی و خوراکی‌ها'),
    ('خوراکی', 'تنقلات و مواد خوراکی'),  # در صورت نیاز می‌توان حذف یا ادغام کرد
    ('پوشاک', 'لباس و پوشاک'),
    ('خانه و آشپزخانه', 'لوازم خانه و آشپزخانه'),
    ('بهداشتی', 'محصولات بهداشتی و مراقبت شخصی'),
    ('زیبایی و سلامت', 'محصولات آرایشی و مراقبت پوست'),
]

class Command(BaseCommand):
    help = 'Create default product categories'

    def handle(self, *args, **options):
        created = 0
        for name, desc in DEFAULT_CATEGORIES:
            obj, created_flag = Category.objects.get_or_create(name=name, defaults={'description': desc})
            if created_flag:
                created += 1
                self.stdout.write(self.style.SUCCESS(f'Created category: {name}'))
            else:
                self.stdout.write(f'Already exists: {name}')
        self.stdout.write(self.style.SUCCESS(f'Done. Created {created} new categories.'))