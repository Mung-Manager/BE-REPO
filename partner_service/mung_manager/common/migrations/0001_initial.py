# Generated by Django 4.2.11 on 2024-03-16 23:38

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeletedRecord',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='삭제된 레코드 아이디')),
                ('original_table', models.CharField(max_length=256, verbose_name='원본 테이블')),
                ('original_id', models.IntegerField(verbose_name='원본 아이디')),
                ('data', models.JSONField(verbose_name='원본 데이터')),
                ('deleted_at', models.DateTimeField(auto_now_add=True, verbose_name='삭제 시간')),
            ],
            options={
                'verbose_name': 'deleted record',
                'verbose_name_plural': 'deleted records',
                'db_table': 'deleted_record',
            },
        ),
    ]
