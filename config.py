import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Configuration for Vercel deployment
# /tmp is the only writable directory in Vercel serverless functions
UPLOAD_FOLDER = "/tmp/uploads"
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB limit
ALLOWED_EXTENSIONS = {"pdf", "docx"}

# Ensure upload directory exists (critical for Vercel)
try:
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
except Exception as e:
    print(f"Warning: Could not create upload folder: {e}")
    # Fallback to /tmp if /tmp/uploads fails
    UPLOAD_FOLDER = "/tmp"

# COMPLETE TECH ROLES CONFIGURATION
ROLE_CONFIG = {
    "software_engineer": {
        "label": "Software Engineer",
        "required_skills": ["data structures", "algorithms", "oop", "git", "unit testing"],
        "nice_to_have": ["system design", "microservices", "ci/cd"],
        "suggestions": ["Add quantified outcomes for key projects", "Include at least one end-to-end production project"]
    },
    "full_stack_developer": {
        "label": "Full Stack Developer",
        "required_skills": ["html", "css", "javascript", "sql", "rest api", "git"],
        "any_of_skill_groups": [
            {
                "name": "Backend language",
                "skills": ["python", "java", "node"],
                "min_required": 1,
                "required": True,
            }
        ],
        "nice_to_have": ["react", "spring boot", "django", "docker", "typescript"],
        "suggestions": ["Show both backend API and frontend UI ownership", "Add deployment and testing details for one full product"]
    },
    "frontend_developer": {
        "label": "Frontend Developer",
        "required_skills": ["html", "css", "javascript", "react", "responsive"],
        "nice_to_have": ["typescript", "nextjs", "tailwind", "accessibility", "webpack"],
        "suggestions": ["Add responsive and accessibility improvements with metrics", "Show component architecture and performance optimization work"]
    },
    "backend_developer": {
        "label": "Backend Developer",
        "required_skills": ["rest api", "sql", "api", "git"],
        "any_of_skill_groups": [
            {
                "name": "Backend language",
                "skills": ["python", "java"],
                "min_required": 1,
                "required": True,
            },
            {
                "name": "Backend framework",
                "skills": ["django", "flask", "fastapi", "spring", "spring boot"],
                "min_required": 1,
                "required": True,
            }
        ],
        "nice_to_have": ["redis", "kafka", "microservices", "docker", "postgresql"],
        "suggestions": ["Highlight one scalable API design decision", "Add caching, queueing, or database tuning impact"]
    },
    "web_developer": {
        "label": "Web Developer",
        "required_skills": ["html", "css", "javascript", "responsive", "rest api"],
        "any_of_skill_groups": [
            {
                "name": "Backend language",
                "skills": ["python", "java"],
                "min_required": 1,
                "required": True,
            }
        ],
        "nice_to_have": ["react", "node", "bootstrap", "tailwind", "git"],
        "suggestions": ["Show backend endpoints consumed by your web UI", "Add one full web app with deployment link and measurable outcomes"]
    },
    "data_analyst": {
        "label": "Data Analyst",
        "required_skills": ["sql", "excel", "power bi", "tableau", "statistics"],
        "nice_to_have": ["python", "pandas", "etl"],
        "suggestions": ["Include dashboard impact metrics", "Show complex SQL analysis examples"]
    },
    "data_scientist": {
        "label": "Data Scientist",
        "required_skills": ["python", "pandas", "numpy", "scikit-learn", "machine learning"],
        "nice_to_have": ["tensorflow", "pytorch", "feature engineering", "model deployment"],
        "suggestions": ["Mention model evaluation metrics and business impact", "Add productionization or inference pipeline experience"]
    },
    "devops_engineer": {
        "label": "DevOps Engineer",
        "required_skills": ["docker", "kubernetes", "jenkins", "terraform", "ci/cd"],
        "nice_to_have": ["aws", "azure", "prometheus", "grafana", "ansible"],
        "suggestions": ["Show deployment frequency or release-time improvements", "Add incident response and observability examples"]
    },
    "cloud_engineer": {
        "label": "Cloud Engineer",
        "required_skills": ["aws", "azure", "gcp", "terraform", "cloudformation"],
        "nice_to_have": ["serverless", "vpc", "kubernetes", "iam", "monitoring"],
        "suggestions": ["Add IaC examples with security controls", "Include cost optimization and reliability outcomes"]
    },
    "qa_engineer": {
        "label": "QA Engineer",
        "required_skills": ["test cases", "test plans", "bug tracking", "regression testing", "api testing"],
        "nice_to_have": ["selenium", "postman", "jira", "automation", "performance testing"],
        "suggestions": ["Describe defect leakage reduction metrics", "Show collaboration with dev and product teams"]
    },
    "software_tester": {
        "label": "Software Tester",
        "required_skills": ["manual testing", "test execution", "bug reporting", "test scenarios", "qa"],
        "nice_to_have": ["jira", "postman", "sql", "regression testing"],
        "suggestions": ["Add examples of critical bugs caught before release", "Include requirement traceability experience"]
    },
    "automation_test_engineer": {
        "label": "Automation Test Engineer",
        "required_skills": ["automation", "selenium", "pytest", "test framework", "ci/cd"],
        "nice_to_have": ["playwright", "cypress", "api testing", "performance testing"],
        "suggestions": ["Highlight flaky test reduction and stability improvements", "Include pipeline integration for automated suites"]
    },
    "system_administrator": {
        "label": "System Administrator",
        "required_skills": ["linux", "windows server", "scripting", "monitoring", "backup"],
        "nice_to_have": ["active directory", "powershell", "bash", "virtualization"],
        "suggestions": ["Add uptime and incident resolution metrics", "Show security hardening and patch management outcomes"]
    },
    "network_engineer": {
        "label": "Network Engineer",
        "required_skills": ["routing", "switching", "tcp/ip", "firewalls", "network troubleshooting"],
        "nice_to_have": ["vpn", "sd-wan", "load balancing", "wireshark"],
        "suggestions": ["Include network performance and latency improvements", "Show outage prevention or root-cause analyses"]
    },
    "database_administrator": {
        "label": "Database Administrator",
        "required_skills": ["sql", "database tuning", "backup", "recovery", "performance"],
        "nice_to_have": ["postgresql", "mysql", "sql server", "replication", "high availability"],
        "suggestions": ["Add indexing and query optimization results", "Show DR planning and RTO/RPO improvements"]
    },
    "cybersecurity_analyst": {
        "label": "Cybersecurity Analyst",
        "required_skills": ["siem", "vulnerability assessment", "incident response", "risk assessment", "security monitoring"],
        "nice_to_have": ["splunk", "threat hunting", "penetration testing", "soc"],
        "suggestions": ["Highlight incident containment timelines", "Add examples of risk reduction through controls"]
    },
    "business_analyst": {
        "label": "Business Analyst",
        "required_skills": ["requirements gathering", "stakeholder management", "user stories", "process mapping", "documentation"],
        "nice_to_have": ["sql", "jira", "agile", "data analysis"],
        "suggestions": ["Include measurable business outcomes", "Show requirement-to-delivery traceability"]
    },
    "product_manager": {
        "label": "Product Manager",
        "required_skills": ["roadmap", "prioritization", "stakeholder management", "product strategy", "analytics"],
        "nice_to_have": ["a/b testing", "scrum", "market research", "user interviews"],
        "suggestions": ["Add product KPI movement and launch outcomes", "Show clear problem framing and tradeoff decisions"]
    },
    "ui_ux_designer": {
        "label": "UI/UX Designer",
        "required_skills": ["figma", "wireframing", "prototyping", "user research", "usability testing"],
        "nice_to_have": ["design systems", "interaction design", "accessibility", "adobe xd"],
        "suggestions": ["Include portfolio links with before/after impact", "Show design decisions backed by user feedback or metrics"]
    },
    "mern_developer": {
        "label": "MERN Stack Developer",
        "required_skills": ["mongodb", "express", "react", "node", "javascript", "rest api", "html", "css"],
        "nice_to_have": ["typescript", "redux", "jwt", "mongoose", "nextjs", "docker"],
        "suggestions": ["Build production-ready MERN apps with role-based access", "Highlight API integration and performance optimization"]
    },
    "python_developer": {
        "label": "Python Developer",
        "required_skills": ["python", "flask", "django", "oop", "rest", "api"],
        "nice_to_have": ["fastapi", "sql", "docker", "pytest"],
        "suggestions": ["Add async API or background jobs experience", "Show test coverage and deployment details"]
    },
    "java_developer": {
        "label": "Java Developer",
        "required_skills": ["java", "spring", "spring boot", "maven", "jpa", "hibernate"],
        "nice_to_have": ["microservices", "kafka", "docker", "junit"],
        "suggestions": ["Show API design and transaction management examples", "Add performance tuning and testing practices"]
    },
    "cpp_developer": {
        "label": "C++ Developer",
        "required_skills": ["c++", "stl", "oop", "algorithms", "data structures", "memory management"],
        "nice_to_have": ["multithreading", "boost", "qt", "cmake"],
        "suggestions": ["Add low-level optimization examples with benchmarks", "Show multithreaded or systems-level project work"]
    },
    "c_developer": {
        "label": "C Developer",
        "required_skills": ["c", "pointers", "memory management", "linux", "embedded systems"],
        "nice_to_have": ["posix", "sockets", "debugging", "firmware"],
        "suggestions": ["Highlight embedded or systems programming projects", "Show debugging/profiling impact on performance"]
    },
    "ruby_developer": {
        "label": "Ruby Developer",
        "required_skills": ["ruby", "rails", "postgresql", "rest api", "rspec"],
        "nice_to_have": ["sidekiq", "redis", "docker", "heroku"],
        "suggestions": ["Show Rails API + background jobs architecture", "Add testing and deployment reliability outcomes"]
    },
    "python_fullstack_developer": {
        "label": "Python Fullstack Developer",
        "required_skills": ["python", "django", "flask", "rest api", "html", "css", "javascript", "sql"],
        "nice_to_have": ["react", "fastapi", "docker", "redis", "postgresql"],
        "suggestions": ["Show one complete backend+frontend product", "Add auth, testing, and deployment evidence"]
    },
    "java_fullstack_developer": {
        "label": "Java Full-Stack Developer",
        "required_skills": ["java", "spring boot", "rest api", "sql", "html", "css", "javascript"],
        "nice_to_have": ["react", "hibernate", "microservices", "docker", "junit"],
        "suggestions": ["Include Spring Boot + UI integration architecture", "Show API testing and production rollout outcomes"]
    },
    "android_developer": {
        "label": "Android Developer",
        "required_skills": ["kotlin", "java", "android", "android studio", "mvvm"],
        "nice_to_have": ["jetpack compose", "coroutines", "room", "retrofit"],
        "suggestions": ["Add Play Store app/project link", "Show crash reduction or performance improvements"]
    },
    "ml_engineer": {
        "label": "ML Engineer",
        "required_skills": ["python", "machine learning", "tensorflow", "pytorch", "model deployment"],
        "nice_to_have": ["mlflow", "kubeflow", "docker", "feature store"],
        "suggestions": ["Show training-to-serving pipeline ownership", "Include latency, throughput, or cost metrics"]
    },
    "ios_developer": {
        "label": "iOS Developer",
        "required_skills": ["swift", "ios", "xcode", "swiftui", "uikit"],
        "nice_to_have": ["combine", "core data", "testing", "app store"],
        "suggestions": ["Add App Store or TestFlight links", "Show app performance and crash analytics improvements"]
    },
    "dotnet_developer": {
        "label": ".NET Developer",
        "required_skills": ["c#", "dotnet", "asp.net", "entity framework", "sql server"],
        "nice_to_have": [".net core", "azure", "microservices", "xunit"],
        "suggestions": ["Show API architecture and EF optimization results", "Add CI/CD and cloud deployment experience"]
    },
    "php_developer": {
        "label": "PHP Developer",
        "required_skills": ["php", "laravel", "mysql", "rest api", "mvc"],
        "nice_to_have": ["symfony", "redis", "docker", "phpunit"],
        "suggestions": ["Show Laravel app architecture and scaling work", "Add testing and deployment reliability improvements"]
    },
    "go_developer": {
        "label": "Go Developer",
        "required_skills": ["go", "golang", "goroutines", "rest api", "microservices"],
        "nice_to_have": ["gin", "gorm", "grpc", "docker", "kubernetes"],
        "suggestions": ["Show concurrency-safe service design", "Include latency/throughput improvements in production"]
    },
}

