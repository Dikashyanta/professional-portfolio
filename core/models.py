from django.db import models


class Profile(models.Model):
    """Singleton-style model for your About/Hero content."""
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100, blank=True, help_text="e.g. Senior Software Engineer")
    location = models.CharField(max_length=100, blank=True)
    years_experience = models.PositiveIntegerField(blank=True, null=True)
    tagline = models.CharField(max_length=200, help_text="e.g. Full-stack developer building fast, accessible web apps")
    bio = models.TextField()
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    hero_image = models.ImageField(upload_to='profile/', blank=True, null=True, help_text="Larger image shown next to the hero heading")
    resume = models.FileField(upload_to='resume/', blank=True, null=True)
    email = models.EmailField()
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Ensures only one Profile object ever exists
        self.pk = 1
        super().save(*args, **kwargs)


class ResumeProfile(models.Model):
    """Singleton model — edit this one object to update the entire resume page."""

    # Identity
    full_name = models.CharField(max_length=150, help_text="Name shown at the top of the resume")
    job_title = models.CharField(max_length=150, blank=True, help_text="e.g. Senior Software Engineer")
    bio = models.TextField(blank=True, help_text="Short career summary paragraph")
    photo = models.ImageField(
        upload_to='resume/',
        blank=True,
        null=True,
        help_text="Profile photo shown on the resume (optional — leave blank to skip)",
    )

    # Contact info
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True, help_text="e.g. +977 98XXXXXXXX")
    location = models.CharField(max_length=100, blank=True, help_text="e.g. Kathmandu, Nepal")
    website = models.URLField(blank=True, help_text="Your portfolio / personal website URL")
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)

    # Downloadable PDF
    resume_pdf = models.FileField(
        upload_to='resume/',
        blank=True,
        null=True,
        help_text="PDF file for the Download button (optional)",
    )

    def __str__(self):
        return f"Resume — {self.full_name}"

    def save(self, *args, **kwargs):
        self.pk = 1  # singleton
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Resume"
        verbose_name_plural = "Resume"


# ── Section models linked to ResumeProfile ────────────────────────────────────

class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('database', 'Database'),
        ('tools', 'Tools & DevOps'),
        ('other', 'Other'),
    ]

    resume = models.ForeignKey(
        ResumeProfile, on_delete=models.CASCADE,
        related_name='skills', null=True, blank=True,
    )
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    icon = models.CharField(max_length=50, blank=True, help_text="FontAwesome class, e.g. fa-brands fa-python")
    description = models.TextField(blank=True, help_text="What you can do with this skill")

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    short_description = models.CharField(max_length=300, help_text="Shown on the card/preview")
    description = models.TextField(help_text="Full description, shown in detail/modal")
    image = models.ImageField(upload_to='projects/')
    tech_stack = models.ManyToManyField(Skill, blank=True)

    client = models.CharField(max_length=100, blank=True, help_text="e.g. Google, Dropbox")
    demo_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)

    featured = models.BooleanField(default=False, help_text="Show on homepage")
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers show first")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    author_name = models.CharField(max_length=100)
    author_title = models.CharField(max_length=150, help_text="e.g. Product Manager, Amazon")
    author_photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    quote = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.author_name} — {self.author_title}"


class WorkExperience(models.Model):
    resume = models.ForeignKey(
        ResumeProfile, on_delete=models.CASCADE,
        related_name='work_experiences', null=True, blank=True,
    )
    job_title = models.CharField(max_length=150)
    company = models.CharField(max_length=150)
    start_date = models.CharField(max_length=30, help_text="e.g. Jan 2020")
    end_date = models.CharField(max_length=30, blank=True, help_text="e.g. Present")
    description = models.TextField(blank=True)
    bullets = models.TextField(blank=True, help_text="One bullet point per line")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-start_date']

    def get_bullets(self):
        return [b.strip() for b in self.bullets.splitlines() if b.strip()]

    def __str__(self):
        return f"{self.job_title} @ {self.company}"


class Education(models.Model):
    resume = models.ForeignKey(
        ResumeProfile, on_delete=models.CASCADE,
        related_name='education_entries', null=True, blank=True,
    )
    degree = models.CharField(max_length=150)
    institution = models.CharField(max_length=150)
    start_year = models.CharField(max_length=10, blank=True)
    end_year = models.CharField(max_length=10, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.degree} — {self.institution}"


class Award(models.Model):
    resume = models.ForeignKey(
        ResumeProfile, on_delete=models.CASCADE,
        related_name='awards', null=True, blank=True,
    )
    title = models.CharField(max_length=150)
    issuer = models.CharField(max_length=150, blank=True)
    year = models.CharField(max_length=10, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Language(models.Model):
    resume = models.ForeignKey(
        ResumeProfile, on_delete=models.CASCADE,
        related_name='languages', null=True, blank=True,
    )
    name = models.CharField(max_length=80)
    proficiency = models.CharField(max_length=80, blank=True, help_text="e.g. Native, Professional")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Interest(models.Model):
    resume = models.ForeignKey(
        ResumeProfile, on_delete=models.CASCADE,
        related_name='interests', null=True, blank=True,
    )
    name = models.CharField(max_length=80)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class ResumeProject(models.Model):
    resume = models.ForeignKey(
        ResumeProfile, on_delete=models.CASCADE,
        related_name='projects', null=True, blank=True,
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, help_text="Short description of what the project does")
    tech_stack = models.CharField(
        max_length=300, blank=True,
        help_text="Comma-separated technologies, e.g. Python, Django, React",
    )
    github_url = models.URLField(blank=True, help_text="Link to the GitHub repository")
    live_url = models.URLField(blank=True, help_text="Link to the live/deployed project (optional)")
    is_open_source = models.BooleanField(default=False, help_text="Show 'Open Source' badge")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def get_tech_list(self):
        return [t.strip() for t in self.tech_stack.split(',') if t.strip()]

    def __str__(self):
        return self.title