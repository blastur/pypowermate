from setuptools import setup

version="2.0.2"
setup(name='pypowermate',
      version=version,
      packages=['pypowermate'],
      install_requires=['evdev', 'future'],
      description='Encapsulates access to the Griffin USB PowerMate "knob" device',
      author='Magnus Olsson',
      author_email='magnus@minimum.se',
      url='https://github.com/blastur/pypowermate',
      download_url='https://github.com/blastur/pypowermate/tarball/{}'.format(version),
      keywords=['powermate', 'knob', 'griffin'],
      classifiers=[],
      )
