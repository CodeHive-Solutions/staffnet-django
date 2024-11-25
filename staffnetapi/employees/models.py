from django.core.exceptions import ValidationError
from django.core.validators import (
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
)
from django.db import models

from .choices import (
    BusinessArea,
    CivilStatus,
    ContractType,
    DocumentType,
    EducationLevel,
    Relationship,
    Rh,
    ShirtSize,
    TerminationReason,
    Gender,
)
from .utilities import user_photo_path


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


# Personal Information Model
class PersonalInformation(models.Model):
    photo = models.ImageField(
        upload_to=user_photo_path, blank=True, verbose_name="Foto"
    )
    identification = models.PositiveIntegerField(
        unique=True,
        verbose_name="Identificación",
        validators=[MinValueValidator(10000)],
        db_index=True,
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
        choices=Gender.choices,
        verbose_name="Género",
    )
    rh = UpperCharField(max_length=3, choices=Rh.choices, verbose_name="RH")
    civil_status = UpperCharField(
        max_length=25, choices=CivilStatus.choices, verbose_name="Estado Civil"
    )
    sons = models.PositiveIntegerField(
        verbose_name="Número de Hijos", validators=[MinValueValidator(0)]
    )
    responsible_persons = models.PositiveIntegerField(
        verbose_name="Personas a Cargo", validators=[MinValueValidator(0)]
    )
    stratum = models.PositiveIntegerField(
        verbose_name="Estrato", validators=[MinValueValidator(0), MaxValueValidator(6)]
    )
    shirt_size = UpperCharField(
        max_length=4, choices=ShirtSize.choices, verbose_name="Talla de Camisa"
    )
    pant_size = models.PositiveIntegerField(
        validators=[MinValueValidator(6), MaxValueValidator(50)],
        verbose_name="Talla de Pantalón",
        null=True,
        blank=True,
    )
    shoe_size = models.PositiveIntegerField(
        verbose_name="Talla de Zapato", validators=[MinValueValidator(20)]
    )

    class Meta:
        verbose_name = "Información Personal"
        verbose_name_plural = "Informaciones Personales"


# Contact Information Model
class ContactInformation(models.Model):
    address = UpperCharField(max_length=255, verbose_name="Dirección")
    neighborhood = UpperCharField(max_length=100, verbose_name="Barrio")
    locality = models.ForeignKey(
        "administration.Locality",
        on_delete=models.PROTECT,
        related_name="employees",
        verbose_name="Localidad",
    )
    fixed_phone = models.CharField(
        verbose_name="Teléfono Fijo",
        null=True,
        blank=True,
        max_length=15,
        validators=[MinLengthValidator(7)],
    )
    cell_phone = UpperCharField(
        verbose_name="Celular", max_length=15, validators=[MinLengthValidator(10)]
    )
    email = UpperEmailField(
        unique=True, verbose_name="Correo Electrónico", null=True, db_index=True
    )
    corporate_email = UpperEmailField(
        unique=True,
        verbose_name="Correo Electrónico Corporativo",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Información de Contacto"
        verbose_name_plural = "Informaciones de Contacto"


# Emergency Contact Model
class EmergencyContact(models.Model):
    name = UpperCharField(max_length=100, verbose_name="Nombre Contacto de Emergencia")
    relationship = UpperCharField(
        max_length=100, choices=Relationship.choices, verbose_name="Parentesco"
    )
    phone = UpperCharField(max_length=15, verbose_name="Teléfono de Emergencia")

    class Meta:
        verbose_name = "Contacto de Emergencia"
        verbose_name_plural = "Contactos de Emergencia"


# Education Model
class Education(models.Model):
    education_level = UpperCharField(
        max_length=100,
        choices=EducationLevel.choices,
        verbose_name="Nivel de Educación",
    )
    title = UpperCharField(max_length=150, verbose_name="Título", null=True, blank=True)
    ongoing_studies = models.BooleanField(
        default=False, verbose_name="Estudios en Curso"
    )

    class Meta:
        verbose_name = "Educación"
        verbose_name_plural = "Educación"


# Employment Details Model
class EmploymentDetails(models.Model):
    affiliation_date = models.DateField(verbose_name="Fecha de Afiliación")
    entry_date = models.DateField(verbose_name="Fecha de Ingreso")
    salary = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name="Salario"
    )
    transportation_allowance = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name="Auxilio de Transporte"
    )
    remote_work = models.BooleanField(default=False, verbose_name="Trabajo Remoto")
    remote_work_application_date = models.DateField(
        verbose_name="Fecha de Aplicación de Teletrabajo", null=True, blank=True
    )
    payroll_account = UpperCharField(max_length=50, verbose_name="Cuenta de Nómina")
    bank = models.ForeignKey(
        "administration.Bank",
        on_delete=models.PROTECT,
        related_name="employees",
        verbose_name="Banco",
    )
    health_provider = models.ForeignKey(
        "administration.HealthProvider",
        on_delete=models.PROTECT,
        related_name="employees",
        verbose_name="EPS",
    )
    legacy_health_provider = models.CharField(
        max_length=100, verbose_name="CAMBIOS EPS (LEGADO)", null=True, blank=True
    )
    pension_fund = models.ForeignKey(
        "administration.PensionFund",
        on_delete=models.PROTECT,
        related_name="employees",
        verbose_name="Fondo de Pensiones",
    )
    compensation_fund = models.ForeignKey(
        "administration.CompensationFund",
        on_delete=models.PROTECT,
        related_name="employees",
        verbose_name="Caja de Compensación",
    )
    saving_fund = models.ForeignKey(
        "administration.SavingFund",
        on_delete=models.PROTECT,
        related_name="employees",
        verbose_name="Cesantías",
    )
    headquarter = models.ForeignKey(
        "administration.Headquarter",
        on_delete=models.PROTECT,
        related_name="employees",
        verbose_name="Sede",
    )
    job_title = models.ForeignKey(
        "administration.JobTitle",
        on_delete=models.PROTECT,
        related_name="employees",
        verbose_name="Cargo",
    )
    appointment_date = models.DateField(
        verbose_name="Fecha de Nombramiento", null=True, blank=True
    )
    legacy_appointment_date = models.CharField(
        verbose_name="Fecha de Nombramiento (LEGADO)",
        max_length=250,
        null=True,
        blank=True,
    )
    management = models.ForeignKey(
        "administration.Management",
        on_delete=models.PROTECT,
        related_name="employees",
        verbose_name="Gerencia",
    )
    campaign = models.ForeignKey(
        "administration.Campaign",
        on_delete=models.PROTECT,
        related_name="employees",
        verbose_name="Campaña",
    )
    business_area = UpperCharField(
        max_length=100, choices=BusinessArea.choices, verbose_name="Área de Negocio"
    )
    contract_type = UpperCharField(
        max_length=100, choices=ContractType.choices, verbose_name="Tipo de Contrato"
    )
    windows_user = UpperCharField(
        max_length=50, verbose_name="Usuario de Windows", null=True, blank=True
    )

    class Meta:
        verbose_name = "Detalles Laborales"
        verbose_name_plural = "Detalles Laborales"

    def clean_remote_work_date(self):
        if self.remote_work and not self.remote_work_application_date:
            raise ValidationError("Fecha de aplicación de teletrabajo requerida.")
        elif not self.remote_work and self.remote_work_application_date:
            raise ValidationError(
                "No se puede aplicar teletrabajo sin marcar la opción."
            )

    def clean(self):
        super().clean()
        self.clean_remote_work_date()


