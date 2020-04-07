Boilerplate code and wiki for common data operations.

## Table of Contents

- [Debugging](#Debugging)
- [Dev Setup](#Dev-Setup)
- [Image Processing](#image-processing)
- [JSON parsing](#JSON-Parsing)
- [Stats](#Stats)

## Debugging

### `jupyter` auto-reload a module in ipython or a notebook

```ipython
%load_ext autoreload
%autoreload 1
%aimport <module>
```

## Dev Setup

### `github` create and push a new repo from the command line
[`hub`](https://hub.github.com/) is an easy way for doing this (`brew install hub`). Go here for  [the long way](https://help.github.com/en/github/importing-your-projects-to-github/adding-an-existing-project-to-github-using-the-command-line).

```bash
$ hub create
$ git push -u origin master
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
Uses the [imagekitio](https://github.com/imagekit-developer/imagekit-python) package. Requires imagekit API keys are sourced from environmental variables in `~/.imagekit_env`. 

```bash
$ source ~/.imagekit_env && python image/image.py
```

## JSON Parsing

Given a json response that looks like: 
```bash
$ python image/image.py | jq  | head -15
{
  "error": null,
  "response": [
    {
      "type": "file",
      "name": "default-image.jpg",
      "fileId": "5e792d7b855bcd575b10cdac",
      "tags": null,
      "customCoordinates": null,
      "isPrivateFile": false,
      "url": "https://ik.imagekit.io/69mp7bhac/default-image.jpg",
      "thumbnail": "https://ik.imagekit.io/69mp7bhac/tr:n-media_library_thumbnail/default-image.jpg",
      "fileType": "image",
      "filePath": "/default-image.jpg"
    },
```

Resources: 
* [jq tutorial](https://stedolan.github.io/jq/tutorial/)

### `jq` get all values for one field within an array of objects

```bash
$ python image/image.py | jq '[ .response[].url ]' | head
[
  "https://ik.imagekit.io/69mp7bhac/default-image.jpg",
  "https://ik.imagekit.io/69mp7bhac/photo-1574144113084-b6f450cc5e0c_Y5IvSc6b4.jpeg",
  "https://ik.imagekit.io/69mp7bhac/photo-1574144113084-b6f450cc5e0c_MpYf03m27.webp",
  "https://ik.imagekit.io/69mp7bhac/headshot3_zQSlTs3bb.webp",
  "https://ik.imagekit.io/69mp7bhac/headshot2_oR1Vn5amZ.webp",
  "https://ik.imagekit.io/69mp7bhac/headshot0_6ETzsKqtE.webp",
  "https://ik.imagekit.io/69mp7bhac/headshot5_SYCuqgLtN.webp",
  "https://ik.imagekit.io/69mp7bhac/headshot4_amj2Uhtdn.webp",
  "https://ik.imagekit.io/69mp7bhac/headshot6_1cVamjitn.webp",
```

### `jq` get multiple fields from within an array of objects 

to grab the raw values...
```bash
$ python image/image.py | jq '.response[] | [ .url, .name] ' | head
[
  "https://ik.imagekit.io/69mp7bhac/default-image.jpg",
  "default-image.jpg"
]
[
  "https://ik.imagekit.io/69mp7bhac/photo-1574144113084-b6f450cc5e0c_Y5IvSc6b4.jpeg",
  "photo-1574144113084-b6f450cc5e0c_Y5IvSc6b4.jpeg"
]
```

to structure as a list of dicts... 

```bash
$ python image/image.py | jq '[ .response[] | {url: .url, name: .name} ]' | head
[{
  "url": "https://ik.imagekit.io/69mp7bhac/default-image.jpg",
  "name": "default-image.jpg"
},
{
  "url": "https://ik.imagekit.io/69mp7bhac/photo-1574144113084-b6f450cc5e0c_Y5IvSc6b4.jpeg",
  "name": "photo-1574144113084-b6f450cc5e0c_Y5IvSc6b4.jpeg"
}]
```
the entire jq command is wrapped in a list, like `jq | '[  ]'`.

### `jq` get all keys from a dict

```bash
$ python image/image.py | jq '[. response[] | keys'
[
"type",
 "name",
 "fileId",
 "tags",
 "customCoordinates",
 "isPrivateFile",
 "url",
 "thumbnail",
 "fileType",
 "filePath"
]
```

## Stats 

Resources: 
* [Intro to power analysis in python](https://towardsdatascience.com/introduction-to-power-analysis-in-python-e7b748dfa26)
* [calculating sample size](https://scientificallysound.org/2017/07/20/python-calculating-sample-size-for-a-2-independent-sample-t-test/)
* [Typical analysis procedure](http://work.thaslwanter.at/Stats/html/statsAnalysis.html)

### `statsmodels` calculate power for a given sample size and alpha

[documentation](https://www.statsmodels.org/stable/generated/statsmodels.stats.power.tt_ind_solve_power.html). 

Helpful when you have unevenly sized samples. Let's assume this is a one-sided t-test (i.e. alternative is not `two-sided`). 

```python
from statsmodels.stats.power import tt_ind_solve_power

tt_ind_solve_power(effect_size=0.03, nobs1=60000, alpha=0.05, ratio=0.08, alternative='larger')
0.51
```

### `statsmodels` calculate sample size for a power and alpha

```python
from statsmodels.stats.power import TTestIndPower

power_analysis = TTestIndPower()
power_analysis.solve_power(alpha=0.05, power=0.8, effect_size=0.03)
17442.872915839584
```
