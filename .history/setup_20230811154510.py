from setuptools import setup, find_packages

setup(
    name='UnifiedLogger',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'loguru',
        'typer',
        'ttkbootstrap',
        'tkfontawesome',
    ],
    entry_points={
        'console_scripts': [
            'unifiedlogger = unifiedlogger:main',  # Adjust as needed
        ],
    },
)
