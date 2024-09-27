from setuptools import setup, find_packages

setup(
    name='tuneparams',
    version='0.1.4',
    packages=find_packages(),
    install_requires=['astor', 'tqdm'],
    entry_points={
        'console_scripts': [
            'tuneparams=tuneparams.cli:main',
        ],
    },
    include_package_data=True,
    author='Sudharshan|Ashish|Risha_Lab',
    author_email='imsudharshan281@gmail.com',
    description='A CLI tool to modify and execute Python scripts.',
    license='MIT',
    url='https://github.com/sudharshan281/tuneX',
)
