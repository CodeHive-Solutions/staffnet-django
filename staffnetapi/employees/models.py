from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator


# Define choices using TextChoices for better structure
class CivilStatus(models.TextChoices):
    SINGLE = "S", "Soltero(a)"
    MARRIED = "C", "Casado(a)"
    DIVORCED = "D", "Divorciado(a)"
    COMMON_LAW = "U", "Unión Libre"
    SEPARATED = "P", "Separado(a)"
    WIDOWED = "V", "Viudo(a)"


class BusinessArea(models.TextChoices):
    OPERATIONS = "Operativos", "Operativos"
    ADMINISTRATIVE = "Administrativos", "Administrativos"


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
    PRIMARY = "Primaria", "Primaria"
    SECONDARY = "Bachiller", "Bachiller"
    TECHNICAL = "Técnico", "Técnico"
    TECHNOLOGICAL = "Tecnológico", "Tecnológico"
    AUXILIARY = "Auxiliar", "Auxiliar"
    UNIVERSITY = "Universitario", "Universitario"
    PROFESSIONAL = "Profesional", "Profesional"
    SPECIALIZATION = "Especialización", "Especialización"


class ContractType(models.TextChoices):
    INDEFINITE_TERM = "Termino Indefinido", "Termino Indefinido"
    FIXED_TERM = "Termino Fijo", "Termino Fijo"
    WORK = "Obra o Labor", "Obra o Labor"
    SERVICE = "Prestación de Servicios", "Prestación de Servicios"
    LEARNING = "Aprendizaje", "Aprendizaje"


class DocumentType(models.TextChoices):
    CC = "CC", "Cédula de Ciudadanía"
    CE = "CE", "Cédula de Extranjería"
    TI = "TI", "Tarjeta de Identidad"
    PP = "PP", "Pasaporte"
    RC = "RC", "Registro Civil"


class Employee(models.Model):
    # Use regex validator for identification
    identification = models.CharField(
        max_length=10, unique=True, verbose_name="Identificación"
    )
    last_name = models.CharField(max_length=100, verbose_name="Apellidos")
    first_name = models.CharField(max_length=100, verbose_name="Nombres")
    document_type = models.CharField(
        max_length=2,
        choices=DocumentType.choices,
        verbose_name="Tipo de Documento",
        default=DocumentType.CC,
    )
    birth_date = models.DateField(verbose_name="Fecha de Nacimiento")
    expedition_place = models.CharField(
        max_length=100, verbose_name="Lugar de Expedición"
    )
    expedition_date = models.DateField(verbose_name="Fecha de Expedición")
    gender = models.CharField(max_length=1, verbose_name="Género")
    rh = models.CharField(max_length=3, choices=Rh.choices, verbose_name="RH")
    civil_status = models.CharField(
        max_length=1, choices=CivilStatus.choices, verbose_name="Estado Civil"
    )

    # Change to PositiveIntegerField for sons
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
    stratum = models.PositiveIntegerField(
        default=2,
        validators=[MinValueValidator(1), MaxValueValidator(6)],
        verbose_name="Estrato",
    )
    fixed_phone = models.CharField(
        max_length=15, verbose_name="Teléfono Fijo", null=True, blank=True
    )
    cell_phone = models.CharField(max_length=15, verbose_name="Celular")

    email = models.EmailField(unique=True, verbose_name="Correo Electrónico")
    corporate_email = models.EmailField(
        unique=True, verbose_name="Correo Electrónico Corporativo"
    )
    address = models.CharField(max_length=255, verbose_name="Dirección")
    neighborhood = models.CharField(max_length=100, verbose_name="Barrio")
    locality = models.ForeignKey(
        "administration.Locality",
        on_delete=models.CASCADE,
        related_name="employees",
        verbose_name="Localidad",
    )
    emergency_contact = models.CharField(
        max_length=100, verbose_name="Contacto de Emergencia"
    )
    emergency_relationship = models.CharField(
        max_length=100, verbose_name="Parentesco Contacto de Emergencia"
    )
    emergency_phone = models.CharField(
        max_length=15, verbose_name="Teléfono de Emergencia"
    )
    # Education
    education_level = models.CharField(
        max_length=100,
        choices=EducationLevel.choices,
        verbose_name="Nivel de Educación",
    )
    title = models.CharField(max_length=150, verbose_name="Título")
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
    payroll_account = models.CharField(max_length=50, verbose_name="Cuenta de Nómina")
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
    appointment_date = models.DateField(verbose_name="Fecha de Nombramiento")
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
    business_area = models.CharField(
        max_length=100, choices=BusinessArea.choices, verbose_name="Área de Negocio"
    )
    contract_type = models.CharField(
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
    remote_work_application_date = models.DateField(
        verbose_name="Fecha de Aplicación de Trabajo Remoto"
    )
    shirt_size = models.PositiveIntegerField(
        validators=[MinValueValidator(6), MaxValueValidator(50)],
        verbose_name="Talla de Camisa",
    )
    pant_size = models.PositiveIntegerField(
        validators=[MinValueValidator(6), MaxValueValidator(50)],
        verbose_name="Talla de Pantalón",
    )
    shoe_size = models.PositiveIntegerField(
        validators=[MinValueValidator(20), MaxValueValidator(50)],
        verbose_name="Talla de Zapato",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"
        indexes = [
            models.Index(fields=["identification"]),
            models.Index(fields=["email"]),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.identification})"
