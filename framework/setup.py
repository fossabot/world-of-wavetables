import setuptools

setuptools.setup(
    name='wowt',
    version='1.0.0',
    author='inflamous',
    author_email='',
    packages=setuptools.find_packages(),
    url='https://github.com/inflamously/world-of-wavetables',
    license='LICENSE.txt',
    description='Create wavetables from sample, combine and mix them up.',
    long_description=open('README.md').read(),
    install_requires=[
        'librosa==0.9.1',
        'typer==0.4.1',
        'numpy==1.22.0',
        'osc-gen==1.3.3',
    ],
)