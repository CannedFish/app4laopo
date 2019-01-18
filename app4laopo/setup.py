import io

from setuptools import find_packages, setup

with io.open('README.md', 'rt', encoding='utf8') as f:
    readme = f.read()

    setup(
        name='app4laopo',
        version='0.1.0',
        url='https://github.com/CannedFish/app4laopo/tree/bs_master/ui/',
        license='BSD',
        maintainer='CannedFish',
        maintainer_email='lianggy0719@126.com',
        description='The UI for app4laopo.',
        long_description=readme,
        packages=find_packages(),
        include_package_data=True,
        zip_safe=False,
        install_requires=[
            'flask',
            'requests'
        ],
        extras_require={
            'test': [
                'pytest',
                'coverage',
            ],
        },
    )
