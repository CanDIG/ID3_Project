import setuptools

with open('README.md', 'r') as file:
    long_description = file.read()

install_requires = ["anytree", "atomicwrites", "attrs",
                    "Click", "funcsigs", "more-itertools",
                    "numpy", "pathlib2", "ped-parser",
                    "pluggy", "pysam",
                    "pytest", "PyVCF", "requests",
                    "scandir", "scipy", "six",
                    "aiohttp"]

setuptools.setup(
    name='id3-variants-training',
    description='Demonstrates training of a decision tree using CanDIG APIs.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/CanDIG/id3-variants-training',
    packages=['id3_variants_training'],
    package_dir={'id3_variants_training': 'src/id3_variants_training'},
    python_requires='>=3.7',
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'train-id3=id3_variants_training.__train__:train',
            'predict-id3=id3_variants_training.__predict__:predict'
        ],
    },
)
