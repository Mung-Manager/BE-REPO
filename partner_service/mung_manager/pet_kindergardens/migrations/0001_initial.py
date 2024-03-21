# Generated by Django 4.2.11 on 2024-03-21 15:20

from django.conf import settings
import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PetKindergarden',
            fields=[
                ('id', models.AutoField(auto_created=True, db_column='pet_kindergarden_id', primary_key=True, serialize=False, verbose_name='펫 유치원 아이디')),
                ('name', models.CharField(max_length=64, verbose_name='유치원 이름')),
                ('main_thumbnail_url', models.URLField(verbose_name='메인 썸네일')),
                ('profile_thumbnail_url', models.URLField(verbose_name='프로필 썸네일 이미지')),
                ('phone_number', models.CharField(blank=True, max_length=16, verbose_name='전화번호')),
                ('visible_phone_number', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=16), size=2, verbose_name='노출 전화번호')),
                ('business_hours', models.CharField(max_length=64, verbose_name='영업 시간')),
                ('road_address', models.CharField(max_length=128, verbose_name='도로명 주소')),
                ('abbr_address', models.CharField(max_length=128, verbose_name='지번 주소')),
                ('short_address', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=128), size=10, verbose_name='간단 주소')),
                ('guide_message', models.TextField(blank=True, verbose_name='안내 메시지')),
                ('latitude', models.DecimalField(decimal_places=10, max_digits=13, verbose_name='위도')),
                ('longitude', models.DecimalField(decimal_places=10, max_digits=13, verbose_name='경도')),
                ('point', django.contrib.gis.db.models.fields.PointField(srid=4326, verbose_name='위치 좌표')),
                ('reservation_available_option', models.CharField(choices=[('당일 예약 가능', 'TODAY'), ('1일 전 예약 가능', 'BEFORE_ONE_DAY'), ('2일 전 예약 가능', 'BEFORE_TWO_DAY'), ('3일 전 예약 가능', 'BEFORE_THREE_DAY'), ('4일 전 예약 가능', 'BEFORE_FOUR_DAY'), ('5일 전 예약 가능', 'BEFORE_FIVE_DAY')], max_length=64, verbose_name='예약 가능 옵션')),
                ('reservation_cancle_option', models.CharField(choices=[('당일 취소 가능', 'TODAY'), ('12시간 전 취소 가능', 'BEFORE_TWELVE_HOUR'), ('1일 전 취소 가능', 'BEFORE_ONE_DAY'), ('2일 전 취소 가능', 'BEFORE_TWO_DAY'), ('3일 전 취소 가능', 'BEFORE_THREE_DAY'), ('4일 전 취소 가능', 'BEFORE_FOUR_DAY'), ('5일 전 취소 가능', 'BEFORE_FIVE_DAY')], max_length=64, verbose_name='예약 취소 옵션')),
                ('daily_pet_limit', models.SmallIntegerField(verbose_name='일일 펫 제한')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성 일시')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정 일시')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pet_kindergardens', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'pet kindergarden',
                'verbose_name_plural': 'pet kindergarden',
                'db_table': 'pet_kindergarden',
            },
        ),
        migrations.CreateModel(
            name='RawPetKindergarden',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('thum_url', models.URLField(db_column='thumUrl')),
                ('tel', models.CharField(db_column='tel', max_length=16)),
                ('virtual_tel', models.CharField(blank=True, db_column='virtualTel', max_length=16)),
                ('name', models.CharField(db_column='name', max_length=64)),
                ('x', models.DecimalField(db_column='x', decimal_places=10, max_digits=13)),
                ('y', models.DecimalField(db_column='y', decimal_places=10, max_digits=13)),
                ('business_hours', models.CharField(db_column='businessHours', max_length=64)),
                ('address', models.CharField(db_column='address', max_length=128)),
                ('road_address', models.CharField(db_column='roadAddress', max_length=128)),
                ('abbr_address', models.CharField(db_column='abbrAddress', max_length=128)),
                ('short_address', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=128), db_column='shortAddress', size=10)),
            ],
            options={
                'verbose_name': 'raw pet kindergarden',
                'verbose_name_plural': 'raw pet kindergarden',
                'db_table': 'raw_pet_kindergarden',
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, db_column='ticket_id', primary_key=True, serialize=False, verbose_name='티켓 아이디')),
                ('usage_time', models.IntegerField(verbose_name='사용 시간')),
                ('usage_count', models.IntegerField(verbose_name='사용 횟수')),
                ('usage_period_in_days', models.IntegerField(verbose_name='사용 기간(일)')),
                ('price', models.IntegerField(verbose_name='금액')),
                ('ticket_type', models.CharField(choices=[('시간', 'TIME'), ('종일', 'ALL_DAY'), ('호텔', 'HOTEL')], max_length=32, verbose_name='티켓 타입')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성 일시')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정 일시')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='삭제 일시')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='삭제 여부')),
                ('pet_kindergarden', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='pet_kindergardens.petkindergarden')),
            ],
            options={
                'verbose_name': 'ticket',
                'verbose_name_plural': 'tickets',
                'db_table': 'ticket',
            },
        ),
    ]
