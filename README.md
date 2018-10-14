# PeeblesLab

This is the simple flask app which serves http://www.peebleslab.com/

The app itself has no site assets or local state; all assets are stored as blobs in the Azure Storage account peebleslab.blob.core.windows.net:

* Comics themselves are served out of the `comics/` container
* Banners are served out of the `banners/` container
* Miscellaneous site assets are served out of the `static/` container

The list of comics, links to the comic/banner, and metadata like the comic's title and alt text are all stored in a table named `comics` in the same Azure Storage account.

## Deploying

The site is currently served from an Azure App Service account.

It turns out deploying a Python app to Azure is pretty wonky.
Per [this page](https://docs.microsoft.com/en-us/visualstudio/python/managing-python-on-azure-app-service?view=vs-2017), setting up a new instance involves

* Installing an "extension" for the latest version of Python
* Setting up `web.config` (in this repo) to point to that Python interpreter
* Adding a `.skipPythonDeployment` marker in this repo, so the git push hook doesn't try to process `requirements.txt` using an ancient version of pip
* Manually logging into the instance and running `pip install -r requirements.txt` using the version of pip that came with the Python distribution you're using
