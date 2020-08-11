import setuptools

with open('README.md', 'r') as file:
    long_description = file.read()

with open('requirements.txt', 'r') as file:
    install_requires = file.readlines()

    for i in range(len(install_requires)):
        install_requires[i] = install_requires[i].strip()

setuptools.setup(
    name='id3-variants-training',
    description='Demonstrates training of a decision tree using CanDIG APIs.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/CanDIG/ID3_Project',
    packages=['id3_variants_training'],
    package_dir={'id3_variants_training': 'src/id3_variants_training'},
    python_requires='>=3.7',
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'train-id3=id3_variants_training.__main__:main',
        ],
    },
)
