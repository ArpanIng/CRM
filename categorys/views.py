from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from agents.mixins import OrganisorAndLoginRequiredMixin
from leads.models import Lead, Category

from .forms import CategoryModelForm


class CategoryListView(LoginRequiredMixin, generic.ListView):
    context_object_name = "categories"
    template_name = "categorys/category_list.html"

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
        context.update(
            {
                "unassigned_lead_count": queryset.filter(category__isnull=True).count(),
            }
        )
        return context

    def get_queryset(self):
        user = self.request.user

        # Return leads associated to the organisation.
        if user.is_organisor:
            queryset = Category.objects.filter(organisation=user.userprofile)
        else:  # is_agent
            # Return leads associated to the agent organisation.
            queryset = Category.objects.filter(organisation=user.agent.organisation)
        return queryset


class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    context_object_name = "category"
    template_name = "categorys/category_detail.html"

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        # leads = related_name attribute from Lead model
        leads = self.get_object().leads.all()

        context.update(
            {
                "leads": leads,
            }
        )
        return context

    def get_queryset(self):
        user = self.request.user

        if user.is_organisor:
            queryset = Category.objects.filter(organisation=user.userprofile)
        else:
            queryset = Category.objects.filter(organisation=user.agent.organisation)
        return queryset


class CategoryCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = CategoryModelForm
    success_url = reverse_lazy("categorys:category_list")
    template_name = "categorys/category_create.html"

    def form_valid(self, form):
        category = form.save(commit=False)
        category.organisation = self.request.user.userprofile
        category.save()
        return super(CategoryCreateView, self).form_valid(form)


class CategoryUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    form_class = CategoryModelForm
    success_url = reverse_lazy("categorys:category_list")
    template_name = "categorys/category_update.html"

    def get_queryset(self):
        user = self.request.user

        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
        return queryset


class CategoryDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    success_url = reverse_lazy("categorys:category_list")
    template_name = "categorys/category_delete.html"

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Category.objects.filter(organisation=user.userprofile)
        else:
            queryset = Category.objects.filter(organisation=user.agent.organisation)
        return queryset