# Termination Details Model
class TerminationDetails(models.Model):
    termination_date = models.DateField(
        verbose_name="Fecha de Terminación", null=True, blank=True
    )
    termination_type = UpperCharField(
        max_length=100,
        choices=(("VOLUNTARIA", "Voluntaria"), ("INVOLUNTARIA", "Involuntaria")),
        verbose_name="Tipo de Terminación",
        null=True,
        blank=True,
    )
    termination_reason = UpperCharField(
        max_length=100,
        choices=TerminationReason.choices,
        verbose_name="Motivo de Terminación",
        null=True,
        blank=True,
    )
    rehire_eligibility = models.BooleanField(
        default=True, verbose_name="Elegible para Recontratación"
    )

    class Meta:
        verbose_name = "Detalles de Terminación"
        verbose_name_plural = "Detalles de Terminación"


# Main Employee Model with OneToOne Relationships
class Employee(models.Model):
    """Employee model with one-to-one relationships and shortcuts to main fields."""

    personal_info = models.OneToOneField(
        PersonalInformation, on_delete=models.CASCADE, related_name="employee"
    )
    contact_info = models.OneToOneField(
        ContactInformation, on_delete=models.CASCADE, related_name="employee"
    )
    emergency_contact = models.OneToOneField(
        EmergencyContact, on_delete=models.CASCADE, related_name="employee"
    )
    education = models.OneToOneField(
        Education, on_delete=models.CASCADE, related_name="employee"
    )
    employment_details = models.OneToOneField(
        EmploymentDetails, on_delete=models.CASCADE, related_name="employee"
    )
    termination_details = models.OneToOneField(
        TerminationDetails, on_delete=models.CASCADE, related_name="employee"
    )
    status = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"

    def __str__(self):
        return f"{self.get_full_name()} ({self.personal_identification})"

    # Shortcut Properties
    @property
    def personal_identification(self):
        """Access the 'identification' field from 'PersonalInformation'."""
        return self.personal_info.identification

    @property
    def personal_first_name(self):
        """Access the 'first_name' field from 'PersonalInformation'."""
        return self.personal_info.first_name

    @property
    def personal_last_name(self):
        """Access the 'last_name' field from 'PersonalInformation'."""
        return self.personal_info.last_name

    @property
    def contact_email(self):
        """Access the 'email' field from 'ContactInformation'."""
        return self.contact_info.email

    @property
    def contact_corporate_email(self):
        """Access the 'corporate_email' field from 'ContactInformation'."""
        return self.contact_info.corporate_email

    def get_full_name(self) -> str:
        """Return the full name of the employee."""
        if self.personal_last_name:
            return f"{self.personal_first_name} {self.personal_last_name}".title()
        return self.personal_first_name.title()
