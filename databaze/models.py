from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager





class Pojisteni(models.Model):
    pojisteni_title = models.CharField(max_length = 180, verbose_name="Pojištění")

    def __str__(self):
        return self.pojisteni_title

    class Meta:
        verbose_name = "Pojištění"
        verbose_name_plural = "Pojištění"



class Klient(models.Model):
    id_klienta = models.CharField(max_length=180)
    jmeno = models.CharField(max_length=180)
    prijmeni = models.CharField(max_length=180)
    narozeni = models.CharField(max_length=180)
    pojisteni = models.ManyToManyField(Pojisteni)


    def __init__(self, *args, **kwargs):
        super(Klient, self).__init__(*args, **kwargs)

    def __str__(self):
        druh_pojisteni = [i.pojisteni_title for i in self.pojisteni.all()]

    def __str__(self):
        return "id_ klienta: {0} | Jmeno: {1} | prijmeni: {2} | narozeni: {3}".format(self.id_klienta, self.jmeno, self.prijmeni, self.narozeni)

    class Meta:
        verbose_name = "Klient"
        verbose_name_plural = "Klienti"



class Kontakt(models.Model):
    email = models.CharField(max_length=180)
    kontakt = models.CharField(max_length=180)
    adresa = models.CharField(max_length=200)
    klient = models.ForeignKey(Klient, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "email: {0} | kontakt: {1} | adresa: {2}".format(self.email, self.kontakt, self.adresa)

    class Meta:
        verbose_name = "Kontakt"
        verbose_name_plural = "Kontakty"



class UzivatelManager(BaseUserManager):

    def create_user(self, email, password):
        print(self.model)
        if email and password:
            user = self.model(email=self.normalize_email(email))
            user.set_password(password)
            user.save()
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_admin = True
        user.save()
        return user




class Uzivatel(AbstractBaseUser):

    email = models.EmailField(max_length = 300, unique=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        verbose_name = "uživatel"
        verbose_name_plural = "uživatelé"

    objects = UzivatelManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return "email: {}".format(self.email)

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True



