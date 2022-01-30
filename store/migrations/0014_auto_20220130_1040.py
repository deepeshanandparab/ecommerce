# Generated by Django 3.2.11 on 2022-01-30 05:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0013_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='terms',
            field=models.CharField(default='accepted', max_length=10),
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_wishlisted', models.BooleanField(default=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlist_product', to='store.product')),
                ('user', models.ManyToManyField(blank=True, null=True, related_name='wishlist_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]