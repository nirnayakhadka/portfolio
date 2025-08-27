# models.py - Updated models with PDF file support
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
import os

class Technology(models.Model):
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=7, default='#3B82F6', help_text='Hex color code')
    icon = models.CharField(max_length=50, blank=True, help_text='CSS class or icon name')
    
    class Meta:
        verbose_name_plural = "Technologies"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class ProjectCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    color = models.CharField(max_length=7, default='#6B7280', help_text='Hex color code')
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Project Categories"
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

def validate_file_size(value):
    """Validate file size - max 100MB for PDFs, 10MB for images"""
    filesize = value.size
    
    if value.name.lower().endswith('.pdf'):
        max_size = 100 * 1024 * 1024  # 100MB for PDFs
        if filesize > max_size:
            raise ValidationError(f"PDF file size cannot exceed 100MB. Current size: {filesize / (1024*1024):.1f}MB")
    else:
        max_size = 10 * 1024 * 1024  # 10MB for images
        if filesize > max_size:
            raise ValidationError(f"Image file size cannot exceed 10MB. Current size: {filesize / (1024*1024):.1f}MB")

def project_image_path(instance, filename):
    """Generate upload path for project images"""
    # Get file extension
    ext = filename.split('.')[-1]
    # Create filename using project slug and timestamp
    from django.utils import timezone
    timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{instance.slug}_{timestamp}.{ext}"
    return f'projects/images/{filename}'

def project_pdf_path(instance, filename):
    """Generate upload path for project PDFs"""
    # Get file extension
    ext = filename.split('.')[-1]
    # Create filename using project slug and original name (cleaned)
    safe_filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_', '.')).rstrip()
    return f'projects/pdfs/{instance.slug}/{safe_filename}'

class Project(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('in-progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on-hold', 'On Hold'),
    ]
    
    PRIORITY_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
        (4, 'Critical'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    
    # Project details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    category = models.ForeignKey(ProjectCategory, on_delete=models.SET_NULL, null=True, blank=True)
    technologies = models.ManyToManyField(Technology, blank=True)
    featured = models.BooleanField(default=False)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2)
    
    # Media files
    image = models.ImageField(
        upload_to=project_image_path,
        blank=True,
        null=True,
        validators=[validate_file_size, FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif', 'webp'])],
        help_text='Upload project image (max 10MB). Supported formats: JPG, PNG, GIF, WebP'
    )
    
    pdf_file = models.FileField(
        upload_to=project_pdf_path,
        blank=True,
        null=True,
        validators=[validate_file_size, FileExtensionValidator(['pdf'])],
        help_text='Upload project documentation (max 100MB). Only PDF files allowed.'
    )
    
    # External links
    github_url = models.URLField(blank=True, help_text='GitHub repository URL')
    demo_url = models.URLField(blank=True, help_text='Live demo URL')
    
    # Timestamps
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_date']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['featured']),
            models.Index(fields=['priority']),
            models.Index(fields=['-created_date']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            
        # Ensure unique slug
        original_slug = self.slug
        counter = 1
        while Project.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            self.slug = f"{original_slug}-{counter}"
            counter += 1
            
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        """Override delete to clean up files"""
        # Delete image file if it exists
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        
        # Delete PDF file if it exists
        if self.pdf_file:
            if os.path.isfile(self.pdf_file.path):
                os.remove(self.pdf_file.path)
                # Also try to remove the directory if it's empty
                try:
                    pdf_dir = os.path.dirname(self.pdf_file.path)
                    if os.path.exists(pdf_dir) and not os.listdir(pdf_dir):
                        os.rmdir(pdf_dir)
                except OSError:
                    pass  # Directory not empty or other OS error
        
        super().delete(*args, **kwargs)
    
    def get_absolute_url(self):
        """Return the URL for project detail page"""
        return reverse('home:project_detail', kwargs={'slug': self.slug})
    
    def get_file_info(self):
        """Get information about attached files"""
        info = {
            'has_image': bool(self.image),
            'has_pdf': bool(self.pdf_file),
            'image_size': self.image.size if self.image else 0,
            'pdf_size': self.pdf_file.size if self.pdf_file else 0,
        }
        info['total_size'] = info['image_size'] + info['pdf_size']
        return info
    
    @property
    def file_count(self):
        """Return total number of attached files"""
        count = 0
        if self.image:
            count += 1
        if self.pdf_file:
            count += 1
        return count
    
    def __str__(self):
        return self.title


from django.utils import timezone

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
    
