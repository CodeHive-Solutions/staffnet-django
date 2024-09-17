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


class TerminationReason(models.TextChoices):
    LOW_REMUNERATION = "BAJA REMUNERACION", "Baja remuneración"
    CALAMITY_FAMILY = "CALAMIDAD FAMILIAR", "Calamidad familiar"
    CHANGE_ACTIVITY = "CAMBIO DE ACTIVIDAD", "Cambio de actividad"
    CONFLICTS_LABOR_RELATIONS = (
        "CONFLICTOS EN RELACIONES LABORALES",
        "Conflictos en relaciones laborales",
    )
    DISPLACEMENT = "DESPLAZAMIENTO", "Desplazamiento"
    LABOR_STRESS = "ESTRES LABORAL", "Estres laboral"
    LACK_TOOLS_PERFORM_JOB = (
        "FALTA DE HERRAMIENTAS PARA  DESEMPEÑAR LA LABOR",
        "Falta de herramientas para  desempeñar la labor",
    )
    LACK_INDUCTION_ENTERING = (
        "FALTA DE INDUCCION AL INGRESAR",
        "Falta de inducción al ingresar",
    )
    LACK_RECOGNITION = "FALTA DE RECONOCIMIENTO", "Falta de reconocimiento"
    WORKING_HOURS = "HORARIO LABORAL", "Horario laboral"
    INCOMPATIBILITY_BOSS = (
        "INCOMPATIBILIDAD CON EL JEFE",
        "Incompatibilidad con el jefe",
    )
    BAD_WORK_ENVIRONMENT = "MAL AMBIENTE LABORAL", "Mal ambiente laboral"
    STUDY_REASONS = "MOTIVOS DE ESTUDIO", "Motivos de estudio"
    HEALTH_REASONS = "MOTIVOS DE SALUD", "Motivos de salud"
    TRAVEL_REASONS = "MOTIVOS DE VIAJE", "Motivos de viaje"
    PERSONAL_REASONS = "MOTIVOS PERSONALES", "Motivos personales"
    NO_OPPORTUNITIES_LABOR_GROWTH = (
        "NO HAY OPORTUNIDADES DE CRECIMIENTO LABORAL",
        "No hay oportunidades de crecimiento laboral",
    )
    NO_OPPORTUNITIES_STUDY = (
        "NO HAY OPORTUNIDADES DE ESTUDIAR",
        "No hay oportunidades de estudiar",
    )
    OTHER_JOB_OFFER = "OTRA OFERTA LABORAL", "Otra oferta laboral"
    OTHER = "OTRO", "Otro"
    PERSONAL_PROBLEMS = "PROBLEMAS PERSONALES", "Problemas personales"
    TERMINATION_CONTRACT_LEARNING = (
        "TERMINACION DE CONTRATO APRENDIZAJE",
        "Terminación de contrato aprendizaje",
    )
    TERMINATION_CONTRACT_JUST_CAUSE = (
        "TERMINACION DE CONTRATO CON JUSTA CAUSA",
        "Terminación de contrato con justa causa",
    )
    TERMINATION_CONTRACT_PROBATION_PERIOD = (
        "TERMINACION DE CONTRATO POR PERIODO DE PRUEBA",
        "Terminación de contrato por periodo de prueba",
    )
    TERMINATION_CONTRACT_WITHOUT_JUST_CAUSE = (
        "TERMINACION DE CONTRATO SIN JUSTA CAUSA",
        "Terminación de contrato sin justa causa",
    )
    TERMINATION_ABANDONMENT_POSITION = (
        "TERMINACION POR ABANDONO DE PUESTO",
        "Terminación por abandono de puesto",
    )
    TERMINATION_WORK_CONTRACTED = (
        "TERMINACION POR OBRA O LABOR CONTRATADA ",
        "Terminación por obra o labor contratada ",
    )


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


class ShirtSize(models.TextChoices):
    XS = "XS", "XS"
    S = "S", "S"
    M = "M", "M"
    L = "L", "L"
    XL = "XL", "XL"
    XXL = "XXL", "XXL"
    XXXL = "XXXL", "XXXL"


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
    TECHNOLOGICAL = "TECNOLOGO", "Tecnologo"
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


class Employee(models.Model):
    photo = models.ImageField(
        upload_to="employees/photos",
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
        on_delete=models.PROTECT,
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
    payroll_account = UpperCharField(max_length=50, verbose_name="Cuenta de Nómina")
    bank = models.ForeignKey(
        "administration.Bank",
        on_delete=models.PROTECT,
        related_name="employees",
        verbose_name="Banco",
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
    shirt_size = models.CharField(
        max_length=4,
        choices=ShirtSize.choices,
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
        validators=[MinValueValidator(25), MaxValueValidator(50)],
        verbose_name="Talla de Zapato",
        null=True,
        blank=True,
    )
    # Memorandums
    memo_1 = UpperCharField(
        verbose_name="Memorando 1", null=True, blank=True, max_length=300
    )
    memo_2 = UpperCharField(
        verbose_name="Memorando 2", null=True, blank=True, max_length=300
    )
    memo_3 = UpperCharField(
        verbose_name="Memorando 3", null=True, blank=True, max_length=300
    )
    # termination_information
    termination_date = models.DateField(
        verbose_name="Fecha de Terminación", null=True, blank=True
    )
    termination_type = UpperCharField(
        max_length=100,
        choices=(
            ("VOLUNTARIA", "Voluntaria"),
            ("INVOLUNTARIA", "Involuntaria"),
        ),
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
    status = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"
        indexes = [
            models.Index(fields=["identification"]),
            models.Index(fields=["windows_user"]),
        ]

    def get_full_name(self) -> str:
        """Return the full name of the user."""

        def capitalize_name(name: str) -> str:
            return " ".join(part.capitalize() for part in name.split())

        if self.last_name:
            return (
                f"{capitalize_name(self.first_name)} {capitalize_name(self.last_name)}"
            )
        return capitalize_name(self.first_name)

    def __str__(self):
        return self.get_full_name() + f" ({self.identification})"

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
        if self.remote_work and self.remote_work_application_date:
            if self.remote_work_application_date < self.entry_date:
                raise ValidationError(
                    "La fecha de aplicación de teletrabajo no puede ser anterior a la fecha de ingreso.",
                )
        if self.termination_date and self.termination_date < self.entry_date:
            raise ValidationError(
                "La fecha de terminación no puede ser anterior a la fecha de ingreso.",
            )
        if not self.memo_1 and self.memo_2:
            raise ValidationError(
                "El memorando 2 no puede ser llenado sin llenar el memorando 1.",
            )
        if not self.memo_2 and self.memo_3:
            raise ValidationError(
                "El memorando 3 no puede ser llenado sin llenar el memorando 2.",
            )
        return super().clean()

    def save(self, *args, **kwargs):
        # Custom logic for setting the image path based on the name field
        if not self.photo:
            self.photo = f"employees/photos/{self.identification}.webp"
        super().save(*args, **kwargs)
