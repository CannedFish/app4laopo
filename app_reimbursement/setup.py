from setuptools import setup, find_packages

setup(
    name='reimbursement',
    version='0.1.0',
    description='The reimbursement application with RESTful API based on Flask-RESTPlus',
    url='',
    author='CannedFish',

    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7'
    ],

    keywords='rest restful api flask swagger openapi flask-restplus',

    packages=find_packages(),

    install_requires=[
        'Flask==1.0.2',
        'flask-restplus==0.12.1',
        'Flask-SQLAlchemy==2.3.2',
        'requests==2.21.0'
    ],
)
