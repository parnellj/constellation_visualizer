try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

config = {
	'name': 'Constellation Visualizer',
	'version': '0.1',
	'url': 'https://github.com/parnellj/constellation_visualizer',
	'download_url': 'https://github.com/parnellj/constellation_visualizer',
	'author': 'Justin Parnell',
	'author_email': 'parnell.justin@gmail.com',
	'maintainer': 'Justin Parnell',
	'maintainer_email': 'parnell.justin@gmail.com',
	'classifiers': [],
	'license': 'GNU GPL v3.0',
	'description': 'Visualizes and sorts constellations as a learning and scheduling aid.',
	'long_description': 'Visualizes and sorts constellations as a learning and scheduling aid.',
	'keywords': '',
	'install_requires': ['nose'],
	'packages': ['constellation_visualizer'],
	'scripts': []
}
	
setup(**config)
