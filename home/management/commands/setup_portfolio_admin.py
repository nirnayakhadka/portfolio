# management/commands/setup_portfolio_admin.py
# Create this file in: home/management/commands/setup_portfolio_admin.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from home.models import Project, Technology, ProjectCategory
from django.utils.text import slugify
import os

class Command(BaseCommand):
    help = 'Setup portfolio admin with sample data and superuser'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-superuser',
            action='store_true',
            help='Create a superuser account',
        )
        parser.add_argument(
            '--create-sample-data',
            action='store_true',
            help='Create sample projects, technologies, and categories',
        )
        parser.add_argument(
            '--username',
            type=str,
            default='admin',
            help='Username for superuser (default: admin)',
        )
        parser.add_argument(
            '--email',
            type=str,
            default='admin@example.com',
            help='Email for superuser',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Setting up Portfolio Admin...')
        )

        # Create superuser
        if options['create_superuser']:
            self.create_superuser(options['username'], options['email'])

        # Create sample data
        if options['create_sample_data']:
            self.create_sample_data()

        # Create necessary directories
        self.create_directories()

        self.stdout.write(
            self.style.SUCCESS('Portfolio Admin setup completed!')
        )

    def create_superuser(self, username, email):
        """Create superuser if it doesn't exist"""
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'Superuser "{username}" already exists.')
            )
            return

        user = User.objects.create_superuser(
            username=username,
            email=email,
            password='admin123'  # Change this in production!
        )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Superuser "{username}" created successfully!\n'
                f'Username: {username}\n'
                f'Password: admin123 (Please change this in production!)\n'
                f'Email: {email}'
            )
        )

    def create_sample_data(self):
        """Create sample technologies, categories, and projects"""
        
        # Create sample technologies
        technologies_data = [
            {'name': 'Python', 'color': '#3776ab', 'icon': 'fab fa-python'},
            {'name': 'Django', 'color': '#092e20', 'icon': 'fas fa-server'},
            {'name': 'JavaScript', 'color': '#f7df1e', 'icon': 'fab fa-js-square'},
            {'name': 'React', 'color': '#61dafb', 'icon': 'fab fa-react'},
            {'name': 'HTML5', 'color': '#e34f26', 'icon': 'fab fa-html5'},
            {'name': 'CSS3', 'color': '#1572b6', 'icon': 'fab fa-css3-alt'},
            {'name': 'PostgreSQL', 'color': '#336791', 'icon': 'fas fa-database'},
            {'name': 'Git', 'color': '#f05032', 'icon': 'fab fa-git-alt'},
        ]

        for tech_data in technologies_data:
            tech, created = Technology.objects.get_or_create(
                name=tech_data['name'],
                defaults={
                    'color': tech_data['color'],
                    'icon': tech_data['icon']
                }
            )
            if created:
                self.stdout.write(f'Created technology: {tech.name}')

        # Create sample categories
        categories_data = [
            {'name': 'Web Development', 'color': '#667eea'},
            {'name': 'Mobile Apps', 'color': '#764ba2'},
            {'name': 'Data Science', 'color': '#f093fb'},
            {'name': 'API Development', 'color': '#4facfe'},
        ]

        for cat_data in categories_data:
            category, created = ProjectCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'slug': slugify(cat_data['name']),
                    'color': cat_data['color']
                }
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create sample projects
        web_dev_category = ProjectCategory.objects.get(name='Web Development')
        python_tech = Technology.objects.get(name='Python')
        django_tech = Technology.objects.get(name='Django')
        js_tech = Technology.objects.get(name='JavaScript')

        projects_data = [
            {
                'title': 'Portfolio Website',
                'description': 'A personal portfolio website built with Django and modern web technologies.',
                'status': 'completed',
                'category': web_dev_category,
                'featured': True,
                'priority': 1,
                'technologies': [python_tech, django_tech, js_tech],
                'github_url': 'https://github.com/username/portfolio',
                'demo_url': 'https://portfolio.example.com',
            },
            {
                'title': 'E-commerce Platform',
                'description': 'A full-featured e-commerce platform with payment integration.',
                'status': 'in-progress',
                'category': web_dev_category,
                'featured': True,
                'priority': 2,
                'technologies': [python_tech, django_tech],
                'github_url': 'https://github.com/username/ecommerce',
            },
            {
                'title': 'Blog System',
                'description': 'A content management system for blogging with admin interface.',
                'status': 'planned',
                'category': web_dev_category,
                'featured': False,
                'priority': 3,
                'technologies': [python_tech, django_tech],
            }
        ]

        for project_data in projects_data:
            technologies = project_data.pop('technologies')
            project, created = Project.objects.get_or_create(
                title=project_data['title'],
                defaults={
                    **project_data,
                    'slug': slugify(project_data['title'])
                }
            )
            
            if created:
                # Add technologies to the project
                project.technologies.set(technologies)
                self.stdout.write(f'Created project: {project.title}')

        self.stdout.write(
            self.style.SUCCESS('Sample data created successfully!')
        )

    def create_directories(self):
        """Create necessary directories for the application"""
        from django.conf import settings
        
        directories = [
            'media/projects',
            'static/admin/css',
            'static/admin/js',
            'templates/admin',
            'reports',
            'logs',
        ]

        for directory in directories:
            dir_path = os.path.join(settings.BASE_DIR, directory)
            os.makedirs(dir_path, exist_ok=True)
            self.stdout.write(f'Created directory: {directory}')

        # Create empty __init__.py files for management commands
        management_dirs = [
            'home/management',
            'home/management/commands',
        ]
        
        for directory in management_dirs:
            dir_path = os.path.join(settings.BASE_DIR, directory)
            os.makedirs(dir_path, exist_ok=True)
            
            init_file = os.path.join(dir_path, '__init__.py')
            if not os.path.exists(init_file):
                open(init_file, 'a').close()
                self.stdout.write(f'Created __init__.py in {directory}')

        self.stdout.write(
            self.style.SUCCESS('All directories created successfully!')
        )