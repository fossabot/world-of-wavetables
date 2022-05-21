from setuptools import setup

setup(
    name='wowt',
    version='1.0.0',
    author='inflamous',
    author_email='',
    package_dir={'': 'src'},
    url='https://github.com/inflamously/world-of-wavetables',
    license='LICENSE.txt',
    description='Create wavetables from sample, combine and mix them up.',
    long_description=open('README.md').read(),
    install_requires=[
        'librosa==0.9.1',
        'typer==0.4.1',
        'numpy==1.19.2',
        'PySoundFile==0.9.0.post1',
        'SoundFile==0.10.3.post1',
        'osc-gen==1.3.3',
    ],
)