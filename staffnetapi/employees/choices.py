# Reduce the size of model.py by moving the choices to a separate file

import enum

from django.db.models import TextChoices


class TerminationReason(TextChoices):
    LOW_REMUNERATION = "BAJA REMUNERACIÓN", "Baja remuneración"
    CALAMITY_FAMILY = "CALAMIDAD FAMILIAR", "Calamidad familiar"
    CHANGE_ACTIVITY = "CAMBIO DE ACTIVIDAD", "Cambio de actividad"
    CONFLICTS_LABOR_RELATIONS = (
        "CONFLICTOS EN RELACIONES LABORALES",
        "Conflictos en relaciones laborales",
    )
    DISPLACEMENT = "DESPLAZAMIENTO", "Desplazamiento"
    LABOR_STRESS = "ESTRÉS LABORAL", "Estrés laboral"
    LACK_TOOLS_PERFORM_JOB = (
        "FALTA DE HERRAMIENTAS PARA  DESEMPEÑAR LA LABOR",
        "Falta de herramientas para  desempeñar la labor",
    )
    LACK_INDUCTION_ENTERING = (
        "FALTA DE INDUCCIÓN AL INGRESAR",
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
        "TERMINACIÓN DE CONTRATO APRENDIZAJE",
        "Terminación de contrato aprendizaje",
    )
    TERMINATION_CONTRACT_JUST_CAUSE = (
        "TERMINACIÓN DE CONTRATO CON JUSTA CAUSA",
        "Terminación de contrato con justa causa",
    )
    TERMINATION_CONTRACT_PROBATION_PERIOD = (
        "TERMINACIÓN DE CONTRATO POR PERIODO DE PRUEBA",
        "Terminación de contrato por periodo de prueba",
    )
    TERMINATION_CONTRACT_WITHOUT_JUST_CAUSE = (
        "TERMINACIÓN DE CONTRATO SIN JUSTA CAUSA",
        "Terminación de contrato sin justa causa",
    )
    TERMINATION_ABANDONMENT_POSITION = (
        "TERMINACIÓN POR ABANDONO DE PUESTO",
        "Terminación por abandono de puesto",
    )
    TERMINATION_WORK_CONTRACTED = (
        "TERMINACIÓN POR OBRA O LABOR CONTRATADA ",
        "Terminación por obra o labor contratada ",
    )


class CivilStatus(TextChoices):
    SINGLE = "SOLTERO(A)", "Soltero(a)"
    COMMON_LAW = "UNION LIBRE", "Unión Libre"
    MARRIED = "CASADO(A)", "Casado(a)"
    DIVORCED = "DIVORCIADO(A)", "Divorciado(a)"
    SEPARATED = "SEPARADO(A)", "Separado(a)"
    WIDOWED = "VIUDO(A)", "Viudo(a)"


class ShirtSize(TextChoices):
    XS = "XS", "XS"
    S = "S", "S"
    M = "M", "M"
    L = "L", "L"
    XL = "XL", "XL"
    XXL = "XXL", "XXL"
    XXXL = "XXXL", "XXXL"


class Relationship(TextChoices):
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


class BusinessArea(TextChoices):
    OPERATIONS = "OPERATIVOS", "Operativos"
    ADMINISTRATIVE = "ADMINISTRATIVOS", "Administrativos"


class Rh(TextChoices):
    O_POSITIVE = "O+", "O+"
    O_NEGATIVE = "O-", "O-"
    A_POSITIVE = "A+", "A+"
    A_NEGATIVE = "A-", "A-"
    B_POSITIVE = "B+", "B+"
    B_NEGATIVE = "B-", "B-"
    AB_POSITIVE = "AB+", "AB+"
    AB_NEGATIVE = "AB-", "AB-"


class EducationLevel(TextChoices):
    PRIMARY = "PRIMARIA", "Primaria"
    SECONDARY = "BACHILLER", "Bachiller"
    TECHNICAL = "TÉCNICO", "Técnico"
    TECHNOLOGICAL = "TECNÓLOGO", "Tecnólogo"
    AUXILIARY = "AUXILIAR", "Auxiliar"
    UNIVERSITY = "UNIVERSITARIO", "Universitario"
    PROFESSIONAL = "PROFESIONAL", "Profesional"
    SPECIALIZATION = "ESPECIALIZACIÓN", "Especialización"


class ContractType(TextChoices):
    INDEFINITE_TERM = "TERMINO INDEFINIDO", "Termino Indefinido"
    WORK = "OBRA O LABOR", "Obra o Labor"
    SERVICE = "PRESTACIÓN DE SERVICIOS", "Prestación de Servicios"
    LEARNING = "APRENDIZAJE", "Aprendizaje"


class DocumentType(TextChoices):
    CC = "CC", "Cédula de Ciudadanía"
    CE = "CE", "Cédula de Extranjería"
    TI = "TI", "Tarjeta de Identidad"
    PP = "PP", "Pasaporte"
    RC = "RC", "Registro Civil"


class Gender(TextChoices):
    MASCULINO = "M", "Masculino"
    FEMENINO = "F", "Femenino"
