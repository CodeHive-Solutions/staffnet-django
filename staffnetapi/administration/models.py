from django.db import models


# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super(Department, self).save(*args, **kwargs)


class JobTitle(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super(JobTitle, self).save(*args, **kwargs)


class Locality(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Localidad"
        verbose_name_plural = "Localidades"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super(Locality, self).save(*args, **kwargs)


class HealthProvider(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Proveedor de Salud"
        verbose_name_plural = "Proveedores de Salud"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super(HealthProvider, self).save(*args, **kwargs)


class PensionFund(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Fondo de Pensiones"
        verbose_name_plural = "Fondos de Pensiones"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super(PensionFund, self).save(*args, **kwargs)


class CompensationFund(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Caja de Compensación"
        verbose_name_plural = "Cajas de Compensación"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super(CompensationFund, self).save(*args, **kwargs)


class SavingFund(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Cesantía"
        verbose_name_plural = "Cesantías"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super(SavingFund, self).save(*args, **kwargs)


class Headquarter(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Sede"
        verbose_name_plural = "Sedes"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super(Headquarter, self).save(*args, **kwargs)


class Management(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Gerencia"
        verbose_name_plural = "Gerencias"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super(Management, self).save(*args, **kwargs)


class Campaign(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Campaña"
        verbose_name_plural = "Campañas"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super(Campaign, self).save(*args, **kwargs)


class Bank(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Banco"
        verbose_name_plural = "Bancos"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super(Bank, self).save(*args, **kwargs)
