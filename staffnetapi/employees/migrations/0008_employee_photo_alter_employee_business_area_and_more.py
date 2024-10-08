# Generated by Django 5.0.7 on 2024-09-11 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0007_alter_employee_emergency_contact_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='employees/photos', verbose_name='Foto'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='business_area',
            field=models.CharField(choices=[('OPERATIVOS', 'Operativos'), ('ADMINISTRATIVOS', 'Administrativos')], max_length=100, verbose_name='Área de Negocio'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='civil_status',
            field=models.CharField(choices=[('SOLTERO(A)', 'Soltero(a)'), ('UNIÓN LIBRE', 'Unión Libre'), ('CASADO(A)', 'Casado(a)'), ('DIVORCIADO(A)', 'Divorciado(a)'), ('SEPARADO(A)', 'Separado(a)'), ('VIUDO(A)', 'Viudo(a)')], max_length=25, verbose_name='Estado Civil'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='contract_type',
            field=models.CharField(choices=[('TERMINO INDEFINIDO', 'Termino Indefinido'), ('TERMINO FIJO', 'Termino Fijo'), ('OBRA O LABOR', 'Obra o Labor'), ('PRESTACIÓN DE SERVICIOS', 'Prestación de Servicios'), ('APRENDIZAJE', 'Aprendizaje')], max_length=100, verbose_name='Tipo de Contrato'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='education_level',
            field=models.CharField(choices=[('PRIMARIA', 'Primaria'), ('BACHILLER', 'Bachiller'), ('TÉCNICO', 'Técnico'), ('TECNOLÓGICO', 'Tecnológico'), ('AUXILIAR', 'Auxiliar'), ('UNIVERSITARIO', 'Universitario'), ('PROFESIONAL', 'Profesional'), ('ESPECIALIZACIÓN', 'Especialización')], max_length=100, verbose_name='Nivel de Educación'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='emergency_relationship',
            field=models.CharField(choices=[('PADRE', 'Padre'), ('MADRE', 'Madre'), ('OTRO', 'Otro'), ('ABUELO(A)', 'Abuelo(a)'), ('AMIGO(A)', 'Amigo(a)'), ('HERMANO(A)', 'Hermano(a)'), ('ESPOSO(A)', 'Esposo(a)'), ('HIJO(A)', 'Hijo(a)'), ('TÍO(A)', 'Tío(a)'), ('PRIMO(A)', 'Primo(a)'), ('FAMILIAR', 'Familiar')], max_length=100, verbose_name='Parentesco Contacto de Emergencia'),
        ),
    ]
