# home/views.py
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Project, Technology, ProjectCategory
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.core.mail import send_mail
from django.conf import settings

def index(request):
    """Home page view - Single page portfolio"""
    context = {
        'page_title': 'Portfolio',
    }
    return render(request, 'home/index.html', context)

def about(request):
    return render(request, 'home/about.html')

def projects_view(request):
    """Projects page view with filtering and pagination"""
    # Get all projects
    projects = Project.objects.all().order_by('-created_date')
    
    # Handle search
    search_query = request.GET.get('search')
    if search_query:
        projects = projects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(technologies__name__icontains=search_query)
        ).distinct()
    
    # Handle category filtering
    category_slug = request.GET.get('category')
    if category_slug:
        projects = projects.filter(category__slug=category_slug)
    
    # Handle status filtering
    status = request.GET.get('status')
    if status:
        projects = projects.filter(status=status)
    
    # Handle technology filtering
    tech_id = request.GET.get('technology')
    if tech_id:
        projects = projects.filter(technologies__id=tech_id)
    
    # Pagination
    paginator = Paginator(projects, 12)  # 12 projects per page
    page_number = request.GET.get('page')
    projects = paginator.get_page(page_number)
    
    # Get all categories and technologies for filters
    categories = ProjectCategory.objects.all()
    technologies = Technology.objects.all()
    
    context = {
        'projects': projects,
        'categories': categories,
        'technologies': technologies,
        'search_query': search_query,
        'current_category': category_slug,
        'current_status': status,
        'current_technology': tech_id,
    }
    
    # Make sure to use the correct template name
    return render(request, 'home/project.html', context)

def project_detail_view(request, slug):
    """Individual project detail view"""
    project = get_object_or_404(Project, slug=slug)
    
    # Get related projects (same category, excluding current)
    related_projects = Project.objects.filter(
        category=project.category
    ).exclude(id=project.id)[:3]
    
    context = {
        'project': project,
        'related_projects': related_projects,
    }
    return render(request, 'home/project_detail.html', context)

def about_view(request):
    """About page view"""
    context = {}
    return render(request, 'home/about.html', context)


# API views for AJAX requests (if needed)
from django.http import JsonResponse

def projects_api(request):
    """API endpoint for projects (for AJAX requests)"""
    projects = Project.objects.all()
    
    # Handle filtering
    status = request.GET.get('status')
    if status and status != 'all':
        projects = projects.filter(status=status)
    
    search = request.GET.get('search')
    if search:
        projects = projects.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )
    
    # Convert to JSON
    projects_data = []
    for project in projects:
        projects_data.append({
            'id': project.id,
            'title': project.title,
            'description': project.description[:120] + '...' if len(project.description) > 120 else project.description,
            'status': project.status,
            'status_display': project.get_status_display(),
            'image_url': project.image.url if project.image else None,
            'github_url': project.github_url,
            'demo_url': project.demo_url,
            'technologies': [tech.name for tech in project.technologies.all()],
            'created_date': project.created_date.strftime('%Y-%m-%d'),
        })
    
    return JsonResponse({'projects': projects_data})

def projects_list(request):
    """Display all projects with filtering and pagination"""
    projects = Project.objects.all().order_by('-created_date')
    
    # Add pagination if needed
    paginator = Paginator(projects, 12)  # Show 12 projects per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'projects': page_obj,
    }
    return render(request, 'projects/projects.html', context)

def project_detail(request, project_id):
    """Display detailed view of a specific project"""
    project = get_object_or_404(Project, id=project_id)
    
    # Get related projects (same technology or category)
    related_projects = Project.objects.filter(
        technologies__in=project.technologies.all()
    ).exclude(id=project.id).distinct()[:4]
    
    context = {
        'project': project,
        'related_projects': related_projects,
    }
    return render(request, 'projects/project_detail.html', context)

@csrf_protect
def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        if name and email and subject and message:
            try:
                # Option 1: Send email (configure your email settings first)
                full_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
                send_mail(
                    subject=f"Contact Form: {subject}",
                    message=full_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=['your-email@example.com'],  # Replace with your email
                    fail_silently=False,
                )
                
                # Option 2: Save to database (if you have a Contact model)
                # Contact.objects.create(name=name, email=email, subject=subject, message=message)
                
                messages.success(request, 'Thank you! Your message has been sent successfully.')
                
                # For AJAX requests
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': True, 'message': 'Message sent successfully!'})
                    
            except Exception as e:
                messages.error(request, 'Sorry, there was an error sending your message. Please try again.')
                
                # For AJAX requests
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'message': 'Error sending message.'})
        else:
            messages.error(request, 'Please fill in all fields.')
            
            # For AJAX requests
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Please fill in all fields.'})
    
    return render(request, 'home/contact.html')

from .models import ContactMessage
from .forms import ContactForm
from django.shortcuts import redirect

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save to database
            contact_message = form.save()
            
            # Send email to you
            try:
                subject = f"New Contact Form Submission: {form.cleaned_data['subject']}"
                message = f"""
New contact form submission from your website:

Name: {form.cleaned_data['name']}
Email: {form.cleaned_data['email']}
Subject: {form.cleaned_data['subject']}

Message:
{form.cleaned_data['message']}

Submitted at: {contact_message.created_at.strftime('%Y-%m-%d %H:%M:%S')}
                """
                
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    ['nirnayakhadka98@gmail.com'],  # Your Gmail
                    fail_silently=False,
                )
                
                # Send confirmation email to sender
                confirmation_subject = "Thank you for contacting Nirnaya Khadka"
                confirmation_message = f"""
Hi {form.cleaned_data['name']},

Thank you for reaching out! I have received your message about "{form.cleaned_data['subject']}" and will get back to you within 24 hours.

Best regards,
Nirnaya Khadka
AI & Machine Learning Specialist

---
This is an automated confirmation email.
                """
                
                send_mail(
                    confirmation_subject,
                    confirmation_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [form.cleaned_data['email']],
                    fail_silently=True,  # Don't fail if confirmation email fails
                )
                
                messages.success(request, 'Your email has been sent successfully! I will get back to you soon.')
                
            except Exception as e:
                messages.error(request, 'Sorry, there was an error sending your email. Please try again or contact me directly.')
            
            return redirect('/contact/')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = ContactForm()
    
    return render(request, 'home/contact.html', {'form': form})

