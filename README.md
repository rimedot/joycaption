# JoyCaption for Meva

A Meva plugin that describes images and
videos with JoyCaption Beta One. For each file it writes a description
(found by normal search), what it sees (people, clothing, setting, style,
themes, visible text) and tags taken from the description.

It is a processor plugin: only a manifest, no code. On this PC the model
runs in Meva's local runner with llama.cpp (installed with the model,
b11612 or newer); it can also run on a paired GPU worker.

## Models

| Model | Download | Note |
|---|---|---|
| JoyCaption Beta One | 5.8 GB | Q4_K_M GGUF (4.9 GB) and its f16 projector (0.9 GB). Needs about 6.5 GB of GPU memory, else it runs partly or fully on the CPU. |

Every file is checked against the sha256 in the manifest. Needs Meva 0.4.0
or newer.

## Install

In Meva, open Settings → Plugins → Install plugin…, paste
`https://github.com/rimedot/joycaption` and choose a version.

## Build

```sh
python3 build.py    # writes joycaption.mevax
```

Publishing a release builds the `.mevax`, attaches it to the release and
attests it. The manifest version must equal the release tag (`v0.3.0` or
`0.3.0`).

## License

MIT. The model has its own license on Hugging Face.
