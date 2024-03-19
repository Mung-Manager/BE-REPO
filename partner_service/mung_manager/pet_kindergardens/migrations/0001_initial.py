# Generated by Django 4.2.11 on 2024-03-14 22:14

import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PetKindergarden',
            fields=[
                ('id', models.AutoField(auto_created=True, db_column='pet_kindergarden_id', primary_key=True, serialize=False, verbose_name='펫 유치원 아이디')),
                ('name', models.CharField(max_length=64, verbose_name='유치원 이름')),
                ('main_thumbnail_url', models.URLField(verbose_name='메인 썸네일')),
                ('profile_thumbnail_url', models.URLField(verbose_name='프로필 이미지')),
                ('phone_number', models.CharField(max_length=16, verbose_name='전화번호')),
                ('visible_phone_number', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=16), size=2, verbose_name='노출 전화번호')),
                ('business_hours', models.CharField(max_length=64, verbose_name='영업 시간')),
                ('road_address', models.CharField(max_length=128, verbose_name='도로명 주소')),
                ('abbr_address', models.CharField(max_length=128, verbose_name='지번 주소')),
                ('short_address', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=128), size=10, verbose_name='간단 주소')),
                ('guide_message', models.TextField(verbose_name='안내 메시지')),
                ('latitude', models.DecimalField(decimal_places=10, max_digits=13, verbose_name='위도')),
                ('longitude', models.DecimalField(decimal_places=10, max_digits=13, verbose_name='경도')),
                ('point', django.contrib.gis.db.models.fields.PointField(srid=4326, verbose_name='위치 좌표')),
                ('reservation_available_option', models.CharField(max_length=64, verbose_name='예약 가능 옵션')),
                ('reservation_cancle_option', models.CharField(max_length=64, verbose_name='예약 취소 옵션')),
                ('daily_pet_limit', models.SmallIntegerField(verbose_name='일일 펫 제한')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성 일시')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정 일시')),
            ],
            options={
                'verbose_name': 'pet kindergarden',
                'verbose_name_plural': 'pet kindergarden',
                'db_table': 'pet_kindergarden',
            },
        ),
    ]