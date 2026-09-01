from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from blog.models import Post

from .forms import ContactForm
from .models import Profile, Project, Skill, Testimonial


def home(request):
    projects = Project.objects.filter(featured=True)[:4]
    testimonials = Testimonial.objects.all()
    posts = Post.objects.filter(published=True)[:3]

    skills = Skill.objects.all()

    context = {
        'projects': projects,
        'testimonials': testimonials,
        'posts': posts,
        'skills': skills,
    }
    return render(request, 'core/home.html', context)


def portfolio(request):
    projects = Project.objects.all()
    context = {'projects': projects}
    return render(request, 'core/portfolio.html', context)


def resume(request):
    from .models import ResumeProfile

    resume_profile = ResumeProfile.objects.prefetch_related(
        'work_experiences', 'skills', 'education_entries',
        'awards', 'languages', 'interests',
    ).first()

    skills_by_category = {}
    if resume_profile:
        for skill in resume_profile.skills.all():
            skills_by_category.setdefault(skill.get_category_display(), []).append(skill)

    context = {
        'resume_profile': resume_profile,
        'skills_by_category': skills_by_category,
    }
    return render(request, 'core/resume.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            service = form.cleaned_data['service']
            message_text = form.cleaned_data['message']

            send_mail(
                subject=f"New contact form message from {name}",
                message=f"From: {name} <{email}>\nService: {service}\n\n{message_text}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
            )
            messages.success(request, "Thanks! Your message has been sent.")
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'core/contact.html', {'form': form})
