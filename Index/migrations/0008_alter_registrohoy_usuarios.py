# Generated by Django 5.1.2 on 2024-10-28 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Index', '0007_alter_usuario_cedula_alter_usuarioatendido_cedula'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrohoy',
            name='usuarios',
            field=models.ManyToManyField(related_name='registro_diario', to='Index.usuarioatendido'),
        ),
    ]