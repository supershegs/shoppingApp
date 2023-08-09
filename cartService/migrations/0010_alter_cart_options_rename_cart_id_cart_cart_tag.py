# Generated by Django 4.2.3 on 2023-07-31 21:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cartService", "0009_cart_user_alter_cart_cart_id"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="cart",
            options={"ordering": ["cart_tag", "-created_at"]},
        ),
        migrations.RenameField(
            model_name="cart",
            old_name="cart_id",
            new_name="cart_tag",
        ),
    ]
