Boilerplate code and wiki steps for common data operations and command line workflows.

## Table of Contents

- [GitHub](#github)
- [Image Processing](#image-processing)

## GitHub

### create and push a new repo from the command line
[`hub`](https://hub.github.com/) is an easy way for doing this (`brew install hub`). Go here for  [the long way](https://help.github.com/en/github/importing-your-projects-to-github/adding-an-existing-project-to-github-using-the-command-line).

```bash
$ hub create
```

## Image Processing

Getting PIL to work in ipython required running `ipython -m pip install Pillow` ([source](https://github.com/python-pillow/Pillow/issues/4288`))

### convert image URLs to webp photos 
[source](https://medium.com/@ajeetham/image-type-conversion-jpg-png-jpg-webp-png-webp-with-python-7d5df09394c9)


```python
urls = ['url1', 'url2']
for url in urls:
	img = get_from_url(url)
	im = img.convert("RGB")
	im.save('{}.webp'.format(urls.index(url)), 'webp')
```

### get imagekit urls

```bash
$ python image/image.py
```