from setuptools import setup, find_packages

setup(
    name="brawlstars-tracker",
    version="0.1",
    packages=find_packages(),
    package_data={
        'brawlstars_tracker.config': ['players.json'],
    },
    install_requires=[
        'python-dotenv==1.0.0',
        'mysql-connector-python==8.2.0',
        'requests==2.31.0',
        'schedule==1.2.1',
    ],
) 