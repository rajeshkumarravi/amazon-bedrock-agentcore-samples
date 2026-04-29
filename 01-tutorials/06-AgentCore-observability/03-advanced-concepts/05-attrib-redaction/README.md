# Redact Agent attributes at source


## Checkout process (git 2.25+)
```
# Clone the repository with no checkout
git clone --no-checkout <repository-url>
cd <repository-name>

# Set up sparse checkout
git sparse-checkout set path/to/desired/directory

# Checkout the content
git checkout main
```

## Initialize
Install Python library manager `uv`.

```
uv sync
```
