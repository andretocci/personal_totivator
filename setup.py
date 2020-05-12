from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()
    # substitute relative image path by absolute ones
    long_description = long_description.replace("readme-images/", "https://raw.githubusercontent.com/DP6/Marketing-Attribution-Models/master/readme-images/")

setup(
    name='personal_totivator',
    version='0.0.1',
    description='Controle e acampanhamento de tarefas',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Andre Tocci',
    author_email='andrerussi002@gmail.com',
    url='https://github.com/andretocci/personal_totivator',
    packages=['personal_totivator'],
    install_requires=['numpy', 'pandas', 'google.colab' ],
    license="Apache License 2.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)