import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4o-mini"

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
MAX_CONTENT_LENGTH = 5 * 1024 * 1024
ALLOWED_EXTENSIONS = {"pdf"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# COMPLETE TECH ROLES CONFIGURATION (20+ roles)
ROLE_CONFIG = {
    # Frontend & Web
    "web_developer": {
        "label": "Web Developer",
        "required_skills": ["html", "css", "javascript", "responsive", "react", "frontend"],
        "nice_to_have": ["node", "bootstrap", "tailwind", "git"],
        "suggestions": ["Build responsive portfolio", "Learn React/Next.js", "Add Tailwind CSS"]
    },

    # Backend Languages
    "python_developer": {
        "label": "Python Developer",
        "required_skills": ["python", "flask", "django", "oop", "rest", "api"],
        "nice_to_have": ["sql", "pandas", "docker", "pytest"],
        "suggestions": ["Add FastAPI experience", "Build REST APIs", "Learn Docker"]
    },

    "java_developer": {
        "label": "Java Developer",
        "required_skills": ["java", "spring", "spring boot", "maven", "jpa", "hibernate"],
        "nice_to_have": ["microservices", "kafka", "docker", "aws"],
        "suggestions": ["Learn Spring Boot 3", "Build microservices", "Add Kafka experience"]
    },

    "cpp_developer": {
        "label": "C++ Developer",
        "required_skills": ["c++", "stl", "oop", "memory management", "pointers", "algorithms"],
        "nice_to_have": ["multithreading", "boost", "qt", "opengl"],
        "suggestions": ["Master STL containers", "Practice LeetCode C++", "Learn multithreading"]
    },

    "c_developer": {
        "label": "C Developer",
        "required_skills": ["c", "pointers", "memory management", "linux", "embedded"],
        "nice_to_have": ["multithreading", "sockets", "posix"],
        "suggestions": ["Practice embedded systems", "Master pointers", "Linux kernel contrib"]
    },

    "ruby_developer": {
        "label": "Ruby Developer",
        "required_skills": ["ruby", "rails", "ror", "postgresql", "redis"],
        "nice_to_have": ["sidekiq", "rspec", "heroku"],
        "suggestions": ["Build Rails SaaS app", "Learn RSpec TDD", "Deploy to Heroku"]
    },

    # Full Stack & Mobile
    "full_stack_developer": {
        "label": "Full Stack Developer",
        "required_skills": ["html", "css", "javascript", "react", "node", "python", "rest"],
        "nice_to_have": ["docker", "aws", "graphql"],
        "suggestions": ["Build MERN stack project", "Deploy to Vercel", "Learn GraphQL"]
    },

    "android_developer": {
        "label": "Android Developer",
        "required_skills": ["kotlin", "java", "android studio", "jetpack", "mvvm"],
        "nice_to_have": ["coroutines", "room", "retrofit"],
        "suggestions": ["Build weather app", "Learn Jetpack Compose", "Publish to Play Store"]
    },

    # Data & ML
    "data_analyst": {
        "label": "Data Analyst",
        "required_skills": ["sql", "excel", "power bi", "tableau", "python"],
        "nice_to_have": ["pandas", "statistics", "etl"],
        "suggestions": ["Build Tableau dashboard", "Learn SQL window functions"]
    },

    "data_scientist": {
        "label": "Data Scientist",
        "required_skills": ["python", "pandas", "numpy", "scikit-learn", "machine learning"],
        "nice_to_have": ["tensorflow", "pytorch", "aws sagemaker"],
        "suggestions": ["Kaggle competitions", "Deploy ML model to Streamlit"]
    },

    "ml_engineer": {
        "label": "ML Engineer",
        "required_skills": ["python", "tensorflow", "pytorch", "docker", "mlflow"],
        "nice_to_have": ["kubeflow", "aws sage", "mleap"],
        "suggestions": ["Productionize ML model", "Learn MLOps pipeline"]
    },

    # DevOps & Cloud
    "devops_engineer": {
        "label": "DevOps Engineer",
        "required_skills": ["docker", "kubernetes", "jenkins", "terraform", "aws"],
        "nice_to_have": ["ansible", "prometheus", "argo"],
        "suggestions": ["Build CI/CD pipeline", "Deploy to EKS"]
    },

    "cloud_engineer": {
        "label": "Cloud Engineer",
        "required_skills": ["aws", "azure", "gcp", "terraform", "cloudformation"],
        "nice_to_have": ["serverless", "eks", "vpc"],
        "suggestions": ["AWS certification", "Terraform IaC project"]
    },

    # Systems & Other
    "software_engineer": {
        "label": "Software Engineer",
        "required_skills": ["data structures", "algorithms", "oop", "git", "unit testing"],
        "nice_to_have": ["system design", "microservices"],
        "suggestions": ["LeetCode 300 problems", "System design prep"]
    },

    "backend_developer": {
        "label": "Backend Developer",
        "required_skills": ["node", "python", "java", "sql", "redis", "rest"],
        "nice_to_have": ["graphql", "kafka", "elasticsearch"],
        "suggestions": ["Build scalable API", "Add caching layer"]
    },

    "frontend_developer": {
        "label": "Frontend Developer",
        "required_skills": ["react", "vue", "angular", "typescript", "webpack"],
        "nice_to_have": ["nextjs", "nuxt", "pwa"],
        "suggestions": ["Build PWA", "Learn Next.js"]
    },

    "ios_developer": {
        "label": "iOS Developer",
        "required_skills": ["swift", "swiftui", "xcode", "uikit"],
        "nice_to_have": ["combine", "coredata"],
        "suggestions": ["SwiftUI app", "App Store submission"]
    },

    # Enterprise
    "dotnet_developer": {
        "label": ".NET Developer",
        "required_skills": ["c#", "dotnet", "asp.net", "entity framework", "sql server"],
        "nice_to_have": [".net core", "blazor"],
        "suggestions": ["Build ASP.NET API", "Learn Blazor"]
    },

    "php_developer": {
        "label": "PHP Developer",
        "required_skills": ["php", "laravel", "symfony", "mysql", "wordpress"],
        "nice_to_have": ["composer", "phpunit"],
        "suggestions": ["Laravel SaaS", "WordPress plugins"]
    },

    "go_developer": {
        "label": "Go Developer",
        "required_skills": ["golang", "go", "goroutines", "gin", "gorm"],
        "nice_to_have": ["microservices", "grpc"],
        "suggestions": ["Microservice in Go", "gRPC APIs"]
    },
}

FRONTEND_ROLE_OPTIONS = {v["label"]: k for k, v in ROLE_CONFIG.items()}
