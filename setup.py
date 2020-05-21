from setuptools import setup


setup(
    name='personal_totivator',
    version='0.0.1',
    description='Controle e acampanhamento de tarefas',
    long_description='long_description',
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