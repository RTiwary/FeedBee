# Generated by Django 2.2.3 on 2020-07-03 19:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('students', models.ManyToManyField(related_name='classrooms', to='users.Student')),
                ('teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='classrooms', to='users.Teacher')),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('unit', models.CharField(max_length=75, null=True)),
                ('school_year', models.CharField(max_length=9, null=True)),
                ('term', models.CharField(max_length=1, null=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='surveys', to='teachers.Classroom')),
                ('completed_students', models.ManyToManyField(related_name='surveys', to='users.Student')),
            ],
        ),
        migrations.CreateModel(
            name='TextQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=500, null=True)),
                ('question_rank', models.IntegerField(null=True)),
                ('survey', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='text_questions', to='teachers.Survey')),
            ],
        ),
        migrations.CreateModel(
            name='MultipleChoiceQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=500, null=True)),
                ('option_a', models.CharField(max_length=200, null=True)),
                ('option_b', models.CharField(max_length=200, null=True)),
                ('option_c', models.CharField(blank=True, max_length=200, null=True)),
                ('option_d', models.CharField(blank=True, max_length=200, null=True)),
                ('option_e', models.CharField(blank=True, max_length=200, null=True)),
                ('question_rank', models.IntegerField(null=True)),
                ('survey', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mc_questions', to='teachers.Survey')),
            ],
        ),
        migrations.CreateModel(
            name='CheckboxQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=500, null=True)),
                ('option_a', models.CharField(max_length=200, null=True)),
                ('option_b', models.CharField(blank=True, max_length=200, null=True)),
                ('option_c', models.CharField(blank=True, max_length=200, null=True)),
                ('option_d', models.CharField(blank=True, max_length=200, null=True)),
                ('option_e', models.CharField(blank=True, max_length=200, null=True)),
                ('question_rank', models.IntegerField(null=True)),
                ('survey', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='checkbox_questions', to='teachers.Survey')),
            ],
        ),
        migrations.CreateModel(
            name='BooleanQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=500, null=True)),
                ('question_rank', models.IntegerField(null=True)),
                ('survey', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='boolean_questions', to='teachers.Survey')),
            ],
        ),
    ]
