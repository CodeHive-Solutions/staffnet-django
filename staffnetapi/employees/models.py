from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    MinLengthValidator,
)


class UpperCharField(models.CharField):
    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        if value:
            value = value.upper()
            setattr(model_instance, self.attname, value)
        return value


class UpperEmailField(models.EmailField):
    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        if value:
            value = value.upper()
            setattr(model_instance, self.attname, value)
        return value


class CivilStatus(models.TextChoices):
    SINGLE = "SOLTERO(A)", "Soltero(a)"
    COMMON_LAW = "UNION LIBRE", "Unión Libre"
    MARRIED = "CASADO(A)", "Casado(a)"
    DIVORCED = "DIVORCIADO(A)", "Divorciado(a)"
    SEPARATED = "SEPARADO(A)", "Separado(a)"
    WIDOWED = "VIUDO(A)", "Viudo(a)"


class Relationship(models.TextChoices):
    FATHER = "PADRE", "Padre"
    MOTHER = "MADRE", "Madre"
    OTHER = "OTRO", "Otro"
    GRANDFATHER = "ABUELO(A)", "Abuelo(a)"
    FRIEND = "AMIGO(A)", "Amigo(a)"
    BROTHER = "HERMANO(A)", "Hermano(a)"
    SPOUSE = "ESPOSO(A)", "Esposo(a)"
    SON = "HIJO(A)", "Hijo(a)"
    UNCLE = "TIO(A)", "Tío(a)"
    COUSIN = "PRIMO(A)", "Primo(a)"
    RELATIVE = "FAMILIAR", "Familiar"


class BusinessArea(models.TextChoices):
    OPERATIONS = "OPERATIVOS", "Operativos"
    ADMINISTRATIVE = "ADMINISTRATIVOS", "Administrativos"


class Rh(models.TextChoices):
    O_POSITIVE = "O+", "O+"
    O_NEGATIVE = "O-", "O-"
    A_POSITIVE = "A+", "A+"
    A_NEGATIVE = "A-", "A-"
    B_POSITIVE = "B+", "B+"
    B_NEGATIVE = "B-", "B-"
    AB_POSITIVE = "AB+", "AB+"
    AB_NEGATIVE = "AB-", "AB-"


class EducationLevel(models.TextChoices):
    PRIMARY = "PRIMARIA", "Primaria"
    SECONDARY = "BACHILLER", "Bachiller"
    TECHNICAL = "TECNICO", "Técnico"  # RH don't want special characters
    TECHNOLOGICAL = "TECNOLOGICO", "Tecnológico"  # RH don't want special characters
    AUXILIARY = "AUXILIAR", "Auxiliar"
    UNIVERSITY = "UNIVERSITARIO", "Universitario"
    PROFESSIONAL = "PROFESIONAL", "Profesional"
    SPECIALIZATION = "ESPECIALIZACION", "Especialización"


class ContractType(models.TextChoices):
    INDEFINITE_TERM = "TERMINO INDEFINIDO", "Termino Indefinido"
    WORK = "OBRA O LABOR", "Obra o Labor"
    SERVICE = "PRESTACION DE SERVICIOS", "Prestación de Servicios"
    LEARNING = "APRENDIZAJE", "Aprendizaje"


class DocumentType(models.TextChoices):
    CC = "CC", "Cédula de Ciudadanía"
    CE = "CE", "Cédula de Extranjería"
    TI = "TI", "Tarjeta de Identidad"
    PP = "PP", "Pasaporte"
    RC = "RC", "Registro Civil"

# ! There is not all the fields

