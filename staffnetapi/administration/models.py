from django.db import models


# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"

    def __str__(self):
        return self.name


class JobTitle(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"

    def __str__(self):
        return self.name


class Locality(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Localidad"
        verbose_name_plural = "Localidades"

    def __str__(self):
        return self.name


class HealthProvider(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Proveedor de Salud"
        verbose_name_plural = "Proveedores de Salud"

    def __str__(self):
        return self.name


class PensionFund(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Fondo de Pensiones"
        verbose_name_plural = "Fondos de Pensiones"

    def __str__(self):
        return self.name


class CompensationFund(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Caja de Compensación"
        verbose_name_plural = "Cajas de Compensación"

    def __str__(self):
        return self.name


class SavingFund(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Cesantía"
        verbose_name_plural = "Cesantías"

    def __str__(self):
        return self.name


class Headquarter(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Sede"
        verbose_name_plural = "Sedes"

    def __str__(self):
        return self.name


class Management(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Gerencia"
        verbose_name_plural = "Gerencias"

    def __str__(self):
        return self.name


class Campaign(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Campaña"
        verbose_name_plural = "Campañas"

    def __str__(self):
        return self.name

class Bank(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Banco"
        verbose_name_plural = "Bancos"

    def __str__(self):
        return self.name