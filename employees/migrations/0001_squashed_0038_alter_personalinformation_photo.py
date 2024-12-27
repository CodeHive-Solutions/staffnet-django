# Generated by Django 5.1.3 on 2024-11-28 14:00

import django.core.validators
import django.db.models.deletion
import employees.models
import employees.utilities
from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('employees', '0001_initial'), ('employees', '0002_employee_headquarter_alter_employee_address_and_more'), ('employees', '0003_remove_employee_department_employee_affiliation_date_and_more'), ('employees', '0004_alter_employee_cell_phone_and_more'), ('employees', '0005_alter_employee_stratum'), ('employees', '0006_alter_employee_civil_status_and_more'), ('employees', '0007_alter_employee_emergency_contact_and_more'), ('employees', '0008_employee_photo_alter_employee_business_area_and_more'), ('employees', '0009_employee_windows_user_alter_employee_corporate_email'), ('employees', '0010_alter_employee_address_alter_employee_business_area_and_more'), ('employees', '0011_alter_employee_corporate_email_alter_employee_email'), ('employees', '0012_alter_employee_identification'), ('employees', '0013_alter_employee_identification'), ('employees', '0014_alter_employee_appointment_date'), ('employees', '0015_alter_employee_last_name_and_more'), ('employees', '0016_remove_employee_employees_e_email_8f5bbc_idx_and_more'), ('employees', '0017_alter_employee_pant_size_alter_employee_shirt_size_and_more'), ('employees', '0018_alter_employee_cell_phone_alter_employee_fixed_phone_and_more'), ('employees', '0019_alter_employee_remote_work_application_date'), ('employees', '0020_alter_employee_appointment_date_and_more'), ('employees', '0021_alter_employee_civil_status_and_more'), ('employees', '0022_alter_employee_email'), ('employees', '0023_employee_legacy_appointment_date_and_more'), ('employees', '0024_employee_memo_1_employee_memo_2_employee_memo_3'), ('employees', '0025_alter_employee_contract_type_alter_employee_stratum'), ('employees', '0026_remove_employee_created_at_and_more'), ('employees', '0027_alter_employee_legacy_appointment_date'), ('employees', '0028_alter_employee_shirt_size_alter_employee_shoe_size'), ('employees', '0029_alter_employee_bank_alter_employee_campaign_and_more'), ('employees', '0030_employee_termination_date_employee_termination_type_and_more'), ('employees', '0031_employee_rehire_eligibility_employee_status_and_more'), ('employees', '0032_alter_employee_status'), ('employees', '0033_alter_employee_education_level'), ('employees', '0034_alter_employee_photo'), ('employees', '0035_alter_employee_memo_1_alter_employee_memo_2_and_more'), ('employees', '0036_contactinformation_education_emergencycontact_and_more'), ('employees', '0037_alter_contactinformation_email_and_more'), ('employees', '0038_alter_personalinformation_photo')]

    initial = True

    dependencies = [
        ('administration', '0002_alter_campaign_options_and_more'),
        ('administration', '0003_rename_headquarters_headquarter_and_more'),
        ('administration', '0004_bank'),
        ('administration', '0005_delete_department'),
        ('administration', '0009_jobtitle_rank'),
    ]

    operations = [
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('education_level', employees.models.UpperCharField(choices=[('PRIMARIA', 'Primaria'), ('BACHILLER', 'Bachiller'), ('TÉCNICO', 'Técnico'), ('TECNÓLOGO', 'Tecnólogo'), ('AUXILIAR', 'Auxiliar'), ('UNIVERSITARIO', 'Universitario'), ('PROFESIONAL', 'Profesional'), ('ESPECIALIZACIÓN', 'Especialización')], max_length=100, verbose_name='Nivel de Educación')),
                ('title', employees.models.UpperCharField(blank=True, max_length=150, null=True, verbose_name='Título')),
                ('ongoing_studies', models.BooleanField(default=False, verbose_name='Estudios en Curso')),
            ],
            options={
                'verbose_name': 'Educación',
                'verbose_name_plural': 'Educación',
            },
        ),
        migrations.CreateModel(
            name='EmergencyContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', employees.models.UpperCharField(max_length=100, verbose_name='Nombre Contacto de Emergencia')),
                ('relationship', employees.models.UpperCharField(choices=[('PADRE', 'Padre'), ('MADRE', 'Madre'), ('OTRO', 'Otro'), ('ABUELO(A)', 'Abuelo(a)'), ('AMIGO(A)', 'Amigo(a)'), ('HERMANO(A)', 'Hermano(a)'), ('ESPOSO(A)', 'Esposo(a)'), ('HIJO(A)', 'Hijo(a)'), ('TIO(A)', 'Tío(a)'), ('PRIMO(A)', 'Primo(a)'), ('FAMILIAR', 'Familiar')], max_length=100, verbose_name='Parentesco')),
                ('phone', employees.models.UpperCharField(max_length=15, verbose_name='Teléfono de Emergencia')),
            ],
            options={
                'verbose_name': 'Contacto de Emergencia',
                'verbose_name_plural': 'Contactos de Emergencia',
            },
        ),
        migrations.CreateModel(
            name='PersonalInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(null=True, upload_to=employees.utilities.user_photo_path, verbose_name='Foto')),
                ('identification', models.PositiveIntegerField(db_index=True, unique=True, validators=[django.core.validators.MinValueValidator(10000)], verbose_name='Identificación')),
                ('last_name', employees.models.UpperCharField(blank=True, max_length=100, null=True, verbose_name='Apellidos')),
                ('first_name', employees.models.UpperCharField(max_length=100, verbose_name='Nombres')),
                ('document_type', employees.models.UpperCharField(choices=[('CC', 'Cédula de Ciudadanía'), ('CE', 'Cédula de Extranjería'), ('TI', 'Tarjeta de Identidad'), ('PP', 'Pasaporte'), ('RC', 'Registro Civil')], default='CC', max_length=2, verbose_name='Tipo de Documento')),
                ('birth_date', models.DateField(verbose_name='Fecha de Nacimiento')),
                ('expedition_place', employees.models.UpperCharField(max_length=100, verbose_name='Lugar de Expedición')),
                ('expedition_date', models.DateField(verbose_name='Fecha de Expedición')),
                ('gender', employees.models.UpperCharField(choices=[('M', 'Masculino'), ('F', 'Femenino')], max_length=1, verbose_name='Género')),
                ('rh', employees.models.UpperCharField(choices=[('O+', 'O+'), ('O-', 'O-'), ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-')], max_length=3, verbose_name='RH')),
                ('civil_status', employees.models.UpperCharField(choices=[('SOLTERO(A)', 'Soltero(a)'), ('UNION LIBRE', 'Unión Libre'), ('CASADO(A)', 'Casado(a)'), ('DIVORCIADO(A)', 'Divorciado(a)'), ('SEPARADO(A)', 'Separado(a)'), ('VIUDO(A)', 'Viudo(a)')], max_length=25, verbose_name='Estado Civil')),
                ('sons', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Número de Hijos')),
                ('responsible_persons', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Personas a Cargo')),
                ('stratum', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(6)], verbose_name='Estrato')),
                ('shirt_size', employees.models.UpperCharField(choices=[('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL'), ('XXXL', 'XXXL')], max_length=4, verbose_name='Talla de Camisa')),
                ('pant_size', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(6), django.core.validators.MaxValueValidator(50)], verbose_name='Talla de Pantalón')),
                ('shoe_size', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(20)], verbose_name='Talla de Zapato')),
            ],
            options={
                'verbose_name': 'Información Personal',
                'verbose_name_plural': 'Informaciones Personales',
            },
        ),
        migrations.CreateModel(
            name='TerminationDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('termination_date', models.DateField(blank=True, null=True, verbose_name='Fecha de Terminación')),
                ('termination_type', employees.models.UpperCharField(blank=True, choices=[('VOLUNTARIA', 'Voluntaria'), ('INVOLUNTARIA', 'Involuntaria')], max_length=100, null=True, verbose_name='Tipo de Terminación')),
                ('termination_reason', employees.models.UpperCharField(blank=True, choices=[('BAJA REMUNERACIÓN', 'Baja remuneración'), ('CALAMIDAD FAMILIAR', 'Calamidad familiar'), ('CAMBIO DE ACTIVIDAD', 'Cambio de actividad'), ('CONFLICTOS EN RELACIONES LABORALES', 'Conflictos en relaciones laborales'), ('DESPLAZAMIENTO', 'Desplazamiento'), ('ESTRÉS LABORAL', 'Estrés laboral'), ('FALTA DE HERRAMIENTAS PARA  DESEMPEÑAR LA LABOR', 'Falta de herramientas para  desempeñar la labor'), ('FALTA DE INDUCCIÓN AL INGRESAR', 'Falta de inducción al ingresar'), ('FALTA DE RECONOCIMIENTO', 'Falta de reconocimiento'), ('HORARIO LABORAL', 'Horario laboral'), ('INCOMPATIBILIDAD CON EL JEFE', 'Incompatibilidad con el jefe'), ('MAL AMBIENTE LABORAL', 'Mal ambiente laboral'), ('MOTIVOS DE ESTUDIO', 'Motivos de estudio'), ('MOTIVOS DE SALUD', 'Motivos de salud'), ('MOTIVOS DE VIAJE', 'Motivos de viaje'), ('MOTIVOS PERSONALES', 'Motivos personales'), ('NO HAY OPORTUNIDADES DE CRECIMIENTO LABORAL', 'No hay oportunidades de crecimiento laboral'), ('NO HAY OPORTUNIDADES DE ESTUDIAR', 'No hay oportunidades de estudiar'), ('OTRA OFERTA LABORAL', 'Otra oferta laboral'), ('OTRO', 'Otro'), ('PROBLEMAS PERSONALES', 'Problemas personales'), ('TERMINACIÓN DE CONTRATO APRENDIZAJE', 'Terminación de contrato aprendizaje'), ('TERMINACIÓN DE CONTRATO CON JUSTA CAUSA', 'Terminación de contrato con justa causa'), ('TERMINACIÓN DE CONTRATO POR PERIODO DE PRUEBA', 'Terminación de contrato por periodo de prueba'), ('TERMINACIÓN DE CONTRATO SIN JUSTA CAUSA', 'Terminación de contrato sin justa causa'), ('TERMINACIÓN POR ABANDONO DE PUESTO', 'Terminación por abandono de puesto'), ('TERMINACIÓN POR OBRA O LABOR CONTRATADA ', 'Terminación por obra o labor contratada ')], max_length=100, null=True, verbose_name='Motivo de Terminación')),
                ('rehire_eligibility', models.BooleanField(default=True, verbose_name='Elegible para Recontratación')),
            ],
            options={
                'verbose_name': 'Detalles de Terminación',
                'verbose_name_plural': 'Detalles de Terminación',
            },
        ),
        migrations.CreateModel(
            name='ContactInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', employees.models.UpperCharField(max_length=255, verbose_name='Dirección')),
                ('neighborhood', employees.models.UpperCharField(max_length=100, verbose_name='Barrio')),
                ('fixed_phone', models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.MinLengthValidator(7)], verbose_name='Teléfono Fijo')),
                ('cell_phone', employees.models.UpperCharField(max_length=15, validators=[django.core.validators.MinLengthValidator(10)], verbose_name='Celular')),
                ('email', employees.models.UpperEmailField(db_index=True, max_length=254, null=True, unique=True, verbose_name='Correo Electrónico')),
                ('corporate_email', employees.models.UpperEmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='Correo Electrónico Corporativo')),
                ('locality', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='employees', to='administration.locality', verbose_name='Localidad')),
            ],
            options={
                'verbose_name': 'Información de Contacto',
                'verbose_name_plural': 'Informaciones de Contacto',
            },
        ),
        migrations.CreateModel(
            name='EmploymentDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('affiliation_date', models.DateField(verbose_name='Fecha de Afiliación')),
                ('entry_date', models.DateField(verbose_name='Fecha de Ingreso')),
                ('salary', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Salario')),
                ('transportation_allowance', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Auxilio de Transporte')),
                ('remote_work', models.BooleanField(default=False, verbose_name='Trabajo Remoto')),
                ('remote_work_application_date', models.DateField(blank=True, null=True, verbose_name='Fecha de Aplicación de Teletrabajo')),
                ('payroll_account', employees.models.UpperCharField(max_length=50, verbose_name='Cuenta de Nómina')),
                ('legacy_health_provider', models.CharField(blank=True, max_length=100, null=True, verbose_name='CAMBIOS EPS (LEGADO)')),
                ('appointment_date', models.DateField(blank=True, null=True, verbose_name='Fecha de Nombramiento')),
                ('legacy_appointment_date', models.CharField(blank=True, max_length=250, null=True, verbose_name='Fecha de Nombramiento (LEGADO)')),
                ('business_area', employees.models.UpperCharField(choices=[('OPERATIVOS', 'Operativos'), ('ADMINISTRATIVOS', 'Administrativos')], max_length=100, verbose_name='Área de Negocio')),
                ('contract_type', employees.models.UpperCharField(choices=[('TERMINO INDEFINIDO', 'Termino Indefinido'), ('OBRA O LABOR', 'Obra o Labor'), ('PRESTACIÓN DE SERVICIOS', 'Prestación de Servicios'), ('APRENDIZAJE', 'Aprendizaje')], max_length=100, verbose_name='Tipo de Contrato')),
                ('windows_user', employees.models.UpperCharField(blank=True, max_length=50, null=True, verbose_name='Usuario de Windows')),
                ('bank', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='employees', to='administration.bank', verbose_name='Banco')),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='employees', to='administration.campaign', verbose_name='Campaña')),
                ('compensation_fund', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='employees', to='administration.compensationfund', verbose_name='Caja de Compensación')),
                ('headquarter', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='employees', to='administration.headquarter', verbose_name='Sede')),
                ('health_provider', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='employees', to='administration.healthprovider', verbose_name='EPS')),
                ('job_title', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='employees', to='administration.jobtitle', verbose_name='Cargo')),
                ('management', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='employees', to='administration.management', verbose_name='Gerencia')),
                ('pension_fund', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='employees', to='administration.pensionfund', verbose_name='Fondo de Pensiones')),
                ('saving_fund', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='employees', to='administration.savingfund', verbose_name='Cesantías')),
            ],
            options={
                'verbose_name': 'Detalles Laborales',
                'verbose_name_plural': 'Detalles Laborales',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emergency_contact', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employee', to='employees.emergencycontact')),
                ('status', models.BooleanField(default=True, verbose_name='Activo')),
                ('contact_info', models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='employee', to='employees.contactinformation')),
                ('education', models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='employee', to='employees.education')),
                ('employment_details', models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='employee', to='employees.employmentdetails')),
                ('personal_info', models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='employee', to='employees.personalinformation')),
                ('termination_details', models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='employee', to='employees.terminationdetails')),
            ],
            options={
                'verbose_name': 'Empleado',
                'verbose_name_plural': 'Empleados',
                'indexes': [],
            },
        ),
    ]