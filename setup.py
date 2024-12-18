from setuptools import setup, find_packages

setup(
    name='tuneparams',
    version='0.3.0',
    packages=find_packages(),
    install_requires=['astor', 'pandas'],
    entry_points={
        'console_scripts': [
            'tuneparams=tuneparams.cli:main',
        ],
    },
    include_package_data=True,
    description='A CLI tool to modify and execute Python scripts.',  # Keeping one description
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Sudharshan | Ashish | Risha_Lab',
    author_email='imsudharshan281@gmail.com',
    license='MIT',
    url='https://github.com/Sudharshan281/tuneparams',
)
