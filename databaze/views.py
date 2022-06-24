from django.shortcuts import render
from django.views import generic
from .models import Klient, Kontakt, Uzivatel
from .forms import KlientForm, KontaktForm, UzivatelForm, LoginForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin



class KlientIndex(generic.ListView):
    template_name = "databaze/klient_index.html" 
    context_object_name = "klienti" 

    def get_queryset(self):
        return Klient.objects.all().order_by("-id")





class DetailKlientView(generic.DetailView):
    model = Klient
    template_name = "databaze/klient_detail.html"





class KontaktIndex(generic.ListView):
    template_name = "databaze/klient_kontakt.html" 
    context_object_name = "kontakty" 

    def get_queryset(self):
        return Kontakt.objects.all().order_by("-id")




# Forms =========================================================




class CreateKlient(LoginRequiredMixin, generic.edit.CreateView):
    form_class = KlientForm
    template_name = "databaze/create_klient.html"

    def get(self, request):
        if not request.user.is_admin:
            messages.info(request, "Nemáš práva pro přidání klienta.")
            return redirect(reverse("klient_index"))
        form = self.form_class(None)
        return render(request, self.template_name, {"form":form})

    def post(self, request):
        if not request.user.is_admin:
            messages.info(request, "Nemáš práva pro přidání klienta.")
            return redirect(reverse("klient_index"))
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect("klient_index")
        return render(request, self.template_name, {"form":form})



class CreateKontakt(generic.edit.CreateView):
    form_class = KontaktForm
    template_name = "databaze/create_kontakt.html"

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {"form":form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save(commit=True)
        return render(request, self.template_name, {"form":form})



class UzivatelViewRegister(generic.edit.CreateView):
    form_class = UzivatelForm
    model = Uzivatel
    template_name = "databaze/user_form.html"

    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, "Už jsi přihlášený, nemůžeš se registrovat.")
            return redirect(reverse("klient_index"))
        else:
            form = self.form_class(None)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        if request.user.is_authenticated:
            messages.info(request, "Už jsi přihlášený, nemůžeš se registrovat.")
            return redirect(reverse("klient_index"))
        form = self.form_class(request.POST)
        if form.is_valid():
            uzivatel = form.save(commit = False)
            password = form.cleaned_data["password"]
            uzivatel.set_password(password)
            uzivatel.save()
            login(request, uzivatel)
            return redirect("klient_index")

        return render(request, self.template_name, {"form":form})



class UzivatelViewLogin(generic.edit.CreateView):
    form_class = LoginForm
    template_name = "databaze/user_form.html"

    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, "Už jsi přihlášený, nemůžeš se přihlásit znovu.")
            return redirect(reverse("klient_index"))
        else:
            form = self.form_class(None)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        if request.user.is_authenticated:
            messages.info(request, "Už jsi přihlášený, nemůžeš se přihlásit znovu.")
            return redirect(reverse("klient_index"))
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email = email, password = password)
            if user:
                login(request, user)
                return redirect("klient_index")
            else:
                messages.error(request, "Tento účet neexistuje.")
        return render(request, self.template_name, {"form": form})



def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    else:
        messages.info(request, "Nemůžeš se odhlásit, pokud nejsi přihlášený.")
    return redirect(reverse("login"))



class CurrentKlientView(generic.DetailView):

    model = Klient
    template_name = "databaze/klient_detail.html"

    def get(self, request, pk):
        try:
            klient = self.get_object()
        except:
            return redirect("klient_index")
        return render(request, self.template_name, {"klient" : klient})


    def post(self, request, pk):
        if request.user.is_authenticated:
            if "edit" in request.POST:
                return redirect("edit_klient", pk=self.get_object().pk)
            else:
                if not request.user.is_admin:
                    messages.info(request, "Nemáš práva pro smazání klienta.")
                    return redirect(reverse("klient_index"))
                else:
                    self.get_object().delete()
        return redirect(reverse("klient_index"))    


class EditKlient(LoginRequiredMixin, generic.edit.CreateView):
    form_class = KlientForm
    template_name = "databaze/create_klient.html"

    def get(self, request, pk):
        if not request.user.is_admin:
            messages.info(request, "Nemáš práva pro úpravu klienta.")
            return redirect(reverse("klient_index"))
        try:
            klient = Klient.objects.get(pk = pk)
        except:
            messages.error(request, "Tento klient neexistuje!")
            return redirect("klient_index")
        form = self.form_class(instance = klient)
        return render(request, self.template_name, {"form":form})

    def post(self, request, pk):
        if not request.user.is_admin:
            messages.info(request, "Nemáš práva pro úpravu klienta.")
            return redirect(reverse("klient_index"))
        form = self.form_class(request.POST)

        if form.is_valid():
            id_klienta = form.cleaned_data["id_klienta"]
            jmeno = form.cleaned_data["jmeno"]
            prijmeni = form.cleaned_data["prijmeni"]
            narozeni = form.cleaned_data["narozeni"]
            pojisteni = form.cleaned_data["pojisteni"]
            try:
                klient = Klient.objects.get(pk = pk)
            except:
                messages.error(request, "Tento klient neexistuje!")
                return redirect(reverse("klient_index"))
            klient.id_klienta = id_klienta
            klient.jmeno = jmeno
            klient.prijmeni = prijmeni
            klient.narozeni = narozeni
            klient.pojisteni.set(pojisteni)
            klient.save()

        return redirect("klient_detail", pk = klient.id)        