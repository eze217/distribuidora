# Generated by Django 4.1 on 2022-09-13 15:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('distribuidora_app', '0008_productoenventa_cantidad_venta'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productoenventa',
            options={'verbose_name': 'Producto en venta'},
        ),
        migrations.CreateModel(
            name='ProductoAlmacenado',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('state', models.BooleanField(default=True, verbose_name='Estado')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('modified_date', models.DateField(auto_now=True, verbose_name='Fecha de modificación')),
                ('deleted_date', models.DateField(auto_now=True, verbose_name='Fecha de eliminación')),
                ('cantidad', models.IntegerField(default=0, verbose_name='Cantidad en venta')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='distribuidora_app.productomodel')),
            ],
            options={
                'verbose_name': 'Producto Almacenado',
            },
        ),
    ]
