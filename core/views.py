from .models import Client
from .forms import ClientForm
from django.db.models import Q
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


class ClientListView(ListView):
    model = Client
    template_name = "core/client_list.html"
    context_object_name = "clients"
    paginate_by = 3

    def get_queryset(self):
        query = self.request.GET.get("q", "").strip()
        sort = self.request.GET.get("sort", "id")

        queryset = Client.objects.all()

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(email__icontains=query)
            )

        allowed_sorts = ["id", "-id", "name", "-name", "email", "-email"]
        if sort in allowed_sorts:
            queryset = queryset.order_by(sort)
        else:
            queryset = queryset.order_by("id")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        query = self.request.GET.get("q", "").strip()
        sort = self.request.GET.get("sort", "id")

        context["query"] = query
        context["sort"] = sort
        context["total"] = self.get_queryset().count()

        return context

class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = "core/client_form.html"
    success_url = reverse_lazy("client_list")

    def form_valid(self, form):
        messages.success(self.request, "Cliente creado correctamente.")
        return super().form_valid(form)

class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "core/client_form.html"
    success_url = reverse_lazy("client_list")

    def form_valid(self, form):
        messages.success(self.request, "Cliente actualizado correctamente.")
        return super().form_valid(form)
    

class ClientDeleteView(DeleteView):
    model = Client
    template_name = "core/client_confirm_delete.html"
    success_url = reverse_lazy("client_list")

    def form_valid(self, form):
        messages.success(self.request, "Cliente eliminado correctamente.")
        return super().form_valid(form)