from django.db import models


class Profile(models.Model):
    """Singleton-style model for your About/Hero content."""
    name = models.CharField(max_length=100)
    tagline = models.CharField(max_length=200, help_text="e.g. Full-stack developer building fast, accessible web apps")
    bio = models.TextField()
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
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


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('database', 'Database'),
        ('tools', 'Tools & DevOps'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=50)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    icon = models.CharField(max_length=50, blank=True, help_text="Optional: icon class name or short code")

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


class Experience(models.Model):
    title = models.CharField(max_length=100, help_text="e.g. Senior Software Engineer")
    location = models.CharField(max_length=100, blank=True)
    years_experience = models.PositiveIntegerField(blank=True, null=True)

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