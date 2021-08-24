from setuptools import setup, find_packages

setup(
    name='kamalsql',
    packages=['kamalsql'],
    version='0.0.2',
    license='MIT',
    description='A simple Python wrapper for your MySQL needs.',
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
