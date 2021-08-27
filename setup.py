from setuptools import setup

# Read the README.md file
with open('README.md') as file_handle:
    file_content = file_handle.read()

setup(
    name='kamalsql',
    packages=['kamalsql'],
    version='1.0.0',
    license='MIT',
    description='A simple Python wrapper for your MySQL needs.',
    long_description=file_content,
    long_description_content_type="text/markdown",
    author='Kamal Sharma',
    author_email='kamaldgrt@gmail.com',
    url='https://github.com/KamalDGRT/kamalsql',
    keywords=['Simple', 'Functional', 'Dependable'],
    install_requires=[
        'mysql-connector',
        'tabulate',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