class Employee(models.Model):
    photo = models.ImageField(
        upload_to="employees/photos",
        null=True,
        blank=True,
        verbose_name="Foto",
    )
    identification = models.PositiveIntegerField(
        unique=True,
        verbose_name="Identificación",
        validators=[MinValueValidator(10000)],
    )
    last_name = UpperCharField(
        max_length=100, verbose_name="Apellidos", null=True, blank=True
    )
    first_name = UpperCharField(max_length=100, verbose_name="Nombres")
    document_type = UpperCharField(
        max_length=2,
        choices=DocumentType.choices,
        verbose_name="Tipo de Documento",
        default=DocumentType.CC,
    )
    birth_date = models.DateField(verbose_name="Fecha de Nacimiento")
    expedition_place = UpperCharField(
        max_length=100, verbose_name="Lugar de Expedición"
    )
    expedition_date = models.DateField(verbose_name="Fecha de Expedición")
    gender = UpperCharField(
        max_length=1,
        choices=(("M", "Masculino"), ("F", "Femenino")),
        verbose_name="Género",
    )
    rh = UpperCharField(max_length=3, choices=Rh.choices, verbose_name="RH")
    civil_status = UpperCharField(
        max_length=25, choices=CivilStatus.choices, verbose_name="Estado Civil"
    )

    sons = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(30)],
        verbose_name="Número de Hijos",
    )

    responsible_persons = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(30)],
        verbose_name="Personas a Cargo",
    )

    stratum = models.CharField(
        max_length=1,
        choices=(
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
            ("4", "4"),
            ("5", "5"),
            ("6", "6"),
        ),
        verbose_name="Estrato",
    )

    fixed_phone = models.CharField(
        verbose_name="Teléfono Fijo",
        null=True,
        blank=True,
        max_length=15,
        validators=[MinLengthValidator(7)],
    )
    cell_phone = UpperCharField(
        verbose_name="Celular",
        max_length=15,
        validators=[MinLengthValidator(10)],
    )
    email = UpperEmailField(unique=True, verbose_name="Correo Electrónico", null=True)
    corporate_email = UpperEmailField(
        unique=True,
        verbose_name="Correo Electrónico Corporativo",
        null=True,
        blank=True,
    )
    address = UpperCharField(max_length=255, verbose_name="Dirección")
    neighborhood = UpperCharField(max_length=100, verbose_name="Barrio")
    locality = models.ForeignKey(
        "administration.Locality",
        on_delete=models.CASCADE,
        related_name="employees",
        verbose_name="Localidad",
    )
    emergency_contact = UpperCharField(
        max_length=100, verbose_name="Nombre Contacto de Emergencia"
    )
    emergency_relationship = UpperCharField(
        max_length=100,
        choices=Relationship.choices,
        verbose_name="Parentesco Contacto de Emergencia",
    )
    emergency_phone = UpperCharField(
        max_length=15, verbose_name="Teléfono de Emergencia"
    )
    # Education
    education_level = UpperCharField(
        max_length=100,
        choices=EducationLevel.choices,
        verbose_name="Nivel de Educación",
    )
    title = UpperCharField(max_length=150, verbose_name="Título", null=True, blank=True)
    ongoing_studies = models.BooleanField(
        default=False, verbose_name="Estudios en Curso"
    )
    # Laboral
    affiliation_date = models.DateField(verbose_name="Fecha de Afiliación")
    health_provider = models.ForeignKey(
        "administration.HealthProvider",
        on_delete=models.CASCADE,
        related_name="employees",
        verbose_name="EPS",
    )
    legacy_health_provider = models.CharField(
        max_length=100, verbose_name="CAMBIOS EPS (LEGADO)", null=True, blank=True
    )
    pension_fund = models.ForeignKey(
        "administration.PensionFund",
        on_delete=models.CASCADE,
        related_name="employees",
        verbose_name="Fondo de Pensiones",
    )
    compensation_fund = models.ForeignKey(
        "administration.CompensationFund",
        on_delete=models.CASCADE,
        related_name="employees",
        verbose_name="Caja de Compensación",
    )
    saving_fund = models.ForeignKey(
        "administration.SavingFund",
        on_delete=models.CASCADE,
        related_name="employees",
        verbose_name="Cesantías",
    )
    payroll_account = UpperCharField(max_length=50, verbose_name="Cuenta de Nómina")
    bank = models.ForeignKey(
        "administration.Bank",
        on_delete=models.CASCADE,
        related_name="employees",
        verbose_name="Banco",
    )
    headquarter = models.ForeignKey(
        "administration.Headquarter",
        on_delete=models.CASCADE,
        related_name="employees",
        verbose_name="Sede",
    )
    job_title = models.ForeignKey(
        "administration.JobTitle",
        on_delete=models.CASCADE,
        related_name="employees",
        verbose_name="Cargo",
    )
    appointment_date = models.DateField(
        verbose_name="Fecha de Nombramiento", null=True, blank=True
    )
    legacy_appointment_date = models.DateField(
        verbose_name="Fecha de Nombramiento (LEGADO)", null=True, blank=True
    )
    management = models.ForeignKey(
        "administration.Management",
        on_delete=models.CASCADE,
        related_name="employees",
        verbose_name="Gerencia",
    )
    campaign = models.ForeignKey(
        "administration.Campaign",
        on_delete=models.CASCADE,
        related_name="employees",
        verbose_name="Campaña",
    )
    business_area = UpperCharField(
        max_length=100, choices=BusinessArea.choices, verbose_name="Área de Negocio"
    )
    contract_type = UpperCharField(
        max_length=100, choices=ContractType.choices, verbose_name="Tipo de Contrato"
    )
    entry_date = models.DateField(verbose_name="Fecha de Ingreso")
    salary = models.DecimalField(
        max_digits=65, decimal_places=2, verbose_name="Salario"
    )
    transportation_allowance = models.DecimalField(
        max_digits=65, decimal_places=2, verbose_name="Auxilio de Transporte"
    )
    remote_work = models.BooleanField(default=False, verbose_name="Trabajo Remoto")
    # If the employee has remote work, the date when it was applied
    remote_work_application_date = models.DateField(
        verbose_name="Fecha de Aplicación de Teletrabajo", null=True, blank=True
    )
    windows_user = UpperCharField(
        max_length=50,
        verbose_name="Usuario de Windows",
        null=True,
        blank=True,
        unique=True,
    )
    shirt_size = models.PositiveIntegerField(
        validators=[MinValueValidator(6), MaxValueValidator(50)],
        verbose_name="Talla de Camisa",
        null=True,
        blank=True,
    )
    pant_size = models.PositiveIntegerField(
        validators=[MinValueValidator(6), MaxValueValidator(50)],
        verbose_name="Talla de Pantalón",
        null=True,
        blank=True,
    )
    shoe_size = models.PositiveIntegerField(
        validators=[MinValueValidator(20), MaxValueValidator(50)],
        verbose_name="Talla de Zapato",
        null=True,
        blank=True,
    )
    memo_1 = models.TextField(verbose_name="Memorando_1", null=True, blank=True)
    memo_2 = models.TextField(verbose_name="Memorando_2", null=True, blank=True)
    memo_3 = models.TextField(verbose_name="Memorando_3", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"
        indexes = [
            models.Index(fields=["identification"]),
            models.Index(fields=["windows_user"]),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.identification}"

    def clean(self) -> None:
        # If remote_work is True and no date is provided, raise an error
        if self.remote_work and not self.remote_work_application_date:
            raise ValidationError(
                "La fecha de aplicación de teletrabajo es requerida.",
            )

        # If remote_work is False and date is set, raise an error or clear the date
        if not self.remote_work and self.remote_work_application_date:
            raise ValidationError(
                "La fecha de aplicación de teletrabajo no es requerida.",
            )
        return super().clean()