MARKET_REQUIRED_SKILLS = {
    "software_engineer": ["problem solving", "api design"],
    "full_stack_developer": ["api integration", "authentication"],
    "frontend_developer": ["api integration", "accessibility"],
    "backend_developer": ["microservices", "authentication"],
    "web_developer": ["api integration", "seo basics"],
    "data_analyst": ["data visualization", "data cleaning"],
    "data_scientist": ["feature engineering", "model evaluation"],
    "devops_engineer": ["monitoring", "infrastructure as code"],
    "cloud_engineer": ["cloud security", "cost optimization"],
    "qa_engineer": ["test automation", "api testing"],
    "software_tester": ["regression testing", "defect lifecycle"],
    "automation_test_engineer": ["framework design", "pipeline integration"],
    "system_administrator": ["incident management", "security hardening"],
    "network_engineer": ["network security", "performance monitoring"],
    "database_administrator": ["query optimization", "high availability"],
    "cybersecurity_analyst": ["threat detection", "security incident response"],
    "business_analyst": ["requirement analysis", "stakeholder communication"],
    "product_manager": ["product analytics", "roadmap planning"],
    "ui_ux_designer": ["interaction design", "design systems"],
    "mern_developer": ["api security", "state management"],
    "python_developer": ["async programming", "testing"],
    "java_developer": ["microservices", "testing"],
    "cpp_developer": ["performance optimization", "multithreading"],
    "c_developer": ["debugging", "low-level optimization"],
    "ruby_developer": ["background jobs", "testing"],
    "python_fullstack_developer": ["authentication", "api integration"],
    "java_fullstack_developer": ["authentication", "api integration"],
    "android_developer": ["app performance", "crash analytics"],
    "ml_engineer": ["mlops", "model monitoring"],
    "ios_developer": ["app performance", "testing"],
    "dotnet_developer": ["api design", "testing"],
    "php_developer": ["testing", "security"],
    "go_developer": ["concurrency", "performance optimization"],
}


def _apply_market_required_skills() -> None:
    for role_key, additions in MARKET_REQUIRED_SKILLS.items():
        role = ROLE_CONFIG.get(role_key)
        if not role:
            continue

        base_required = role.get("required_skills", [])
        merged = list(base_required)
        for skill in additions:
            if skill not in merged:
                merged.append(skill)

        role["required_skills"] = merged


_apply_market_required_skills()

FRONTEND_ROLE_OPTIONS = {v["label"]: k for k, v in ROLE_CONFIG.items()}
