import random

from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views import generic

from leads.models import Agent
from .forms import AgentModelForm
from .mixins import OrganisorAndLoginRequiredMixin


class AgentListView(OrganisorAndLoginRequiredMixin, generic.ListView):
    context_object_name = "agents"
    template_name = "agents/agent_list.html"

    def get_queryset(self):
        """Return agents associated with the orgranisor's organisation."""
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    """Create agent/user with is_agent=True."""

    form_class = AgentModelForm
    success_url = reverse_lazy("agents:agent_list")
    template_name = "agents/agent_create.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organisor = False
        user.set_password(f"{random.randint(1, 100_000)}")
        user.save()
        Agent.objects.create(
            user=user,
            organisation=self.request.user.userprofile,
        )
        send_mail(
            subject="You're invited to be an agent",
            message="You were added as an agent. Please login!",
            from_email="admin@test.com",
            recipient_list=[user.email],
        )
        return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(OrganisorAndLoginRequiredMixin, generic.DetailView):
    context_object_name = "agent"
    template_name = "agents/agent_detail.html"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    context_object_name = "agent"
    form_class = AgentModelForm
    success_url = reverse_lazy("agents:agent_list")
    template_name = "agents/agent_update.html"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs(**kwargs)
        kwargs["instance"] = kwargs["instance"].user
        return kwargs


class AgentDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    context_object_name = "agent"
    success_url = reverse_lazy("agents:agent_list")
    template_name = "agents/agent_delete.html"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)
