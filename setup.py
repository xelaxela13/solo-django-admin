from setuptools import setup

setup(
    name="solo_django_admin",
    version="0.1.5",
    description="Django admin for non Django ORM",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Oleksii Stepanenko",
    author_email="xelaxela13@gmail.com",
    url="https://github.com/xelaxela13/solo_django_admin.git",
    packages=["solo_django_admin", "solo_django_admin.core"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "Django>=4.2",
        "python-dotenv>=1.0.0",
        "tortoise-orm>=0.21.0"
    ],
)
