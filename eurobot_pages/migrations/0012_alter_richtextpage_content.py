# Generated by Django 3.2.10 on 2022-01-11 22:57

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('eurobot_pages', '0011_alter_richtextpage_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='richtextpage',
            name='content',
            field=wagtail.core.fields.StreamField([('full_richtext', wagtail.core.blocks.RichTextBlock()), ('raw_html', wagtail.core.blocks.RawHTMLBlock())], blank=True, null=True),
        ),
    ]
