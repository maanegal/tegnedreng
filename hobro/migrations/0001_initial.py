# Generated by Django 2.1.5 on 2019-02-16 17:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alias', models.CharField(max_length=30)),
                ('photo', models.ImageField(default='default.jpg', upload_to='')),
                ('title', models.CharField(max_length=100)),
                ('text', models.TextField()),
                ('release_date', models.DateField()),
                ('artist_name', models.CharField(max_length=60)),
                ('bc_embed_code', models.CharField(max_length=100)),
                ('sp_embed_code', models.CharField(max_length=100, null=True)),
                ('link_yt', models.CharField(max_length=100, null=True)),
                ('link_bc', models.CharField(max_length=100, null=True)),
                ('link_sp', models.CharField(max_length=100, null=True)),
                ('link_sc', models.CharField(max_length=100, null=True)),
                ('link_it', models.CharField(max_length=100, null=True)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('photo', models.ImageField(default='default.jpg', upload_to='')),
                ('text', models.TextField()),
                ('alias', models.CharField(max_length=30)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.CharField(max_length=200)),
                ('tagged_in_album', models.ManyToManyField(related_name='album_hashtag', to='hobro.Album')),
            ],
        ),
        migrations.CreateModel(
            name='ItemEmbed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_stamp', models.IntegerField()),
                ('target', models.CharField(max_length=60)),
                ('slug', models.SlugField(unique=True)),
                ('target_album', models.ManyToManyField(to='hobro.Album')),
                ('target_character', models.ManyToManyField(to='hobro.Character')),
            ],
        ),
        migrations.CreateModel(
            name='MusicVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alias', models.CharField(max_length=30)),
                ('title', models.CharField(max_length=100)),
                ('text', models.TextField()),
                ('release_date', models.DateField(null=True)),
                ('artist_name', models.CharField(max_length=60)),
                ('embed_url', models.CharField(max_length=100)),
                ('link_yt', models.CharField(max_length=100, null=True)),
                ('link_bc', models.CharField(max_length=100, null=True)),
                ('link_sp', models.CharField(max_length=100, null=True)),
                ('link_sc', models.CharField(max_length=100, null=True)),
                ('link_it', models.CharField(max_length=100, null=True)),
                ('slug', models.SlugField(unique=True)),
                ('appears', models.ManyToManyField(related_name='appears_in_video', to='hobro.Character')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('time_stamp', models.IntegerField()),
                ('page_name', models.CharField(max_length=60)),
                ('layout', models.CharField(default='standard', max_length=30)),
                ('link_fb', models.CharField(max_length=100, null=True)),
                ('link_tw', models.CharField(max_length=100, null=True)),
                ('slug', models.SlugField(unique=True)),
                ('appears', models.ManyToManyField(to='hobro.Character')),
            ],
        ),
        migrations.CreateModel(
            name='PostPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('photo', models.ImageField(default='default.jpg', upload_to='')),
                ('time_stamp', models.IntegerField()),
                ('page_name', models.CharField(max_length=60)),
                ('layout', models.CharField(default='standard', max_length=30)),
                ('link_fb', models.CharField(max_length=100, null=True)),
                ('link_ig', models.CharField(max_length=100, null=True)),
                ('link_tw', models.CharField(max_length=100, null=True)),
                ('slug', models.SlugField(unique=True)),
                ('appears', models.ManyToManyField(to='hobro.Character')),
            ],
        ),
        migrations.CreateModel(
            name='PostVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('video', models.FileField(upload_to='')),
                ('title', models.CharField(max_length=160, null=True)),
                ('photo', models.ImageField(default='default.jpg', upload_to='')),
                ('time_stamp', models.IntegerField()),
                ('page_name', models.CharField(max_length=60)),
                ('layout', models.CharField(default='standard', max_length=30)),
                ('link_fb', models.CharField(max_length=100, null=True)),
                ('link_ig', models.CharField(max_length=100, null=True)),
                ('link_tw', models.CharField(max_length=100, null=True)),
                ('slug', models.SlugField(unique=True)),
                ('appears', models.ManyToManyField(to='hobro.Character')),
            ],
        ),
        migrations.CreateModel(
            name='ProfileEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_stamp', models.IntegerField()),
                ('expires', models.IntegerField(null=True)),
                ('page_name', models.CharField(max_length=60)),
                ('photo', models.ImageField(default='default.jpg', upload_to='')),
                ('text', models.TextField()),
                ('link_fb', models.CharField(max_length=100, null=True)),
                ('link_tw', models.CharField(max_length=100, null=True)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('time_stamp', models.IntegerField()),
                ('expires', models.IntegerField(null=True)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alias', models.CharField(max_length=30)),
                ('photo', models.ImageField(default='default.jpg', upload_to='')),
                ('title', models.CharField(max_length=100)),
                ('track_number', models.IntegerField(null=True)),
                ('text', models.TextField()),
                ('artist_name', models.CharField(max_length=60)),
                ('bc_embed_code', models.CharField(max_length=100)),
                ('sp_embed_code', models.CharField(max_length=100, null=True)),
                ('link_yt', models.CharField(max_length=100, null=True)),
                ('link_bc', models.CharField(max_length=100, null=True)),
                ('link_sp', models.CharField(max_length=100, null=True)),
                ('link_sc', models.CharField(max_length=100, null=True)),
                ('link_it', models.CharField(max_length=100, null=True)),
                ('slug', models.SlugField(unique=True)),
                ('album', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hobro.Album')),
                ('appears', models.ManyToManyField(related_name='appears_on_song', to='hobro.Character')),
                ('producer', models.ManyToManyField(related_name='producer', to='hobro.Character')),
            ],
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('time_stamp', models.IntegerField()),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SwgrsMedia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('photo', models.ImageField(default='swgrs/profile.jpg', upload_to='')),
                ('profile', models.ImageField(default='swgrs/profile.jpg', upload_to='')),
                ('video', models.FileField(null=True, upload_to='')),
                ('video_title', models.CharField(max_length=160, null=True)),
                ('time_stamp', models.IntegerField()),
                ('layout', models.CharField(default='standard', max_length=30)),
                ('link_fb', models.CharField(max_length=100, null=True)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SwgrsPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('link_yt', models.CharField(max_length=100, null=True)),
                ('time_stamp', models.IntegerField()),
                ('profile', models.ImageField(default='swgrs/profile.jpg', upload_to='')),
                ('layout', models.CharField(default='standard', max_length=30)),
                ('link_fb', models.CharField(max_length=100, null=True)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SwgrsSong',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alias', models.CharField(max_length=30)),
                ('photo', models.ImageField(default='swgrs/profile.jpg', upload_to='')),
                ('title', models.CharField(max_length=100)),
                ('text', models.TextField()),
                ('sc_embed_code', models.CharField(max_length=100)),
                ('link_sc', models.CharField(max_length=100, null=True)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='musicvideo',
            name='song',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='hobro.Song'),
        ),
        migrations.AddField(
            model_name='itemembed',
            name='target_musicvideo',
            field=models.ManyToManyField(to='hobro.MusicVideo'),
        ),
        migrations.AddField(
            model_name='itemembed',
            name='target_song',
            field=models.ManyToManyField(to='hobro.Song'),
        ),
        migrations.AddField(
            model_name='itemembed',
            name='target_swgrssong',
            field=models.ManyToManyField(to='hobro.SwgrsSong'),
        ),
        migrations.AddField(
            model_name='hashtag',
            name='tagged_in_post',
            field=models.ManyToManyField(related_name='post_hashtag', to='hobro.Post'),
        ),
        migrations.AddField(
            model_name='hashtag',
            name='tagged_in_postphoto',
            field=models.ManyToManyField(related_name='photo_hashtag', to='hobro.PostPhoto'),
        ),
        migrations.AddField(
            model_name='hashtag',
            name='tagged_in_postvideo',
            field=models.ManyToManyField(related_name='video_hashtag', to='hobro.PostVideo'),
        ),
        migrations.AddField(
            model_name='hashtag',
            name='tagged_in_song',
            field=models.ManyToManyField(related_name='song_hashtag', to='hobro.Song'),
        ),
        migrations.AddField(
            model_name='hashtag',
            name='tagged_in_swgrs_media',
            field=models.ManyToManyField(related_name='swgrs_media_hashtag', to='hobro.SwgrsMedia'),
        ),
        migrations.AddField(
            model_name='hashtag',
            name='tagged_in_swgrs_post',
            field=models.ManyToManyField(related_name='swgrs_post_hashtag', to='hobro.SwgrsPost'),
        ),
        migrations.AddField(
            model_name='hashtag',
            name='tagged_in_swgrs_song',
            field=models.ManyToManyField(related_name='swgrs_song_hashtag', to='hobro.SwgrsSong'),
        ),
    ]
