# admin.py - Fixed admin file with corrected URL reference
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.http import HttpResponse
from django.contrib import messages
from django.core.files.storage import default_storage
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from io import BytesIO
import json
import os
from datetime import datetime
from .models import Project, Technology, ProjectCategory

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'icon', 'colored_name', 'projects_count']
    list_editable = ['color', 'icon']
    search_fields = ['name']
    ordering = ['name']
    actions = ['export_technologies_pdf']
    
    def colored_name(self, obj):
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            obj.color,
            obj.name
        )
    colored_name.short_description = 'Name (Colored)'
    
    def projects_count(self, obj):
        count = obj.project_set.count()
        if count > 0:
            # FIXED: Corrected the URL reference
            url = reverse('admin:home_project_changelist') + f'?technologies__id__exact={obj.id}'
            return format_html('<a href="{}">{} projects</a>', url, count)
        return '0 projects'
    projects_count.short_description = 'Projects'
    
    def export_technologies_pdf(self, request, queryset):
        return self.generate_technologies_report(queryset)
    export_technologies_pdf.short_description = "Export selected technologies to PDF"
    
    def generate_technologies_report(self, queryset):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title = Paragraph("Technologies Report", styles['Title'])
        story.append(title)
        story.append(Spacer(1, 20))
        
        # Report info
        report_info = Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal'])
        story.append(report_info)
        story.append(Spacer(1, 20))
        
        # Technologies table
        data = [['Technology', 'Color', 'Icon', 'Projects Count']]
        
        for tech in queryset:
            data.append([
                tech.name,
                tech.color,
                tech.icon or 'N/A',
                str(tech.project_set.count()),
            ])
        
        table = Table(data, colWidths=[2*inch, 1.5*inch, 1*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(table)
        doc.build(story)
        
        buffer.seek(0)
        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="technologies_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf"'
        return response

@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'slug', 'projects_count', 'created_date']
    list_editable = ['color']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    ordering = ['name']
    actions = ['export_categories_pdf']
    
    def projects_count(self, obj):
        count = obj.project_set.count()
        if count > 0:
            url = reverse('admin:home_project_changelist') + f'?category__id__exact={obj.id}'
            return format_html('<a href="{}">{} projects</a>', url, count)
        return '0 projects'
    projects_count.short_description = 'Projects'
    
    def export_categories_pdf(self, request, queryset):
        return self.generate_categories_report(queryset)
    export_categories_pdf.short_description = "Export selected categories to PDF"
    
    def generate_categories_report(self, queryset):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title = Paragraph("Project Categories Report", styles['Title'])
        story.append(title)
        story.append(Spacer(1, 20))
        
        # Report info
        report_info = Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal'])
        story.append(report_info)
        story.append(Spacer(1, 20))
        
        # Categories table
        data = [['Category', 'Slug', 'Color', 'Projects Count', 'Created Date']]
        
        for category in queryset:
            data.append([
                category.name,
                category.slug,
                category.color,
                str(category.project_set.count()),
                category.created_date.strftime('%Y-%m-%d')
            ])
        
        table = Table(data, colWidths=[1.5*inch, 1.5*inch, 1*inch, 1*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(table)
        doc.build(story)
        
        buffer.seek(0)
        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="categories_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"'
        return response

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'status', 'status_colored', 'category', 'featured', 
        'priority', 'technologies_display', 'has_demo', 'has_attachments', 'created_date'
    ]
    list_filter = [
        'status', 'category', 'featured', 'priority', 'technologies', 'created_date'
    ]
    list_editable = ['status', 'featured', 'priority']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['technologies']
    date_hierarchy = 'created_date'
    readonly_fields = ['created_date', 'updated_date', 'image_preview', 'pdf_info', 'file_sizes']
    actions = [
        'mark_as_completed', 'mark_as_featured', 'mark_as_in_progress',
        'delete_selected_projects', 'export_projects_summary_pdf', 'export_projects_detailed_pdf'
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description')
        }),
        ('Project Details', {
            'fields': ('status', 'category', 'technologies', 'featured', 'priority')
        }),
        ('Media & Files', {
            'fields': ('image', 'image_preview', 'pdf_file', 'pdf_info', 'file_sizes'),
            'description': 'Upload project image and/or PDF documentation'
        }),
        ('Links', {
            'fields': ('github_url', 'demo_url'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_date', 'updated_date'),
            'classes': ('collapse',)
        })
    )
    
    def status_colored(self, obj):
        colors_map = {
            'planned': '#c084fc',
            'in-progress': '#facc15',
            'completed': '#4ade80',
            'on-hold': '#f87171',
        }
        color = colors_map.get(obj.status, '#94a3b8')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_colored.short_description = 'Status'
    status_colored.admin_order_field = 'status'
    
    def technologies_display(self, obj):
        techs = obj.technologies.all()[:3]
        if not techs:
            return '-'
        
        tech_html = []
        for tech in techs:
            tech_html.append(
                format_html(
                    '<span style="background-color: {}; color: white; padding: 2px 6px; '
                    'border-radius: 3px; font-size: 10px; margin-right: 2px;">{}</span>',
                    tech.color,
                    tech.name
                )
            )
        
        total_count = obj.technologies.count()
        if total_count > 3:
            tech_html.append(f'+{total_count - 3} more')
            
        return mark_safe(''.join(tech_html))
    technologies_display.short_description = 'Technologies'
    
    def has_demo(self, obj):
        if obj.demo_url:
            return format_html(
                '<a href="{}" target="_blank" style="color: #059669;">🔗 Demo</a>',
                obj.demo_url
            )
        return format_html('<span style="color: #94a3b8;">No Demo</span>')
    has_demo.short_description = 'Demo Link'
    
    def has_attachments(self, obj):
        attachments = []
        if obj.image:
            attachments.append('📷 Image')
        if hasattr(obj, 'pdf_file') and obj.pdf_file:
            attachments.append('📄 PDF')
        
        if attachments:
            return format_html(
                '<span style="color: #059669;">{}</span>',
                ' | '.join(attachments)
            )
        return format_html('<span style="color: #94a3b8;">No Files</span>')
    has_attachments.short_description = 'Files'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="150" height="100" '
                'style="object-fit: cover; border-radius: 5px;" />',
                obj.image.url
            )
        return "No image uploaded"
    image_preview.short_description = 'Image Preview'
    
    def pdf_info(self, obj):
        if hasattr(obj, 'pdf_file') and obj.pdf_file:
            file_size = self.format_file_size(obj.pdf_file.size)
            file_name = os.path.basename(obj.pdf_file.name)
            
            return format_html(
                '<div style="border: 1px solid #ddd; padding: 10px; border-radius: 5px; background-color: #f9f9f9;">'
                '<strong>📄 {}</strong><br/>'
                '<span style="color: #666;">Size: {}</span><br/>'
                '<a href="{}" target="_blank" style="color: #059669; text-decoration: none;">'
                '🔗 View PDF</a>'
                '</div>',
                file_name[:50] + ('...' if len(file_name) > 50 else ''),
                file_size,
                obj.pdf_file.url
            )
        return "No PDF uploaded"
    pdf_info.short_description = 'PDF Document'
    
    def file_sizes(self, obj):
        info = []
        total_size = 0
        
        if obj.image:
            size = obj.image.size
            total_size += size
            info.append(f"Image: {self.format_file_size(size)}")
        
        if hasattr(obj, 'pdf_file') and obj.pdf_file:
            size = obj.pdf_file.size
            total_size += size
            info.append(f"PDF: {self.format_file_size(size)}")
        
        if info:
            info.append(f"<strong>Total: {self.format_file_size(total_size)}</strong>")
            return format_html('<br/>'.join(info))
        
        return "No files uploaded"
    file_sizes.short_description = 'File Sizes'
    
    def format_file_size(self, size_bytes):
        """Convert bytes to human readable format"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB"]
        import math
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_names[i]}"
    
    # Custom Actions
    def mark_as_completed(self, request, queryset):
        count = queryset.update(status='completed')
        self.message_user(request, f'{count} projects marked as completed.', messages.SUCCESS)
    mark_as_completed.short_description = "Mark selected projects as completed"
    
    def mark_as_featured(self, request, queryset):
        count = queryset.update(featured=True)
        self.message_user(request, f'{count} projects marked as featured.', messages.SUCCESS)
    mark_as_featured.short_description = "Mark selected projects as featured"
    
    def mark_as_in_progress(self, request, queryset):
        count = queryset.update(status='in-progress')
        self.message_user(request, f'{count} projects marked as in progress.', messages.SUCCESS)
    mark_as_in_progress.short_description = "Mark selected projects as in progress"
    
    def delete_selected_projects(self, request, queryset):
        """Custom delete action that properly handles file cleanup and shows detailed results"""
        deleted_count = 0
        failed_deletions = []
        
        for project in queryset:
            try:
                project_title = project.title
                
                # Handle image deletion if exists
                if project.image:
                    try:
                        project.image.delete(save=False)
                    except Exception as img_error:
                        # Log image deletion error but continue with project deletion
                        pass
                
                # Handle PDF deletion if exists
                if hasattr(project, 'pdf_file') and project.pdf_file:
                    try:
                        project.pdf_file.delete(save=False)
                    except Exception as pdf_error:
                        # Log PDF deletion error but continue with project deletion
                        pass
                
                # Delete the project
                project.delete()
                deleted_count += 1
                
            except Exception as e:
                failed_deletions.append(f"'{project.title}': {str(e)}")
        
        # Show success message
        if deleted_count > 0:
            self.message_user(
                request, 
                f'Successfully deleted {deleted_count} project{"s" if deleted_count > 1 else ""}.', 
                messages.SUCCESS
            )
        
        # Show error messages for failed deletions
        if failed_deletions:
            for error in failed_deletions[:5]:  # Limit error messages to avoid clutter
                self.message_user(request, f'Failed to delete {error}', messages.ERROR)
            
            if len(failed_deletions) > 5:
                self.message_user(
                    request, 
                    f'...and {len(failed_deletions) - 5} more deletion errors.', 
                    messages.ERROR
                )
    
    delete_selected_projects.short_description = "🗑️ Delete selected projects"
    
    def export_projects_summary_pdf(self, request, queryset):
        return self.generate_projects_report(queryset, detailed=False)
    export_projects_summary_pdf.short_description = "📄 Export summary PDF"
    
    def export_projects_detailed_pdf(self, request, queryset):
        return self.generate_projects_report(queryset, detailed=True)
    export_projects_detailed_pdf.short_description = "📋 Export detailed PDF"
    
    def generate_projects_report(self, queryset, detailed=False):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.HexColor('#1e293b')
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.HexColor('#475569')
        )
        
        # Title
        report_type = "Detailed" if detailed else "Summary"
        title = Paragraph(f"Projects Report ({report_type})", title_style)
        story.append(title)
        story.append(Spacer(1, 20))
        
        # Report info
        report_info = Paragraph(
            f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>"
            f"Total Projects: {queryset.count()}", 
            styles['Normal']
        )
        story.append(report_info)
        story.append(Spacer(1, 30))
        
        if detailed:
            # Detailed report - one project per section
            for project in queryset:
                # Project title
                project_title = Paragraph(project.title, subtitle_style)
                story.append(project_title)
                
                # Project details table
                project_data = [
                    ['Status:', project.get_status_display()],
                    ['Category:', project.category.name if project.category else 'N/A'],
                    ['Featured:', 'Yes' if project.featured else 'No'],
                    ['Priority:', str(project.priority)],
                    ['Created:', project.created_date.strftime('%Y-%m-%d')],
                    ['GitHub:', project.github_url if project.github_url else 'N/A'],
                    ['Demo:', project.demo_url if project.demo_url else 'N/A'],
                ]
                
                # File attachments info
                attachments = []
                if project.image:
                    attachments.append(f"Image ({self.format_file_size(project.image.size)})")
                if hasattr(project, 'pdf_file') and project.pdf_file:
                    attachments.append(f"PDF ({self.format_file_size(project.pdf_file.size)})")
                
                project_data.append(['Files:', ', '.join(attachments) or 'N/A'])
                
                # Technologies
                tech_names = ', '.join([tech.name for tech in project.technologies.all()]) or 'N/A'
                project_data.append(['Technologies:', tech_names])
                
                project_table = Table(project_data, colWidths=[1.5*inch, 4.5*inch])
                project_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                ]))
                
                story.append(project_table)
                story.append(Spacer(1, 12))
                
                # Description
                if project.description:
                    desc_title = Paragraph("Description:", styles['Heading3'])
                    story.append(desc_title)
                    
                    # Clean description for PDF
                    clean_desc = project.description.replace('<br>', '\n').replace('<p>', '').replace('</p>', '\n')
                    description = Paragraph(clean_desc[:500] + ('...' if len(clean_desc) > 500 else ''), styles['Normal'])
                    story.append(description)
                
                story.append(Spacer(1, 30))
        else:
            # Summary report - table format
            data = [['Project', 'Status', 'Category', 'Technologies', 'Files', 'Featured', 'Created']]
            
            for project in queryset:
                tech_names = ', '.join([tech.name for tech in project.technologies.all()[:2]])
                if project.technologies.count() > 2:
                    tech_names += f' (+{project.technologies.count() - 2})'
                
                # File info for summary
                file_info = []
                if project.image:
                    file_info.append('IMG')
                if hasattr(project, 'pdf_file') and project.pdf_file:
                    file_info.append('PDF')
                
                data.append([
                    project.title[:20] + '...' if len(project.title) > 20 else project.title,
                    project.get_status_display(),
                    (project.category.name[:12] + '...' if len(project.category.name) > 12 else project.category.name) if project.category else 'N/A',
                    tech_names or 'N/A',
                    ','.join(file_info) or 'None',
                    'Yes' if project.featured else 'No',
                    project.created_date.strftime('%Y-%m-%d')
                ])
            
            table = Table(data, colWidths=[1.5*inch, 0.8*inch, 0.8*inch, 1.2*inch, 0.6*inch, 0.5*inch, 0.8*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            
            story.append(table)
        
        doc.build(story)
        
        buffer.seek(0)
        report_type_file = "detailed" if detailed else "summary"
        filename = f"projects_{report_type_file}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    
    # Override delete methods to ensure proper cleanup
    def delete_model(self, request, obj):
        """Called when deleting a single object from change form"""
        try:
            project_title = obj.title
            
            # Handle image deletion
            if obj.image:
                try:
                    obj.image.delete(save=False)
                except Exception:
                    pass  # Continue even if image deletion fails
            
            # Handle PDF deletion
            if hasattr(obj, 'pdf_file') and obj.pdf_file:
                try:
                    obj.pdf_file.delete(save=False)
                except Exception:
                    pass  # Continue even if PDF deletion fails
            
            obj.delete()
            self.message_user(request, f'Project "{project_title}" deleted successfully.', messages.SUCCESS)
            
        except Exception as e:
            self.message_user(request, f'Error deleting project: {str(e)}', messages.ERROR)

    def delete_queryset(self, request, queryset):
        """Called when using the default 'delete selected' action"""
        # This will use our custom delete_selected_projects logic
        self.delete_selected_projects(request, queryset)

# Customize admin site headers
admin.site.site_header = "Nirnaya's Portfolio Admin"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Welcome to Portfolio Administration"

from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject')
    readonly_fields = ('created_at',)
    list_per_page = 25
    
    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'subject', 'message')
        }),
        ('Status', {
            'fields': ('is_read', 'created_at')
        }),
    )
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected messages as unread"
    
    actions = ['mark_as_read', 'mark_as_unread']
