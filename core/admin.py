from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Profile, Skill, Project, Testimonial,
    ResumeProfile, WorkExperience, Education, Award, Language, Interest,
    ResumeProject,
)


# ── General site models ────────────────────────────────────────────────────────

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'tagline', 'email')

    def has_add_permission(self, request):
        return not Profile.objects.exists()


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'resume')
    list_filter = ('category',)
    search_fields = ('name', 'description')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'featured', 'order', 'created_at')
    list_filter = ('featured',)
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tech_stack',)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'author_title', 'order')


# ── Resume inline classes ──────────────────────────────────────────────────────

class WorkExperienceInline(admin.StackedInline):
    model = WorkExperience
    extra = 1
    fields = ('job_title', 'company', 'start_date', 'end_date', 'description', 'bullets', 'order')
    ordering = ('order',)
    verbose_name = "Work Experience"
    verbose_name_plural = "✦ Work Experiences"


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1
    fields = ('name', 'category', 'icon', 'description', 'order')
    ordering = ('category', 'name')
    verbose_name = "Skill"
    verbose_name_plural = "✦ Skills"

    # Provide ordering field
    def get_fields(self, request, obj=None):
        return ('name', 'category', 'icon', 'description')


class EducationInline(admin.TabularInline):
    model = Education
    extra = 1
    fields = ('degree', 'institution', 'start_year', 'end_year', 'order')
    ordering = ('order',)
    verbose_name = "Education"
    verbose_name_plural = "✦ Education"


class AwardInline(admin.TabularInline):
    model = Award
    extra = 1
    fields = ('title', 'issuer', 'year', 'order')
    ordering = ('order',)
    verbose_name = "Award"
    verbose_name_plural = "✦ Awards"


class LanguageInline(admin.TabularInline):
    model = Language
    extra = 1
    fields = ('name', 'proficiency', 'order')
    ordering = ('order',)
    verbose_name = "Language"
    verbose_name_plural = "✦ Languages"


class InterestInline(admin.TabularInline):
    model = Interest
    extra = 1
    fields = ('name', 'order')
    ordering = ('order',)
    verbose_name = "Interest"
    verbose_name_plural = "✦ Interests"


class ResumeProjectInline(admin.StackedInline):
    model = ResumeProject
    extra = 1
    fields = ('title', 'description', 'tech_stack', 'github_url', 'live_url', 'is_open_source', 'order')
    ordering = ('order',)
    verbose_name = "Project"
    verbose_name_plural = "✦ Projects"


# ── Master Resume admin ────────────────────────────────────────────────────────

@admin.register(ResumeProfile)
class ResumeProfileAdmin(admin.ModelAdmin):
    """One page to rule them all — edit your entire resume here."""

    # ── Fieldsets group the top-level fields into collapsible sections ──
    fieldsets = (
        ("🧑 Identity", {
            'description': 'Your name, title, and career summary shown at the top of the resume.',
            'fields': ('full_name', 'job_title', 'bio', 'photo'),
        }),
        ("📞 Contact Information", {
            'description': 'Contact details shown in the top-right of the resume.',
            'fields': ('email', 'phone', 'location', 'website', 'github_url', 'linkedin_url'),
        }),
        ("📄 Downloadable PDF", {
            'description': 'Upload a PDF and a Download button will appear on the resume page.',
            'fields': ('resume_pdf',),
            'classes': ('collapse',),
        }),
    )

    # ── All resume sections appear as inline tables below the main form ──
    inlines = [
        WorkExperienceInline,
        ResumeProjectInline,
        SkillInline,
        EducationInline,
        AwardInline,
        LanguageInline,
        InterestInline,
    ]

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="height:60px;border-radius:50%;"/>', obj.photo.url)
        return "No photo"
    photo_preview.short_description = "Photo"

    def has_add_permission(self, request):
        # Only one resume object allowed
        return not ResumeProfile.objects.exists()

    def changelist_view(self, request, extra_context=None):
        """Redirect straight to the edit page since there's only one object."""
        from django.urls import reverse
        obj, _ = ResumeProfile.objects.get_or_create(pk=1, defaults={'full_name': 'Your Name'})
        url = reverse('admin:core_resumeprofile_change', args=[obj.pk])
        from django.shortcuts import redirect
        return redirect(url)
