from setuptools import setup

import os

# Installed name used for various commands (both script and setuptools).
command_name = os.environ.get("HB_ALT_NAME") or "heart_beat"

with open("dev_requirements.txt") as file:
    tests_require = [dep.strip() for dep in file.readlines()]

setup(name="heart_beat",
      version="0.1",
      description=("Flask application for tracking the number of times self "
        "service health check is called."),
      author="Alex Lord",
      author_email="alex.lord@isilon.com",
      url="git@github.west.isilon.com:PRE-Tools/heart_beat.git",
      packages=["heart_beat", "heart_beat.test"],
      include_package_data=True,
      install_requires=["setuptools", "pip",  # Input flexibility
                        "SQLAlchemy", "Flask", "flask_sqlalchemy"],  # Functionality
      tests_require=tests_require,  # Testing, external due to Travis
      test_suite="heart_beat.test",
      classifiers=[
          "Development Status :: 4 - Beta",
          "Environment :: Web Environment",
          "Environment :: Console",
          "Intended Audience :: Information Technology",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3.2",
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 3.4",
      ],
      zip_safe=True,
)
