from setuptools import setup

import os

# Installed name used for various commands (both script and setuptools).
command_name = os.environ.get("FBB_ALT_NAME") or "flask_brownbag"

with open("dev_requirements.txt") as file:
    tests_require = [dep.strip() for dep in file.readlines()]

setup(name="flask_brownbag",
      version="0.1",
      description=("Flask application for tracking the number of times self "
        "service health check is called."),
      author="Alex Lord",
      author_email="alex.lord@isilon.com",
      url="git@github.west.isilon.com:alord/flask_brownbag.git",
      packages=["heart_beat", "the_flask_module"],
      include_package_data=True,
      install_requires=["setuptools", "pip", "SQLAlchemy", "flask",
          "flask_sqlalchemy", "ipython", "pyzmq", "jinja2", "tornado",
          "jsonschema", "terminado"],
      tests_require=tests_require,  # Testing, external due to Travis
      test_suite="heart_beat.test",
      classifiers=[
          "Development Status :: 2 - Pre-Alpha",
          "Environment :: Other Environment",
          "Intended Audience :: Developers",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3.4",
      ],
      zip_safe=True,
)
