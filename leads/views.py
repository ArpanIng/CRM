from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views import generic

from agents.mixins import OrganisorAndLoginRequiredMixin

from .forms import LeadModelForm, AssignAgentForm, LeadCategoryUpdateForm
from .models import Lead


class HomepageView(generic.TemplateView):
    template_name = "homepage.html"


class LeadListView(LoginRequiredMixin, generic.ListView):
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user

        # Return leads associated to the organisation.
        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile, agent__isnull=False
            )
        else:  # is_agent
            # Return leads associated to the agent organisation.
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation, agent__isnull=False
            )
            # Return leads only assigned to the logged in agent.
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile,
                agent__isnull=True,
            )
        context.update(
            {
                "unassigned_leads": queryset,
            }
        )
        return context


class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user

        # Return leads associated to the organisation.
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:  # is_agent
            # Return leads associated to the agent organisation.
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            # Return leads only assigned to the logged in agent.
            queryset = queryset.filter(agent__user=user)
        return queryset


class LeadCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    form_class = LeadModelForm
    template_name = "leads/lead_create.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(
            {
                "request": self.request,
            }
        )
        return kwargs

    # Sends mails everytime a new lead is created
    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.organisation = self.request.user.userprofile
        lead.save()
        send_mail(
            subject="A lead has been created",
            message="Go to the site to to view lead",
            from_email="admin@test.com",
            recipient_list=["test@test.com"],
        )
        return super(LeadCreateView, self).form_valid(form)


class LeadUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    form_class = LeadModelForm
    context_object_name = "lead"
    template_name = "leads/lead_update.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(
            {
                "request": self.request,
            }
        )
        return kwargs

    def get_queryset(self):
        user = self.request.user
        # Return leads associated to the organisation.
        return Lead.objects.filter(organisation=user.userprofile)

    def form_valid(self, form):
        form.save()
        return super(LeadUpdateView, self).form_valid(form)


class LeadDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    model = Lead
    context_object_name = "lead"
    success_url = reverse_lazy("leads:lead_list")
    template_name = "leads/lead_delete.html"

    def get_queryset(self):
        user = self.request.user
        # Return leads associated to the organisation.
        return Lead.objects.filter(organisation=user.userprofile)


class AssignAgentview(OrganisorAndLoginRequiredMixin, generic.FormView):
    """Assign agents to unassigned leads."""

    form_class = AssignAgentForm
    success_url = reverse_lazy("leads:lead_list")
    template_name = "leads/assign_agent.html"

    def get_form_kwargs(self, **kwargs) -> dict[str]:
        kwargs = super(AssignAgentview, self).get_form_kwargs(**kwargs)
        kwargs.update(
            {
                "request": self.request,
            }
        )
        return kwargs

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentview, self).form_valid(form)


class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = LeadCategoryUpdateForm
    template_name = "leads/lead_category_update.html"

    def get_queryset(self):
        user = self.request.user

        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            queryset = queryset.filter(agent__user=user)
        return queryset

    # def get_success_url(self):
    # return reverse_lazy("leads:lead_detail", kwargs={"pk": self.get_object().id})
