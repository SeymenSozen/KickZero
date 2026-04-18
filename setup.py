from setuptools import setup, find_packages

# README.md dosyasını uzun açıklama olarak oku
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="kickzero",
    version="1.3.1",
    author="Seymen Sözen",
    description="A modular and asynchronous framework for Kick.com chatbots.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SeymenSozen/KickZero", # GitHub Limanı ⚓
    project_urls={
        "Bug Tracker": "https://github.com/SeymenSozen/KickZero/issues",
        "Documentation": "https://github.com/SeymenSozen/KickZero#readme",
    },
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Topic :: Communications :: Chat",
    ],
    python_requires='>=3.8',
    install_requires=[
        "aiohttp",
        "websockets",
        "colorama",
    ],
)