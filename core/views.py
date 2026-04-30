import csv
from .models import Client
from .forms import ClientForm
from django.db.models import Q
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse


class ClientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Client
    template_name = "core/client_list.html"
    context_object_name = "clients"
    paginate_by = 3
    permission_required = 'core.view_client'

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
        context["query"] = self.request.GET.get("q", "").strip()
        context["sort"] = self.request.GET.get("sort", "id")
        context["total"] = self.get_queryset().count()
        return context


class ClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = "core/client_form.html"
    success_url = reverse_lazy("client_list")
    permission_required = 'core.add_client'

    def form_valid(self, form):
        messages.success(self.request, "Cliente creado correctamente.")
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "core/client_form.html"
    success_url = reverse_lazy("client_list")
    permission_required = 'core.change_client'

    def form_valid(self, form):
        messages.success(self.request, "Cliente actualizado correctamente.")
        return super().form_valid(form)


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Client
    template_name = "core/client_confirm_delete.html"
    success_url = reverse_lazy("client_list")
    permission_required = 'core.delete_client'

    def form_valid(self, form):
        messages.success(self.request, "Cliente eliminado correctamente.")
        return super().form_valid(form)


class ClientExportCSVView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'core.view_client'

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="clients.csv"'
        writer = csv.writer(response)
        writer.writerow(["ID", "Nombre", "Email"])
        for client in Client.objects.all():
            writer.writerow([client.id, client.name, client.email])
        return response


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "core/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_clients"] = Client.objects.count()
        return context


class ClientDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Client
    template_name = "core/client_detail.html"
    context_object_name = "client"
    permission_required = 'core.view_client'
